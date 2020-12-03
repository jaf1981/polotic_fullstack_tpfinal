"""dj_bootcamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from products.views import (
home_view,
home_secre, 
MedicoTurnoListView, 
MedicoHistoriaListView,
HistoriaCreate,
HistoriaUpdate, 
TurnoListView, 
TurnoCreate, 
TurnoUpdate, 
TurnoDelete, 
TurnoListView,
TurnoGciaListView, 
PacienteListView, 
PacienteCreate, 
PacienteUpdate, 
PacienteDelete,
PedidoCreate,
PedidoUpdate,
PedidoDelete,
ItemsPedidoCreate,
ItemsPedidoUpdate,
ItemsPedidoDelete,
ItemsPedidoListView,
ItemsPedidoTallerListView,
PedidoListView,
PedidoGciaListView,
PedidoTallerListView)

urlpatterns = [
    path('', home_view, name="home"),
    path('turno/add/', TurnoCreate.as_view(), name="turno-add"),
    path('turno/<int:pk>/', TurnoUpdate.as_view(), name="turno-update"),
    path('turno/<int:pk>/delete', TurnoDelete.as_view(), name="turno-delete"),
    path('paciente/add/', PacienteCreate.as_view(), name="paciente-add"),
    path('paciente/<int:pk>/', PacienteUpdate.as_view(), name="paciente-update"),
    path('paciente/<int:pk>/delete', PacienteDelete.as_view(), name="paciente-delete"),    
    path('ver_pacientes', PacienteListView.as_view(), name="lista_pacientes"),
    path('secre/', home_secre, name="home_secre"),
    path('ver_turnos', TurnoListView.as_view(), name="lista_turnos"),
    path('ver_turnos_gcia', TurnoGciaListView.as_view(), name="lista_turnos_gcia"),    
    path('medico_turnos', MedicoTurnoListView.as_view(), name="lista_turnos_medicos"),
    path('ver_historias_m', MedicoHistoriaListView.as_view(), name="lista_historias_m"),
    path('historia/add/', HistoriaCreate.as_view(), name="historia-add"),
    path('historia/<int:pk>/', HistoriaUpdate.as_view(), name="historia-update"),
    path('pedido/add/', PedidoCreate.as_view(), name="pedido-add"),
    path('pedido/<int:pk>/', PedidoUpdate.as_view(), name="pedido-update"), 
    path('pedido/<int:pk>/delete', PedidoDelete.as_view(), name="pedido-delete"),
    path('items_pedido/add/', ItemsPedidoCreate.as_view(), name="items-pedido-add"),
    path('items_pedido/<int:pk>/', ItemsPedidoUpdate.as_view(), name="items-pedido-update"), 
    path('pedido/<int:pk>/delete', ItemsPedidoDelete.as_view(), name="items-pedido-delete"),    
    path('ver_pedidos', PedidoListView.as_view(), name="lista_pedidos"),
    path('ver_pedidos_gcia', PedidoGciaListView.as_view(), name="lista_pedidos_gcia"),
    path('ver_pedidos_taller', PedidoTallerListView.as_view(), name="lista_pedidos_taller"),    
    path('ver_items_pedidos', ItemsPedidoListView.as_view(), name="lista_items_pedidos"),            
    path('ver_items_pedidos_taller', ItemsPedidoTallerListView.as_view(), name="lista_items_pedidos_taller"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', home_view),
    path('admin/', admin.site.urls)
]
