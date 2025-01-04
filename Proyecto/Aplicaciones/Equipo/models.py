from django.db import models

# Modelo Proyecto
class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField()
    progreso = models.FloatField(default=0.0)

    def __str__(self):
        return self.nombre

    # Método para calcular el progreso
    def calcular_progreso(self):
        total_tareas = self.tareas.count()
        if total_tareas == 0:
            return 0.0
        tareas_completadas = self.tareas.filter(completada=True).count()
        return (tareas_completadas / total_tareas) * 100

    # Método para actualizar el progreso
    def actualizar_progreso(self):
        self.progreso = self.calcular_progreso()
        self.save(update_fields=['progreso'])  # Solo guarda el campo progreso


# Modelo Tarea
class Tarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    # Actualizar progreso del proyecto al guardar o actualizar la tarea
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda la tarea
        self.proyecto.actualizar_progreso()  # Actualiza el progreso del proyecto

    def delete(self, *args, **kwargs):
        proyecto = self.proyecto  # Almacenar el proyecto antes de eliminar la tarea
        super().delete(*args, **kwargs)  # Eliminar la tarea
        proyecto.actualizar_progreso()  # Actualizar progreso después de la eliminación


# Modelo Comentario
class Comentario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor} - {self.tarea.nombre}"
