from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('publicar', views.crear_publicacion, name='crear-publicacion'),
]