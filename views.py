from django.shortcuts import render, redirect,HttpResponse
from .models import Product, Category,Event,ContactMessage
from django.urls import reverse
from django.contrib.auth import authenticate,logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import BlogPost
from .forms import BlogPostForm




def home(request):   
    return render(request, 'home.html')

def AboutUs(request):
    return render(request, 'AboutUs.html')

def Book_Discription(request):
    return render(request, 'Book_Discription.html')

def Contact(request):
    return render(request, 'Contact.html')

def event(request):
    return render(request, 'event.html')

def Blog(request):
    return render(request, 'Blog.html')

def BookGenre(request):
    return render(request, 'BookGenre.html')

def newpass(request):
    return render(request, 'new pass.html')

#IMPORTSNT

def SignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return HttpResponse("Your password and confirm password are not the same")
        else:
            data = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            data.save()
            return redirect('login')

    return render(request, 'SignUp.html')



def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect(reverse('mainpage'))
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been LOGGED OUT!"))
    #return redirect('home')
    return redirect(reverse('home'))


def forget(request):
    return render(request, 'forget.html')

def saveEnquiry(request):
    return render(request,'Contact.html')


def mainpage(request):
    products = Product.objects.all()  # Get all products or filter as needed
    return render(request, 'mainpage.html', {'products': products})

@login_required
def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def category_view(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'category.html', {'products': products, 'category_name': category_name})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userpro.html'

class CustomLoginView(LoginView):
    template_name = 'login.html'

def explore(request):
    most_popular_books = Product.objects.filter(section='most_popular')
    best_sellers = Product.objects.filter(section='best_sellers')
    weekly_best_sellers = Product.objects.filter(section='weekly_best_sellers')

    context = {
        'most_popular_books': most_popular_books,
        'best_sellers': best_sellers,
        'weekly_best_sellers': weekly_best_sellers,
    }

    return render(request, 'explore.html', context)

def products_by_section(request, section_name):
    products = Product.objects.filter(section=section_name)
    return render(request, 'explore.html', {'products': products, 'section_name': section_name})

def userpro(request):
    return render(request, 'userpro.html')


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event.html', {'events': events})

def search(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(author__icontains=query)
        )
    return render(request, 'search_results.html', {'results': results, 'query': query})

#contact function
def save_enquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save the message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')  # Replace 'contact' with the name of your contact page URL pattern
    return render(request, 'Contact.html')

#blog's fucion
def blog_page(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.approved = False 
            post.save()
            return redirect('blog_page')
    else:
        form = BlogPostForm()

    featured_posts = {
        'bookReview': BlogPost.objects.filter(approved=True, feature='bookReview').order_by('-created_at'),
        'authorSpotlight': BlogPost.objects.filter(approved=True, feature='authorSpotlight').order_by('-created_at'),
        'childrensCorner': BlogPost.objects.filter(approved=True, feature='childrensCorner').order_by('-created_at'),
        'latest': BlogPost.objects.filter(approved=True, feature='latest').order_by('-created_at'),
        'userReview': BlogPost.objects.filter(approved=True, feature='userReview').order_by('-created_at'),
    }

    context = {
        'form': form,
        'featured_posts': featured_posts
    }
    return render(request, 'Blog.html', context)

def set_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('set_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password has been set successfully. You can now log in with your new password.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
            return redirect('set_password')

    return render(request, 'set_password.html')