from django.shortcuts import render

from .models import Quizz


# Placeholder functions
def get_current_quizz():
    return Quizz.objects.first()


def get_current_round(quizz):
    return quizz.rounds.first()


def get_current_question(round):
    return round.questions.first()


def index(request):
    quizz = get_current_quizz()
    round_ = get_current_round(quizz)
    question = get_current_question(round_)
    return render(
        request,
        'quizzer/question.html',
        {
            'quizz': quizz,
            'round': round_,
            'question': question
        }
    )
