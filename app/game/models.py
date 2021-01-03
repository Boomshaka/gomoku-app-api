import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

GRID_SIZE = 15


def generate_empty_grid():
    return [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]


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
        default=generate_empty_grid
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

    def get(self, row, col):
        """Get value at given row,col position"""
        if row < 0 or col < 0 or row >= GRID_SIZE or col >= GRID_SIZE:
            return 0
        return self.grid[row][col]

    def make_move(self, row, col, player=1):
        """
            Fills grid index specified by row,col
        """
        grid = self.grid
        if row < 0 or col < 0 or row >= GRID_SIZE or col >= GRID_SIZE:
            raise IndexError(
                f"Board column and row must be between 0 and {GRID_SIZE}"
            )
        if grid[row][col] != 0:
            raise ValueError("Index already contains a gamepiece")
        grid[row][col] = 1
        return grid

    def check_winner(self):
        """
            Check if there is a winner.
            Output:
                0 if no winner,
                winning player's number (1,2) if there's a winner
        """
        grid = self.grid
        # check in 4 directions: down-left, down, down-right, right
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] == 0:
                    continue
                player_num = grid[i][j]
                # check if there exist 5 in a line
                for d in dirs:
                    x, y = i, j
                    count = 0
                    for _ in range(5):
                        if self.get(x, y) != player_num:
                            break
                        x += d[0]
                        y += d[1]
                        count += 1
                    # if 5 in a line, return winner
                    if count == 5:
                        return player_num
        return 0
