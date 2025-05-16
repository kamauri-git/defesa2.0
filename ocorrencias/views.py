import io
from django.db.models import Count
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
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from io import BytesIO





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
    ocorrencias = Ocorrencia.objects.all().order_by('-numero')
    return render(request, 'ocorrencias/lista_ocorrencias.html', {'ocorrencias': ocorrencias})

# Função para relatórios
def relatorios(request):
    return render(request, 'ocorrencias/relatorios.html')

# Função para salvar a ocorrência

# Função para listar todas as ocorrências
def listar_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all().order_by('-numero')
    return render(request, 'ocorrencias/lista_ocorrencias.html', {'ocorrencias': ocorrencias})

def gerar_relatorio_pdf(request):
    # Filtros: obter parâmetros da requisição (ex: data, bairro, etc)
    data_inicio = request.GET.get('data_inicial', None)
    data_fim = request.GET.get('data_final', None)
    bairro = request.GET.get('bairro', None)
    
    # Filtrar ocorrências com base nos parâmetros (ajuste conforme necessário)
    ocorrencias = Ocorrencia.objects.all().order_by('-numero')
    
    if data_inicio:
        ocorrencias = ocorrencias.filter(data__gte=data_inicial).order_by('-numero')
    
    if data_fim:
        ocorrencias = ocorrencias.filter(data__lte=data_final).order_by('-numero')
    
    if bairro:
        ocorrencias = ocorrencias.filter(bairro__icontains=bairro).order_by('-numero')
      
     
# Função para página de busca e relatórios
def busca_relatorios(request):
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    endereco = request.GET.get('endereco')
    distrito = request.GET.get('distrito')
    motivo = request.GET.get('motivo')
    
    ocorrencias = Ocorrencia.objects.all().order_by('-numero')

    if data_inicial and data_final:
        ocorrencias = ocorrencias.filter(data__range=[data_inicial, data_final])
    elif data_inicial:
        ocorrencias = ocorrencias.filter(data__gte=data_inicial)
    elif data_final:
        ocorrencias = ocorrencias.filter(data__lte=data_final)

    if endereco:
        ocorrencias = ocorrencias.filter(endereco__icontains=endereco)
    
    if distrito:
        ocorrencias = ocorrencias.filter(distrito__icontains=distrito)
    
    if motivo:
        ocorrencias = ocorrencias.filter(motivo__icontains=motivo)

    return render(request, 'ocorrencias/relatorios.html', {'ocorrencias': ocorrencias})


@require_POST
def editar_ocorrencia_inline(request, id):
    ocorrencia = get_object_or_404(Ocorrencia, id=id)

    ocorrencia.numero = request.POST.get('numero')
    ocorrencia.sigrc = request.POST.get('sigrc')
    ocorrencia.endereco = request.POST.get('endereco')
    ocorrencia.bairro = request.POST.get('bairro')
    ocorrencia.distrito = request.POST.get('distrito')
    ocorrencia.area_risco = request.POST.get('area_risco')
    ocorrencia.motivo = request.POST.get('motivo')
    ocorrencia.data = request.POST.get('data')

    ocorrencia.save()

    return redirect('lista_ocorrencias')



def excluir_ocorrencia(request, id):
    ocorrencia = get_object_or_404(Ocorrencia, id=id)
    ocorrencia.delete()
    return redirect('lista_ocorrencias')

def home(request):
    return render(request, 'ocorrencias/home.html')

def graficos_ocorrencias(request):
    # Pegando filtros que vieram via GET
    tipo = request.GET.get('tipo')
    bairro = request.GET.get('bairro')
    distrito = request.GET.get('distrito')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    # Inicializando a consulta de ocorrências
    ocorrencias = Ocorrencia.objects.all()

    # Aplicando filtros
    if tipo:
        ocorrencias = ocorrencias.filter(tipo=tipo)
    if bairro:
        ocorrencias = ocorrencias.filter(bairro=bairro)
    if distrito:
        ocorrencias = ocorrencias.filter(distrito=distrito)
    if data_inicial:
        ocorrencias = ocorrencias.filter(data__gte=data_inicial)
    if data_final:
        ocorrencias = ocorrencias.filter(data__lte=data_final)

    # Agrupando dados para gráficos
    motivos_count = ocorrencias.values('motivo').annotate(total=Count('id')).order_by('-total')
    distritos_count = ocorrencias.values('distrito').annotate(total=Count('id')).order_by('-total')

    # Calculando totais
    total_motivos = sum([motivo['total'] for motivo in motivos_count])
    total_distritos = sum([distrito['total'] for distrito in distritos_count])

    context = {
        'motivos_count': motivos_count,
        'distritos_count': distritos_count,
        'total_motivos': total_motivos,
        'total_distritos': total_distritos,
    }

    return render(request, 'ocorrencias/graficos.html', context)


def salvar_ocorrencia(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('lista_ocorrencias')
            except IntegrityError as e:
                if 'ocorrencias_ocorrencia_numero_key' in str(e):
                    form.add_error('numero', 'Número de FOC já cadastrado.')
    else:
        form = OcorrenciaForm()

    return render(request, 'ocorrencias/cadastro.html', {'form': form})

def gerar_relatorio_pdf(request):
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    motivo = request.GET.get('motivo')
    bairro = request.GET.get('bairro')
    distrito = request.GET.get('distrito')
    endereco = request.GET.get('endereco')

    ocorrencias = Ocorrencia.objects.all().order_by('-numero')

    if data_inicial and data_final:
        ocorrencias = ocorrencias.filter(data__range=[data_inicial, data_final])
    if motivo:
        ocorrencias = ocorrencias.filter(motivo__icontains=motivo)
    if bairro:
        ocorrencias = ocorrencias.filter(bairro__icontains=bairro)
    if distrito:
        ocorrencias = ocorrencias.filter(distrito__icontains=distrito)
    if endereco:
        ocorrencias = ocorrencias.filter(endereco__icontains=endereco)

    buffer = BytesIO()
    # Usar página em paisagem para dar mais largura
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    elementos = []

    titulo = Paragraph("Relatório de Ocorrências", styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    dados = [
        ['Número', 'Data', 'Motivo', 'Bairro', 'Distrito', 'Endereço']
    ]
    for o in ocorrencias:
        dados.append([
            str(o.numero),
            o.data.strftime('%d/%m/%Y') if o.data else '',
            o.motivo,
            o.bairro,
            o.distrito,
            o.endereco,
        ])

    # Definindo larguras relativas para cada coluna (ajuste se quiser)
    colunas_largura = [50, 70, 150, 100, 100, 200]

    tabela = Table(dados, colWidths=colunas_largura, repeatRows=1, hAlign='CENTER')

    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgoldenrodyellow),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.darkorange),
    ])

    tabela.setStyle(estilo)

    elementos.append(tabela)

    doc.build(elementos)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_ocorrencias.pdf"'
    return response