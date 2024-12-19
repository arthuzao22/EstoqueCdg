from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .models import Empresa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


# Lista de empresas
class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = 'empresa_list.html'
    context_object_name = 'empresas'
    def get(self, request):
        empresas = Empresa.objects.all()  # Obtenha a lista de empresas
        return render(request, 'empresa_list.html', {'empresas': empresas})

    def post(self, request):
        # Receba os dados enviados via POST
        nova_empresa = request.POST.get('empresa')
        nova_endereco = request.POST.get('endereco')
        print(nova_empresa)
        if nova_empresa:
            Empresa.objects.create(nome=nova_empresa, endereco=nova_endereco)  # Cria uma nova empresa
        return HttpResponseRedirect(reverse('empresa-list'))

# Criar uma nova empresa
class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    template_name = 'empresa_form.html'
    fields = ['nome', 'endereco']
    success_url = reverse_lazy('empresa-list')

# Deletar uma empresa
class EmpresaDeleteView(LoginRequiredMixin, DeleteView):
    model = Empresa
    template_name = 'empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa-list')
