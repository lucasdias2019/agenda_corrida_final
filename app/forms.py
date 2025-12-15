from django import forms
from .models import ModeloDeCorrida, HistoricoCorrida

# RF01, RF02: Formulário para ModeloDeCorrida
class ModeloDeCorridaForm(forms.ModelForm):
    class Meta:
        model = ModeloDeCorrida
        # Inclui o campo 'usuario' para ser preenchido pela view, não pelo usuário
        fields = ['nome', 'distancia_planejada_km', 'duracao_estimada_min', 'objetivo', 'usuario'] 
        
        widgets = {
            'usuario': forms.HiddenInput(), # Esconde o campo 'usuario'
        }

# RF04, RF02: Formulário para HistoricoCorrida
class HistoricoCorridaForm(forms.ModelForm):
    # Sobrescreve a label para ser mais amigável e garante input numerico
    tempo_total_min = forms.IntegerField(
        label="Tempo Total da Corrida (em Minutos)", 
        widget=forms.NumberInput(attrs={'min': 0})
    )
    
    # Sobrescreve o campo de data para usar o seletor de data HTML
    data_realizacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = HistoricoCorrida # <- ESTA LINHA ESTAVA COM O ERRO DE DIGITAÇÃO
        # Inclui o campo 'usuario' para ser preenchido pela view, não pelo usuário
        fields = ['data_realizacao', 'modelo_corrida', 'tempo_total_min', 'observacoes', 'usuario']

        widgets = {
            'usuario': forms.HiddenInput(), # Esconde o campo 'usuario'
        }