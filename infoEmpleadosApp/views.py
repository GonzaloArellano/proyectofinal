from django.shortcuts import render, redirect
from .models import Trabajador, Afp, Sistema_de_salud, Cargo, Permiso, EstadoPermiso, Liquidacion
from .forms import RegistrarActualizarTrabajadorForm, CrearPermisoForm, LoginForm
from django import forms
# Create your views here.

#Value 1 siempre es aprobobado
#Value 2 siempre es rechazado
#Value 3 siempre es pendiente

#Jefe RRHH = 1, Empleado RRHH = 2, Empleado = 3

def ListarTrabajadores(request):
    Cookie_rut = request.COOKIES.get('Rut')    
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    
    FiltroBusqueda = request.GET.get('OpcionBusqueda')
    ValorFiltro = request.GET.get('Valor')
    
    if FiltroBusqueda == "Nombre":
        trabajadores = Trabajador.objects.filter(Nombre__icontains=ValorFiltro)
    elif FiltroBusqueda == "Rut":
        trabajadores = Trabajador.objects.filter(Rut__icontains=ValorFiltro)
    elif FiltroBusqueda == "Cargo":
        trabajadores = Trabajador.objects.filter(Cargo__Nombre__icontains=ValorFiltro)
    else:
        trabajadores = Trabajador.objects.all()
        ValorFiltro = ""
        FiltroBusqueda = ""
    
    context = {
        "trabajadores": trabajadores,
        "Filtro": FiltroBusqueda,
        "ValorFiltro": ValorFiltro
    }
    return render(request, "ListadoTrabajadores.html", context)

def MostrarTrabajador(request, rut):
    Cookie_rut = request.COOKIES.get('Rut')
    trabajador_buscando = Trabajador.objects.get(Rut = Cookie_rut)
    if trabajador_buscando.Cargo.id == 3 and rut != Cookie_rut:
        return render(request, 'Algo.html')
    trabajador = Trabajador.objects.get(Rut = rut)
    context = {"Trabajador" : trabajador}
    return render(request, 'perfil.html', context)

def RegistrarTrabajador(request):
    Cookie_rut = request.COOKIES.get('Rut')    
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    form = RegistrarActualizarTrabajadorForm()
    if request.method == "POST":
        form.data = request.POST
        if form.is_valid: 
            form.files = request.FILES
            trabajador = Trabajador()
            trabajador.Nombre = form.data.get('Nombre')
            trabajador.Apellido = form.data.get('Apellido')
            trabajador.Sexo = form.data.get('Sexo')
            trabajador.Rut = form.data.get('Rut')
            trabajador.Contraseña = form.data.get('Contraseña')
            trabajador.Correo = form.data.get('Correo')
            trabajador.Telefono = form.data.get('Telefono')
            trabajador.Cargo = Cargo.objects.get(id=form.data.get('Cargo'))
            trabajador.Fecha_ingreso = form.data.get('Fecha_de_Ingreso')
            trabajador.Direccion = form.data.get('Direccion')
            trabajador.Imagen = form.files.get('Imagen')
            trabajador.Salario = form.data.get('Salario')
            trabajador.AFP = Afp.objects.get(id=form.data.get('Afp'))
            trabajador.Sistema_de_salud = Sistema_de_salud.objects.get(id=form.data.get('Sistema_de_salud'))
            trabajador.save()
            return redirect("ListaTrabajadores")
    context = {"form": form}
    return render(request, 'RegistrarTrabajadorForm.html', context)

