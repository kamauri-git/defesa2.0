from django.urls import path
from . import views
from ocorrencias.views import graficos_ocorrencias
from .views import gerar_relatorio_pdf

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('cadastro/', views.cadastro_ocorrencia, name='cadastro_ocorrencia'),  # Cadastro de ocorrências
    path('salvar/', views.salvar_ocorrencia, name='salvar_ocorrencia'),
    path('lista/', views.lista_ocorrencias, name='lista_ocorrencias'),  # Lista de ocorrências
    path('relatorios/', views.busca_relatorios, name='relatorios'),  # Nova URL para busca e relatórios
    path('gerar_relatorio_pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),  # URL para gerar PDF
    path('ocorrencia/editar/<int:id>/', views.editar_ocorrencia_inline, name='editar_ocorrencia_inline'),
    path('ocorrencia/excluir/<int:id>/', views.excluir_ocorrencia, name='excluir_ocorrencia'),
    path('graficos/', graficos_ocorrencias, name='graficos_ocorrencias'),
    path('relatorio/pdf/', gerar_relatorio_pdf, name='relatorio_pdf')

]
