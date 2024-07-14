from django.contrib import admin
from django.urls import path
from cart import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cart_summary,name="cart_summary"),
    path('cart/add/', views.cart_add,name="cart_add"),
    path('cart/delete/', views.cart_delete,name="cart_delete"),
    #path('cart/update/', views.cart_update,name="cart_update"),
   
    
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





admin.site.index_title = "BIBLIOPHILES"
admin.site.site_header = "The Admin Panel" 
admin.site.site_title = "BIBLIOPHILES Site Admin"


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





admin.site.index_title = "BIBLIOPHILES"
admin.site.site_header = "The Admin Panel" 
admin.site.site_title = "BIBLIOPHILES Site Admin"