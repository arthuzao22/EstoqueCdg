from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages  # Para mensagens do front-end
from .models import Movimentacoes
from produto.models import Estoque, Produto
from formato.models import Formato
from categoria.models import Categoria
from .forms import MovimentacoesForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def filtrar_produtos_por_formato(request):
    """Filtra produtos por categoria e formato."""
    try:
        id_categoria = request.GET.get('id_categoria')
        if id_categoria:
            produtos = Produto.objects.filter(id_categoria=id_categoria, status=1)
            produtos_data = [
                {
                    'id': produto.id,
                    'nome': produto.nome,
                    'formato': produto.formato,
                    'id_formato_id': produto.id_formato.formato
                }
                for produto in produtos
            ]
            return JsonResponse(produtos_data, safe=False)
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': f"Erro ao filtrar produtos: {str(e)}"}, status=500)


# Listar movimentações
class MovimentacoesListView(LoginRequiredMixin, ListView):
    model = Movimentacoes
    template_name = 'movimentacoes_list.html'
    context_object_name = 'movimentacoes'
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        queryset = Movimentacoes.objects.order_by("-id")
        paginator = Paginator(queryset, 20)  # Definindo paginação com 10 itens por página
        
        page = request.GET.get('page')
        try:
            movimentacoes = paginator.get_page(page)
        except PageNotAnInteger:
            movimentacoes = paginator.get_page(1)
        except EmptyPage:
            movimentacoes = paginator.get_page(paginator.num_pages)
        
        context = {
            'movimentacoes': movimentacoes,
            'categorias': Categoria.objects.all()
        }
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            categorias = Categoria.objects.order_by("id").filter(id=True)
            context['categorias'] = categorias
            return context
        except Exception as e:
            messages.error(self.request, f"Erro ao carregar movimentações: {str(e)}")
            return {}


# Criar movimentação
class MovimentacoesCreateView(LoginRequiredMixin, CreateView):
    model = Movimentacoes
    form_class = MovimentacoesForm
    template_name = 'movimentacoes_form.html'
    success_url = reverse_lazy('movimentacoes-create')
    
    def post(self, request, *args, **kwargs):
        """Debug: Log de todos os dados POST recebidos"""
        print("🔄 POST REQUEST RECEBIDO:")
        print("📦 Dados POST:", dict(request.POST))
        print("👤 Usuário:", request.user)
        return super().post(request, *args, **kwargs)
    
    def form_invalid(self, form):
        """Debug: Log dos erros quando o formulário é inválido"""
        print("🚨 FORMULÁRIO INVÁLIDO!")
        print("📋 Dados recebidos:", self.request.POST.dict())
        print("❌ Erros do formulário:")
        print(form.errors.as_json())
        
        # Log detalhado para cada campo com erro
        for field, errors in form.errors.items():
            print(f"   Campo '{field}': {errors}")
        
        logger.error(f"Erro de validação no formulário: {form.errors.as_json()}")
        messages.error(self.request, "Há erros no formulário. Verifique os campos destacados.")
        return super().form_invalid(form)

    def form_valid(self, form):
        try:
            form.instance.id_usuario = self.request.user
            estoque = Estoque.objects.get(id_produto=form.cleaned_data['id_produto'])
            if form.cleaned_data['tipo_movimentacao'] == 'Entrada':
                estoque.qtde += form.cleaned_data['qtde']
            elif form.cleaned_data['tipo_movimentacao'] == 'Saída':
                if estoque.qtde >= form.cleaned_data['qtde']:
                    estoque.qtde -= form.cleaned_data['qtde']
                else:
                    form.add_error('qtde', 'Quantidade insuficiente no estoque.')
                    return self.form_invalid(form)
            estoque.save()
            messages.success(self.request, "Movimentação criada com sucesso!")
            return super().form_valid(form)
        except Estoque.DoesNotExist:
            form.add_error('id_produto', 'Produto não encontrado no estoque.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Erro ao criar movimentação: {str(e)}")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['categorias'] = Categoria.objects.all()
            return context
        except Exception as e:
            messages.error(self.request, f"Erro ao carregar contexto: {str(e)}")
            return {}


# Deletar movimentação
class MovimentacoesDeleteView(LoginRequiredMixin, DeleteView):
    model = Movimentacoes
    template_name = 'movimentacoes_confirm_delete.html'
    success_url = reverse_lazy('movimentacoes-list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            estoque = Estoque.objects.get(id_produto=obj.id_produto)
            if obj.tipo_movimentacao == 'Entrada':
                estoque.qtde -= obj.qtde
            elif obj.tipo_movimentacao == 'Saída':
                estoque.qtde += obj.qtde
            estoque.save()
            messages.success(request, "Movimentação excluída e estoque atualizado com sucesso!")
            return super().delete(request, *args, **kwargs)
        except Estoque.DoesNotExist:
            messages.error(request, "Estoque não encontrado para o produto relacionado.")
            return HttpResponse("Estoque não encontrado para o produto", status=400)
        except Exception as e:
            messages.error(request, f"Erro ao deletar movimentação: {str(e)}")
            return HttpResponse(f"Erro: {str(e)}", status=500)
