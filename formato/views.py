from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages  # Para mensagens do front-end
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Formato


# Lista de formatos
class FormatoListView(LoginRequiredMixin, ListView):
    def get(self, request):
        try:
            formatos = Formato.objects.all()  # Obtenha a lista de formatos
            return render(request, 'formato_list.html', {'formatos': formatos})
        except Exception as e:
            messages.error(request, f"Erro ao carregar a lista de formatos: {str(e)}")
            return render(request, 'formato_list.html', {'formatos': []})

    def post(self, request):
        try:
            # Receba os dados enviados via POST
            nova_formato = request.POST.get('formato')
            if nova_formato:
                Formato.objects.create(formato=nova_formato)  # Cria um novo formato
                messages.success(request, "Formato criado com sucesso!")
            else:
                messages.error(request, "Por favor, insira um formato válido.")
            return HttpResponseRedirect(reverse('formato-list'))
        except Exception as e:
            messages.error(request, f"Erro ao criar o formato: {str(e)}")
            return HttpResponseRedirect(reverse('formato-list'))


# Criar um novo formato
class FormatoCreateView(LoginRequiredMixin, CreateView):
    model = Formato
    template_name = 'formato_form.html'
    fields = ['formato']
    success_url = reverse_lazy('formato-list')

    def form_valid(self, form):
        try:
            messages.success(self.request, "Formato criado com sucesso!")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Erro ao criar o formato: {str(e)}")
            return self.form_invalid(form)


# Deletar um formato
class FormatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Formato
    template_name = 'formato_confirm_delete.html'
    success_url = reverse_lazy('formato-list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, "Formato deletado com sucesso!")
            return response
        except Exception as e:
            messages.error(request, f"Erro ao deletar o formato: {str(e)}")
            return HttpResponseRedirect(self.success_url)
