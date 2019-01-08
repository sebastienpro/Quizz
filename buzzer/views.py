from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from Quizz.settings import REDIS
from quizzer.views import get_current_quizz
from quizzer.models import Team

import redis

redis_conn = redis.Redis(host=REDIS['host'], port=REDIS['port'], db=REDIS['database'])

def teams(request):
    quizzer_state = get_current_quizz()
    teams = Team.objects.filter(participations__quizz=quizzer_state.quizz)
    return render(request, 'buzzer/team.html', {'teams': teams})


def register_buzzer(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
        request.session['team_id'] = team_id
        request.session['team_name'] = team.name
    except Team.DoesNotExist:
        return redirect('buzzer:teams')
    return redirect('buzzer:buzzer')


def buzzer(request):
    team_name = request.session.get('team_name')
    if not team_name:
        return redirect('buzzer:teams')
    return render(request, 'buzzer/buzzer.html', {'team_name': team_name})


@csrf_exempt
def buzz(request):
    team_id = request.session.get('team_id')
    redis_conn.setnx('buzzer', team_id)
    return HttpResponse('')
