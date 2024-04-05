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
    fields = [ 'candidato', 'examinador_1', 'examinador_2', 'examinador_3', 'examinador_4', 'examinador_5', 'prova' ]
    success_url = reverse_lazy("notas_form")

class NotasUpdateView(UpdateView):
    model = Notas
    fields = [ 'candidato', 'examinador_1', 'examinador_2', 'examinador_3', 'examinador_4', 'examinador_5', 'prova' ]
    template_name = 'notas_form.html'
    success_url = reverse_lazy("notas_list")

class NotasDeleteView(DeleteView):
    model = Notas
    template_name = 'notas_form.html'
    fields = [ 'candidato', 'examinador_1', 'examinador_2', 'examinador_3', 'examinador_4', 'examinador_5', 'prova' ]
    success_url = reverse_lazy("notas_list")

class MediaPonderadaView(ListView):
    template_name = 'media_list.html'
    context_object_name = 'medias'

    def get_queryset(self):
        queryset = (
            Notas.objects.raw('''
                SELECT
                    n.id, n.candidato,
                    sum(n.examinador_1*p.peso)/sum(p.peso) AS media_1,
                    sum(n.examinador_2*p.peso)/sum(p.peso) AS media_2,
                    sum(n.examinador_3*p.peso)/sum(p.peso) AS media_3,
                    sum(n.examinador_4*p.peso)/sum(p.peso) AS media_4,
                    sum(n.examinador_5*p.peso)/sum(p.peso) AS media_5
                FROM 
                    main_notas n 
                INNER JOIN
                    main_pesos p 
                ON
                    n.prova_id = p.id
                GROUP BY
                    candidato
            ''')
        )
        return queryset