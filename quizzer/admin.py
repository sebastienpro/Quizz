from django.contrib import admin

from .models import Quizz, Round, Question, Team, Participate

admin.site.register(Quizz)
admin.site.register(Round)
admin.site.register(Question)
admin.site.register(Team)
admin.site.register(Participate)
