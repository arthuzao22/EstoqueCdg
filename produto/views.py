from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages  # Para mensagens do front-end
from .models import Produto
from .models import Estoque

from categoria.models import Categoria
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect

# PRODUTOS

# Listar produtos
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produto_list.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['categorias'] = Categoria.objects.all()  # Obtém todas as categorias
            return context
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao carregar os dados: {str(e)}")
            return {}

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            categorias_filter = self.request.GET.get('categorias_filter')  # Obtém o parâmetro da URL
            if categorias_filter:
                queryset = queryset.filter(id_categoria=categorias_filter)  # Filtra produtos da categoria
            return queryset
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao filtrar os produtos: {str(e)}")
            return Produto.objects.none()


# Criar produto
class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'id_categoria', 'formato', 'id_formato', 'estoquemin', 'unidades']
    success_url = reverse_lazy('produto-list')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                response = super().form_valid(form)
                # Criação do estoque com quantidade inicial 0
                Estoque.objects.create(id_produto=self.object, qtde=0)
                messages.success(self.request, "Produto criado com sucesso!")
            return response
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao criar o produto: {str(e)}")
            return self.form_invalid(form)


# Atualizar produto
class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'id_categoria', 'formato', 'id_formato', 'estoquemin', 'unidades']
    success_url = reverse_lazy('produto-list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Produto atualizado com sucesso!")
            return response
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao atualizar o produto: {str(e)}")
            return self.form_invalid(form)


# Deletar produto
class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'produto_confirm_delete.html'
    success_url = reverse_lazy('produto-list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Produto deletado com sucesso!")
            return response
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao deletar o produto: {str(e)}")
            return HttpResponseRedirect(self.success_url)


# ESTOQUE

# Listar itens do estoque
class EstoqueListView(LoginRequiredMixin, ListView):
    model = Estoque
    template_name = 'estoque/estoque_list.html'
    context_object_name = 'estoques'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['categorias'] = Categoria.objects.all()  # Obtém todas as categorias
            estoques = context['estoques']
            # Adicionar o cálculo diretamente ao queryset
            for estoque in estoques:
                estoque.calculo = estoque.qtde * estoque.id_produto.unidades
            return context
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao carregar os dados do estoque: {str(e)}")
            return {}

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            categorias_filter = self.request.GET.get('categorias_filter')  # Parâmetro da URL
            if categorias_filter:
                queryset = queryset.filter(id_produto__id_categoria=categorias_filter)
            return queryset
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao filtrar os estoques: {str(e)}")
            return Estoque.objects.none()
