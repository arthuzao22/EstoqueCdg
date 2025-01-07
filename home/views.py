from django.db.models import F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from produto.models import Estoque, Produto

class HomeView(View):
    def get(self, request, *args, **kwargs):
        # Filtra os produtos
        produtos_estoque_zerado = Estoque.objects.filter(qtde=0)
        produtos_estoque = Estoque.objects.all()
        produtos_estoque_min = Estoque.objects.filter(qtde__lte=F('id_produto__estoquemin'))

        # Conta o número de produtos 
        cont_estoque_zerado = len(produtos_estoque_zerado)
        cont_estoque = len(produtos_estoque)
        cont_estoque_min = len(produtos_estoque_min)

        # ------------------------------------------------------
        if request.user.is_authenticated:
            nome = request.user.first_name  # Pega o nome de usuário
            sobrenome = request.user.last_name  # Pega o sobrenome de usuário
            username = nome + ' ' + sobrenome
        else:
            username = None  # Caso o usuário não esteja logado

        # Renderiza a página inicial
        return render(request, 'home_view.html', {
            'username': username,
            'produtos_estoque_zerado': produtos_estoque_zerado,
            'cont_estoque_zerado': cont_estoque_zerado,
            'cont_estoque': cont_estoque,
            'cont_estoque_min': cont_estoque_min
        })
