from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import QuizzerState


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
