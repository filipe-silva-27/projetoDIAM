from django.urls import include, path
from . import views
from . import models

# (. significa que importa views da mesma directoria)

app_name = 'loja'

urlpatterns = [
    # path("base", views.index, name="index"),
    path("", views.loja, name="loja"),
    path('checkout/',views.checkout, name="checkout"),
    path("login/",views.login1,name="login1"),
    path("logout/", views.logout1, name="logout1"),
    path("registo/",views.register,name="register"),
    path("produto<int:produto_id>/",views.detalheProd,name="detalheProd"),
    path("novoProduto/",views.criaProduto,name="criaProduto"),
    
    ##MOSTRA,ADICIONA,REMOVE CARRINHO
    path('cart/',views.cart, name="cart"),
    path("add_to_cart/<int:produto_id>/", views.add_cart,name="add_cart"),
    path("remove_from_cart/<int:produto_id>/", views.remove_cart,name="remove_cart"),
]