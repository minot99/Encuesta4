from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager    

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True, default='default_username')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def has_module_perms(self, app_label):
        """
        Determine whether the user has permission to view the app_label module.

        Simplest possible answer: Yes, always.
        """
        return True

    def has_perm(self, perm, obj=None):
        """
        Determine whether the user has the given permission.

        Simplest possible answer: Yes, always.
        """
        return True

class Docente(models.Model):
    nombre = models.CharField(max_length=100, default='')
    apellido = models.CharField(max_length=100, default='')
    cedula = models.CharField(max_length=15, default='')
    telefono_oficina = models.CharField(max_length=20, default='')
    telefono_personal = models.CharField(max_length=20, default='')
    correo_institucional = models.EmailField(default='')

    habla_ingles_en_clase = models.CharField(max_length=20, default='')
    porcentaje_tiempo_ingles = models.PositiveIntegerField(default=0)

    incentiva_hablar_ingles = models.CharField(max_length=20, default='')
    tiempo_dialogo_ingles = models.PositiveIntegerField(default=0)

    tipo_senalizaciones_ingles = models.CharField(max_length=100, default='')
    senalizaciones_aula_ingles = models.CharField(max_length=20, default='')
    cantidad_senalizaciones_aula = models.PositiveIntegerField(default=0)

    interactua_directivos_ingles = models.PositiveIntegerField(default=0)
    interactua_docentes_ingles = models.PositiveIntegerField(default=0)
    interactua_padres_ingles = models.PositiveIntegerField(default=0)
    interactua_estudiantes_ingles = models.CharField(max_length=20, default='')
    porcentaje_interaccion_estudiantes = models.PositiveIntegerField(default=0)

    actividades_ingles_fuera_aula = models.CharField(max_length=100, default='')
    frecuencia_actividades_ingles = models.CharField(max_length=20, default='')

    experiencia_anos = models.PositiveIntegerField(default=0)
    sector_experiencia = models.CharField(max_length=50, default='')
    niveles_impartidos = models.CharField(max_length=100, default='')
    nivel_actual = models.CharField(max_length=50, default='')

    titulo_ensenanza_ingles = models.CharField(max_length=20, default='')
    titulos_formales_ingles = models.TextField(default='')
    cursos_nacionales_ingles = models.TextField(default='')
    cursos_internacionales_ingles = models.TextField(default='')

    certificacion_ingles = models.CharField(max_length=20, default='')
    nombre_titulacion = models.CharField(max_length=100, default='')
    ano_certificacion = models.PositiveIntegerField(default=0)
    vencimiento_certificacion = models.CharField(max_length=10, default='')

    nivel_ingles_docente = models.CharField(max_length=50, default='')
    dispuesto_renovar_certificacion = models.CharField(max_length=20, default='')

    frecuencia_uso_recursos_ingles = models.CharField(max_length=20, default='')
    acceso_recursos_ingles = models.CharField(max_length=20, default='')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Coordinador(models.Model):
    # Formulario 1
    docentes_por_asignatura = models.PositiveIntegerField()
    participa_activamente_ppb = models.BooleanField()
    estudiantes_por_nivel_ppb = models.PositiveIntegerField()
    docentes_capacitados_ppb = models.PositiveIntegerField()
    docentes_aprobados_ppb = models.PositiveIntegerField()
    docentes_capacitacion_exterior = models.PositiveIntegerField()

    # Formulario 2
    codigos_plan_estudio = models.CharField(max_length=255)
    planes_estudio = models.CharField(max_length=255)
    asignaturas_ingles_en_plan = models.BooleanField()
    asignaturas_ingles_dictadas = models.BooleanField()
    planes_clase_contraste = models.TextField()
    horas_ingles = models.PositiveIntegerField()
    horas_teoricas = models.PositiveIntegerField()
    horas_practicas = models.PositiveIntegerField()

    # Formulario 3
    actividades_propio_centro = models.BooleanField()
    actividades_meduca_centro = models.BooleanField()
    actividades_externas_centro = models.BooleanField()
    detalle_actividades_anual = models.TextField()
    cantidad_estudiantes_actividades_externas = models.JSONField(default=dict)  # This can store grade-wise participation.

    # Formulario 4
    after_school_existencia = models.BooleanField()
    after_school_descripcion = models.TextField()
    after_school_participacion = models.JSONField(default=dict)  # Grade-wise participation.

    # Formulario 5
    tipo_senalizaciones_ingles = models.JSONField(default=list)
    senalizaciones_aula_ingles = models.BooleanField()
    cantidad_senalizaciones_aula = models.PositiveIntegerField()

    # Formulario 6
    interactua_directivos_ingles = models.PositiveIntegerField()
    interactua_docentes_ingles = models.PositiveIntegerField()
    interactua_padres_ingles = models.PositiveIntegerField()
    interactua_estudiantes_ingles = models.BooleanField()
    porcentaje_interaccion_estudiantes = models.PositiveIntegerField()
    actividades_ingles_fuera_aula = models.JSONField(default=list)
    frecuencia_actividades_ingles = models.CharField(max_length=20)

    def __str__(self):
        return f"Coordinador ID: {self.id}"

