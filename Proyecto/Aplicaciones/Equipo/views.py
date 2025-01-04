from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from .models import Proyecto, Tarea, Comentario

# Listar Proyectos
def inicio(request):
    proyectos = Proyecto.objects.all()
    for proyecto in proyectos:
        proyecto.progreso = proyecto.calcular_progreso()
        proyecto.save()
    return render(request, 'inicio.html', {'proyectos': proyectos})

# Crear Proyecto
def crear_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_entrega = parse_date(request.POST.get('fecha_entrega'))

        if not fecha_entrega:
            return HttpResponse("Fecha de entrega no válida", status=400)

        Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_entrega=fecha_entrega,
            progreso=0
        )
        return redirect('inicio')

    return render(request, 'crearProyecto.html')

# Detalle Proyecto
def detalle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    tareas = proyecto.tareas.all()
    progreso = proyecto.calcular_progreso()
    proyecto.progreso = progreso
    proyecto.save()
    return render(request, 'detalleProyecto.html', {
        'proyecto': proyecto,
        'tareas': tareas,
        'progreso': progreso
    })

# Crear Tarea
def crear_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = parse_date(request.POST.get('fecha_inicio'))
        fecha_limite = parse_date(request.POST.get('fecha_limite'))
        completada = request.POST.get('completada') == 'on'

        if not fecha_inicio or not fecha_limite:
            return HttpResponse("Fechas no válidas", status=400)

        Tarea.objects.create(
            proyecto=proyecto,
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_limite=fecha_limite,
            completada=completada
        )
        proyecto.progreso = proyecto.calcular_progreso()
        proyecto.save()
        return redirect('detalle_proyecto', proyecto_id=proyecto.id)

    return render(request, 'crearTarea.html', {'proyecto': proyecto})

# Editar Proyecto
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_entrega = parse_date(request.POST.get('fecha_entrega'))

        if not fecha_entrega:
            return HttpResponse("Fecha de entrega no válida", status=400)

        proyecto.nombre = nombre
        proyecto.descripcion = descripcion
        proyecto.fecha_entrega = fecha_entrega
        proyecto.save()

        return redirect('detalle_proyecto', proyecto_id=proyecto.id)

    return render(request, 'editarProyecto.html', {'proyecto': proyecto})

# Eliminar Proyecto
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    return redirect('inicio')

# Crear Comentario
def crear_comentario(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        autor = request.POST.get('autor')
        contenido = request.POST.get('contenido')

        Comentario.objects.create(
            tarea=tarea,
            autor=autor,
            contenido=contenido
        )
        return redirect('detalle_proyecto', proyecto_id=tarea.proyecto.id)

    return render(request, 'crearComentario.html', {'tarea': tarea})

# Calendario
def calendario(request):
    tareas = Tarea.objects.all()
    return render(request, 'calendario.html', {'tareas': tareas})
