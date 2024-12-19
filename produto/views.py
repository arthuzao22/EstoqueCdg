from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Produto
from categoria.models import Categoria  # Importação do modelo Categoria
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

#PRODUTOS

# Listar produtos
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produto_list.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Obtém todas as categorias da base de dados
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        categorias_filter = self.request.GET.get('categorias_filter')  # Obtém o parâmetro da URL
        if categorias_filter:
            queryset = queryset.filter(id_categoria=categorias_filter)  # Filtra pelos produtos da categoria
        return queryset


# Criar produto
class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'id_categoria', 'formato', 'id_formato', 'estoqueMin','unidades']
    success_url = reverse_lazy('produto-list')

    def form_valid(self, form):
        # Salva o produto e cria o estoque com qtde 0
        with transaction.atomic():
            response = super().form_valid(form)
            # Acessando o produto recém-criado via self.object
            # Isso já acessa a instância do produto criada
            Estoque.objects.create(id_produto=self.object, qtde=0)
        return response

# Atualizar produto
class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'id_categoria', 'formato', 'id_formato', 'estoqueMin','unidades']
    success_url = reverse_lazy('produto-list')

# Deletar produto
class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'produto_confirm_delete.html'
    success_url = reverse_lazy('produto-list')
    
# ESTOQUE    
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import Estoque

# Listar itens do estoque
class EstoqueListView(LoginRequiredMixin, ListView):
    model = Estoque
    template_name = 'estoque/estoque_list.html'
    context_object_name = 'estoques'
    
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Obtém todas as categorias da base de dados
        estoques = context['estoques']
        # Adicionar o cálculo diretamente ao queryset
        for estoque in estoques:
            estoque.calculo = estoque.qtde * estoque.id_produto.unidades
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        categorias_filter = self.request.GET.get('categorias_filter')  # Parâmetro da URL
        if categorias_filter:
            queryset = queryset.filter(id_produto__id_categoria=categorias_filter)
        return queryset
    
    
