from django.contrib import admin
from django.urls import path, include
from ocorrencias import views  # Adicione esta linha para importar o views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relatorios/', views.busca_relatorios, name='relatorios'),
    path('', include('ocorrencias.urls')),  # Certifique-se de que o app está incluído corretamente
]
