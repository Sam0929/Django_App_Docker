from django import forms
from .models import Transaction
from decimal import Decimal

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'value', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Ex: Salário, Aluguel, Compra no mercado'}
        )
        self.fields['value'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'OBS: Use valores positivos para entradas e negativos para saídas (ex: -50.25)'}
        )
        self.fields['description'].widget.attrs.update(
            {'class': 'form-textarea', 'rows': 4, 'placeholder': 'Detalhes adicionais (opcional)'}
        )
   