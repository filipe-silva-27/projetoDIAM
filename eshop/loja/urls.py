from django.urls import include, path
from . import views
from . import models

# (. significa que importa views da mesma directoria)

app_name = 'loja'

urlpatterns = [
    path("base", views.index, name="index"),
    path("", views.loja, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path("login/",views.login1,name="login1"),
    path("registo/",views.register,name="register"),
    path("produto<int:produto_id>/",views.detalheProd,name="detalheProd"),

]