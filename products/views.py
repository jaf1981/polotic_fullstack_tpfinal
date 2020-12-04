from django.http import (
    HttpResponse,
    JsonResponse,
    Http404,
    HttpResponseRedirect)

from django.db.models import Q    
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils import timezone
from datetime import timedelta, date, datetime
from django.utils.dateparse import parse_date
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *

#para chequear pertenencia a grupo/s y redirigir a distintos html a los usuarios.
def en_grupo(u, *grupo):
   if u.is_authenticated:
       if bool(u.groups.filter(name__in=grupo)):
           return True
   return False 

def group_required(*group_names):
   """Decorator para poder chequear pertenencia a grupos y habilitar o no acceso a vistas."""

   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)):
               return True
       return False 
   return user_passes_test(in_groups)

# Create your views here.
   

def home_view(request, *args, **kwargs):
    grupos = ['Secretarias', 'Medicos', 'Ventas', 'Taller', 'Gerencia']
    if not request.user.is_authenticated:
        return render(request, "home.html")
    elif en_grupo(request.user, grupos[0]) == True:
        context1 = {'grupo': grupos[0]}
        return render(request, "home_secre.html", context1)
    elif en_grupo(request.user, grupos[1]) == True:
        context2 = {'grupo': grupos[1]}
        return render(request, "home_medico.html", context2)
    elif en_grupo(request.user, grupos[2]) == True:
        context3 = {'grupo': grupos[2]}
        return render(request, "home_vtas.html", context3)
    elif en_grupo(request.user, grupos[3]) == True:
        context4 = {'grupo': grupos[3]}
        return render(request, "home_taller.html", context4)
    elif en_grupo(request.user, grupos[4]) == True:
        context5 = {'grupo': grupos[4]}
        return render(request, "home_gerencia.html", context5)
    else:
        return render(request, "home.html")    

grupo = 'Secretarias'
@group_required(grupo)
def home_secre(request, *args, **kwargs):
    context = {'grupo': grupo}
    return render(request, "home_secre.html", context)


class TurnoListView(LoginRequiredMixin, generic.ListView):
    model = Turno
    context_object_name = 'lista_turnos'
    template_name = 'lista_turnos.html'
    
    def get_queryset(self):
        queryset = Turno.objects.all() 
        if self.request.GET.get('fecha_desde'):
            fecha_desde = parse_date(self.request.GET.get('fecha_desde'))
            queryset = queryset.filter(diahora__gte=fecha_desde)   
        if self.request.GET.get('fecha_hasta'):
            fecha_hasta = parse_date(self.request.GET.get('fecha_hasta'))
            queryset = queryset.filter(diahora__lte=fecha_hasta)
        if self.request.GET.get('paciente'):
            paciente = self.request.GET.get('paciente')
            queryset = queryset.filter(Q(paciente__paciente_nombre__icontains=paciente) | Q(paciente__paciente_apellido__icontains=paciente))
        return queryset.order_by('diahora')


class TurnoCreate(LoginRequiredMixin, CreateView):
    model = Turno
    form_class = TurnoForm
    template_name= 'agregar_turnos.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_turnos')


class TurnoUpdate(LoginRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name= 'modificar_turnos.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_turnos')


class TurnoDelete(LoginRequiredMixin, DeleteView):
    model = Turno
    template_name= 'eliminar_turnos.html'
    success_url = reverse_lazy('lista_turnos')

class PacienteListView(LoginRequiredMixin, generic.ListView):
    model = Paciente
    context_object_name = 'lista_pacientes'
    template_name = 'lista_pacientes.html'
    
    def get_queryset(self):
        queryset = Paciente.objects.all() 
        if self.request.GET.get('paciente_nombre'):
            paciente_nombre = self.request.GET.get('paciente_nombre')
            queryset = queryset.filter(paciente_nombre=paciente_nombre)   
        if self.request.GET.get('paciente_apellido'):
            paciente_apellido = self.request.GET.get('paciente_apellido')
            queryset = queryset.filter(paciente_apellido=paciente_apellido)
        return queryset.order_by('paciente_apellido')    

class PacienteCreate(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name= 'agregar_pacientes.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_pacientes')

class PacienteUpdate(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name= 'modificar_pacientes.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_pacientes')

