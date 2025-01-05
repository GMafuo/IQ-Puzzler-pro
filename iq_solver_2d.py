from typing import Tuple
from base import Plateau, Direction, IqSolverBase, DirectionOrientation, DirectionRotation

from pieces import EMPTY, PieceColor
import time
import os
    
BOARD_WIDTH = 11
BOARD_HEIGHT = 5

class IqSolver2d(IqSolverBase):
    
    def _init_board(self) -> Plateau:
        """Initialise un plateau vide aux dimensions standard"""
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

def choisir_interface():
    print("Choisissez l'interface :")
    print("1 : Terminal")
    print("2 : Interface graphique")
    
    while True:
        choix = input("Entrez votre choix (1 ou 2) : ")
        if choix == "1":
            return "terminal"
        elif choix == "2":
            return "gui"
        print("Choix invalide. Veuillez entrer 1 ou 2.")

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

def placer_pieces_niveau(solver: IqSolverBase, game: str):
    def placer_piece(color: PieceColor, direction: tuple[DirectionOrientation, DirectionRotation], depart: tuple[int, int]):
        solver.placer_piece(color, (0, *direction), depart=(*depart, 0))
            
    if game == "Starter1":  
        placer_piece("green", (0, 1), (1, 0))
        placer_piece("red", (2, -1), (4, 0))
        placer_piece("lime", (3, 1), (9, 1))
        placer_piece("lightblue", (2, 1), (2, 4))
        placer_piece("violet", (1, 1), (0, 0))
        placer_piece("lightgreen", (0, -1), (5, 1))
        placer_piece("pink", (2, 1), (6, 3))
        placer_piece("cyan", (0, 1), (5, 2))
        placer_piece("lightred", (3, 1), (1,3))
    elif game == "Starter2":  
        placer_piece("lightblue", (3, 1), (0, 2))
        placer_piece("red", (2, 1), (4, 2))
        placer_piece("violet", (3, 1), (6, 2))
        placer_piece("yellow", (2, -1), (9, 0))
        placer_piece("blue", (2, -1), (10, 0))
        placer_piece("lightgreen", (1, -1), (9, 2))
        placer_piece("cyan", (2, 1), (8, 2))
        placer_piece("pink", (2, 1), (9, 3))
        placer_piece("green", (3, 1), (5, 4))
    elif game == "Junior1":
        placer_piece("yellow", (2, -1), (3, 0))
        placer_piece("pink", (2, 1), (5, 0))
        placer_piece("lime", (1, -1), (6, 0))
        placer_piece("violet", (2, -1), (2, 3))
        placer_piece("cyan", (1, 1), (0, 3))
        placer_piece("lightred", (3, 1), (2,4))
        placer_piece("red", (1, -1), (2, 2))
        placer_piece("lightblue", (0, 1), (4, 2))
    elif game == "Junior2":
        placer_piece("yellow", (0, 1), (0, 0))
        placer_piece("violet", (3, -1), (3, 2))
        placer_piece("lightblue", (2, 1), (2, 4))
        placer_piece("blue", (1, -1), (0, 1))
        placer_piece("red", (2, 1), (3, 4))
        placer_piece("lightgreen", (3, -1), (4, 4))
        placer_piece("cyan", (0, 1), (5, 1))
        placer_piece("orange", (2, 1), (7, 4))
    elif game == "Expert1" :
        placer_piece("yellow", (0, 1), (0, 0))
        placer_piece("cyan", (2, 1), (1, 1))
        placer_piece("lightgreen", (2, -1), (2, 3))
        placer_piece("blue", (0, -1), (1, 3))
        placer_piece("green", (1, 1), (4, 0))
        placer_piece("lime", (1, 1), (4, 3))
    elif game == "Expert2" : 
        placer_piece("cyan", (3, 1), (3, 1))
        placer_piece("violet", (3, -1), (5, 2))
        placer_piece("pink", (0, 1), (7, 1))
        placer_piece("orange", (2, -1), (10, 1))
        placer_piece("blue", (3, 1), (9, 4))
        placer_piece("lightred", (0, -1), (4,3))
    elif game == "Master1" :
        placer_piece("cyan", (3, 1), (10, 1))
        placer_piece("lime", (3, -1), (7, 1))
        placer_piece("green", (0, 1), (5, 2))
    elif game == "Master2" : 
        placer_piece("cyan", (3, 1), (7, 1))
        placer_piece("red", (3, 1), (5, 3))
        placer_piece("blue", (2, 1), (10, 1))

if __name__ == "__main__":
    interface = choisir_interface()
    
    if interface == "gui":
        from iq_solver_gui import Application
        app = Application()
        app.run()
    else:
        GAME = choisir_difficulte()
        TEST = False
        
        solution_file = f"{__file__}.{GAME}.solution.txt"
        
        if os.path.exists(solution_file):
            os.remove(solution_file)

        solver = IqSolver2d(
            file_name_text=solution_file
        )

        placer_pieces_niveau(solver, GAME)

        if TEST:
            solver.print_board(no_dups=False)
        else:
            solver.afficher_plateau()
            solver.charger_plateau()
            solver.resoudre()
            

