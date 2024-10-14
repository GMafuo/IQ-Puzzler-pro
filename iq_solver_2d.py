from typing import Tuple
from base import Plateau, Direction, IqSolverBase, DirectionOrientation, DirectionRotation

from pieces import EMPTY, StoneColor
import time
    

BOARD_WIDTH = 11
BOARD_HEIGHT = 5


class IqSolver2d(IqSolverBase):
    def _init_board(self) -> Plateau:
        return [
            [
                [EMPTY for _ in range(BOARD_WIDTH)]
                for _ in range(BOARD_HEIGHT)
            ]
        ]

    def _initialiser_directions(self) -> Tuple[Direction, ...]:
        return tuple(
            (0, orientation, rotation) 
            for orientation in (0, 1, 2, 3)
            for rotation in (1, -1)
        )

def choisir_difficulte():
    options = {
        "1": "Starter1",
        "2": "Starter2",
        "3": "Junior1",
        "4": "Junior2",
        "5": "Expert1",
        "6": "Expert2",
        "7": "Master1",
        "8": "Master2"
    }
    print("Choisissez la difficulté :")
    for key, value in options.items():
        print(f"{key} : {value}")
    
    choix = input("Entrez le numéro de votre choix : ")
    return options.get(choix, "Starter1")  

GAME = choisir_difficulte()
TEST = False

solver = IqSolver2d(
    file_name_text=f"{__file__}.{GAME}.solution.txt"
)


def placer_pierre(color: StoneColor, direction: tuple[DirectionOrientation, DirectionRotation], depart: tuple[int, int]):
    solver.placer_pierre(color, (0, *direction), depart=(*depart, 0))


if GAME == "Starter1":  
    placer_pierre("green", (0, 1), (1, 0))
    placer_pierre("red", (2, -1), (4, 0))
    placer_pierre("lime", (3, 1), (9, 1))
    placer_pierre("lightblue", (2, 1), (2, 4))
    placer_pierre("violet", (1, 1), (0, 0))
    placer_pierre("lightgreen", (0, -1), (5, 1))
    placer_pierre("pink", (2, 1), (6, 3))
    placer_pierre("cyan", (0, 1), (5, 2))
    placer_pierre("lightred", (3, 1), (1,3))
elif GAME == "Starter2":  
    placer_pierre("lightblue", (3, 1), (0, 2))
    placer_pierre("red", (2, 1), (4, 2))
    placer_pierre("violet", (3, 1), (6, 2))
    placer_pierre("yellow", (2, -1), (9, 0))
    placer_pierre("blue", (2, -1), (10, 0))
    placer_pierre("lightgreen", (1, -1), (9, 2))
    placer_pierre("cyan", (2, 1), (8, 2))
    placer_pierre("pink", (2, 1), (9, 3))
    placer_pierre("green", (3, 1), (5, 4))
elif GAME == "Junior1":
    placer_pierre("yellow", (2, -1), (3, 0))
    placer_pierre("pink", (2, 1), (5, 0))
    placer_pierre("lime", (1, -1), (6, 0))
    placer_pierre("violet", (2, -1), (2, 3))
    placer_pierre("cyan", (1, 1), (0, 3))
    placer_pierre("lightred", (3, 1), (2,4))
    placer_pierre("red", (1, -1), (2, 2))
    placer_pierre("lightblue", (0, 1), (4, 2))
elif GAME == "Junior2":
    placer_pierre("yellow", (0, 1), (0, 0))
    placer_pierre("violet", (3, -1), (3, 2))
    placer_pierre("lightblue", (2, 1), (2, 4))
    placer_pierre("blue", (1, -1), (0, 1))
    placer_pierre("red", (2, 1), (3, 4))
    placer_pierre("lightgreen", (3, -1), (4, 4))
    placer_pierre("cyan", (0, 1), (5, 1))
    placer_pierre("orange", (2, 1), (7, 4))
elif GAME == "Expert1" :
    placer_pierre("yellow", (0, 1), (0, 0))
    placer_pierre("cyan", (2, 1), (1, 1))
    placer_pierre("lightgreen", (2, -1), (2, 3))
    placer_pierre("blue", (0, -1), (1, 3))
    placer_pierre("green", (1, 1), (4, 0))
    placer_pierre("lime", (1, 1), (4, 3))
elif GAME == "Expert2" : 
    placer_pierre("cyan", (3, 1), (3, 1))
    placer_pierre("violet", (3, -1), (5, 2))
    placer_pierre("pink", (0, 1), (7, 1))
    placer_pierre("orange", (2, -1), (10, 1))
    placer_pierre("blue", (3, 1), (9, 4))
    placer_pierre("lightred", (0, -1), (4,3))
elif GAME == "Master1" :
    placer_pierre("cyan", (3, 1), (10, 1))
    placer_pierre("lime", (3, -1), (7, 1))
    placer_pierre("green", (0, 1), (5, 2))
elif GAME == "Master2" : 
    placer_pierre("cyan", (3, 1), (7, 1))
    placer_pierre("red", (3, 1), (5, 3))
    placer_pierre("blue", (2, 1), (10, 1))

if TEST:
    solver.print_board(no_dups=False)
else:
    solver.charger_plateau()
    solver.resoudre()
    solver.print_solutions()
    solver.afficher_plateau()
   

