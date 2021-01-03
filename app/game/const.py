"""
    The following lists are the possible patterns
    of pieces and their respective scores.
    Values are formatted as:
        {player}_{length} where:
            player = 1 or 2,
            length = 5 or 6
        -> This is a combination of pieces

        score_{length} where:
            length = 5 || 6
        -> This is the score to be assigned for respective pattern
"""
ONE_6 = [
    [0, 1, 1, 1, 1, 1],  # five
    [1, 1, 1, 1, 1, 0],  # five
    [0, 1, 1, 1, 1, 0],  # straight four
    [0, 1, 0, 1, 1, 1],  # four
    [1, 1, 1, 0, 1, 0],  # four
    [0, 1, 1, 0, 1, 1],  # four
    [1, 1, 0, 1, 1, 0],  # four
    [0, 1, 1, 1, 0, 1],  # four
    [1, 0, 1, 1, 1, 0],  # four
    [0, 1, 1, 1, 0, 0],  # straight three
    [0, 0, 1, 1, 1, 0],  # straight three
    [0, 1, 0, 1, 1, 0],  # straight three
    [0, 1, 1, 0, 1, 0],  # straight three
    [2, 1, 1, 1, 0, 0],  # three
    [0, 0, 1, 1, 1, 2],  # three
    [2, 1, 1, 0, 1, 0],  # three
    [0, 1, 0, 1, 1, 2],  # three
    [0, 1, 1, 0, 1, 2],  # three
    [2, 1, 0, 1, 1, 0],  # three
    [0, 0, 1, 1, 0, 0],  # straight two
    [0, 1, 0, 0, 1, 0],  # straight two
    [0, 0, 0, 1, 1, 2],  # two
    [2, 1, 1, 0, 0, 0],  # two
    [0, 0, 1, 0, 1, 2],  # two
    [2, 1, 0, 1, 0, 0],  # two
    [0, 1, 0, 0, 1, 2],  # two
    [2, 1, 0, 0, 1, 0],  # two
    [0, 0, 1, 0, 0, 0],  # free one
    [0, 0, 0, 1, 0, 0],  # free one
    [2, 1, 1, 1, 1, 2],  # Deadfour
]

ONE_5 = [
    [1, 1, 1, 1, 1],   # win
    [1, 1, 1, 1, 0],  # four
    [0, 1, 1, 1, 1],  # four
    [0, 1, 1, 1, 0],  # straight three
    [1, 0, 0, 1, 1],  # three
    [1, 1, 0, 0, 1],  # three
    [1, 0, 1, 0, 1],  # three
    [0, 1, 0, 1, 0],   # two
    [1, 0, 0, 0, 1],  # two
    [2, 1, 1, 1, 2],  # deadthree
    [2, 1, 1, 2, 0],  # deadtwo
    [0, 2, 1, 1, 2],  # deadtwo
]

TWO_6 = [
    [0, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 0],  # straight four
    [0, 2, 0, 2, 2, 2],  # four
    [2, 2, 2, 0, 2, 0],  # four
    [0, 2, 2, 0, 2, 2],  # four
    [2, 2, 0, 2, 2, 0],  # four
    [0, 2, 2, 2, 0, 2],  # four
    [2, 0, 2, 2, 2, 0],  # four
    [0, 1, 1, 1, 0, 0],  # straight three
    [0, 0, 1, 1, 1, 0],  # straight three
    [0, 2, 0, 2, 2, 0],  # straight three
    [0, 2, 2, 0, 2, 0],  # straight three
    [1, 2, 2, 2, 0, 0],  # three
    [0, 0, 2, 2, 2, 1],  # three
    [1, 2, 2, 0, 2, 0],  # three
    [0, 2, 0, 2, 2, 1],  # three
    [0, 2, 2, 0, 2, 1],  # three
    [1, 2, 0, 2, 2, 0],  # three
    [0, 0, 2, 2, 0, 0],  # straight two
    [0, 2, 0, 0, 2, 0],  # straight two
    [0, 0, 0, 2, 2, 1],
    [1, 2, 2, 0, 0, 0],
    [0, 0, 2, 0, 2, 1],
    [1, 2, 0, 2, 0, 0],
    [0, 2, 0, 0, 2, 1],
    [1, 2, 0, 0, 2, 0],
    [0, 0, 2, 0, 0, 0],  # free one
    [0, 0, 0, 2, 0, 0],  # free one
    [1, 2, 2, 2, 2, 1],  # Deadfour
]
TWO_5 = [
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2],
    [0, 2, 2, 2, 0],
    [2, 0, 0, 2, 2],  # three
    [2, 2, 0, 0, 2],  # three
    [2, 0, 2, 0, 2],  # three
    [0, 2, 0, 2, 0],   # two
    [2, 0, 0, 0, 2],  # two
    [1, 2, 2, 2, 1],  # deadthree
    [1, 2, 2, 1, 0],  # deadtwo
    [0, 1, 2, 2, 1],  # deadtwo
]

SCORE_6 = [
    100000000,
    10000000,
    10000000,
    500000,
    500000,
    500000,
    500000,
    500000,
    500000,
    100000,
    100000,
    100000,
    100000,
    500,
    500,
    500,
    500,
    500,
    500,
    50,
    50,
    5,
    5,
    5,
    5,
    5,
    5,
    1,
    1,
    0
]

SCORE_5 = [
    10000000,
    10000,
    10000,
    100000,
    500,
    500,
    500,
    5,
    5,
    0,
    0,
    0
]
