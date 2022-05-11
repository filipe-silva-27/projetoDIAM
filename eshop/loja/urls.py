from django.urls import include, path
from . import views
from . import models

# (. significa que importa views da mesma directoria)

app_name = 'loja'

urlpatterns = [
    # path("base", views.index, name="index"),
    path("", views.loja, name="loja"),

    #DETALHES DA CONTA
    path("detalhesConta/", views.detailConta, name="detailConta"),

    ##LOGIN_LOGOUT_REGISTO
    path("login/",views.login1,name="login1"),
    path("registo/",views.register,name="register"),
    path("logout/", views.logout1, name="logout1"),

    ##CHECKOUT
    path('checkout/',views.checkout, name="checkout"),

    #Criação_Detalhe_produto
    path("produto<int:produto_id>/",views.detalheProd,name="detalheProd"),
    path("novoProduto/",views.criaProduto,name="criaProduto"),
    
    ##MOSTRA,ADICIONA,REMOVE CARRINHO
    path('cart/',views.cart, name="cart"),
    path("add_to_cart/<int:produto_id>/", views.add_cart,name="add_cart"),
    path("remove_from_cart/<int:produto_id>/", views.remove_cart,name="remove_cart"),
    path("remove_one/<int:produto_id>/",views.remove_one,name="remove_one"),

    ##SellerSpace
    path('seller/',views.seller,name="seller")

]