from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from Quizz.settings import REDIS
from .models import QuizzerState, Participate, Question, Round, Team

import redis
redis_conn = redis.Redis(host=REDIS['host'], port=REDIS['port'], db=REDIS['database'])


# Placeholder functions
def get_current_quizz():
    return QuizzerState.objects.filter(state=True).order_by('-pk')[0]


def clean_asshole():
    redis_conn.delete("fucked")

@login_required(login_url='/admin/login/')
def index(request):
    quizzer_state = get_current_quizz()
    return render(
        request,
        'quizzer/question.html',
        {
            'quizz': quizzer_state.quizz,
            'round': quizzer_state.round,
            'question': quizzer_state.question
        }
    )


def teams(request):
    quizzer_state = get_current_quizz()
    subscribed_teams = Participate.objects.filter(quizz=quizzer_state.quizz)
    response = {'teams': []}
    for team in subscribed_teams:
        response['teams'].append({'name': team.team.name, 'points': team.points, 'id': team.pk})
    return JsonResponse(response)


@login_required
def next_question(request):
    quizzer_state = get_current_quizz()
    quizzer_state.next()
    clean_asshole()
    response = {'question': quizzer_state.question_name, 'round': quizzer_state.round_name}
    return JsonResponse(response)


@login_required
def previous_question(request):
    quizzer_state = get_current_quizz()
    quizzer_state.previous()
    response = {'question': quizzer_state.question_name, 'round': quizzer_state.round_name}
    return JsonResponse(response)


@login_required
def get_team_has_buzzed(request):
    team_id = redis_conn.get("buzzer")
    try:
        team = Team.objects.get(pk=team_id)
        return JsonResponse({"team": team.name})
    except Team.DoesNotExist:
        return JsonResponse({"team": None})


@login_required
def clear_buzzer(request):
    redis_conn.delete("buzzer")
    return JsonResponse({"team": None})


@login_required
def add_point(request, team_id):
    quizzer_state = get_current_quizz()
    team_participation = Participate.objects.get(team_id=team_id, quizz=quizzer_state.quizz)
    team_participation.points += 1
    team_participation.save()
    return teams(request)


@login_required
def add_asshole_card(request, team_id):
    redis_conn.sadd("fucked", team_id)
    return JsonResponse({})
