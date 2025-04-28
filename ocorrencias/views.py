from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from ocorrencias.models import Ocorrencia
from .forms import OcorrenciaForm
from django.utils import timezone
from .models import Ocorrencia
from django.http import HttpResponse


# Função para a página inicial
def home(request):
    return render(request, 'ocorrencias/home.html')

# Função para o cadastro de ocorrência
def cadastro_ocorrencia(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            form.save()  # Salva os dados no banco
            return redirect('lista_ocorrencias')  # Redireciona para a lista de ocorrências
    else:
        form = OcorrenciaForm()

    return render(request, 'ocorrencias/cadastro.html', {'form': form})

# Função para lista de ocorrências
def lista_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all()
    return render(request, 'ocorrencias/lista_ocorrencias.html', {'ocorrencias': ocorrencias})

# Função para relatórios
def relatorios(request):
    return render(request, 'ocorrencias/relatorios.html')

# Função para salvar a ocorrência
def salvar_ocorrencia(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        sigrc = request.POST.get('sigrc')
        
        if not numero or not sigrc:
            return HttpResponse("Erro: os campos 'numero' e 'sigrc' são obrigatórios", status=400)

        ocorrencia = Ocorrencia(
            numero=numero,
            sigrc=sigrc,
            endereco=request.POST.get('endereco'),
            bairro=request.POST.get('bairro'),
            distrito=request.POST.get('distrito'),
            area_risco=request.POST.get('area_risco'),
            motivo=request.POST.get('motivo'),
            data=request.POST.get('data')
        )
        ocorrencia.save()
        return redirect('lista_ocorrencias')  # redireciona para a lista de ocorrências
    return redirect('cadastro_ocorrencia')  # caso não seja POST, retorna ao cadastro


# Função para listar todas as ocorrências
def listar_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all()
    return render(request, 'ocorrencias/lista_ocorrencias.html', {'ocorrencias': ocorrencias})




