from django.shortcuts import render, get_object_or_404
from .cart import Cart
from myapp.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_book()
    quantities = cart.get_quants()
    totals = cart.total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        cart_quantity = len(cart)
        return JsonResponse({'status': 'success', 'qty': cart_quantity, 'message': 'Product added to cart successfully.'})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)

def cart_delete(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        cart.delete(product=product_id)
        return JsonResponse({'status': 'success', 'message': 'Product removed from cart.'})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)

def cart_update(request):
    pass
