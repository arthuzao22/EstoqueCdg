from django.contrib import admin
from django.urls import path
from empresa.views import EmpresaListView, EmpresaCreateView, EmpresaDeleteView
from categoria.views import CategoriaListView, CategoriaCreateView, CategoriaDeleteView
from formato.views import FormatoListView, FormatoCreateView, FormatoDeleteView
from produto.views import ProdutoListView, ProdutoCreateView, ProdutoUpdateView, ProdutoDeleteView, EstoqueListView
from movimentacoes.views import  MovimentacoesListView, MovimentacoesCreateView, MovimentacoesDeleteView, filtrar_produtos_por_formato
from usuarios.views import register_view, login_view
from home.views import home_view
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    # Rotas para Empresa
    path('empresa/', EmpresaListView.as_view(), name='empresa-list'),
    path('empresa/novo/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('empresa/<int:pk>/deletar/', EmpresaDeleteView.as_view(), name='empresa-delete'),

    # Rotas para Formato
    path('formato/', FormatoListView.as_view(), name='formato-list'),
    path('formato/novo/', FormatoCreateView.as_view(), name='formato-create'),
    path('formato/<int:pk>/deletar/', FormatoDeleteView.as_view(), name='formato-delete'),
    
    # Rotas para categoria
    path('categoria/', CategoriaListView.as_view(), name='categoria-list'),
    path('categoria/novo/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categoria/<int:pk>/deletar/', CategoriaDeleteView.as_view(), name='categoria-delete'),
    
    # Rotas para o produto
    path('produto/', ProdutoListView.as_view(), name='produto-list'),
    path('produto/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('produto/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto-update'),
    path('produto/<int:pk>/deletar/', ProdutoDeleteView.as_view(), name='produto-delete'),
    
    #Rotas para movimentações
    path('movimentacoes/', MovimentacoesListView.as_view(), name='movimentacoes-list'),
    path('movimentacoes/novo/', MovimentacoesCreateView.as_view(), name='movimentacoes-create'),
    path('movimentacoes/<int:pk>/deletar/', MovimentacoesDeleteView.as_view(), name='movimentacoes-delete'),
    path('filtrar-produtos/', filtrar_produtos_por_formato, name='filtrar_produtos'),

    
    # Rotas para Estoque
    path('estoque/', EstoqueListView.as_view(), name='estoque-list'),
    
    #Rotas para Usuarios
    path('usuarios/login/', login_view, name='usuarios-login'),
    path('usuarios/register/', register_view, name='usuarios-register'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
