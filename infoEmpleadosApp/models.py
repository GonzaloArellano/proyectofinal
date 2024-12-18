from django.db import models

# Create your models here.

class Cargo(models.Model):
    Nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.Nombre

class Afp(models.Model):
    Nombre = models.CharField(max_length=50)
    Porcentaje_Descuento = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.Nombre

class Sistema_de_salud(models.Model):
    Nombre = models.CharField(max_length=50)
    Porcentaje_Descuento = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.Nombre

class Trabajador(models.Model):
    Nombre = models.CharField(max_length=30)
    Apellido = models.CharField(max_length=20)
    Rut = models.CharField(max_length=10, primary_key=True, unique=True)
    Sexo = models.CharField(max_length=20)
    Contraseña = models.CharField(max_length=50)
    Imagen = models.ImageField(upload_to="Trabajadores")
    Fecha_ingreso = models.DateField(auto_now_add=True)
    Correo = models.EmailField(max_length=254)
    Telefono = models.CharField(max_length=9)
    Direccion = models.CharField(max_length=100)
    Salario = models.IntegerField()
    Cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=False, null=False)
    AFP = models.ForeignKey(Afp, on_delete=models.CASCADE, blank=False, null=False)
    Sistema_de_salud = models.ForeignKey(Sistema_de_salud, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.Nombre

class Liquidacion(models.Model):
    Trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, blank=False, null=False)
    Fecha = models.DateField(auto_now_add=True)
    Sueldo_Liquido = models.IntegerField()
    Descuento_Afp = models.IntegerField()
    Descuento_Salud = models.IntegerField()

class EstadoPermiso(models.Model):
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre

class Permiso(models.Model):
    Trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, blank=False, null=False)
    EstadoPermiso = models.ForeignKey(EstadoPermiso, on_delete=models.CASCADE, blank=False, null=False)
    Fecha_de_inicio = models.DateField()
    Fecha_de_solicitud = models.DateField(auto_now_add=True)
    Cantidad_de_dias = models.IntegerField()
    Motivo = models.CharField(max_length=100)