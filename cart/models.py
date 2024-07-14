from django.db import models
from myapp.models import Product  # Import your Product model from myapp
#from django.contrib.auth.models import User


class Cart(models.Model):
    # Your Cart model definition
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    pass

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Update the reference to Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
