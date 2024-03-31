"""projetoIntegrador URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from main.views import CadastroCandidatosCreate, CadastroCandidatosList, CadastriCandidatoUpdate, CadastroCandidatoDelete
from main.views import CadastroExaminadorList, CadastriExaminadorUpdate, CadastroExaminadorCreate, CadastroExaminadorDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('candidato-form', CadastroCandidatosCreate.as_view(template_name='candidato_form.html'), name='candidato_form'),
    path('candidato-list', CadastroCandidatosList.as_view(template_name='candidato_list.html'), name='candidato_list'),
    path("update-candidato/<int:pk>", CadastriCandidatoUpdate.as_view(template_name='candidato_form.html'), name='candidato_update'),
    path("delete-candidato/<int:pk>", CadastroCandidatoDelete.as_view(template_name='candidato_confirm_delete.html'), name="candidato_delete"),
    path('examinador-form', CadastroExaminadorCreate.as_view(template_name='examinador_form.html'), name='examinador_form'),
    path('examinador-list', CadastroExaminadorList.as_view(template_name='examinador_list.html'), name='examinador_list'),
    path("update-examinador/<int:pk>", CadastriExaminadorUpdate.as_view(template_name='examinador_form.html'), name='examinador_update'),
    path("delete-examinador/<int:pk>", CadastroExaminadorDelete.as_view(template_name='examinador_confirm_delete.html'), name="examinador_delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
