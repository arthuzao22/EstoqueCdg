from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages  # Para mensagens do front-end
from django.views import View
from .models import Categoria


class CategoriaListView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            categorias = Categoria.objects.all()  # Obtenha todas as categorias
            return render(request, 'categoria_list.html', {'categorias': categorias})
        except Exception as e:
            messages.error(request, f"Erro ao carregar as categorias: {str(e)}")
            return render(request, 'categoria_list.html', {'categorias': []})

    def post(self, request):
        try:
            # Processar o formulário manualmente
            nova_categoria = request.POST.get('categoria')
            imagem = request.FILES.get('img')  # Obter o arquivo de imagem enviado
            if nova_categoria:
                Categoria.objects.create(categoria=nova_categoria, img=imagem)  # Criar nova categoria com imagem
                messages.success(request, "Categoria criada com sucesso!")
            else:
                messages.error(request, "Por favor, insira um nome válido para a categoria.")
            return HttpResponseRedirect(reverse_lazy('categoria-list'))
        except Exception as e:
            messages.error(request, f"Erro ao criar a categoria: {str(e)}")
            return HttpResponseRedirect(reverse_lazy('categoria-list'))


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    template_name = 'categoria_list.html'  # Usando o mesmo template
    fields = ['categoria', 'img']
    success_url = reverse_lazy('categoria-list')

    def form_valid(self, form):
        try:
            messages.success(self.request, "Categoria criada com sucesso!")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Erro ao criar a categoria: {str(e)}")
            return self.form_invalid(form)


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Categoria deletada com sucesso!")
            return response
        except Exception as e:
            messages.error(request, f"Erro ao deletar a categoria: {str(e)}")
            return HttpResponseRedirect(self.success_url)
