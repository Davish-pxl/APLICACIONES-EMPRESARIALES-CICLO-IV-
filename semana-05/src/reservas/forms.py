from django import forms

DEPORTE_CHOICES = [
    ('Fútbol', 'Fútbol'),
    ('Básquetbol', 'Básquetbol'),
    ('Vóley', 'Vóley'),
    ('Pádel', 'Pádel'),
]

CANCHA_CHOICES = [
    ('Cancha Sintética 1 (Fútbol 7)', 'Cancha Sintética 1 (Fútbol 7)'),
    ('Cancha Sintética 2 (Fútbol 7)', 'Cancha Sintética 2 (Fútbol 7)'),
    ('Losa Polideportiva Central', 'Losa Polideportiva Central'),
    ('Coliseo Municipal', 'Coliseo Municipal'),
    ('Cancha de Pádel Club', 'Cancha de Pádel Club'),
]

class ReservaForm(forms.Form):
    cancha = forms.ChoiceField(
        choices=CANCHA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    deporte = forms.ChoiceField(
        choices=DEPORTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AAAA-MM-DD'})
    )
    hora = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '18:00'})
    )
    duracion_horas = forms.FloatField(
        initial=1.0,
        label="Duración (Horas)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'})
    )
    precio_hora = forms.FloatField(
        initial=20.0,
        label="Precio por Hora (S/)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )
    cliente = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class ConsultaForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )