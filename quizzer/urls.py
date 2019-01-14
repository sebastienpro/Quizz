from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teams/', views.teams, name='teams'),
    path('next/', views.next_question, name='next'),
    path('prev/', views.previous_question, name='previous'),
    path('buzzed/', views.get_team_has_buzzed, name='get_team_has_buzzed'),
    path('clearbuzz/', views.clear_buzzer, name='clear_buzzer'),
    path('add/<int:team_id>/', views.add_point, name='add_point'),
    path('remove/<int:team_id>/', views.remove_point, name='remove_point'),
    path('asshole/<int:team_id>/', views.add_asshole_card, name='add_asshole_card'),
]
