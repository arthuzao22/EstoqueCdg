from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Movimentacoes
from django.shortcuts import get_object_or_404
from produto.models import Estoque
from django.http import HttpResponse
from .forms import MovimentacoesForm
from formato.models import Formato  # Importação do modelo Categoria
from categoria.models import Categoria  # Importação do modelo Categoria
from django.http import HttpResponse
from django.http import JsonResponse
from produto.models import Produto  # Certifique-se de que está importando o modelo Produto corretamente

def filtrar_produtos_por_formato(request):
    id_categoria = request.GET.get('id_categoria')  # Corrigido para 'id_categoria'
    print(id_categoria)
    if id_categoria:
        produtos = Produto.objects.filter(id_categoria=id_categoria)
        produtos_data = [{'id': produto.id, 'nome': produto.nome} for produto in produtos]
        # for produtos_data in produtos_data:
        #     print(produtos_data)
        return JsonResponse(produtos_data, safe=False)
    return JsonResponse([], safe=False)

# Listar movimentações
class MovimentacoesListView(LoginRequiredMixin, ListView):
    model = Movimentacoes
    template_name = 'movimentacoes_list.html'
    context_object_name = 'movimentacoes'

# Criar movimentação
class MovimentacoesCreateView(LoginRequiredMixin, CreateView):
    model = Movimentacoes
    form_class = MovimentacoesForm
    template_name = 'movimentacoes_form.html'
    success_url = reverse_lazy('movimentacoes-list')

    def form_valid(self, form):
        form.instance.id_usuario = self.request.user
        try:
            estoque = Estoque.objects.get(id_produto=form.cleaned_data['id_produto'])
        except Estoque.DoesNotExist:
            form.add_error('id_produto', 'Produto não encontrado no estoque.')
            return self.form_invalid(form)

        if form.cleaned_data['tipo_movimentacao'] == 'Entrada':
            estoque.qtde += form.cleaned_data['qtde']
        elif form.cleaned_data['tipo_movimentacao'] == 'Saída':
            if estoque.qtde >= form.cleaned_data['qtde']:
                estoque.qtde -= form.cleaned_data['qtde']
            else:
                form.add_error('qtde', 'Quantidade insuficiente no estoque.')
                return self.form_invalid(form)

        estoque.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Envia as categorias para o template
        return context

class MovimentacoesDeleteView(LoginRequiredMixin, DeleteView):
    model = Movimentacoes
    template_name = 'movimentacoes_confirm_delete.html'
    success_url = reverse_lazy('movimentacoes-list')

    def form_valid(self, request, *args, **kwargs):
        print('entrouy aqui')
        obj = self.get_object()
        estoque = Estoque.objects.get(id_produto=obj.id_produto)
        if obj.tipo_movimentacao == 'Entrada':
            estoque.qtde -= obj.qtde
        elif obj.tipo_movimentacao == 'Saída':
            estoque.qtde += obj.qtde
        estoque.save()
        return super().delete(request, *args, **kwargs)

