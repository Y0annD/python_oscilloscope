# -*- coding: utf-8 -*-
from Tkinter import Tk, Canvas

class Lissajou(Canvas):
    """
    Ecran de visualisation : Lissajou
   """
    def __init__(self, parent=None, width=200, height=200, background="pink"):
        """
        Initialisation
        parent : le parent dans l'application
        background : fond d'ecran
        """

        self.width = width
        self.height = height
        
        Canvas.__init__(self, width=self.width, height=self.height, background=background)
        self.parent = parent

        # Signal X-Y
        self.signal_XY = None
        self.signal_XY_liste = []
        self.color_XY = "green"
        self.signal_XY_allowed = 0;

    def draw_lissajou(self, signal_X_liste=None, signal_Y_liste=None):
        """
        Affichage de signal
        signal : liste des couples (temps,elongation) ou (elongation X, elongation Y)
        """
        plot = []
        if self.signal_XY_allowed and signal_X_liste and signal_Y_liste:
            if self.signal_XY > -1:
                self.delete(self.signal_XY)
                self.signal_XY_liste = []
            for i in range(0, len(signal_X_liste)):
                self.signal_XY_liste.append((signal_X_liste[i][1], signal_Y_liste[i][1]))
            plot = [(x*self.width + self.width/2, y*self.height + self.height/2) for (x, y) in self.signal_XY_liste]
            self.signal_XY = self.create_line(plot, fill=self.color_XY, smooth=1, width=3)
        return plot

if __name__ == "__main__":
    root = Tk()
    lissajou = Lissajou(root)
    lissajou.pack()
    root.mainloop()