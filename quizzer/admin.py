from django.contrib import admin

from .models import Quizz, Round, Question, Team, Participate


admin.site.register(Round)
admin.site.register(Question)
admin.site.register(Team)
admin.site.register(Participate)


class RoundInline(admin.StackedInline):
    model = Round


@admin.register(Quizz)
class QuizzAdmin(admin.ModelAdmin):
    inlines = [
        RoundInline,
    ]
    list_display = ('name', 'rounds_names',)

    def rounds_names(self, obj):
        return ', '.join(obj.rounds.order_by('id').values_list('name', flat=True))
