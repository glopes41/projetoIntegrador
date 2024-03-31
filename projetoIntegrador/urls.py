from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from main.views import CadastroCandidatosCreate, CadastroCandidatosList, CadastroCandidatoUpdate, CadastroCandidatoDelete
from main.views import CadastroExaminadorList, CadastroExaminadorUpdate, CadastroExaminadorCreate, CadastroExaminadorDelete
from main.views import CadastroTipoList, CadastroTipoCreate, CadastroTipoUpdate, CadastroTipoDelete
from main.views import CadastroProvaList, CadastroProvaCreate, CadastroProvaUpdate, CadastroProvaDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('candidato-form', CadastroCandidatosCreate.as_view(template_name='candidato_form.html'), name='candidato_form'),
    path('candidato-list', CadastroCandidatosList.as_view(template_name='candidato_list.html'), name='candidato_list'),
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
    path('prova-list', CadastroProvaList.as_view(template_name='prova_list.html'), name='prova_list'),
    path('prova-form', CadastroProvaCreate.as_view(template_name='prova_form.html'), name='prova_form'),
    path("update-prova/<int:pk>", CadastroProvaUpdate.as_view(template_name='prova_form.html'), name='prova_update'),
    path("delete-prova/<int:pk>", CadastroProvaDelete.as_view(template_name='prova_confirm_delete.html'), name="prova_delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
