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
    next_round = False
    if not quizzer_state.question:
        next_question = Question.objects.filter(quizz=quizzer_state.quizz, round=quizzer_state.round).order_by('order', 'pk')[0]
        response = {'question': next_question.question}
    else:
        round_questions = Question.objects.filter(round=quizzer_state.round).order_by('order', 'pk')
        next_question_id = 0
        for question in round_questions:
            next_question_id += 1
            if question.pk == quizzer_state.question.pk:
                break
        try:
            next_question = round_questions[next_question_id]
            response = {'question': next_question.question}
        except IndexError:
            response = {'question': None}
            next_round = True
    if next_round:
        rounds = Round.objects.filter(quizz=quizzer_state.quizz).order_by('pk')
        round_cpt = 0
        for quizz_round in rounds:
            round_cpt += 1
            if quizz_round.pk == quizzer_state.round.pk:
                break
        quizzer_state.round = rounds[round_cpt]
        quizzer_state.question = None
    else:
        quizzer_state.question = next_question
    quizzer_state.save()
    return JsonResponse(response)
