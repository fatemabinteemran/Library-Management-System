from django import forms
from django.contrib.auth.models import User
from .models import BlogPost 
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

#Blog
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content','author','feature']  # Adjust fields as per your BlogPost model