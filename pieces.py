from colorama import Fore, Back, Style

COULEURS = {
    'vert': Fore.GREEN,
    'lime': Fore.LIGHTGREEN_EX,
    'rose': Fore.MAGENTA,
    'jaune': Fore.YELLOW,
    'bleu_clair': Fore.LIGHTBLUE_EX,
    'bleu': Fore.BLUE,
    'rouge_clair': Fore.LIGHTRED_EX,
    'rouge': Fore.RED,
    'orange': Fore.YELLOW + Back.RED,
    'violet': Fore.MAGENTA + Back.BLUE,
    'cyan': Fore.CYAN
}

PIECES = {
    'vert': [(0,0), (1,0), (2,0), (2,1)],
    'lime': [(0,0), (1,0), (1,1), (2,1)],
    'rose': [(0,0), (1,0), (2,0), (1,1)],
    'jaune': [(0,0), (1,0), (0,1), (1,1)],
    'bleu_clair': [(0,0), (1,0), (2,0), (3,0)],
    'bleu': [(0,0), (0,1), (1,1), (2,1)],
    'rouge_clair': [(0,0), (1,0), (2,0), (2,1), (2,2)],
    'rouge': [(0,0), (1,0), (1,1), (2,1)],
    'orange': [(0,0), (1,0), (1,1)],
    'violet': [(0,0), (1,0), (1,1)],
    'cyan': [(0,0), (1,0)]
}

MARQUEURS = {couleur: couleur[0].upper() for couleur in COULEURS}

def afficher_piece(couleur):
    forme = PIECES[couleur]
    max_x = max(x for x, y in forme)
    max_y = max(y for x, y in forme)
    
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in forme:
                print(COULEURS[couleur] + '■' + Style.RESET_ALL, end='')
            else:
                print(' ', end='')
        print()

if __name__ == "__main__":
    for couleur in PIECES:
        print(f"Pièce {couleur}:")
        afficher_piece(couleur)
        print()
