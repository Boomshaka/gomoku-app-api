import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


def generate_empty_board():
    return [[0 for x in range(15)] for y in range(15)]


class Game(models.Model):
    ONE = 1
    TWO = 2
    ZERO = 0
    STARTED = 'Started'
    PLAYING = 'Playing'
    FINISHED = 'Finished'
    WINNER_CHOICES = (
        (ONE, 'one'),
        (TWO, 'two'),
        (ZERO, 'zero')
    )
    STATUS_CHOICES = (
        (STARTED, 'started'),
        (PLAYING, 'playing'),
        (FINISHED, 'finished')
    )

    id = models.UUIDField(primary_key=True, blank=True, default=uuid.uuid4)
    grid = ArrayField(
        ArrayField(models.IntegerField(blank=True, default=0)),
        blank=True,
        default=generate_empty_board
    )
    winner = models.IntegerField(
        choices=WINNER_CHOICES,
        blank=True,
        default=ZERO
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        blank=True,
        default=STARTED,
        max_length=20
    )
    date = models.DateTimeField(auto_now_add=True)
