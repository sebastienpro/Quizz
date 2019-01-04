from django.contrib import admin

from .models import Quizz, Round, Question, Team, Participate, QuizzerState

admin.site.register(Question)
admin.site.register(Team)
admin.site.register(Participate)
admin.site.register(QuizzerState)


class QuestionInline(admin.StackedInline):
    model = Question


class RoundInline(admin.TabularInline):
    model = Round


@admin.register(Quizz)
class QuizzAdmin(admin.ModelAdmin):
    inlines = [
        RoundInline,
    ]
    list_display = ('name', 'rounds_names',)

    def rounds_names(self, obj):
        return ', '.join(obj.rounds.order_by('id').values_list('name', flat=True))


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]
