from django.db import models

# Create your models here.


class Quizz(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Round(models.Model):
    name = models.CharField(max_length=255)
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)


class Question(models.Model):
    TYPE_CHOICES = (
        ('txt', 'texte'),
        ('img', 'image'),
        ('vid', 'video')
    )
    question = models.TextField(null=False)
    answer = models.TextField(null=True, default=None)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    order = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Participate(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.quizz.name+" / "+self.team.name
