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

class HistoricoCorridaForm(forms.ModelForm):
    data_realizacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = HistoricoCorrida
        fields = ['data_realizacao', 'modelo_corrida', 'tempo_total_min', 'observacoes', 'usuario']

        widgets = {
            'usuario': forms.HiddenInput(), 
        }