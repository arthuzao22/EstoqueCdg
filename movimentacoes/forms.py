from django import forms
from .models import Movimentacoes

class MovimentacoesForm(forms.ModelForm):
    class Meta:
        model = Movimentacoes
        fields = ['tipo_movimentacao', 'qtde', 'data_chegada_saida', 'id_empresa', 'id_produto']
        widgets = {
            'data_chegada_saida': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_qtde(self):
        """Validação personalizada para quantidade"""
        qtde = self.cleaned_data.get('qtde')
        if qtde <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return qtde
