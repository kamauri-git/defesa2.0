from django.contrib import admin
from django.urls import path, include
from ocorrencias import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relatorios/', views.busca_relatorios, name='relatorios'),
    path('', include('ocorrencias.urls')), 
    ]
