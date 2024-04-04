from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from main.views import NotasCreateView, NotasDeleteView, NotasListView, NotasUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('notas-form', NotasCreateView.as_view(), name='notas_form'),
    path('notas-list', NotasListView.as_view(), name='notas_list'),
    path("update-notas/<int:pk>", NotasUpdateView.as_view(), name='notas_update'),
    path("delete-notas/<int:pk>", NotasDeleteView.as_view(), name="notas_delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