def ActualizarTrabajador(request, rut):
    Cookie_rut = request.COOKIES.get('Rut')    
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    trabajador = Trabajador.objects.get(Rut = rut)
    form = RegistrarActualizarTrabajadorForm()
    form.initial['Nombre'] = trabajador.Nombre
    form.initial['Apellido'] = trabajador.Apellido
    form.initial['Rut'] = trabajador.Rut
    form.initial['Contraseña'] = trabajador.Contraseña
    form.initial['Sexo'] = trabajador.Sexo
    form.initial['Correo'] = trabajador.Correo
    form.initial['Cargo'] = trabajador.Cargo
    form.initial['Telefono'] = trabajador.Telefono
    form.initial['Fecha_de_Ingreso'] = trabajador.Fecha_ingreso
    form.initial['Direccion'] = trabajador.Direccion
    form.files['Imagen'] = trabajador.Imagen ##Revisar
    form.initial['Salario'] = trabajador.Salario
    form.initial['Afp'] = trabajador.AFP.id
    form.initial['Sistema_de_salud'] = trabajador.Sistema_de_salud.id
    context = { "form" : form}
    if request.method == "POST":
        form.data = request.POST
        if form.is_valid:
            form.files = request.FILES
            trabajador = Trabajador()
            trabajador.Nombre = form.data.get('Nombre')
            trabajador.Apellido = form.data.get('Apellido')
            trabajador.Sexo = form.data.get('Sexo')
            trabajador.Rut = form.data.get('Rut')
            trabajador.Correo = form.data.get('Correo')
            trabajador.Contraseña = form.data.get('Contraseña')
            trabajador.Telefono = form.data.get('Telefono')
            trabajador.Cargo = Cargo.objects.get(id=form.data.get('Cargo'))
            trabajador.Fecha_ingreso = form.data.get('Fecha_de_Ingreso')
            trabajador.Direccion = form.data.get('Direccion')
            trabajador.Imagen = form.files.get('Imagen')
            trabajador.Salario = form.data.get('Salario')
            trabajador.AFP = Afp.objects.get(id=form.data.get('Afp'))
            trabajador.Sistema_de_salud = Sistema_de_salud.objects.get(id=form.data.get('Sistema_de_salud'))
            trabajador.save()
            return redirect("ListaTrabajadores")
    return render(request, "ActualizarTrabajadorForm.html", context)

def EliminarTrabajador(request, rut):
    Cookie_rut = request.COOKIES.get('Rut')
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    trabajador = Trabajador.objects.get(Rut=rut)
    if request.method == "POST":
        if "confirm" in request.POST:
            trabajador.delete()
        return redirect("ListaTrabajadores")
    context = {"trabajador": trabajador}
    return render(request, 'Eliminar.html', context)

def CrearPermiso(request):
    form = CrearPermisoForm()
    if request.method == "POST":
        form = CrearPermisoForm(request.POST)
        if form.is_valid():
            Cookie_rut = request.COOKIES.get('Rut')
            trabajador = Trabajador.objects.get(Rut=Cookie_rut)
            permiso = Permiso(
                EstadoPermiso=EstadoPermiso.objects.get(id=3),
                Cantidad_de_dias=form.cleaned_data['Cantidad_de_dias'],
                Fecha_de_inicio=form.cleaned_data['Fecha_de_inicio'],
                Trabajador=trabajador,
                Motivo=form.cleaned_data['Motivo']
            )
            permiso.save()
            return redirect('PermisoEnviado')
    context = {"form": form}
    return render(request, 'PermisoForm.html', context)

def PermisoEnviado(request):
    return render(request, 'PermisoEnviado.html')

def ListarPermisos(request):
    Cookie_rut = request.COOKIES.get('Rut')
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    FiltroBusqueda = request.GET.get('OpcionBusqueda')
    ValorFiltro = request.GET.get('Valor')
    FiltroEstado = request.GET.get('OpcionEstado')
    permisos = Permiso.objects.all()
    if FiltroBusqueda == "Nombre":
        permisos = permisos.filter(Trabajador__Nombre__icontains=ValorFiltro)
    elif FiltroBusqueda == "Rut":
        permisos = permisos.filter(Trabajador__Rut__icontains=ValorFiltro)
    if FiltroEstado:
        permisos = permisos.filter(EstadoPermiso__id=FiltroEstado)
    context = {
        "Permisos": permisos,
        "Filtro": FiltroBusqueda,
        "ValorFiltro": ValorFiltro,
        "Opcion": FiltroEstado
    }
    return render(request, "ListaPermisos.html", context)

