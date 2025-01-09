from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages  # Para mensagens do front-end
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Empresa


# Lista de empresas
class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = 'empresa_list.html'
    context_object_name = 'empresas'

    def get(self, request):
        try:
            empresas = Empresa.objects.all()  # Obtenha a lista de empresas
            return render(request, 'empresa_list.html', {'empresas': empresas})
        except Exception as e:
            messages.error(request, f"Erro ao carregar a lista de empresas: {str(e)}")
            return render(request, 'empresa_list.html', {'empresas': []})

    def post(self, request):
        try:
            # Receba os dados enviados via POST
            nova_empresa = request.POST.get('empresa')
            nova_endereco = request.POST.get('endereco')
            if nova_empresa:
                Empresa.objects.create(nome=nova_empresa, endereco=nova_endereco)  # Cria uma nova empresa
                messages.success(request, "Empresa criada com sucesso!")
            else:
                messages.error(request, "Por favor, insira um nome de empresa válido.")
            return HttpResponseRedirect(reverse('empresa-list'))
        except Exception as e:
            messages.error(request, f"Erro ao criar a empresa: {str(e)}")
            return HttpResponseRedirect(reverse('empresa-list'))


# Criar uma nova empresa
class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    template_name = 'empresa_form.html'
    fields = ['nome', 'endereco']
    success_url = reverse_lazy('empresa-list')

    def form_valid(self, form):
        try:
            messages.success(self.request, "Empresa criada com sucesso!")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Erro ao criar a empresa: {str(e)}")
            return self.form_invalid(form)

