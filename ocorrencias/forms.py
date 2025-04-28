from django import forms
from .models import Ocorrencia

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ['numero', 'sigrc', 'tipo', 'motivo', 'data', 'endereco', 'bairro', 'distrito']
        widgets = {
            'data_ocorrencia': forms.DateInput(attrs={'type': 'date'}),
        }
