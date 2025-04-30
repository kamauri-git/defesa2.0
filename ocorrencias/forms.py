from django import forms
from .models import Ocorrencia

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ['numero', 'sigrc', 'tipo', 'motivo', 'data', 'endereco', 'bairro', 'distrito', 'area_risco']
        widgets = {
            'data_ocorrencia': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if Ocorrencia.objects.filter(numero=numero).exists():
            raise forms.ValidationError("Já existe ocorrência registrada com esse número.")
        return numero

    def clean_sigrc(self):
        sigrc = self.cleaned_data.get('sigrc')
        if Ocorrencia.objects.filter(sigrc=sigrc).exists():
            raise forms.ValidationError("Já existe ocorrência registrada com esse SIGRC.")
        return sigrc