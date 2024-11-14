# IQ-Puzzler Pro Solver

## Description
Ce projet est une implémentation d'un solveur pour le jeu IQ-Puzzler Pro utilisant une approche de résolution de Problème de Satisfaction de Contraintes (PSC). Le programme permet de résoudre différents niveaux de difficulté du jeu, allant du niveau Starter au niveau Master.

## Fonctionnalités
- Résolution automatique des puzzles
- 16 niveaux de difficulté disponibles :
  - Starter 
  - Junior 
  - Expert 
  - Master 
- Visualisation du plateau en mode console avec couleurs
- Sauvegarde des solutions trouvées

## Algorithme
Le solveur utilise une méthode ad-hoc de résolution de PSC avec :
- Backtracking pour l'exploration des solutions
- Forward checking pour l'optimisation
- Pré-calcul des rotations possibles des pièces
- Détection précoce des impasses

## Structure du Projet
- `iq_solver_2d.py` : Classe principale du solveur 2D
- `base.py` : Classes et fonctions de base pour la résolution
- `pieces.py` : Définition des pièces et leurs caractéristiques

## Installation
### Cloner le repository
```bash
git clone git@github.com:GMafuo/IQ-Puzzler-pro.git
```
### Installer les dépendances
```bash
pip install termcolor
```
## Utilisation
```bash
python3 iq_solver_2d.py
```
Suivez les instructions à l'écran pour choisir le niveau de difficulté.

## Format des Pièces
Chaque pièce est définie par ses coordonnées relatives et une couleur :
```bash
PieceS = {
"green": ((0, 0), (1, 0), (1, 1), (2, 0)),
"pink": ((0,0), (1,0),(1,-1), (2,-1), (3,-1)),
# etc...
}
```

## Plateau de Jeu
- Dimensions : 11x5 cases
- Représentation en console avec des marqueurs colorés
- État vide représenté par '·'

## Exemples de Solutions
Les solutions sont sauvegardées dans des fichiers texte au format :
```
iq_solver_2d.py.[NIVEAU].solution.txt
```

## Technologies Utilisées
- Python 3.x
- termcolor pour l'affichage coloré en console

## Auteurs
- Simon Nguyen

- Mathéo Girard

## Remerciements
- Projet réalisé dans le cadre du cours IA41 - Introduction à l'Intelligence Artificielle
- Basé sur le jeu IQ-Puzzler Pro de Smart Games