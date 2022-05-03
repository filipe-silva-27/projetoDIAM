from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)

urlpatterns = [
    path("base", views.index, name="index"),
    path("", views.loja, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),

]