from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .models import Formato
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


# Lista de formatos
class FormatoListView(LoginRequiredMixin, ListView):
    def get(self, request):
        formatos = Formato.objects.all()  # Obtenha a lista de formatos
        return render(request, 'formato_list.html', {'formatos': formatos})

    def post(self, request):
        # Receba os dados enviados via POST
        nova_formato = request.POST.get('formato')
        if nova_formato:
            Formato.objects.create(formato=nova_formato)  # Cria um novo formato
        return HttpResponseRedirect(reverse('formato-list'))


# Criar um novo formato
class FormatoCreateView(LoginRequiredMixin, CreateView):
    model = Formato
    template_name = 'formato_form.html'
    fields = ['formato']
    success_url = reverse_lazy('formato-list')

# Deletar um formato
class FormatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Formato
    template_name = 'formato_confirm_delete.html'
    success_url = reverse_lazy('formato-list')
