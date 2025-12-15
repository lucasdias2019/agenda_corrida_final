from django import forms
from .models import ModeloDeCorrida, HistoricoCorrida

# formulário para modelo de corrida
class HistoricoCorridaForm(forms.ModelForm):
    tempo_total_min = forms.IntegerField(
        label="Tempo Total da Corrida (em Minutos)", 
        widget=forms.NumberInput(attrs={'min': 0})
    )

class HistoricoCorridaForm(forms.ModelForm):
    data_realizacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = HistoricoCorrida
        fields = ['data_realizacao', 'model git o_corrida', 'tempo_total_min', 'observacoes', 'usuario']
        
        widgets = {
            'usuario': forms.HiddenInput(), 
        }