class PacienteDelete(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name= 'eliminar_pacientes.html'
    success_url = reverse_lazy('lista_pacientes')
        
# Vistas Medicos

class MedicoTurnoListView(LoginRequiredMixin, generic.ListView):
    model = Turno
    context_object_name = 'lista_turnos_m'
    template_name = 'lista_turnos_medicos.html'
    
    def get_queryset(self):
        queryset = Turno.objects.filter(Q(profesional=self.request.user)).order_by('diahora') 
        if self.request.GET.get('fecha_desde'):
            fecha_desde = self.request.GET.get('fecha_desde')
            print(fecha_desde)
            queryset = queryset.filter(Q(diahora__gte=fecha_desde))    
        if self.request.GET.get('fecha_hasta'):
            fecha_hasta = self.request.GET.get('fecha_hasta')
            queryset = queryset.filter(Q(diahora__lte=fecha_hasta))
        if self.request.GET.get('paciente'):
            paciente = self.request.GET.get('paciente')
            queryset = queryset.filter(Q(paciente__paciente_nombre__contains=paciente) | Q(paciente__paciente_apellido__contains=paciente))
        return queryset.order_by('diahora')

class MedicoHistoriaListView(LoginRequiredMixin, generic.ListView):
    model = Historia
    context_object_name = 'historias_m'
    template_name = 'lista_historias_m.html'
    
    def get_queryset(self):
        queryset = Historia.objects.filter(Q(profesional=self.request.user)).order_by('diahora') 
        if self.request.GET.get('fecha_desde'):
            fecha_desde = self.request.GET.get('fecha_desde')
            print(fecha_desde)
            queryset = queryset.filter(Q(diahora__gte=fecha_desde))    
        if self.request.GET.get('fecha_hasta'):
            fecha_hasta = self.request.GET.get('fecha_hasta')
            queryset = queryset.filter(Q(diahora__lte=fecha_hasta))
        if self.request.GET.get('paciente'):
            paciente = self.request.GET.get('paciente')
            queryset = queryset.filter(Q(paciente__paciente_nombre__contains=paciente) | Q(paciente__paciente_apellido__contains=paciente))
        return queryset.order_by('diahora')

class HistoriaCreate(LoginRequiredMixin, CreateView):
    model = Historia
    form_class = HistoriaForm
    template_name= 'agregar_historias.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_historias_m')

    def get_form_kwargs(self):
        kwargs = super(HistoriaCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class HistoriaUpdate(LoginRequiredMixin, UpdateView):
    model = Historia
    form_class = HistoriaFormUpdate
    template_name= 'modificar_historias.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_historias_m')


# Vistas Ventas

class PedidoListView(LoginRequiredMixin, generic.ListView):
    model = Pedido
    context_object_name = 'lista_pedidos'
    template_name = 'lista_pedidos.html'
    
    def get_queryset(self):
        queryset = Pedido.objects.filter(Q(vendedor=self.request.user)).order_by('fecha') 
        if self.request.GET.get('fecha_desde'):
            fecha_desde = self.request.GET.get('fecha_desde')
            queryset = queryset.filter(Q(fecha__gte=fecha_desde))    
        if self.request.GET.get('fecha_hasta'):
            fecha_hasta = self.request.GET.get('fecha_hasta')
            queryset = queryset.filter(Q(fecha__lte=fecha_hasta))
        if self.request.GET.get('paciente'):
            paciente = self.request.GET.get('paciente')
            queryset = queryset.filter(Q(paciente__paciente_nombre__icontains=paciente) | Q(paciente__paciente_apellido__icontains=paciente))
        return queryset.order_by('fecha')






