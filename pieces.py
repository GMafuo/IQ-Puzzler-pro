from typing import Literal, Tuple

from termcolor import colored


PieceShape = Tuple[tuple[int, int], ...]

PieceColor = Literal[
    "green", "pink", "yellow", "violet", "lightred",
    "red", "orange", "blue", "lightblue",
    "cyan", "lightgreen", "lime", "empty"
]

EMPTY:PieceColor = "empty"

PieceS: dict[PieceColor, PieceShape] = {
    "green": ((0, 0), (1, 0), (1, 1), (2, 0)),
    "pink": ((0,0), (1,0),(1,-1), (2,-1), (3,-1)),
    "yellow": ((0, 0), (1, 0), (2, 0), (2, 1), (3, 0)),
    "violet": ((0, 0), (1, 0), (1, -1), (2, -1), (2, -2)),
    "lightred": ((0, 0), (0, 1), (0, 2), (0, 3), (1, 3)),
    "red": ((0, 0), (0, 1), (1, 1), (1, 2)),
    "orange": ((0, 0), (1, 0), (1, 1), (2, 1), (1, 2)),
    "blue": ((0, 0), (0, 1), (1, 1), (2, 1)),
    "lightblue": ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    "cyan": ((0, 0), (1, 0), (1, -1)),
    "lightgreen": ((0, 0), (0, 1), (1, 1), (2, 1), (2, 0)),
    "lime": ((0, 0), (0, 1), (1, -1), (1, 0), (1, 1)),
}

Piece_SIZES: dict[PieceColor, int] = {
    color: len(PieceS[color]) for color in PieceS
}

symbol = "🟔"

def color(color: str, marker: str):
    return (colored(text=marker, color=color, force_color=True), marker)

Piece_MARKER: dict[PieceColor, tuple[str, str]] = {
    "green": color(color='green', marker='G'),
    "pink": color(color="light_magenta", marker='p'),
    "yellow": color(color="yellow", marker='y'),
    "violet": color(color="magenta", marker='v'),
    "lightred": color(color="light_red", marker='r'),
    "red": color(color="red", marker='R'),
    "orange": color(color="light_yellow", marker='o'),
    "blue": color(color="blue", marker='B'),
    "lightblue": color(color="light_blue", marker='b'),
    "cyan": color(color="cyan", marker='c'),
    "lightgreen": color(color="light_green", marker='g'),
    "lime": color(color="light_cyan", marker='l'),
    EMPTY: ('·', '·'),
}

