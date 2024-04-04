from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Notas

class NotasListView(ListView):
    model = Notas
    template_name = 'notas_list.html'
    paginate_by = 10
    
class NotasCreateView(CreateView):
    model = Notas
    template_name = 'notas_form.html'
    fields = [ 'candidato', 'examinador_1', 'examinador_2', 'examinador_3', 'examinador_4', 'examinador_5', 'prova_id' ]
    success_url = reverse_lazy("notas_form")

class NotasUpdateView(UpdateView):
    model = Notas
    fields = [ 'candidato', 'examinador_1', 'examinador_2', 'examinador_3', 'examinador_4', 'examinador_5', 'prova_id' ]
    template_name = 'notas_form.html'
    success_url = reverse_lazy("notas_list")

class NotasDeleteView(DeleteView):
    model = Notas
    template_name = 'notas_form.html'
    fields = [ 'candidato', 'examinador_1', 'examinador_2', 'examinador_3', 'examinador_4', 'examinador_5', 'prova_id' ]
    success_url = reverse_lazy("notas_list")