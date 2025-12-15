from django import forms
from .models import ModeloDeCorrida, HistoricoCorrida

# formulário para modelo de corrida
class ModeloDeCorridaForm(forms.ModelForm):
    class Meta:
        model = ModeloDeCorrida
        fields = ['nome', 'distancia_planejada_km', 'duracao_estimada_min', 'objetivo', 'usuario'] 
        
        widgets = {
            'usuario': forms.HiddenInput(), 
        }

class HistoricoCorridaForm(forms.ModelForm):
    data_realizacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = HistoricoCorrida
        fields = ['data_realizacao', 'modelo_corrida', 'tempo_total_min', 'observacoes', 'usuario']
        
        widgets = {
            'usuario': forms.HiddenInput(), 
        }