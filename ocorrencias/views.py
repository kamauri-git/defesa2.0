import io
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from ocorrencias.models import Ocorrencia
from .forms import OcorrenciaForm
from django.utils import timezone
from .models import Ocorrencia
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.db.models import Q

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

def gerar_relatorio_pdf(request):
    # Filtros: obter parâmetros da requisição (ex: data, bairro, etc)
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)
    bairro = request.GET.get('bairro', None)
    
    # Filtrar ocorrências com base nos parâmetros (ajuste conforme necessário)
    ocorrencias = Ocorrencia.objects.all()
    
    if data_inicial:
        ocorrencias = ocorrencias.filter(data__gte=data_inicial)
    
    if data_final:
        ocorrencias = ocorrencias.filter(data__lte=data_final)
    
    if bairro:
        ocorrencias = ocorrencias.filter(bairro__icontains=bairro)
    
    # Criando o PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    text = p.beginText(40, 750)
    text.setFont("Helvetica", 10)

    text.textLine("Relatório de Ocorrências")
    text.textLine("-" * 40)

    # Adicionar as ocorrências ao PDF
    for ocorrencia in ocorrencias:
        text.textLine(f"N.º: {ocorrencia.numero} | SIGRC: {ocorrencia.sigrc} | "
                      f"Endereço: {ocorrencia.endereco} | Bairro: {ocorrencia.bairro} | "
                      f"Distrito: {ocorrencia.distrito} | Data: {ocorrencia.data}")
    
    p.drawText(text)
    p.showPage()
    p.save()

    # Enviar o PDF como resposta
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


# Função para página de busca e relatórios
def busca_relatorios(request):
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    endereco = request.GET.get('endereco')
    distrito = request.GET.get('distrito')
    motivo = request.GET.get('motivo')
    
    ocorrencias = Ocorrencia.objects.all()

    if data_inicial and data_final:
        ocorrencias = ocorrencias.filter(data__range=[data_inicial, data_final])

    if endereco:
        ocorrencias = ocorrencias.filter(endereco__icontains=endereco)
    
    if distrito:
        ocorrencias = ocorrencias.filter(distrito__icontains=distrito)
    
    if motivo:
        ocorrencias = ocorrencias.filter(motivo__icontains=motivo)

    return render (request, 'ocorrencias/relatorios.html', {'ocorrencias': ocorrencias})

