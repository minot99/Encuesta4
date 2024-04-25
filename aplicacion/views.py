from django.shortcuts import render, redirect
from django.core import serializers
import json
from microsoft_authentication.auth.auth_decorators import microsoft_login_required
from django.views.generic import TemplateView
import requests
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
import xlsxwriter
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from aplicacion.models import User
from django.db.models import Count, Sum, Avg
from django.utils.safestring import mark_safe
import json

# Create your views here.
def home(request):
    if "token_cache" not in request.session.keys():
        return render(request, "aplicacion/index.html")
    else:
        return redirect("formulario")

@microsoft_login_required()
def formulario(request):
    complete_session(request=request)
    usuario_nivel = request.session['user_data']['NIVEL_DESC']
    if usuario_nivel == 'DOCENTE':
        return redirect('docente')
    else:
        if usuario_nivel == 'DIRECTOR':
            return redirect('director')
        else:
            return redirect('microsoft_authentication/logout/')

@microsoft_login_required()
def hello(request):
    complete_session(request=request)
    return render(request, "aplicacion/hello.html", {
        'data': request.session["user_data"]
    })

@microsoft_login_required()
def docente(request):
    if is_docente(request):
        return render(request, "aplicacion/docente.html",{
            "nombre_usuario": request.session["user_data"]["NOMBRE_USUARIO"],
            "cedula_usuario": request.session["user_data"]["CEDULA_USUARIO"],
            "correo_usuario": request.session["user_data"]["CORREO_USUARIO"],
        })
    else:
        redirect('formulario')

def docente_bd(request):
    contexto = {'docente': Docente.objects.all()}
    return render(request, "aplicacion/docente_bd.html", contexto)

