from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django .contrib.auth.forms import UserChangeForm
# from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models
from django.utils import timezone

    
def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    section = models.CharField(
        max_length=50,
        choices=[
            ('most_popular', 'Most Popular'),
            ('best_sellers', 'Best Sellers'),
            ('weekly_best_sellers', 'Weekly Best Sellers')
        ],
        default='most_popular'  # Provide a default value here
    )
    description = models.CharField(max_length=5000)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.name

class UpdateUserForm(UserChangeForm):
        user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
        bio= models.TextField()
def __str__(self):
        return str(self.user)


class Category(models.Model):
        name = models.CharField(max_length=50,unique=True)
def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/events/')

    def __str__(self):
        return self.title
    

#contact   
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'
    

#Blog
class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    approved = models.BooleanField(default=False)
    feature = models.CharField(
        max_length=50,
        choices=[
            ('bookReview', 'Book Review'),
            ('authorSpotlight', 'Author Spotlight'),
            ('childrensCorner', "Children's Corner"),
            ('latest', 'Latest'),
            ('userReview', 'User Review')
        ],
        default='bookReview'
    )

    def __str__(self):
        return self.title