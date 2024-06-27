from django.db import models
from django.contrib.auth.models import User


class Creature(models.Model):
    name = models.CharField(
        max_length=100,
    )
    initiative = models.CharField(
        max_length=5
    )
    tracker = models.ForeignKey(
        'Tracker',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name} {self.initiative}'


class Tracker(models.Model):
    name = models.CharField(
        max_length=20
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.name}'