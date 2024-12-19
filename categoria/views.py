from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categoria
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View

class CategoriaListView(LoginRequiredMixin, View):
    def get(self, request):
        categorias = Categoria.objects.all()  # Obtenha a lista de categorias
        return render(request, 'categoria_list.html', {'categorias': categorias})

    def post(self, request):
        # Receba os dados enviados via POST
        nova_categoria = request.POST.get('categoria')
        if nova_categoria:
            Categoria.objects.create(categoria=nova_categoria)  # Cria uma nova categoria
        return HttpResponseRedirect(reverse('categoria-list'))


# Criar categoria
class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    template_name = 'categoria_list.html'  # O template agora é o mesmo para criação e listagem
    fields = ['categoria']
    success_url = reverse_lazy('categoria-list')  # Redireciona após criação para a lista

# Deletar categoria
class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')
