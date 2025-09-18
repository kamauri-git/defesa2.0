import io
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.db.models import Count
from django.db import IntegrityError
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .models import Ocorrencia
from .forms import OcorrenciaForm
from django.http import JsonResponse
from django.db.models import Count
from django.utils.dateparse import parse_date


# --------------------- LOGIN / LOGOUT ---------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redireciona para 'next' se veio de uma página protegida
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')  # Senão, vai para home
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


# --------------------- PÁGINA HOME ---------------------

@login_required
def home(request):
    return render(request, "ocorrencias/home.html")


# --------------------- CADASTRO / LISTA ---------------------

@login_required
def cadastro_ocorrencia(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ocorrencias')
    else:
        form = OcorrenciaForm()
    return render(request, 'ocorrencias/cadastro.html', {'form': form})


@login_required
def lista_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all().order_by('-numero')
    return render(request, 'ocorrencias/lista_ocorrencias.html', {'ocorrencias': ocorrencias})


@login_required
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


# --------------------- EDIÇÃO / EXCLUSÃO ---------------------

@login_required
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


@login_required
def excluir_ocorrencia(request, id):
    ocorrencia = get_object_or_404(Ocorrencia, id=id)
    ocorrencia.delete()
    return redirect('lista_ocorrencias')


# --------------------- RELATÓRIOS / GRÁFICOS ---------------------

@login_required
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


@login_required
def graficos_ocorrencias(request):
    tipo = request.GET.get('tipo')
    bairro = request.GET.get('bairro')
    distrito = request.GET.get('distrito')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    ocorrencias = Ocorrencia.objects.all()
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

    motivos_count = ocorrencias.values('motivo').annotate(total=Count('id')).order_by('-total')
    distritos_count = ocorrencias.values('distrito').annotate(total=Count('id')).order_by('-total')

    context = {
        'motivos_count': motivos_count,
        'distritos_count': distritos_count,
        'total_motivos': sum(m['total'] for m in motivos_count),
        'total_distritos': sum(d['total'] for d in distritos_count),
    }
    return render(request, 'ocorrencias/graficos.html', context)


@login_required
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
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    elementos = [Paragraph("Relatório de Ocorrências", styles['Title']), Spacer(1, 12)]

    dados = [['Número', 'Data', 'Motivo', 'Bairro', 'Distrito', 'Endereço']]
    for o in ocorrencias:
        dados.append([
            str(o.numero),
            o.data.strftime('%d/%m/%Y') if o.data else '',
            o.motivo,
            o.bairro,
            o.distrito,
            o.endereco
        ])

    tabela = Table(dados, colWidths=[50, 70, 150, 100, 100, 200], repeatRows=1, hAlign='CENTER')
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgoldenrodyellow),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.darkorange),
    ]))
    elementos.append(tabela)

    doc.build(elementos)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_ocorrencias.pdf"'
    return response

@login_required
def graficos_ocorrencias(request):
    distrito = request.GET.get('distrito')
    motivo = request.GET.get('motivo')

    qs = Ocorrencia.objects.all()
    if distrito: qs = qs.filter(distrito=distrito)
    if motivo: qs = qs.filter(motivo=motivo)

    motivos_count = list(qs.values('motivo').annotate(total=Count('motivo')))
    distritos_count = list(qs.values('distrito').annotate(total=Count('distrito')))

    return JsonResponse({
        'motivos': {'labels':[m['motivo'] for m in motivos_count], 'data':[m['total'] for m in motivos_count]},
        'distritos': {'labels':[d['distrito'] for d in distritos_count], 'data':[d['total'] for d in distritos_count]},
        'total_motivos': sum(m['total'] for m in motivos_count),
        'total_distritos': sum(d['total'] for d in distritos_count),
    })

@login_required
def graficos_ajax(request):
    motivo = request.GET.get('motivo', '')
    distrito = request.GET.get('distrito', '')

    qs = Ocorrencia.objects.all()
    if motivo: qs = qs.filter(motivo=motivo)
    if distrito: qs = qs.filter(distrito=distrito)

    motivos_data = list(qs.values('motivo').annotate(total=Count('motivo')))
    distritos_data = list(qs.values('distrito').annotate(total=Count('distrito')))

    return JsonResponse({'motivos': motivos_data, 'distritos': distritos_data})

@login_required
def graficos_page(request):
    return render(request, 'ocorrencias/graficos.html')

@login_required
def graficos_data(request):
    """Retorna dados JSON filtráveis para os gráficos"""
    # Filtros opcionais via GET
    distrito = request.GET.get('distrito')
    motivo = request.GET.get('motivo')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    qs = Ocorrencia.objects.all()

    if distrito:
        qs = qs.filter(distrito=distrito)
    if motivo:
        qs = qs.filter(motivo=motivo)
    if data_inicial:
        qs = qs.filter(data__gte=parse_date(data_inicial))
    if data_final:
        qs = qs.filter(data__lte=parse_date(data_final))

    # Contagem por motivo
    motivos_count = qs.values('motivo').annotate(total=Count('id')).order_by('-total')
    distritos_count = qs.values('distrito').annotate(total=Count('id')).order_by('-total')

    data = {
        "motivos": {
            "labels": [m['motivo'] for m in motivos_count],
            "data": [m['total'] for m in motivos_count],
        },
        "distritos": {
            "labels": [d['distrito'] for d in distritos_count],
            "data": [d['total'] for d in distritos_count],
        },
        "total_motivos": sum([m['total'] for m in motivos_count]),
        "total_distritos": sum([d['total'] for d in distritos_count]),
    }
    return JsonResponse(data)