class Director(models.Model):
    nombre = models.CharField(max_length=100, default='N/A')
    apellido = models.CharField(max_length=100, default='N/A')
    cedula = models.CharField(max_length=20, default='N/A')
    telefono_oficina = models.CharField(max_length=20, default='N/A')
    telefono_personal = models.CharField(max_length=20, default='N/A')
    correo_institucional = models.EmailField(default='N/A@example.com')
    correo_personal1 = models.EmailField(default='N/A@example.com')
    correo_personal2 = models.EmailField(default='N/A@example.com')
    codigo_siace = models.CharField(max_length=20, default='N/A')
    nombre_centro_educativo = models.CharField(max_length=255, default='N/A')
    region_educativa = models.CharField(max_length=100, default='N/A')
    provincia = models.CharField(max_length=100, default='N/A')
    direccion = models.CharField(max_length=255, default='N/A')
    nivel_escolar = models.CharField(max_length=50, default='N/A')
    matricula_total = models.IntegerField(default=0)
    grado1 = models.CharField(max_length=100, default='N/A')
    femenino1 = models.IntegerField(default=0)
    masculino1 = models.IntegerField(default=0)
    grado2 = models.CharField(max_length=100, default='N/A')
    femenino2 = models.IntegerField(default=0)
    masculino2 = models.IntegerField(default=0)
    grado3 = models.CharField(max_length=100, default='N/A')
    femenino3 = models.IntegerField(default=0)
    masculino3 = models.IntegerField(default=0)
    grado4 = models.CharField(max_length=100, default='N/A')
    femenino4 = models.IntegerField(default=0)
    masculino4 = models.IntegerField(default=0)
    total_docentes = models.IntegerField(default=0)
    docentes1 = models.IntegerField(default=0)
    docentes2 = models.IntegerField(default=0)
    docentes3 = models.IntegerField(default=0)
    docentes4 = models.IntegerField(default=0)
    estudiantes_salon = models.IntegerField(default=0)
    docentes_asignatura = models.IntegerField(default=0)
    participa_ppb = models.CharField(max_length=10, default='N/A')
    estudiantes_nivel_ppb = models.IntegerField(default=0)
    docentes_capacitados_ppb = models.IntegerField(default=0)
    docentes_aprobados_ppb = models.IntegerField(default=0)
    docentes_capacitacion_exterior = models.IntegerField(default=0)
    codigos_plan_estudio = models.CharField(max_length=255, default='N/A')
    planes_estudio = models.CharField(max_length=255, default='N/A')
    asignaturas_ingles_plan_estudios = models.CharField(max_length=10, default='N/A')
    asignaturas_ingles_dictadas = models.CharField(max_length=10, default='N/A')
    planes_clase = models.CharField(max_length=255, default='N/A')
    horas_ingles = models.IntegerField(default=0)
    horas_teoricas = models.IntegerField(default=0)
    horas_practicas = models.IntegerField(default=0)
    actividades_propio_centro = models.CharField(max_length=10, default='N/A')
    actividades_meduca_centro = models.CharField(max_length=10, default='N/A')
    actividades_externas_centro = models.CharField(max_length=10, default='N/A')
    detalle_actividades_anual = models.CharField(max_length=255, default='N/A')
    cantidad_estudiantes_actividades_externas_1 = models.IntegerField(default=0)
    cantidad_estudiantes_actividades_externas_2 = models.IntegerField(default=0)
    cantidad_estudiantes_actividades_externas_3 = models.IntegerField(default=0)
    cantidad_estudiantes_actividades_externas_4 = models.IntegerField(default=0)
    after_school_existencia = models.CharField(max_length=10, default='N/A')
    after_school_descripcion = models.CharField(max_length=255, default='N/A')
    after_school_participacion_1 = models.CharField(max_length=255, default='N/A')
    after_school_participacion_2 = models.CharField(max_length=255, default='N/A')
    after_school_participacion_3 = models.CharField(max_length=255, default='N/A')
    after_school_participacion_4 = models.CharField(max_length=255, default='N/A')
    after_school_recursos = models.CharField(max_length=255, default='N/A')

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.nombre_centro_educativo}"

