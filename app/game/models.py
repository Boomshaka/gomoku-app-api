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

    def make_move(self, row, col, player=1):
        grid = self.grid
        if row < 0 or col < 0 or row >= 15 or col >= 15:
            raise IndexError("Board column and row must be between 0 and 15")
        if grid[row][col] != 0:
            raise ValueError("Index already contains a gamepiece")
        grid[row][col] = 1
        return grid