def export_docente(request):
    # Obtener los datos para exportar
    docentes = Docente.objects.all()

    # Crear un nuevo libro de trabajo de Excel
    workbook = xlsxwriter.Workbook('formulario_docente.xlsx')
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de las columnas
    headers = [
        'Nombre', 'Apellido', 'Cédula', 'Teléfono Oficina', 'Teléfono Personal',
        'Correo Institucional', 'Habla Inglés en Clase', 'Porcentaje de Tiempo en Inglés',
        'Incentiva Hablar Inglés', 'Tiempo de Diálogo en Inglés', 'Tipo de Señalizaciones en Inglés',
        'Señalizaciones en el Aula de Inglés', 'Cantidad de Señalizaciones en el Aula de Inglés',
        'Interactúa con Directivos en Inglés', 'Interactúa con Docentes en Inglés',
        'Interactúa con Padres en Inglés', 'Interactúa con Estudiantes en Inglés',
        'Porcentaje de Interacción con Estudiantes en Inglés', 'Actividades de Inglés Fuera del Aula',
        'Frecuencia de Actividades de Inglés', 'Experiencia en Años', 'Sector de Experiencia',
        'Niveles Impartidos', 'Nivel Actual', 'Título de Enseñanza de Inglés',
        'Títulos Formales en Inglés', 'Cursos Nacionales de Inglés', 'Cursos Internacionales de Inglés',
        'Certificación de Inglés', 'Nombre de la Titulación', 'Año de Certificación',
        'Vencimiento de la Certificación', 'Nivel de Inglés del Docente',
        'Dispuesto a Renovar Certificación', 'Frecuencia de Uso de Recursos de Inglés',
        'Acceso a Recursos de Inglés'
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Escribir los datos de los docentes en el archivo Excel
    for row, docente in enumerate(docentes):
        worksheet.write(row + 1, 0, docente.nombre)
        worksheet.write(row + 1, 1, docente.apellido)
        worksheet.write(row + 1, 2, docente.cedula)
        worksheet.write(row + 1, 3, docente.telefono_oficina)
        worksheet.write(row + 1, 4, docente.telefono_personal)
        worksheet.write(row + 1, 5, docente.correo_institucional)
        worksheet.write(row + 1, 6, docente.habla_ingles_en_clase)
        worksheet.write(row + 1, 7, docente.porcentaje_tiempo_ingles)
        worksheet.write(row + 1, 8, docente.incentiva_hablar_ingles)
        worksheet.write(row + 1, 9, docente.tiempo_dialogo_ingles)
        worksheet.write(row + 1, 10, docente.tipo_senalizaciones_ingles)
        worksheet.write(row + 1, 11, docente.senalizaciones_aula_ingles)
        worksheet.write(row + 1, 12, docente.cantidad_senalizaciones_aula)
        worksheet.write(row + 1, 13, docente.interactua_directivos_ingles)
        worksheet.write(row + 1, 14, docente.interactua_docentes_ingles)
        worksheet.write(row + 1, 15, docente.interactua_padres_ingles)
        worksheet.write(row + 1, 16, docente.interactua_estudiantes_ingles)
        worksheet.write(row + 1, 17, docente.porcentaje_interaccion_estudiantes)
        worksheet.write(row + 1, 18, docente.actividades_ingles_fuera_aula)
        worksheet.write(row + 1, 19, docente.frecuencia_actividades_ingles)
        worksheet.write(row + 1, 20, docente.experiencia_anos)
        worksheet.write(row + 1, 21, docente.sector_experiencia)
        worksheet.write(row + 1, 22, docente.niveles_impartidos)
        worksheet.write(row + 1, 23, docente.nivel_actual)
        worksheet.write(row + 1, 24, docente.titulo_ensenanza_ingles)
        worksheet.write(row + 1, 25, docente.titulos_formales_ingles)
        worksheet.write(row + 1, 26, docente.cursos_nacionales_ingles)
        worksheet.write(row + 1, 27, docente.cursos_internacionales_ingles)
        worksheet.write(row + 1, 28, docente.certificacion_ingles)
        worksheet.write(row + 1, 29, docente.nombre_titulacion)
        worksheet.write(row + 1, 30, docente.ano_certificacion)
        worksheet.write(row + 1, 31, docente.vencimiento_certificacion)
        worksheet.write(row + 1, 32, docente.nivel_ingles_docente)
        worksheet.write(row + 1, 33, docente.dispuesto_renovar_certificacion)
        worksheet.write(row + 1, 34, docente.frecuencia_uso_recursos_ingles)
        worksheet.write(row + 1, 35, docente.acceso_recursos_ingles)

    # Cerrar el libro de trabajo
    workbook.close()

    # Devolver el archivo Excel como respuesta HTTP para descargar
    with open('formulario_docente.xlsx', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="formulario_docente.xlsx"'
    return response

def form_docente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre-docente')
        apellido = request.POST.get('apellido-docente')
        cedula = request.POST.get('cedula-docente')
        telefono_oficina = request.POST.get('tel-ofi-docente')
        telefono_personal = request.POST.get('tel-per-docente')
        correo_institucional = request.POST.get('correo-inst-docente')
        habla_ingles_en_clase = request.POST.get('habla-ingles-clase-ingles')
        porcentaje_tiempo_ingles = request.POST.get('porcentaje-tiempo-ingles')
        incentiva_hablar_ingles = request.POST.get('incentiva-hablar-ingles')
        tiempo_dialogo_ingles = request.POST.get('tiempo-dialogo-ingles')
        senalizaciones_aula_ingles = request.POST.get('senalizaciones-aula-ingles')
        cantidad_senalizaciones_aula = request.POST.get('cantidad-senalizaciones-aula')
        interactua_directivos_ingles = request.POST.get('interactua-directivos')
        interactua_docentes_ingles = request.POST.get('interactua-docentes')
        interactua_padres_ingles = request.POST.get('interactua-padres')
        interactua_estudiantes_ingles = request.POST.get('interactua-estudiantes')
        porcentaje_interaccion_estudiantes = request.POST.get('interactua-estudiantes-porcentaje')
        frecuencia_actividades_ingles = request.POST.get('frecuencia-actividades')
        experiencia_anos = request.POST.get('anos-experiencia')
        sector_experiencia = request.POST.get('sector-experiencia')
        niveles_impartidos = request.POST.getlist('niveles-impartidos')
        nivel_actual = request.POST.get('nivel-actual')
        titulo_ensenanza_ingles = request.POST.get('titulo-ensenanza')
        titulos_formales_ingles = request.POST.get('titulos-formales')
        cursos_nacionales_ingles = request.POST.get('cursos-nacionales')
        cursos_internacionales_ingles = request.POST.get('cursos-internacionales')
        certificacion_ingles = request.POST.get('certificacion-ingles')
        nombre_titulacion = request.POST.get('nombre-titulacion')
        ano_certificacion = request.POST.get('ano-certificacion')
        vencimiento_certificacion = request.POST.get('ano-vencimiento')
        nivel_ingles_docente = request.POST.get('nivel-ingles-docente')
        dispuesto_renovar_certificacion = request.POST.get('renovar-certificacion')
        frecuencia_uso_recursos_ingles = request.POST.get('frecuencia-recursos')
        acceso_recursos_ingles = request.POST.get('acceso-recursos')

        docente = Docente(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono_oficina=telefono_oficina,
            telefono_personal=telefono_personal,
            correo_institucional=correo_institucional,
            habla_ingles_en_clase=habla_ingles_en_clase,
            porcentaje_tiempo_ingles=porcentaje_tiempo_ingles,
            incentiva_hablar_ingles=incentiva_hablar_ingles,
            tiempo_dialogo_ingles=tiempo_dialogo_ingles,
            senalizaciones_aula_ingles=senalizaciones_aula_ingles,
            cantidad_senalizaciones_aula=cantidad_senalizaciones_aula,
            interactua_directivos_ingles=interactua_directivos_ingles,
            interactua_docentes_ingles=interactua_docentes_ingles,
            interactua_padres_ingles=interactua_padres_ingles,
            interactua_estudiantes_ingles=interactua_estudiantes_ingles,
            porcentaje_interaccion_estudiantes=porcentaje_interaccion_estudiantes,
            frecuencia_actividades_ingles=frecuencia_actividades_ingles,
            experiencia_anos=experiencia_anos,
            sector_experiencia=sector_experiencia,
            niveles_impartidos=niveles_impartidos,
            nivel_actual=nivel_actual,
            titulo_ensenanza_ingles=titulo_ensenanza_ingles,
            titulos_formales_ingles=titulos_formales_ingles,
            cursos_nacionales_ingles=cursos_nacionales_ingles,
            cursos_internacionales_ingles=cursos_internacionales_ingles,
            certificacion_ingles=certificacion_ingles,
            nombre_titulacion=nombre_titulacion,
            ano_certificacion=ano_certificacion,
            vencimiento_certificacion=vencimiento_certificacion,
            nivel_ingles_docente=nivel_ingles_docente,
            dispuesto_renovar_certificacion=dispuesto_renovar_certificacion,
            frecuencia_uso_recursos_ingles=frecuencia_uso_recursos_ingles,
            acceso_recursos_ingles=acceso_recursos_ingles
        )
        docente.save()

        return HttpResponseRedirect('/gracias/')

    return render(request, 'aplicacion/docente.html')

@microsoft_login_required()
def director(request):
    if is_director(request):
        return render(request, "aplicacion/director.html",{
            "nombre_usuario": request.session["user_data"]["NOMBRE_USUARIO"],
            "cedula_usuario": request.session["user_data"]["CEDULA_USUARIO"],
            "correo_usuario": request.session["user_data"]["CORREO_USUARIO"],
        })
    else:
        return redirect('formulario')

def director_bd(request):
    contexto = {'director': Director.objects.all()}
    return render(request, "aplicacion/director_bd.html", contexto)

def export_director(request):
    # Obtener los datos para exportar
    director = Director.objects.all()

    # Crear un nuevo libro de trabajo de Excel
    workbook = xlsxwriter.Workbook('formulario_director.xlsx')
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de las columnas
    headers = [
        'Nombre', 'Apellido', 'Cédula', 'Teléfono Oficina', 'Teléfono Personal',
        'Correo Institucional', 'Correo Personal 1', 'Correo Personal 2', 'Código SIACE',
        'Nombre Centro Educativo', 'Región Educativa', 'Provincia', 'Dirección',
        'Nivel Escolar', 'Matrícula Total', 'Grado 1', 'Femenino 1', 'Masculino 1',
        'Grado 2', 'Femenino 2', 'Masculino 2', 'Grado 3', 'Femenino 3', 'Masculino 3',
        'Grado 4', 'Femenino 4', 'Masculino 4', 'Total Docentes', 'Docentes 1', 'Docentes 2',
        'Docentes 3', 'Docentes 4', 'Estudiantes Salón', 'Docentes Asignatura',
        'Participa PPB', 'Estudiantes Nivel PPB', 'Docentes Capacitados PPB',
        'Docentes Aprobados PPB', 'Docentes Capacitación Exterior', 'Códigos Plan Estudio',
        'Planes Estudio', 'Asignaturas Inglés Plan Estudios', 'Asignaturas Inglés Dictadas',
        'Planes Clase', 'Horas Inglés', 'Horas Teóricas', 'Horas Prácticas',
        'Actividades Propio Centro', 'Actividades MEDUCA Centro', 'Actividades Externas Centro',
        'Detalle Actividades Anual', 'Cantidad Estudiantes Actividades Externas 1',
        'Cantidad Estudiantes Actividades Externas 2', 'Cantidad Estudiantes Actividades Externas 3',
        'Cantidad Estudiantes Actividades Externas 4', 'After School Existencia',
        'After School Descripción', 'After School Participación 1', 'After School Participación 2',
        'After School Participación 3', 'After School Participación 4', 'After School Recursos'
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Escribir los datos de los directores en el archivo Excel
    for row, d in enumerate(director):
        worksheet.write(row + 1, 0, d.nombre)
        worksheet.write(row + 1, 1, d.apellido)
        worksheet.write(row + 1, 2, d.cedula)
        worksheet.write(row + 1, 3, d.telefono_oficina)
        worksheet.write(row + 1, 4, d.telefono_personal)
        worksheet.write(row + 1, 5, d.correo_institucional)
        worksheet.write(row + 1, 6, d.correo_personal1)
        worksheet.write(row + 1, 7, d.correo_personal2)
        worksheet.write(row + 1, 8, d.codigo_siace)
        worksheet.write(row + 1, 9, d.nombre_centro_educativo)
        worksheet.write(row + 1, 10, d.region_educativa)
        worksheet.write(row + 1, 11, d.provincia)
        worksheet.write(row + 1, 12, d.direccion)
        worksheet.write(row + 1, 13, d.nivel_escolar)
        worksheet.write(row + 1, 14, d.matricula_total)
        worksheet.write(row + 1, 15, d.grado1)
        worksheet.write(row + 1, 16, d.femenino1)
        worksheet.write(row + 1, 17, d.masculino1)
        worksheet.write(row + 1, 18, d.grado2)
        worksheet.write(row + 1, 19, d.femenino2)
        worksheet.write(row + 1, 20, d.masculino2)
        worksheet.write(row + 1, 21, d.grado3)
        worksheet.write(row + 1, 22, d.femenino3)
        worksheet.write(row + 1, 23, d.masculino3)
        worksheet.write(row + 1, 24, d.grado4)
        worksheet.write(row + 1, 25, d.femenino4)
        worksheet.write(row + 1, 26, d.masculino4)
        worksheet.write(row + 1, 27, d.total_docentes)
        worksheet.write(row + 1, 28, d.docentes1)
        worksheet.write(row + 1, 29, d.docentes2)
        worksheet.write(row + 1, 30, d.docentes3)
        worksheet.write(row + 1, 31, d.docentes4)
        worksheet.write(row + 1, 32, d.estudiantes_salon)
        worksheet.write(row + 1, 33, d.docentes_asignatura)
        worksheet.write(row + 1, 34, d.participa_ppb)
        worksheet.write(row + 1, 35, d.estudiantes_nivel_ppb)
        worksheet.write(row + 1, 36, d.docentes_capacitados_ppb)
        worksheet.write(row + 1, 37, d.docentes_aprobados_ppb)
        worksheet.write(row + 1, 38, d.docentes_capacitacion_exterior)
        worksheet.write(row + 1, 39, d.codigos_plan_estudio)
        worksheet.write(row + 1, 40, d.planes_estudio)
        worksheet.write(row + 1, 41, d.asignaturas_ingles_plan_estudios)
        worksheet.write(row + 1, 42, d.asignaturas_ingles_dictadas)
        worksheet.write(row + 1, 43, d.planes_clase)
        worksheet.write(row + 1, 44, d.horas_ingles)
        worksheet.write(row + 1, 45, d.horas_teoricas)
        worksheet.write(row + 1, 46, d.horas_practicas)
        worksheet.write(row + 1, 47, d.actividades_propio_centro)
        worksheet.write(row + 1, 48, d.actividades_meduca_centro)
        worksheet.write(row + 1, 49, d.actividades_externas_centro)
        worksheet.write(row + 1, 50, d.detalle_actividades_anual)
        worksheet.write(row + 1, 51, d.cantidad_estudiantes_actividades_externas_1)
        worksheet.write(row + 1, 52, d.cantidad_estudiantes_actividades_externas_2)
        worksheet.write(row + 1, 53, d.cantidad_estudiantes_actividades_externas_3)
        worksheet.write(row + 1, 54, d.cantidad_estudiantes_actividades_externas_4)
        worksheet.write(row + 1, 55, d.after_school_existencia)
        worksheet.write(row + 1, 56, d.after_school_descripcion)
        worksheet.write(row + 1, 57, d.after_school_participacion_1)
        worksheet.write(row + 1, 58, d.after_school_participacion_2)
        worksheet.write(row + 1, 59, d.after_school_participacion_3)
        worksheet.write(row + 1, 60, d.after_school_participacion_4)
        worksheet.write(row + 1, 61, d.after_school_recursos)

    # Cerrar el libro de trabajo
    workbook.close()

    # Devolver el archivo Excel como respuesta HTTP para descargar
    with open('formulario_director.xlsx', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="formulario_director.xlsx"'
    return response

def form_director(request):
    if request.method == 'POST':
        # Procesar el formulario enviado
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        telefono_oficina = request.POST.get('telefono_oficina')
        telefono_personal = request.POST.get('telefono_personal')
        correo_institucional = request.POST.get('correo_institucional')
        correo_personal1 = request.POST.get('correo_personal1')
        correo_personal2 = request.POST.get('correo_personal2')
        codigo_siace = request.POST.get('codigo_siace')
        nombre_centro_educativo = request.POST.get('nombre_centro_educativo')
        region_educativa = request.POST.get('region_educativa')
        provincia = request.POST.get('provincia')
        direccion = request.POST.get('direccion')
        nivel_escolar = request.POST.get('nivel_escolar')
        matricula_total = request.POST.get('matricula_total')
        grado1 = request.POST.get('grado1')
        femenino1 = request.POST.get('femenino1')
        masculino1 = request.POST.get('masculino1')
        grado2 = request.POST.get('grado2')
        femenino2 = request.POST.get('femenino2')
        masculino2 = request.POST.get('masculino2')
        grado3 = request.POST.get('grado3')
        femenino3 = request.POST.get('femenino3')
        masculino3 = request.POST.get('masculino3')
        grado4 = request.POST.get('grado4')
        femenino4 = request.POST.get('femenino4')
        masculino4 = request.POST.get('masculino4')
        total_docentes = request.POST.get('total_docentes')
        docentes1 = request.POST.get('docentes1')
        docentes2 = request.POST.get('docentes2')
        docentes3 = request.POST.get('docentes3')
        docentes4 = request.POST.get('docentes4')
        estudiantes_salon = request.POST.get('estudiantes_salon')
        docentes_asignatura = request.POST.get('docentes_asignatura')
        participa_ppb = request.POST.get('participa_ppb')
        estudiantes_nivel_ppb = request.POST.get('estudiantes_nivel_ppb')
        docentes_capacitados_ppb = request.POST.get('docentes_capacitados_ppb')
        docentes_aprobados_ppb = request.POST.get('docentes_aprobados_ppb')
        docentes_capacitacion_exterior = request.POST.get('docentes_capacitacion_exterior')
        codigos_plan_estudio = request.POST.get('codigos_plan_estudio')
        planes_estudio = request.POST.get('planes_estudio')
        asignaturas_ingles_plan_estudios = request.POST.get('asignaturas_ingles_plan_estudios')
        asignaturas_ingles_dictadas = request.POST.get('asignaturas_ingles_dictadas')
        planes_clase = request.POST.get('planes_clase')
        horas_ingles = request.POST.get('horas_ingles')
        horas_teoricas = request.POST.get('horas_teoricas')
        horas_practicas = request.POST.get('horas_practicas')
        actividades_propio_centro = request.POST.get('actividades_propio_centro')
        actividades_meduca_centro = request.POST.get('actividades_meduca_centro')
        actividades_externas_centro = request.POST.get('actividades_externas_centro')
        detalle_actividades_anual = request.POST.get('detalle_actividades_anual')
        cantidad_estudiantes_actividades_externas_1 = request.POST.get('cantidad_estudiantes_actividades_externas_1')
        cantidad_estudiantes_actividades_externas_2 = request.POST.get('cantidad_estudiantes_actividades_externas_2')
        cantidad_estudiantes_actividades_externas_3 = request.POST.get('cantidad_estudiantes_actividades_externas_3')
        cantidad_estudiantes_actividades_externas_4 = request.POST.get('cantidad_estudiantes_actividades_externas_4')
        after_school_existencia = request.POST.get('after_school_existencia')
        after_school_descripcion = request.POST.get('after_school_descripcion')
        after_school_participacion_1 = request.POST.get('after_school_participacion_1')
        after_school_participacion_2 = request.POST.get('after_school_participacion_2')
        after_school_participacion_3 = request.POST.get('after_school_participacion_3')
        after_school_participacion_4 = request.POST.get('after_school_participacion_4')
        after_school_recursos = request.POST.get('after_school_recursos')

        # Crear una instancia del modelo Director con los datos obtenidos
        director = Director(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono_oficina=telefono_oficina,
            telefono_personal=telefono_personal,
            correo_institucional=correo_institucional,
            correo_personal1=correo_personal1,
            correo_personal2=correo_personal2,
            codigo_siace=codigo_siace,
            nombre_centro_educativo=nombre_centro_educativo,
            region_educativa=region_educativa,
            provincia=provincia,
            direccion=direccion,
            nivel_escolar=nivel_escolar,
            matricula_total=matricula_total,
            grado1=grado1,
            femenino1=femenino1,
            masculino1=masculino1,
            grado2=grado2,
            femenino2=femenino2,
            masculino2=masculino2,
            grado3=grado3,
            femenino3=femenino3,
            masculino3=masculino3,
            grado4=grado4,
            femenino4=femenino4,
            masculino4=masculino4,
            total_docentes=total_docentes,
            docentes1=docentes1,
            docentes2=docentes2,
            docentes3=docentes3,
            docentes4=docentes4,
            estudiantes_salon=estudiantes_salon,
            docentes_asignatura=docentes_asignatura,
            participa_ppb=participa_ppb,
            estudiantes_nivel_ppb=estudiantes_nivel_ppb,
            docentes_capacitados_ppb=docentes_capacitados_ppb,
            docentes_aprobados_ppb=docentes_aprobados_ppb,
            docentes_capacitacion_exterior=docentes_capacitacion_exterior,
            codigos_plan_estudio=codigos_plan_estudio,
            planes_estudio=planes_estudio,
            asignaturas_ingles_plan_estudios=asignaturas_ingles_plan_estudios,
            asignaturas_ingles_dictadas=asignaturas_ingles_dictadas,
            planes_clase=planes_clase,
            horas_ingles=horas_ingles,
            horas_teoricas=horas_teoricas,
            horas_practicas=horas_practicas,
            actividades_propio_centro=actividades_propio_centro,
            actividades_meduca_centro=actividades_meduca_centro,
            actividades_externas_centro=actividades_externas_centro,
            detalle_actividades_anual=detalle_actividades_anual,
            cantidad_estudiantes_actividades_externas_1=cantidad_estudiantes_actividades_externas_1,
            cantidad_estudiantes_actividades_externas_2=cantidad_estudiantes_actividades_externas_2,
            cantidad_estudiantes_actividades_externas_3=cantidad_estudiantes_actividades_externas_3,
            cantidad_estudiantes_actividades_externas_4=cantidad_estudiantes_actividades_externas_4,
            after_school_existencia=after_school_existencia,
            after_school_descripcion=after_school_descripcion,
            after_school_participacion_1=after_school_participacion_1,
            after_school_participacion_2=after_school_participacion_2,
            after_school_participacion_3=after_school_participacion_3,
            after_school_participacion_4=after_school_participacion_4,
            after_school_recursos=after_school_recursos
        )
        # Guardar el objeto Director en la base de datos
        director.save()

        # Redireccionar a alguna página o hacer alguna otra acción después de procesar el formulario
        return HttpResponseRedirect('/gracias/')

    # Si el método de solicitud es GET o el formulario no es válido, simplemente renderiza el formulario vacío
    return render(request, 'aplicacion/director.html')

@microsoft_login_required()
def coordinador_5(request):
    return render(request, "aplicacion/coordinador_5.html")

@microsoft_login_required()
def tecnologia_6(request):
    return render(request, "aplicacion/tecnologia_6.html")

@microsoft_login_required()
def otros_docentes_7(request):
    return render(request, "aplicacion/otros_docentes_7.html")

@microsoft_login_required()
def lengua_8(request):
    return render(request, "aplicacion/lengua_8.html")

@microsoft_login_required()
def ester_9(request):
    return render(request, "aplicacion/ESTER_9.html")

@microsoft_login_required()
def gracias(request):
    return render(request, "aplicacion/gracias.html")

class logout_page(TemplateView):
    template_name = 'admin/logout.html'

def complete_session(request):
    if "user_data" not in request.session.keys():
        session_data = json.loads(request.session["token_cache"])
        access_token_dict = session_data["AccessToken"]
        account_dict = session_data["Account"]
        token_data_id = next(iter(access_token_dict))
        account_data_id = next(iter(account_dict))
        account = account_dict[account_data_id]["username"]
        access_token = access_token_dict[token_data_id]["secret"]

        url = f"https://formulario-api-aeekxgs7da-uc.a.run.app/api/user/{account}"
        headers = {'Authorization': access_token}
        response = requests.get(url, headers = headers)
        response_json = response.json()
        request.session["user_data"] = response_json
        
def is_docente(request):
    return request.session['user_data']['NIVEL_DESC'] == 'DOCENTE'

def is_director(request):
    return request.session['user_data']['NIVEL_DESC'] == 'DIRECTOR'
# def make_redirect(request):
#     sesion_data = serializers.deserialize('json', request.session["token_cache"])

# def request_user_data(token):
#     return token
def crear_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:index')  # Redirige al panel de administración
    else:
        form = UserCreationForm()
    return render(request, 'aplicacion/crear_user.html', {'form': form})

def editar_user(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin:index')  # Redirige al panel de administración
    else:
        form = UserEditForm(instance=user)
    return render(request, 'aplicacion/editar_user.html', {'form': form})

def eliminar_user(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('admin:index')  # Redirige al panel de administración
    return render(request, 'aplicacion/eliminar_user.html', {'user': user})

def user(request):
    users = User.objects.all()
    return render(request, 'admin/user.html', {'users': users})


#VISTAS PARA LOS GRAFICOS

@microsoft_login_required()
def graficos(request):
    # Lógica para obtener y procesar los datos de centros educativos
    complete_session_centros_educativos(request)
    data = request.session.get("centros_educativos_data", {})

    if data:
        for centro in data:
            for key, value in centro.items():
                if value is None:
                    centro[key] = 'No disponible'

    data_json = mark_safe(json.dumps(data))

    # Renderizar la plantilla con el contexto necesario
    return render(request, "aplicacion/graficos.html", {
        'data_json': data_json
    })

def datos_nivel_bilinguismo(request):
    niveles = Docente.objects.values('nivel_ingles_docente').annotate(total=Count('nivel_ingles_docente')).order_by('nivel_ingles_docente')
    data = {
        'niveles': list(niveles)
    }
    return JsonResponse(data)

#Promedio porcentaje de actividades de bilinguismo
def promedios_generales(request):
    promedio_tiempo_ingles = Docente.objects.aggregate(Avg('porcentaje_tiempo_ingles'))['porcentaje_tiempo_ingles__avg'] or 0
    promedio_tiempo_dialogo_ingles = Docente.objects.aggregate(Avg('tiempo_dialogo_ingles'))['tiempo_dialogo_ingles__avg'] or 0
    promedio_cantidad_senalizaciones = Docente.objects.aggregate(Avg('cantidad_senalizaciones_aula'))['cantidad_senalizaciones_aula__avg'] or 0
    promedio_interaccion_estudiantes = Docente.objects.aggregate(Avg('porcentaje_interaccion_estudiantes'))['porcentaje_interaccion_estudiantes__avg'] or 0
    


    data = {
        'promedio_tiempo_ingles': promedio_tiempo_ingles,
        'promedio_tiempo_dialogo_ingles': promedio_tiempo_dialogo_ingles,
        'promedio_cantidad_senalizaciones': promedio_cantidad_senalizaciones,
        'promedio_interaccion_estudiantes': promedio_interaccion_estudiantes,
    }
    return JsonResponse(data)

def complete_session_centros_educativos(request):
    if "centros_educativos_data" not in request.session.keys():
        session_data = json.loads(request.session["token_cache"])
        access_token_dict = session_data["AccessToken"]
        token_data_id = next(iter(access_token_dict))
        access_token = access_token_dict[token_data_id]["secret"]

        url = "https://formulario-api-aeekxgs7da-uc.a.run.app/api/centroseducativos"
        headers = {'Authorization': access_token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            request.session["centros_educativos_data"] = response_json
        else:
            print("Error al obtener datos de centros educativos: ", response.status_code)

        
        


