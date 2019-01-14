import markdown
import redis

from django.db import models

from Quizz.settings import REDIS

redis_conn = redis.Redis(host=REDIS['host'], port=REDIS['port'], db=REDIS['database'])


class Quizz(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Round(models.Model):
    name = models.CharField(max_length=255)
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name='rounds')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'pk']


class Question(models.Model):
    TYPE_CHOICES = (
        ('txt', 'texte'),
        ('img', 'image'),
        ('vid', 'video')
    )
    question = models.TextField(null=False)
    answer = models.TextField(null=True, default=None, blank=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='txt')
    order = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order', 'pk']

    @property
    def question_html(self):
        return markdown.markdown(self.question)


class QuizzerState(models.Model):
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    state = models.NullBooleanField(default=None)

    def __str__(self):
        if self.round:
            return f"{self.quizz.name}/{self.round.name} -> {self.state}"
        else:
            return f"{self.quizz.name} -> {self.state}"

    def next(self):
        self.question = self.get_next_question()
        if not self.question:
            self.round = self.get_next_round()
        self.save()

    def previous(self):
        self.question = self.get_prev_question()
        if not self.question:
            self.round = self.get_prev_round()
        self.save()

    def get_next_question(self):
        if not self.question:
            return Question.objects.filter(round=self.round).first()
        questions = list(Question.objects.filter(round=self.round))
        idx = questions.index(self.question)
        try:
            return questions[idx + 1]
        except IndexError:
            return None

    def get_next_round(self):
        if not self.round:
            return Round.objects.filter(quizz=self.quizz).first()
        rounds = list(Round.objects.filter(quizz=self.quizz))
        idx = rounds.index(self.round)
        try:
            return rounds[idx + 1]
        except IndexError:
            return None

    def get_prev_question(self):
        if not self.question:
            return Question.objects.filter(round=self.round).last()
        questions = list(Question.objects.filter(round=self.round))
        idx = questions.index(self.question)
        if idx == 0:
            return None
        try:
            return questions[idx - 1]
        except IndexError:
            return None

    def get_prev_round(self):
        if not self.round:
            return Round.objects.filter(quizz=self.quizz).last()
        rounds = list(Round.objects.filter(quizz=self.quizz))
        idx = rounds.index(self.round)
        if idx == 0:
            return None
        try:
            return rounds[idx - 1]
        except IndexError:
            return None

    @property
    def question_name(self):
        if self.question:
            return self.question.question_html

    @property
    def round_name(self):
        if self.round:
            return self.round.name


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Participate(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='participations')
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.quizz.name+" / "+self.team.name

    @property
    def is_fucked(self):
        fucked = redis_conn.smembers("fucked")
        if self.team_id in {int(f) for f in fucked}:
            return True
        else:
            return False
