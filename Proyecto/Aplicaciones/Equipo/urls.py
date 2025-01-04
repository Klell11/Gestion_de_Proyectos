from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('proyecto/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyecto/<int:proyecto_id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('proyecto/<int:proyecto_id>/crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('proyecto/<int:proyecto_id>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('proyecto/<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('tarea/<int:tarea_id>/crear_comentario/', views.crear_comentario, name='crear_comentario'),
    path('calendario/', views.calendario, name='calendario'),
]
