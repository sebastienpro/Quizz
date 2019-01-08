from django.urls import path

from . import views

urlpatterns = [
    path('', views.buzzer, name='buzzer'),
    path('buzz', views.buzz, name='buzz'),
    path('teams', views.teams, name='teams'),
    path('register-buzzer/<int:team_id>/', views.register_buzzer, name='register_buzzer'),
]
