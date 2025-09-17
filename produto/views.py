from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages  # Para mensagens do front-end
from .models import Produto
from .models import Estoque
from rest_framework.response import Response
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from categoria.models import Categoria
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect

# PRODUTOS
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produto_list.html'
    context_object_name = 'produtos'
         
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['categorias'] = Categoria.objects.all()
            context['produtos_estoque_min'] = self.get_desativados()  # Produtos desativados
            return context
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao carregar os dados: {str(e)}")
            return {}

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            categorias_filter = self.request.GET.get('categorias_filter')
            if categorias_filter:
                queryset = queryset.filter(id_categoria=categorias_filter, status=1)
            else:
                queryset = queryset.filter(id_categoria=1)
            return queryset
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao filtrar os produtos: {str(e)}")
            return Produto.objects.none()

    def get_desativados(self):
        return Produto.objects.filter(status=0)


# Criar produto
class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'id_categoria', 'formato', 'id_formato', 'estoquemin', 'unidades']
    success_url = reverse_lazy('produto-list')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Define o status como 1 antes de salvar
                form.instance.status = 1
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


class ProdutoStatusView(LoginRequiredMixin, View):
    success_url = reverse_lazy('produto-list')

    def post(self, request, *args, **kwargs):
        produto = get_object_or_404(Produto, pk=kwargs['pk'])
        acao = request.POST.get('acao')  # Recebe a ação do formulário (ativar/desativar)

        try:
            if acao == 'desativar':
                produto.status = 0
                messages.success(request, f"Produto {produto.nome} desativado com sucesso!")
            elif acao == 'ativar':
                produto.status = 1
                messages.success(request, f"Produto {produto.nome} ativado com sucesso!")
            else:
                messages.error(request, "Ação inválida.")
                return redirect(self.success_url)

            produto.save()
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")

        return redirect(self.success_url)

# ESTOQUE

# Listar itens do estoque
class EstoqueListView(LoginRequiredMixin, ListView):
    model = Estoque
    template_name = 'estoque/estoque_list.html'
    context_object_name = 'estoques'
    
    def get_queryset(self):
        return Estoque.objects.exclude(qtde=0)

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
                queryset = queryset.filter(id_produto__id_categoria=categorias_filter).exclude(qtde=0)
            else:
                queryset = queryset.filter(id_produto__id_categoria=1).exclude(qtde=0)  # Filtro padrão (id_categoria=1)

            return queryset
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro ao filtrar os estoques: {str(e)}")
            return Estoque.objects.none()


class PublicEstoqueListView(ListView):
    """Página pública do estoque (sem necessidade de login).

    Exibe itens em estoque (qtde != 0) e permite filtro por categoria via
    parâmetro GET `categorias_filter`.
    """
    model = Estoque
    template_name = 'estoque/estoque_public.html'
    context_object_name = 'estoques'
    paginate_by = 24

    def get_queryset(self):
        try:
            queryset = Estoque.objects.exclude(qtde=0)
            categorias_filter = self.request.GET.get('categorias_filter')
            if categorias_filter:
                queryset = queryset.filter(id_produto__id_categoria=categorias_filter).exclude(qtde=0)
            return queryset
        except Exception:
            return Estoque.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        # Adiciona o cálculo para exibição (unidades * qtde)
        for estoque in context.get('estoques', []):
            estoque.calculo = estoque.qtde * estoque.id_produto.unidades
        return context
 
