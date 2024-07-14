#here is the context processor so our cart can work on all oages of website
def cart(request):
    from .cart import Cart
    return {'cart': Cart(request)}


