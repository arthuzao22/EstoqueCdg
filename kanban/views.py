from django.views.generic import ListView
from .models import Kanban
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


class KanBanListView(ListView):
    model = Kanban
    template_name = 'kanban.html'
    context_object_name = 'kanban_list'  # Nome usado no template

class KanbanUpdateView(UpdateView):
    model = Kanban
    fields = ['nome']
    template_name = 'kanban_form.html'
    success_url = reverse_lazy('kanban-list')

class KanbanDeleteView(DeleteView):
    model = Kanban
    template_name = 'kanban_confirm_delete.html'
    success_url = reverse_lazy('kanban-list')
