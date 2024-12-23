from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from .models import Categoria

class CategoriaListView(LoginRequiredMixin, View):
    def get(self, request):
        categorias = Categoria.objects.all()  # Obtenha todas as categorias
        return render(request, 'categoria_list.html', {'categorias': categorias})

    def post(self, request):
        # Processar o formulário manualmente
        nova_categoria = request.POST.get('categoria')
        imagem = request.FILES.get('img')  # Obter o arquivo de imagem enviado
        if nova_categoria:
            Categoria.objects.create(categoria=nova_categoria, img=imagem)  # Criar nova categoria com imagem
        return HttpResponseRedirect(reverse_lazy('categoria-list'))


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    template_name = 'categoria_list.html'  # Usando o mesmo template
    fields = ['categoria', 'img']
    success_url = reverse_lazy('categoria-list')


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')
