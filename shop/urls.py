from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'), 
    path('login/', views.login_view, name='login'),
    path('search/', views.product_search, name='product_search'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('', views.product_list, name='product_list'),             # Product page
    path('cart/', views.cart_view, name='cart'),                   # Cart page (name must be 'cart')
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]



   
    
   