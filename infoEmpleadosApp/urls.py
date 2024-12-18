"""
URL configuration for ProyectoRRHH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from infoEmpleadosApp import views as v

urlpatterns = [
    path('', v.Home, name='Home'),
    path('ListaTrabajadores/', v.ListarTrabajadores, name="ListaTrabajadores"),
    path('RegistrarTrabajador/', v.RegistrarTrabajador, name="RegistrarTrabajador"),
    path('ActualizarTrabajador/<str:rut>', v.ActualizarTrabajador, name="ActualizarInfoTrabajador"),
    path('EliminarTrabajador/<str:rut>', v.EliminarTrabajador, name="EliminarTrabajador"),
    path('PerfilTrabajador/<str:rut>', v.MostrarTrabajador, name="PerfilTrabajador"),
    path('CrearPermiso/', v.CrearPermiso, name="CrearPermiso"),
    path('PermisoEnviado/', v.PermisoEnviado, name="PermisoEnviado"),
    path('ListarPermisos/', v.ListarPermisos, name="ListaPermisos"),
    path('ValidarPermiso/<int:id>', v.ValidarPermiso, name="ValidarPermiso"),
    path('Login/', v.Login, name='Login'),
    path('Logout/', v.Logout, name="Logout"),
    path('CalcularLiquidaciones/<str:rut>', v.CalcularLiquidaciones, name="CalcularLiquidaciones"),
    path('ListarLiquidaciones/<str:rut>', v.ListarLiquidaciones, name="ListarLiquidaciones"),
    path('LiquidacionOpcion/<str:rut>', v.LiquidacionOpcion, name="LiquidacionOpcion"),
    path('ListaPermisosPropios/', v.ListarPermisosPropios, name="ListarPermisosPropios")
]
