from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teams/', views.teams, name='teams'),
    path('next/', views.next_question, name='next'),
    path('prev/', views.previous_question, name='previous'),
    path('buzzed/', views.get_team_has_buzzed, name='get_team_has_buzzed'),
    path('clearbuzz/', views.clear_buzzer, name='clear_buzzer'),
]
