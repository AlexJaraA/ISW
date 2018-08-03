import sys
sys.path.append('..')

from django import forms
from django.core import validators
from funcs import functions


class FormName(forms.Form):
    price = forms.FloatField(label="Precio", min_value=0)
    riskfree = forms.FloatField(label="Tasa libre de riesgo")
    symbol = forms.CharField(label="Símbolo", widget=forms.Select(choices=functions.get_symbols()))
    exercise_time = forms.IntegerField(label="Tiempo de ejercicio (Meses)", min_value=0)
    type_opt = forms.CharField(label='Tipo de Opcion',
                               widget=forms.Select(choices=[("compra", "Compra"), ("venta", "Venta")]))
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
