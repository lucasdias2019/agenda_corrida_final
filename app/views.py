from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse 
from .models import ModeloDeCorrida, HistoricoCorrida
from .forms import ModeloDeCorridaForm, HistoricoCorridaForm 

# Função auxiliar para simular o usuário logado para o CRUD
def get_user_logged_in():
    """Tenta obter o usuário de teste; se não existir, o cria."""
    try:
        return User.objects.get(username='corredor_teste')
    except User.DoesNotExist:
        user = User.objects.create_user('corredor_teste', 'teste@agenda.com', '123456')
        return user

def popular_banco_dados(request):
    """Cria dados de teste para demonstração (Rota /popular-bd/)."""
    user = get_user_logged_in()
    
    # Modelos de corrida 
    ModeloDeCorrida.objects.get_or_create(usuario=user, nome='Treino Padrão 5km', defaults={'distancia_planejada_km': 5.0, 'duracao_estimada_min': 30, 'objetivo': 'Manter ritmo'})
    ModeloDeCorrida.objects.get_or_create(usuario=user, nome='Treino Leve 3km', defaults={'distancia_planejada_km': 3.0, 'duracao_estimada_min': 20, 'objetivo': 'Recuperação'})
    
    # Histórico de corridas 
    try:
        modelo_5k = ModeloDeCorrida.objects.get(usuario=user, nome='Treino Padrão 5km')
        if HistoricoCorrida.objects.filter(usuario=user).count() < 2:
            HistoricoCorrida.objects.create(usuario=user, modelo_corrida=modelo_5k, data_realizacao=timezone.now() - timedelta(days=7), tempo_total_min=35, observacoes='Ótimo tempo inicial.')
            HistoricoCorrida.objects.create(usuario=user, modelo_corrida=modelo_5k, data_realizacao=timezone.now() - timedelta(days=3), tempo_total_min=42, observacoes='Corrida de recuperação tranquila.')
    except ModeloDeCorrida.DoesNotExist:
        pass 
    
    return HttpResponse("Banco de dados populado com sucesso para o usuário 'fulano'!")

# Consultar os dados do sistema
def listagem_completa(request):
    usuarios = User.objects.all()
    modelos = ModeloDeCorrida.objects.all().order_by('nome') 
    historico = HistoricoCorrida.objects.all().order_by('-data_realizacao')
    
    context = {
        'usuarios': usuarios,
        'modelos': modelos,
        'historico': historico,
    }
    
    return render(request, 'listagem_completa.html', context)

# Criação de modelo
def criar_modelo_corrida(request):
    usuario_logado = get_user_logged_in() 
    
    if request.method == 'POST':
        form = ModeloDeCorridaForm(request.POST)
        if form.is_valid():
            modelo = form.save(commit=False)
            modelo.usuario = usuario_logado 
            modelo.save()
            return redirect('listagem_completa') 
    else:
        form = ModeloDeCorridaForm(initial={'usuario': usuario_logado.id})

    context = {'form': form, 'titulo': 'Cadastrar Novo Modelo de Corrida'}
    return render(request, 'modelo_form.html', context)

# Edição de modelo
def editar_modelo_corrida(request, pk):
    usuario_logado = get_user_logged_in()
    modelo = get_object_or_404(ModeloDeCorrida, pk=pk, usuario=usuario_logado) 
    
    if request.method == 'POST':
        form = ModeloDeCorridaForm(request.POST, instance=modelo)
        if form.is_valid():
            form.save()
            return redirect('listagem_completa')
    else:
        form = ModeloDeCorridaForm(instance=modelo)

    context = {'form': form, 'titulo': f'Editar Modelo: {modelo.nome}'}
    return render(request, 'modelo_form.html', context)

# Exclusão de modelo 
def excluir_modelo_corrida(request, pk):
    usuario_logado = get_user_logged_in()
    modelo = get_object_or_404(ModeloDeCorrida, pk=pk, usuario=usuario_logado)
    
    if request.method == 'POST':
        modelo.delete()
        return redirect('listagem_completa')
        
    context = {'item': modelo, 'tipo': 'Modelo de Corrida'}
    return render(request, 'confirmar_exclusao.html', context) 

# Registrar histórico 
def registrar_historico(request):
    usuario_logado = get_user_logged_in() 

    if request.method == 'POST':
        form = HistoricoCorridaForm(request.POST)
        if form.is_valid():
            historico = form.save(commit=False)
            historico.usuario = usuario_logado
            historico.save()
            return redirect('listagem_completa') 
    else:
        modelos_disponiveis = ModeloDeCorrida.objects.filter(usuario=usuario_logado)
        form = HistoricoCorridaForm(initial={'usuario': usuario_logado.id})
        form.fields['modelo_corrida'].queryset = modelos_disponiveis 

    context = {'form': form, 'titulo': 'Registrar Nova Corrida'}
    return render(request, 'historico_form.html', context)

# Edição de histórico
def editar_historico(request, pk):
    usuario_logado = get_user_logged_in()
    historico = get_object_or_404(HistoricoCorrida, pk=pk, usuario=usuario_logado)
    
    if request.method == 'POST':
        form = HistoricoCorridaForm(request.POST, instance=historico)
        if form.is_valid():
            form.save()
            return redirect('listagem_completa')
    else:
        modelos_disponiveis = ModeloDeCorrida.objects.filter(usuario=usuario_logado)
        form = HistoricoCorridaForm(instance=historico)
        form.fields['modelo_corrida'].queryset = modelos_disponiveis

    context = {'form': form, 'titulo': f'Editar Registro Histórico ID: {historico.id}'}
    return render(request, 'historico_form.html', context)

# Exclusão de histórico 
def excluir_historico(request, pk):
    usuario_logado = get_user_logged_in()
    historico = get_object_or_404(HistoricoCorrida, pk=pk, usuario=usuario_logado)
    
    if request.method == 'POST':
        historico.delete()
        return redirect('listagem_completa')
        
    context = {'item': historico, 'tipo': 'Registro de Histórico'}
    return render(request, 'confirmar_exclusao.html', context)