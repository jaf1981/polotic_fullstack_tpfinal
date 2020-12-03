from django.forms import ModelForm
from products.models import *
from django.contrib.auth.models import User

# Creamos las clases de formularios.
class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesional'].queryset = User.objects.filter(groups__name='Medicos')
        self.fields['diahora'].help_text = 'Formato de fecha DD/MM/YYYY HH:MM:SS.'
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control rounded-pill'
            })

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control rounded-pill'
            })

class HistoriaForm(ModelForm):
    class Meta:
        model = Historia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(HistoriaForm, self).__init__(*args, **kwargs)
        self.fields['profesional'].queryset = User.objects.filter(id=self.request.user.id)    

class HistoriaFormUpdate(ModelForm):
    class Meta:
        model = Historia
        fields = '__all__'
        exclude = ['profesional', 'paciente',]


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.fields['vendedor'].queryset = User.objects.filter(id=self.request.user.id)

class PedidoFormUpdate(ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        exclude = ['vendedor', 'paciente',]

class ItemsPedidoForm(ModelForm):
    class Meta:
        model = ItemsPedido
        fields = '__all__'        