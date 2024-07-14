from myapp.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def total(self):
        # get product ids
        product_ids = self.cart.keys()
        # lookup those keys in our product database models
        products = Product.objects.filter(id__in=product_ids)
        # get quantities
        quantities = self.cart
        # start counting at 0
        total = 0
        for key, value in quantities.items():
            # convert key stringinto intteger so we can do....
            key =int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value)
        return total
    

    def __len__(self):
        return sum(self.cart.values())
    
    def get_book(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        return self.cart

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        self.cart = {}
        self.save()