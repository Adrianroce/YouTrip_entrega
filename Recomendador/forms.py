from django import forms

class Cuestionario():
    def __init__(self):
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.p4 = 0
        self.p5 = 0
        self.fecha_inicio = None
        self.fecha_fin = None

class CuestionarioForm(forms.Form):
    p1 = forms.IntegerField(required=True)
    p2 = forms.IntegerField(required=True)
    p3 = forms.IntegerField(required=True)
    p4 = forms.IntegerField(required=True)
    p5 = forms.IntegerField(required=True)
    fecha_inicio = forms.DateField(required=True)
    fecha_fin = forms.DateField(required=True)
