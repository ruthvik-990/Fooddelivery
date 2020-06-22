from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',IndexView,name="home" ),
    path('not_logged_in',NotLoggedInView,name="notloggedin"),
    path('restaurants/',RestaurantView,name="restaurants"),
    path('order_summary/<str:pk>/',OrderSummaryView,name="order_summary"),
    path('individual/<int:id>/',IndividualView,name="individual"),
    path('cart/',CartView,name="cart" ),
    path('checkout/',CheckoutView,name="checkout" ),
    path('register/',RegisterView,name="register"),
    path('login/',LoginView,name="login"),
    path('logout/',LogoutView,name='logout'),
    path('update_item/',UpdateOrder,name='update_item'),
    path('process_order/',ProcessOrder,name="process_order"),
    path('user_accounts/',UserAccountsView,name="user_accounts")
]