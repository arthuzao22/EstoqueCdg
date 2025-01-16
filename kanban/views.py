from django.views.generic import ListView
from .models import Kanban
from django.urls import reverse_lazy


class KanBanListView(ListView):
    model = Kanban
    template_name = 'kanban.html'
    context_object_name = 'kanban_list'  # Nome usado no template


