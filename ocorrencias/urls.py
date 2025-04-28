from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('cadastro/', views.cadastro_ocorrencia, name='cadastro_ocorrencia'),  # Cadastro de ocorrências
    path('salvar/', views.salvar_ocorrencia, name='salvar_ocorrencia'),
    path('lista/', views.lista_ocorrencias, name='lista_ocorrencias'),  # Lista de ocorrências
    path('relatorios/', views.relatorios, name='relatorios'),  # Relatórios
    path('listar/', views.listar_ocorrencias, name='listar'),
    path('relatorios/', views.busca_relatorios, name='busca_relatorios'),  # Nova URL para busca e relatórios
    path('gerar_relatorio_pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),  # URL para gerar PDF
]