class CoordinadorTecnologia(models.Model):
    # Multimedia resources
    tiene_multimedia = models.BooleanField(default=False)
    materiales_multimedia = models.JSONField(default=list)
    cantidad_cd = models.IntegerField(default=0)
    cantidad_dvd = models.IntegerField(default=0)
    cantidad_mp4 = models.IntegerField(default=0)
    cantidad_streaming = models.IntegerField(default=0)
    cantidad_otros_multimedia = models.IntegerField(default=0)

    # English learning software details
    software_existencia = models.BooleanField(default=False)
    software_cantidad = models.IntegerField(default=0)
    software_listado = models.TextField(blank=True, null=True)
    software_licencia = models.BooleanField(default=False)
    software_internet_requerido = models.BooleanField(default=False)
    software_usuarios = models.IntegerField(default=0)

    # IT infrastructure
    existencia_laboratorios = models.BooleanField(default=False)
    cantidad_laboratorios = models.IntegerField(default=0)
    computadoras_por_laboratorio = models.IntegerField(default=0)
    marca_equipos = models.CharField(max_length=255, blank=True, null=True)
    ano_fabricacion = models.IntegerField(blank=True, null=True)
    computadoras_bocinas = models.BooleanField(default=False)
    computadoras_auriculares = models.BooleanField(default=False)
    computadoras_microfonos = models.BooleanField(default=False)
    computadoras_internet = models.BooleanField(default=False)

    # Internet and Wi-Fi infrastructure
    internet_existencia = models.BooleanField(default=False)
    tipo_enlace_internet = models.CharField(max_length=100, blank=True, null=True)
    ancho_banda = models.IntegerField(default=0)
    wifi_solucion_existencia = models.BooleanField(default=False)
    wifi_alcance = models.JSONField(default=list)
    wifi_cobertura_porcentaje = models.IntegerField(default=0)
    acceso_wifi_administrativos = models.BooleanField(default=False)
    acceso_wifi_docentes = models.BooleanField(default=False)
    acceso_wifi_estudiantes = models.BooleanField(default=False)
    percepcion_velocidad_internet = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"CoordinadorTecnologia ID: {self.id}"

class OtrosDocentes(models.Model):
    habla_ingles_otras_asignaturas = models.BooleanField(default=False)
    porcentaje_tiempo_ingles_otras = models.IntegerField()
    incentiva_hablar_ingles_otras = models.BooleanField(default=False)

    def __str__(self):
        return f"Docente: {self.id}"

class CoordinadorLengua(models.Model):
    # Formulario 1 - Recursos Multimedia
    presentaciones = models.IntegerField(default=0)
    simulaciones = models.IntegerField(default=0)
    juegos = models.IntegerField(default=0)
    objetos_aprendizaje = models.IntegerField(default=0)
    entornos_virtuales = models.IntegerField(default=0)
    cantidad_cd = models.IntegerField(default=0)
    cantidad_dvd = models.IntegerField(default=0)
    cantidad_mp4 = models.IntegerField(default=0)
    cantidad_streaming = models.IntegerField(default=0)
    cantidad_otros = models.IntegerField(default=0)

    # Formulario 2 - Materiales Fungibles
    fungibles_existencia = models.BooleanField(default=False)
    materiales_tipo_ubicacion = models.TextField(blank=True)
    materiales_inventario = models.TextField(blank=True)
    materiales_reposicion = models.CharField(max_length=255, blank=True)
    medios_compra = models.TextField(blank=True)

    def __str__(self):
        return f"Coordinador de Lengua: {self.id}"
    
class ESTER(models.Model):
    cantidad_cursos = models.IntegerField(default=0, help_text="Cantidad de cursos disponibles en ESTER")
    cantidad_ova = models.IntegerField(default=0, help_text="Cantidad de Objetos Virtuales de Aprendizaje (OVA) disponibles")
    cantidad_libros_ingles = models.IntegerField(default=0, help_text="Cantidad de libros en inglés disponibles")
    cantidad_audiolibros = models.IntegerField(default=0, help_text="Cantidad de audiolibros disponibles")
    cantidad_otros_recursos = models.IntegerField(default=0, help_text="Cantidad de otros recursos disponibles")

    acceso_ester_numero_2023_2024 = models.IntegerField(default=0, help_text="Número total de accesos de directores y docentes al Ecosistema ESTER durante 2023 y 2024")
    acceso_ester_porcentaje_2023_2024 = models.IntegerField(default=0, help_text="Porcentaje de acceso de directores y docentes al Ecosistema ESTER durante 2023 y 2024", validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"ESTER Recursos ID: {self.id}"