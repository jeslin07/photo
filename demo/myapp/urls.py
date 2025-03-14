from django.urls import path
from .views import *
from . import views
from .views import product_view
from django.contrib import admin

urlpatterns = [
    path("", base,name="base"),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path('contact/', views.contact, name='contact'),
    path('save-the-date/', save_the_date, name='save_the_date'),
     path('product/', product_view, name='product'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
     path('payment/', views.payment, name='payment_page'),


]