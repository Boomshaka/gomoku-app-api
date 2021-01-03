import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

from game.const import (
    ONE_6,
    ONE_5,
    TWO_6,
    TWO_5,
    SCORE_6,
    SCORE_5
)

GRID_SIZE = 15


def generate_start_grid():
    grid = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    grid[7][7] = 2
    return grid


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
        default=generate_start_grid
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
    ghost_grid = generate_start_grid()

    def get(self, row, col):
        """Get value at given row,col position"""
        if row < 0 or col < 0 or row >= GRID_SIZE or col >= GRID_SIZE:
            return 0
        return self.grid[row][col]

    def has_neighbor(self, row, col):
        """
            Check whether a given row,
            col index has any neighboring game piece
        """
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]
        if self.grid[row][col] != 0:
            return False
        for (xdirection, ydirection) in directions:
            if (xdirection != 0 and
                    ((col + xdirection) < 0 or
                     (col + xdirection) >= GRID_SIZE)):
                continue
            if (ydirection != 0 and
                    ((row + ydirection) < 0 or
                     (row + ydirection) >= GRID_SIZE)):
                continue
            if self.grid[row + ydirection][col + xdirection] != 0:
                # print(f"neighbor at [{row}][{col}]")
                return True
        return False

    def find_choices(self):
        """Returns list of moves the AI will consider"""
        choices = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] != 0:
                    continue
                if not self.has_neighbor(i, j):
                    continue
                choices.append((i, j))
        return choices if choices != [] else [(7, 7)]

    def add_new_choices(self, choice, existing_choices):
        """
            Upon making a new move,
            returns a list of additional moves the AI may consider
        """
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]
        additional_choices = []
        if choice is not None:
            for (xdirection, ydirection) in directions:
                if (xdirection != 0 and
                        ((choice[1] + xdirection) < 0 or
                         (choice[1] + xdirection) >= GRID_SIZE)):
                    continue
                if (ydirection != 0 and
                        ((choice[0] + ydirection) < 0 or
                         (choice[0] + ydirection) >= GRID_SIZE)):
                    continue
                if ((self.grid[choice[0] + ydirection]
                    [choice[1] + xdirection] == 0) and
                        (choice[0] + ydirection, choice[1] + xdirection)
                        not in existing_choices):
                    additional_choices.append(
                        (choice[0] + ydirection, choice[1] + xdirection)
                    )
        return additional_choices

    def window(self, iterable, size=5):
        """sliding window to create a set of iterable vectors"""
        i = iter(iterable)
        window = []
        for j in range(0, size):
            window.append(next(i))
        yield window
        for j in i:
            window = window[1:] + [j]
            yield window

    def evaluate_vector(self, vector):
        """
            Calculate the score of a sequence of gamepieces
            Returns: score values for both player 1 and player 2
        """
        score = {'one': 0, 'two': 0}

        # Check through the combinations of 5 pieces,
        # and determine the score of the vector
        if len(vector) == 5:
            for i in range(len(ONE_5)):
                if ONE_5[i] == vector:
                    score['one'] += SCORE_5[i] * 1
                if TWO_5[i] == vector:
                    score['two'] += SCORE_5[i] * 1
            return score

        mygenerator = list(self.window(vector, 5))

        # check through the combinations of 5 consecutive pieces,
        # and determine the score of the vector
        for i in mygenerator:
            for j in range(len(ONE_5)):
                if i == ONE_5[j]:
                    score['one'] += (SCORE_5[j]
                                     * len(mygenerator)
                                     + len(mygenerator))
                if i == TWO_5[j]:
                    score['two'] += (SCORE_5[j]
                                     * len(mygenerator)
                                     + len(mygenerator))

        mygenerator = list(self.window(vector, 6))

        # check through the combinations of 6 consecutive pieces,
        # and determine the score of the vector
        for i in mygenerator:
            for j in range(len(ONE_6)):
                if i == ONE_6[j]:
                    score['one'] += (SCORE_6[j]
                                     * len(mygenerator)
                                     + len(mygenerator))
                if i == TWO_6[j]:
                    score['two'] += (SCORE_6[j]
                                     * len(mygenerator)
                                     + len(mygenerator))

        return score

    def evaluate_board_score(self):
        '''
            Given a boardstate, calculates the boardscore.
            Score is a numerical value to determine
            which player is in an advantageous state.
        '''
        vectors = []
        board_score = 0

        # Look through vertical and horizontal lines
        for i in range(GRID_SIZE):
            vectors.append(self.ghost_grid[i])
        for j in range(0, GRID_SIZE):
            vectors.append(list(
                self.ghost_grid[x][j] for x in range(GRID_SIZE)
            ))

        # Look through the 2 diagonal lines extending from the corner
        vectors.append(list(
            self.ghost_grid[x][x] for x in range(GRID_SIZE)
        ))
        vectors.append(list(
            self.ghost_grid[x][GRID_SIZE - x - 1] for x in range(GRID_SIZE)
        ))

        # Look through the rest of the diagonal
        # lines with length >= 5, if applicable
        if GRID_SIZE >= 6:
            for i in range(1, GRID_SIZE - 4):
                vectors.append(list((
                    self.ghost_grid[row][row - i]
                    for row in range(i, GRID_SIZE)
                )))
                vectors.append(list((
                    self.ghost_grid[col - i][col]
                    for col in range(i, GRID_SIZE)
                )))

            for i in range(4, GRID_SIZE - 1):
                vectors.append(list(
                    self.ghost_grid[i - x][x] for x in range(i, -1, -1)
                ))
                vectors.append(list((
                    self.ghost_grid
                    [GRID_SIZE - 1 - x]
                    [GRID_SIZE - 1 - (i - x)]
                    for x in range(i, -1, -1)
                )))

        for v in vectors:
            score = self.evaluate_vector(v)
            board_score += score['two'] - score['one']
        return board_score

    def minimax(
            self,
            choices,
            depth,
            max_depth,
            alpha,
            beta,
            max_player,
            temp_choice=None,
            store_choice=None):
        """
            Minimax algorithm with depth = 2 and alpha beta pruning
            to search for the ideal move to make.
            Recursively searches a game tree of possible board states,
            and finds the board state that is most advantageous to the AI.
        """

        # Grab list of possible choices to make
        new_choices = choices.copy()
        if max_player == 1:
            next_player = 2
        else:
            next_player = 1
        # Make a move into the ghost grid
        self.make_ghost_move(temp_choice, next_player)

        # Once we reach the bottom of the search tree,
        # determine its board score along with the
        # next choice the AI has to make to reach this score
        if depth == 0:  # or win
            score = self.evaluate_board_score()
            self.remove_ghost_move(temp_choice)
            val = {'choice': store_choice, 'score': score}
            return val

        # Because we made a move in the ghost grid at temp_choice,
        # that block will no longer be available
        if temp_choice is not None:
            new_choices.remove(temp_choice)
        new_choices.extend(self.add_new_choices(temp_choice, new_choices))
        new_choice = None

        # AI wants to maximize the gain
        if max_player == 2:
            maxVal = float("-inf")
            for choice in new_choices:
                # If we're at the top node,
                # save our immediate next move into store_choice
                # so that we can retrieve it when
                # the AI has decided its next move
                if depth == max_depth:
                    store_choice = choice
                # Traverse down a node of the search tree
                val = self.minimax(
                    choices=new_choices,
                    depth=depth - 1,
                    max_depth=max_depth,
                    alpha=alpha,
                    beta=beta,
                    max_player=1,
                    temp_choice=choice,
                    store_choice=store_choice
                )
                self.remove_ghost_move(temp_choice)

                # If we find a new maximum, update its value
                if val['score'] >= maxVal:
                    # print("")
                    # print("NEW MAX VAL", val['score'], maxVal)
                    # print("")
                    # print("larger choice taken between",
                    #       val['score'],
                    #       maxVal
                    # )
                    maxVal = val['score']
                    new_choice = val['choice']
                alpha = max(alpha, val['score'])

                # Alpha beta pruning states that all proceeding choices
                # will be worse than the current best choice we have.
                # Therefore we stop evaluating this branch
                if beta <= alpha:
                    break
            # print(f"Final choice returned: ({new_choice}) score:{maxVal})")
            return {'choice': new_choice, 'score': maxVal}

        # Player wants to minimize the gain
        else:
            minVal = float("inf")
            for choice in new_choices:
                # new_choices.remove(choice)
                # Traverse down a node of the search tree
                val = self.minimax(
                    choices=new_choices,
                    depth=depth - 1,
                    max_depth=max_depth,
                    alpha=alpha,
                    beta=beta,
                    max_player=2,
                    temp_choice=choice,
                    store_choice=store_choice
                )
                if val['score'] <= minVal:
                    # print("smaller choice taken between",
                    #       val['score'],
                    #       minVal
                    # )
                    minVal = val['score']
                    new_choice = val['choice']
                beta = min(beta, val['score'])

                # Alpha beta pruning states that all proceeding choices
                # will be worse than the current best choice we have.
                # Therefore we stop evaluating this branch
                if beta <= alpha:
                    self.remove_ghost_move(temp_choice)
                    break
            self.remove_ghost_move(temp_choice)
            # print(
            #   f"Smallest choice returned:
            #   ({new_choice}) score:{minVal})"
            # )
            return {'choice': new_choice, 'score': minVal}

    def make_ghost_move(self, choice, player_turn):
        """
            Makes a move into the ghost_grid
            Argument for player turn is required unlike make_move,
            because minimax searches with depth = 2
            meaning that ghost grid can represent
            board states up to 2 moves ahead.
        """
        if choice is not None:
            self.ghost_grid[choice[0]][choice[1]] = player_turn

    def remove_ghost_move(self, choice):
        """Erase a filled slot on the ghost grid"""
        if choice is not None:
            self.ghost_grid[choice[0]][choice[1]] = 0

    def choose_AI_move(self):
        """Call onto minimax algorithm to find the optimal move for AI"""
        choices = self.find_choices()
        val = self.minimax(
            choices, depth=2,
            max_depth=2,
            alpha=-1000000000,
            beta=1000000000,
            max_player=2
        )
        return val

    def make_AI_move(self):
        val = self.choose_AI_move()
        row = val.get('choice')[0]
        col = val.get('choice')[1]
        return self.make_move(row, col, player=2)

    def make_move(self, row, col, player=1):
        """Fills grid index specified by row,col"""
        grid = self.grid
        if row < 0 or col < 0 or row >= GRID_SIZE or col >= GRID_SIZE:
            raise IndexError(
                f"Board column and row must be between 0 and {GRID_SIZE}"
            )
        if grid[row][col] != 0:
            raise ValueError("Index already contains a gamepiece")
        grid[row][col] = player
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
