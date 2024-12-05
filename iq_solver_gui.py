import tkinter as tk
from tkinter import ttk
import time
from typing import Optional
from base import Plateau, IqSolverBase
from iq_solver_2d import IqSolver2d, BOARD_WIDTH, BOARD_HEIGHT, placer_pieces_niveau
from pieces import EMPTY, Piece_MARKER, PieceColor

class IqSolverGUI(IqSolver2d):
    def __init__(self, canvas: tk.Canvas):
        super().__init__(afficher_tous_les_plateaux=True)
        self.canvas = canvas
        self.cell_size = 40
        self.margin = 20
        
    def afficher_plateau(self, plateau: Plateau | None = None, sans_doublons: bool = False):
        # Afficher aussi dans le terminal
        # super().afficher_plateau(plateau, sans_doublons)
        
        est_solution = plateau is not None and self._plateau_to_str(plateau) in self.plateaux_trouves
        
        # Affichage graphique
        if plateau is None:
            plateau = self.plateau
            
        self.canvas.delete("all")
        
        # Dessiner le plateau
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = plateau[0][y][x]
                fill_color = self._get_color(color)
                
                x1 = self.margin + x * self.cell_size
                y1 = self.margin + y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")
                
                # Ajouter le marqueur de la pièce
                if color != EMPTY:
                    self.canvas.create_text(
                        x1 + self.cell_size/2,
                        y1 + self.cell_size/2,
                        text=Piece_MARKER[color][1],
                        fill="black"
                    )
        
        # Forcer la mise à jour de l'interface
        self.canvas.update()
        
        time.sleep(0.1)  # Délai pour toutes les étapes
        
    def _get_color(self, piece_color: PieceColor) -> str:
        # Conversion des couleurs du terminal vers des couleurs Tkinter
        color_mapping = {
            "green": "#00B58F",
            "pink": "#FF34B4",
            "yellow": "#FFBA00",
            "violet": "#4A1951",
            "lightred": "#FF002B",
            "red": "#D50020",
            "orange": "#FF6A24",
            "blue": "#002088",
            "lightblue": "#009FDC",
            "cyan": "#00D9E9",
            "lightgreen": "#B9BD00",
            "lime": "#00EAAA",
            EMPTY: "#FFFFFF"
        }
        return color_mapping.get(piece_color, "#FFFFFF")

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IQ Solver")
        
        # Configuration du style
        style = ttk.Style()
        style.configure("Custom.TButton", padding=10, font=('Helvetica', 12))
        
        # Frame principale avec padding et fond blanc
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style="Custom.TFrame")
        
        # Titre
        title_label = ttk.Label(main_frame, text="IQ Solver", font=('Helvetica', 24, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Frame pour la sélection de difficulté
        difficulty_frame = ttk.Frame(main_frame)
        difficulty_frame.grid(row=1, column=0, pady=(0, 20))
        
        # Label de difficulté avec style
        ttk.Label(difficulty_frame, 
                 text="Sélectionnez la difficulté:", 
                 font=('Helvetica', 12)).grid(row=0, column=0, pady=(0, 10))
        
        # Combobox pour la difficulté
        self.difficulty = tk.StringVar(value="Starter1")
        difficulties = ["Starter1", "Starter2", "Junior1", "Junior2", 
                       "Expert1", "Expert2", "Master1", "Master2"]
        difficulty_menu = ttk.Combobox(difficulty_frame, 
                                     textvariable=self.difficulty,
                                     values=difficulties,
                                     state="readonly",
                                     width=30,
                                     font=('Helvetica', 10))
        difficulty_menu.grid(row=1, column=0, pady=(0, 20))
        
        # Bouton Play avec style
        play_button = ttk.Button(difficulty_frame, 
                               text="▶ Play", 
                               command=self.start_solving,
                               style="Custom.TButton")
        play_button.grid(row=2, column=0)
        
        # Canvas plateau
        canvas_width = BOARD_WIDTH * 40 + 40
        canvas_height = BOARD_HEIGHT * 40 + 40
        self.canvas = tk.Canvas(main_frame, 
                              width=canvas_width,
                              height=canvas_height,
                              background="white")
        
        self.solver: Optional[IqSolverGUI] = None
        
    def start_solving(self):
        self.canvas.grid(row=2, column=0, pady=20)
        self.solver = IqSolverGUI(self.canvas)
        game = self.difficulty.get()
        
        placer_pieces_niveau(self.solver, game)
        
        self.solver.resoudre()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()