def ValidarPermiso(request, id):
    Cookie_rut = request.COOKIES.get('Rut')    
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    permiso = Permiso.objects.get(id=id)
    if request.method == 'POST':
        if permiso.EstadoPermiso.Nombre == 'Pendiente':
            AceptadoORechazado = request.POST.get('opcion')
            permiso.EstadoPermiso = EstadoPermiso.objects.get(id=AceptadoORechazado)
            permiso.save()
        return redirect('ListaPermisos')

def Login(request):
    if request.COOKIES.get('Rut') is not None:
        return redirect('PerfilTrabajador', request.COOKIES.get('Rut'))
    
    form = LoginForm()
    context = {"form": form}
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                CredencialesTrabajador = Trabajador.objects.get(
                    Rut=form.cleaned_data['Rut'], 
                    Contraseña=form.cleaned_data['Contraseña']
                )
                response = redirect('PerfilTrabajador', CredencialesTrabajador.Rut)
                response.set_cookie('Rut', CredencialesTrabajador.Rut, secure=True)
                return response
            except Trabajador.DoesNotExist:
                return render(request, 'CredencialesInvalidas.html')
    
    return render(request, 'LoginForm.html', context)

def Logout(request):
    response = redirect('Login')
    if not request.COOKIES.get('Rut'):
        return response
    response.delete_cookie('Rut')
    return response

def EsAdministrador(rut):
    Credenciales = Trabajador.objects.get(Rut = rut)
    return not Credenciales.Cargo.id == 3

class SeleccionarTrabajadorForm(forms.Form):
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), label="Seleccionar Trabajador")


def CalcularLiquidaciones(request, rut):
    Cookie_rut = request.COOKIES.get('Rut')    
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    trabajador = Trabajador.objects.get(Rut=rut)
    if request.method == "POST":
        afp = Afp.objects.get(id=trabajador.AFP.id)
        salud = Sistema_de_salud.objects.get(id=trabajador.Sistema_de_salud.id)
        liquidacion = Liquidacion(
            Trabajador=trabajador,
            Descuento_Afp=(trabajador.Salario * afp.Porcentaje_Descuento) / 100,
            Descuento_Salud=(trabajador.Salario * salud.Porcentaje_Descuento) / 100,
            Sueldo_Liquido=int(trabajador.Salario - (trabajador.Salario * afp.Porcentaje_Descuento) / 100 - (trabajador.Salario * salud.Porcentaje_Descuento) / 100)
        )
        liquidacion.save()
        return redirect('ListaTrabajadores')
    else:
        form = SeleccionarTrabajadorForm(initial={'trabajador': trabajador.Rut})
    
    context = {"form": form, "trabajador": trabajador}
    return render(request, 'CalcularLiquidaciones.html', context)


def ListarLiquidaciones(request, rut):
    Cookie_rut = request.COOKIES.get('Rut')    
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    trabajador = Trabajador.objects.get(Rut=rut)
    liquidaciones = Liquidacion.objects.filter(Trabajador=trabajador)
    context = {"liquidaciones": liquidaciones, "trabajador": trabajador}
    return render(request, "ListarLiquidaciones.html", context)

def ListarPermisosPropios(request):
    Cookie_rut = request.COOKIES.get('Rut')
    permisos = Permiso.objects.filter(Trabajador__Rut=Cookie_rut)
    
    FiltroEstado = request.GET.get('OpcionEstado')
    if FiltroEstado:
        permisos = permisos.filter(EstadoPermiso__id=FiltroEstado)
    
    context = {
        "permisos": permisos,
        "Opcion": FiltroEstado
    }
    return render(request, "ListadoPermisosPropios.html", context)

def Home(request):
    return render(request, 'Home.html')

def LiquidacionOpcion(request, rut):
    Cookie_rut = request.COOKIES.get('Rut')    
    if not EsAdministrador(Cookie_rut):
        return render(request, 'Algo.html')
    trabajador = Trabajador.objects.get(Rut=rut)
    context = {"trabajador": trabajador}
    return render(request, 'LiquidacionOpcion.html', context)

#def custom_404(request, exception):
    return render(request, '404.html', status=404)