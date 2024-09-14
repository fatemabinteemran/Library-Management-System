from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from myapp.models import Product
from django.urls import reverse

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order
        order = Order.objects.get(id=pk)
        # get order items
        items = OrderItem.objects.filter(order=pk)

        return render(request, 'payment/orders.html', {"order":order, "items":items})
    else:
        messages.error(request, "Access Denied!!")
        return redirect('mainpage')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        messages.error(request, "Access Denied!!")
        return redirect('mainpage')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, "payment/shipped_dash.html", {"orders": orders})
    else:
        messages.error(request, "Access Denied!!")
        return redirect('mainpage')

def process_order(request):
    if not request.user.is_authenticated:
        messages.error(request, "Access Denied")
        return redirect('home')

    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_book()
        quantities = cart.get_quants()
        totals = cart.total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        if my_shipping:
            full_name = my_shipping['shipping_full_name']
            email = my_shipping['shipping_email']
            shipping_address = (
                f"{my_shipping['shipping_address1']}\n"
                f"{my_shipping['shipping_address2']}\n"
                f"{my_shipping['shipping_city']}\n"
                f"{my_shipping['shipping_state']}\n"
                f"{my_shipping['shipping_zipcode']}\n"
                f"{my_shipping['shipping_country']}\n"
            )
            amount_paid = totals

            create_order = Order(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid
            )
            create_order.save()

            for product in cart_products:
                product_id = product.id
                price = product.price
                quantity = quantities.get(str(product_id), 0)
                if quantity > 0:
                    create_order_item = OrderItem(
                        order=create_order,
                        product=product,
                        user=request.user if request.user.is_authenticated else None,
                        quantity=quantity,
                        price=price
                    )
                    create_order_item.save()

            # Empty the cart after placing the order
            cart.clear()

            messages.success(request, "Order Placed!!")
            return redirect('mainpage')

        messages.error(request, "Failed to process order. Please try again.")
        return redirect('payment:checkout')

    return redirect('payment:checkout')  # Redirect in case of GET request or other scenarios

def billing_info(request):
    if not request.user.is_authenticated:
        messages.error(request, "Access Denied")
        return redirect('home')

    cart = Cart(request)
    cart_products = cart.get_book()
    quantities = cart.get_quants()
    totals = cart.total()

    shipping_form = ShippingForm(request.POST or None)

    if request.method == 'POST' and shipping_form.is_valid():
        my_shipping = request.POST.dict()
        request.session['my_shipping'] = my_shipping
        billing_form = PaymentForm()
        return render(request, "payment/billing_info.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_info": request.POST,
            "billing_form": billing_form,
        })

    return render(request, "payment/billing_info.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
    })

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_book()
    quantities = cart.get_quants()
    totals = cart.total()

    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_form = ShippingForm(request.POST or None)

        if request.method == "POST" and shipping_form.is_valid():
            shipping_address = shipping_form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            messages.success(request, "Shipping address saved successfully!")
            return redirect('payment:checkout')
    else:
        shipping_form = ShippingForm(request.POST or None)
        if request.method == "POST" and shipping_form.is_valid():
            # Process the guest checkout form if necessary
            pass

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form
    })

def payment_success(request):
    return render(request, "payment/payment_success.html", {})
