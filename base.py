import os
import re
from typing import Callable, Literal, Tuple, List
from copy import deepcopy

from pieces import EMPTY, Piece_MARKER, Piece_SIZES, PieceS, PieceColor, PieceShape

Coord = tuple[int, int, int]  # Coordonnées (x, y, z)
Plateau = list[list[list[PieceColor]]]  # Structure du plateau de jeu

DirectionLevel = Literal[-1, 0, 1]  # Niveau vertical
DirectionOrientation = Literal[0, 1, 2, 3]  # Orientation horizontale (0-3)
DirectionRotation = Literal[1, -1]  # Sens de rotation
Direction = tuple[DirectionLevel, DirectionOrientation, DirectionRotation]


class IqSolverBase:
    """Classe de base pour résoudre le puzzle IQ.
    Implémente les fonctionnalités principales de manipulation du plateau et des pièces."""
    
    def __init__(
            self,
            file_name_text: str | None = None,
            afficher_tous_les_plateaux: bool = True,
    ) -> None:
        super().__init__()
        self.file_name_text = file_name_text
        self.afficher_tous_les_plateaux = afficher_tous_les_plateaux
        self.plateau = self._init_board()
        self.toutes_les_directions: Tuple[Direction, ...] = self._initialiser_directions(
        )
        self.plateaux_trouves: set[str] = set()
        self._initialiser_directions_piece()
        self.dernier_plateau: str | None = None
        self.solution_trouvee = False

    def _cloner_plateau(self, plateau: Plateau) -> Plateau:
         return deepcopy(plateau)

    def _initialiser_directions_piece(self):
        """Initialise toutes les rotations possibles pour chaque pièce.
        Stocke les résultats dans:
        - self.rotations_piece : formes possibles pour chaque pièce
        - self.directions_piece : directions correspondantes"""
        self.rotations_piece: dict[PieceColor, Tuple[Tuple[Coord, ...], ...]] = {}
        self.directions_piece: dict[PieceColor, Tuple[Direction, ...]] = {}
        for couleur, piece in PieceS.items():
            formes_normalisees: set[str] = set()
            formes: list[Tuple[Coord, ...]] = []
            directions: list[Direction] = []
            for direction in self.toutes_les_directions:
                forme = self.rotate_piece(piece=piece, direction=direction)
                mins = tuple(min(p[i] for p in forme) for i in range(len(forme[0])))
                forme_normalisee = ','.join(sorted(':'.join(str(c - m)for c, m in zip(p, mins))for p in forme))
                if forme_normalisee not in formes_normalisees:
                    formes.append(forme)
                    directions.append(direction)
                    formes_normalisees.add(forme_normalisee)

            self.rotations_piece[couleur] = tuple(formes)
            self.directions_piece[couleur] = tuple(directions)

    def _plateau_to_str(self, plateau: Plateau, index_marqueur: Literal[0, 1] = 0):
        lines: List[List[str]] = [[] for _ in plateau[0]]

        def _map(couleur: PieceColor):
            return Piece_MARKER[couleur][index_marqueur]

        for niveau in plateau:
            for y, ligne in enumerate(niveau):
                lines[y].append(' '.join(_map(c) for c in ligne))

        return '\n'.join('  '.join(ligne) for ligne in lines)

    def sauvegarder_plateau(self, plateau: Plateau):
        plateau_str = self._plateau_to_str(plateau)
        self.plateaux_trouves.add(plateau_str)
        # return
        if self.file_name_text is not None:
            with open(self.file_name_text, mode="a", encoding='utf-8') as file:
                file.write(
                    f"{self._plateau_to_str(plateau=plateau, index_marqueur=1)}\n\n")

    def charger_plateau(self):
        if self.file_name_text is not None and os.path.isfile(self.file_name_text):
            with open(self.file_name_text, "r", encoding='utf-8') as file:
                derniers_plateaux = [plateau for plateau in file.read().split('\n\n') if plateau]
                if derniers_plateaux:
                    self.dernier_plateau = derniers_plateaux[-1]

    def afficher_plateau(self, plateau: Plateau | None = None, sans_doublons: bool = False):
        if plateau is None:
            plateau = self.plateau
        plateau_str = self._plateau_to_str(plateau)
        if sans_doublons and plateau_str in self.plateaux_trouves:
            return None

        print(plateau_str)
        print()

    def transformer(self, p: tuple[int, int], direction: Direction) -> Coord:
        """Applique une transformation (rotation/translation) à un point.
        Args:
            p: Point à transformer
            direction: Direction de transformation
        Returns:
            Nouvelles coordonnées du point"""
        niveau, orientation, rotation = direction

        dx: Coord
        dy: Coord
        if niveau == 1:
            dx = ((0 if orientation in {0, 1} else -1), (0 if orientation in {0, 3} else -1))
            dy = (rotation * (-dx[0] - 1), rotation * (-dx[1] - 1))
        elif niveau == 0:
            dx = ((1 if orientation == 0 else -1 if orientation == 2 else 0), (1 if orientation == 1 else -1 if orientation == 3 else 0))
            dy = (-dx[1] * rotation, dx[0] * rotation)
        else:
            dx = ((1 if orientation in {0, 1} else 0), (1 if orientation in {0, 3} else 0))
            dy = (rotation * (dx[0] - 1), rotation * (dx[1] - 1))

        return (p[0] * dx[0] + p[1] * dy[0], p[0] * dx[1] + p[1] * dy[1])

    def appliquer_piece(self, piece: Tuple[Coord, ...], fn: Callable[[Coord], Coord]) -> Tuple[Coord, ...]:
        return tuple(fn(p) for p in piece)

    def rotate_piece(self, piece: PieceShape, direction: Direction) -> Tuple[Tuple[int, int], ...]: 
        return tuple(self.transformer(p, direction) for p in piece)

    def verifier_coordonnees(self, plateau: Plateau, x: int, y: int) -> bool:  
         return 0 <= y < len(plateau[0]) and 0 <= x < len(plateau[0][y])

    def _placer_piece(self, plateau: Plateau, couleur_piece: PieceColor, forme: Tuple[Coord, ...], depart: Coord) -> Plateau | None:
        forme = self.appliquer_piece(piece=forme, fn=lambda p: (p[0] + depart[0], p[1] + depart[1]))
        plateau = self._cloner_plateau(plateau)

        for (x, y) in forme: 
            if not self.verifier_coordonnees(plateau, x, y) or plateau[0][y][x] != EMPTY:  
                return None

            plateau[0][y][x] = couleur_piece

        return plateau

    def tester_plateau(self, plateau: Plateau, couleurs_restantes: list[PieceColor]) -> bool:
        """Vérifie si le plateau actuel permet encore de placer les pièces restantes."""
        verifie: set[Coord] = set()

        taille_max = max(Piece_SIZES[couleur] for couleur in couleurs_restantes)
        taille_min = min(Piece_SIZES[couleur] for couleur in couleurs_restantes)

        def test_xy(x: int, y: int) -> int:  
            if (x, y) in verifie:
                return 0

            if not self.verifier_coordonnees(plateau, x, y):  
                return 0

            if plateau[0][y][x] != EMPTY:
                return 0

            verifie.add((x, y))
            resultat = 1
            for dx, dy in ((0, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, -1), (1, 1)):
                resultat += test_xy(x + dx, y + dy)
            return resultat

        tailles: set[int] = set()
        for y, ligne in enumerate(plateau[0]): 
            for x in range(len(ligne)):
                if (x, y) in verifie:
                    continue
                t = test_xy(x, y)
                if t > 0:
                    if t < taille_min:
                        return False

                    tailles.add(t)

        return taille_max <= max(tailles)

    def _nettoyer_dernier_plateau(self, plateau: str | None, couleur: PieceColor) -> str | None:
        if plateau is None:
            return None
        marqueur = Piece_MARKER[couleur][1]
        vide = Piece_MARKER[EMPTY][1]
        return re.sub(r'[^' + vide + marqueur + r'\n ]', vide, plateau)

    def placer_prochaine_piece(self, plateau: Plateau, couleurs: List[PieceColor]):
        def essayer_placer_forme(couleur, forme, x, y, z):
            prochain_plateau = self._placer_piece(plateau=plateau, couleur_piece=couleur, forme=forme, depart=(x, y, z))
            if prochain_plateau is None:
                return False
            if dernier_plateau_nettoye is not None:
                prochain_plateau_str = self._nettoyer_dernier_plateau(self._plateau_to_str(prochain_plateau, index_marqueur=1), couleur)
                if prochain_plateau_str == dernier_plateau_nettoye:
                    return False
            if self.afficher_tous_les_plateaux:
                self.afficher_plateau(prochain_plateau)
            if derniere_piece:
                self.sauvegarder_plateau(prochain_plateau)
                if EMPTY not in [case for ligne in prochain_plateau[0] for case in ligne]:
                    self.solution_trouvee = True
                    return True
            elif self.tester_plateau(prochain_plateau, couleurs):
                self.placer_prochaine_piece(prochain_plateau, couleurs)
                if hasattr(self, 'solution_trouvee') and self.solution_trouvee:
                    return True
            return True

        couleur = couleurs[0]
        couleurs = couleurs[1:]
        derniere_piece = len(couleurs) == 0
        dernier_plateau_nettoye = self._nettoyer_dernier_plateau(self.dernier_plateau, couleur)

        for z, niveau in enumerate(plateau):
            for y, ligne in enumerate(niveau):
                for x in range(len(ligne)):
                    for forme in self.rotations_piece[couleur]:
                        if essayer_placer_forme(couleur, forme, x, y, z):
                            if hasattr(self, 'solution_trouvee') and self.solution_trouvee:
                                return

    def placer_piece(self, couleur: PieceColor, direction: Direction, depart: Coord):
        forme = self.rotate_piece(piece=PieceS[couleur], direction=direction)
        prochain_plateau = self._placer_piece(self.plateau, couleur, forme, depart)
        if prochain_plateau is not None:
            self.plateau = prochain_plateau
        return prochain_plateau

    def resoudre(self):
        couleurs_utilisees = set(
            couleur
            for niveau in self.plateau
            for ligne in niveau
            for couleur in ligne
        )

        self.placer_prochaine_piece(plateau=self.plateau, couleurs=[c for c in PieceS if c not in couleurs_utilisees])
        
    def print_solutions(self):
        for b in self.plateaux_trouves:
            print(b)
            print()

    def afficher_solutions(self, file_name: str):
        with open(file_name, mode="w", encoding='utf-8') as file:
            file.write("\n".join(f"{b}\n" for b in self.plateaux_trouves))

    def afficher_directions_test_piece(self, couleur: PieceColor, depart: Coord):
        for direction in self.directions_piece[couleur]:
            prochain_plateau = self.placer_piece(couleur, direction, depart)
            if prochain_plateau is not None:
                print(direction)
                self.afficher_plateau(prochain_plateau)

   