class PedidoCreate(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name= 'agregar_pedidos.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_pedidos')

    def get_form_kwargs(self):
        kwargs = super(PedidoCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class PedidoUpdate(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoFormUpdate
    template_name= 'modificar_pedidos.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_pedidos')


class PedidoDelete(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name= 'eliminar_pedidos.html'
    success_url = reverse_lazy('lista_pedidos')


class ItemsPedidoListView(LoginRequiredMixin, generic.ListView):
    model = ItemsPedido
    context_object_name = 'lista_items_pedidos'
    template_name = 'lista_items_pedidos.html'
    
    def get_queryset(self, *args):
        queryset = ItemsPedido.objects.filter(Q(pedido__vendedor=self.request.user)) 
        if self.request.GET.get('producto'):
            producto = self.request.GET.get('producto')
            queryset = queryset.filter(Q(product__prod_title__icontains=producto) | Q(product__prod_category__icontains=producto))
        if self.request.GET.get('num_pedido'):
            pedido = self.request.GET.get('num_pedido')
            queryset = queryset.filter(Q(pedido__id=pedido))
        
        return queryset.order_by('subtotal_pedido')

        

class ItemsPedidoCreate(LoginRequiredMixin, CreateView):
    model = ItemsPedido
    form_class = ItemsPedidoForm
    template_name= 'agregar_items_pedidos.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_items_pedidos')


class ItemsPedidoUpdate(LoginRequiredMixin, UpdateView):
    model = ItemsPedido
    form_class = ItemsPedidoForm
    template_name= 'modificar_items_pedidos.html'
    context_object_name = 'lista'
    success_url = reverse_lazy('lista_items_pedidos')


class ItemsPedidoDelete(LoginRequiredMixin, DeleteView):
    model = ItemsPedido
    template_name= 'eliminar_items_pedidos.html'
    success_url = reverse_lazy('lista_pedidos')


# Vista Taller

class PedidoTallerListView(LoginRequiredMixin, generic.ListView):
    model = Pedido
    context_object_name = 'lista_pedidos'
    template_name = 'lista_pedidos_taller.html'
    
    def get_queryset(self):
        queryset = Pedido.objects.filter(Q(estado='Ta')).order_by('fecha') 
        if self.request.GET.get('fecha_desde'):
            fecha_desde = self.request.GET.get('fecha_desde')
            queryset = queryset.filter(Q(fecha__gte=fecha_desde))    
        if self.request.GET.get('fecha_hasta'):
            fecha_hasta = self.request.GET.get('fecha_hasta')
            queryset = queryset.filter(Q(fecha__lte=fecha_hasta))
        if self.request.GET.get('paciente'):
            paciente = self.request.GET.get('paciente')
            queryset = queryset.filter(Q(paciente__paciente_nombre__icontains=paciente) | Q(paciente__paciente_apellido__icontains=paciente))
        return queryset.order_by('fecha')

class ItemsPedidoTallerListView(LoginRequiredMixin, generic.ListView):
    model = ItemsPedido
    context_object_name = 'lista_items_pedidos'
    template_name = 'lista_items_pedidos_taller.html'
    
    def get_queryset(self):
        queryset = ItemsPedido.objects.filter(Q(pedido__estado='Ta')) 
        if self.request.GET.get('producto'):
            producto = self.request.GET.get('producto')
            queryset = queryset.filter(Q(product__prod_title__icontains=producto) | Q(product__prod_category__icontains=producto))
        if self.request.GET.get('num_pedido'):
            pedido = self.request.GET.get('num_pedido')
            queryset = queryset.filter(Q(pedido__id=pedido))
        return queryset.order_by('pedido__fecha')

#Vistas Gerencia

class TurnoGciaListView(LoginRequiredMixin, generic.ListView):
    model = Turno
    context_object_name = 'lista_turnos'
    template_name = 'lista_turnos_gcia.html'
    
    def get_queryset(self):
        queryset = Turno.objects.all() 
        if self.request.GET.get('asistencia'):
            asistencia = self.request.GET.get('asistencia')
            queryset = queryset.filter(asistencia=asistencia)
        if self.request.GET.get('fecha_desde'):
            fecha_desde = parse_date(self.request.GET.get('fecha_desde'))
            queryset = queryset.filter(diahora__gte=fecha_desde)   
        if self.request.GET.get('fecha_hasta'):
            fecha_hasta = parse_date(self.request.GET.get('fecha_hasta'))
            queryset = queryset.filter(diahora__lte=fecha_hasta)
        if self.request.GET.get('paciente'):
            paciente = self.request.GET.get('paciente')
            queryset = queryset.filter(Q(paciente__paciente_nombre__icontains=paciente) | Q(paciente__paciente_apellido__icontains=paciente))
        return queryset.order_by('diahora')

class PedidoGciaListView(LoginRequiredMixin, generic.ListView):
    model = Pedido
    context_object_name = 'lista_pedidos'
    template_name = 'lista_pedidos_gcia.html'
    
    def get_queryset(self):
        queryset = Pedido.objects.all().order_by('fecha') 
        if self.request.GET.get('fecha_desde'):
            fecha_desde = self.request.GET.get('fecha_desde')
            queryset = queryset.filter(Q(fecha__gte=fecha_desde))    
        if self.request.GET.get('fecha_hasta'):
            fecha_hasta = self.request.GET.get('fecha_hasta')
            queryset = queryset.filter(Q(fecha__lte=fecha_hasta))
        if self.request.GET.get('paciente'):
            paciente = self.request.GET.get('paciente')
            queryset = queryset.filter(Q(paciente__paciente_nombre__icontains=paciente) | Q(paciente__paciente_apellido__icontains=paciente))
        if self.request.GET.get('vendedor'):
            vendedor = self.request.GET.get('vendedor')
            queryset = queryset.filter(Q(vendedor__first_name__icontains=vendedor) | Q(vendedor__last_name__icontains=vendedor))
        if self.request.GET.get('estado'):
            estado = self.request.GET.get('estado')
            queryset = Pedido.objects.filter(Q(estado=estado)).order_by('fecha')
        return queryset.order_by('fecha')
