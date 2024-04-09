from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from main.views import CandidatoCreateView, CandidatoListView, CadastroCandidatoUpdate, CadastroCandidatoDelete
from main.views import CadastroExaminadorList, CadastroExaminadorUpdate, CadastroExaminadorCreate, CadastroExaminadorDelete
from main.views import CadastroTipoList, CadastroTipoCreate, CadastroTipoUpdate, CadastroTipoDelete
from main.views import CadastroAvaliacaoList, CadastroAvaliacaoDelete, CadastroAvaliacaoCreate, CadastroAvaliacaoUpdate
from main.views import CadastroConcursoDelete, CadastroConcursoCreate, CadastroConcursoList, CadastroConcursoUpdate
from main.views import ConsultaMedias, VerificaHabilitadosList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('candidato-form', CandidatoCreateView.as_view(template_name='candidato_form.html'), name='candidato_form'),
    path('candidato-list', CandidatoListView.as_view(template_name='candidato_list.html'), name='candidato_list'),
    path("update-candidato/<int:pk>", CadastroCandidatoUpdate.as_view(template_name='candidato_form.html'), name='candidato_update'),
    path("delete-candidato/<int:pk>", CadastroCandidatoDelete.as_view(template_name='candidato_confirm_delete.html'), name="candidato_delete"),
    path('examinador-form', CadastroExaminadorCreate.as_view(template_name='examinador_form.html'), name='examinador_form'),
    path('examinador-list', CadastroExaminadorList.as_view(template_name='examinador_list.html'), name='examinador_list'),
    path("update-examinador/<int:pk>", CadastroExaminadorUpdate.as_view(template_name='examinador_form.html'), name='examinador_update'),
    path("delete-examinador/<int:pk>", CadastroExaminadorDelete.as_view(template_name='examinador_confirm_delete.html'), name="examinador_delete"),
    path('tipo-list', CadastroTipoList.as_view(template_name='tipo_list.html'), name='tipo_list'),
    path('tipo-form', CadastroTipoCreate.as_view(template_name='tipo_form.html'), name='tipo_form'),
    path("update-tipo/<int:pk>", CadastroTipoUpdate.as_view(template_name='tipo_form.html'), name='tipo_update'),
    path("delete-tipo/<int:pk>", CadastroTipoDelete.as_view(template_name='tipo_confirm_delete.html'), name="tipo_delete"),
    path('avaliacao-list', CadastroAvaliacaoList.as_view(), name='avaliacao_list'),
    path('avaliacao-form', CadastroAvaliacaoCreate.as_view(), name='avaliacao_form'),
    path("update-avalicao/<int:pk>", CadastroAvaliacaoUpdate.as_view(), name='avaliacao_update'),
    path("delete-avaliacao/<int:pk>", CadastroAvaliacaoDelete.as_view(), name="avaliacao_delete"),
    path('concurso-list', CadastroConcursoList.as_view(), name='concurso_list'),
    path('concurso-form', CadastroConcursoCreate.as_view(), name='concurso_form'),
    path("update-concurso/<int:pk>", CadastroConcursoUpdate.as_view(), name='concurso_update'),
    path("delete-concurso/<int:pk>", CadastroConcursoDelete.as_view(), name="concurso_delete"),
    path('medias-list', ConsultaMedias.as_view(), name='medias_list'),
    path('habilitados-list', VerificaHabilitadosList.as_view(), name='habilitados_list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
