from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import QuizzerState, Participate, Question, Round


# Placeholder functions
def get_current_quizz():
    return QuizzerState.objects.filter(state=True).order_by('-pk')[0]


@login_required(login_url='/admin/login/')
def index(request):
    quizzer_state = get_current_quizz()

    if quizzer_state.question:
        return render(
            request,
            'quizzer/question.html',
            {
                'quizz': quizzer_state.quizz,
                'round': quizzer_state.round,
                'question': quizzer_state.question
            }
        )
    else:
        return render(request, 'quizzer/start.html')


def teams(request):
    quizzer_state = get_current_quizz()
    subscribed_teams = Participate.objects.filter(quizz=quizzer_state.quizz)
    response = {'teams': []}
    for team in subscribed_teams:
        response['teams'].append({team.team.name: team.points})
    return JsonResponse(response)


@login_required
def next_question(request):
    quizzer_state = get_current_quizz()
    quizzer_state.next()
    response = {'question': quizzer_state.question_name, 'round': quizzer_state.round_name}
    return JsonResponse(response)
