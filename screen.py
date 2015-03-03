# -*- coding: utf-8 -*-
from Tkinter import Tk, Canvas
import math

class Screen(Canvas):
    """
    Ecran de visualisation : grille + signaux

   """
    def __init__(self, parent=None, width=800, height=800, background="white"):
        """
        Initialisation

        parent : le parent dans l'application
        width,height : dimension de l'ecran
        background : fond d'ecran

        signal_X, ... : identifiants des signaux 
        color_X, ... : couleur d'affichage des siganux
        """
        Canvas.__init__(self)
        self.parent = parent

        self.width = width
        self.height = height

        self.signal_X = None
        self.color_X = "red"
        self.signal_Y = None
        self.color_Y = "green"
        self.signal_XY = None
        self.color_XY = "#ff00ff"

        self.grid = []

        self.configure(bg=background, bd=2, relief="sunken")
        self.bind("<Configure>", self.resize)

    def resize(self, event):
        """
        En cas de reconfiguration de fenetre
        """
        print("Screen.resize()")
        if event:

            self.width = event.width
            self.height = event.height
            # on redessine la grille
            self.draw_grid(self.width/(self.parent.get_time()),self.height/10)

            
    def draw_grid(self, nX=10, nY=10):
        """
        Representation des carreaux de la grille

        nX : pas horizontal
        nY : pas vertical
        """
        print("Screen.draw_grid('%d','%d')" % (nX, nY))

        for i in range(0,len(self.grid)):
            self.delete("X",self.grid[i])
            
        self.grid = []

        # repere
        self.grid.append(self.create_line(10,self.height/2,
                         self.width, self.height/2,
                         arrow="last", fill="blue"))
        self.grid.append(
                         self.create_line(10, self.height - 5,
                         10, 5,
                         arrow="last", fill="blue"))

        # grille
        # calcul du nombre de lignes à afficher
        numberX = (self.width - 10) / nX
        numberY = (self.height - 5) / nY

        # on dessine les lignes
        for i in range(1, numberX + 1):
            line = self.create_line(i*nX,0,i*nX,self.height)
            self.grid.append(line)

        for i in range(1, (numberY + 1)/2):
            self.grid.append(self.create_line(10, (self.height/2)+i*nY,self.width, (self.height/2)+i*nY))
            
            self.grid.append(self.create_line(10, (self.height/2)-i*nY,self.width, (self.height/2)-i*nY))


            
    def plot_signal(self, name, signal=None):
        """
        Affichage de signal

        name : nom du signal ("X","Y","X-Y")
        signal : liste des couples (temps,elongation) ou (elongation X, elongation Y)
        """
        print "Screen.plot_signal()"
        self.draw_grid(self.width/10,self.height/10)
        draw_X = self.parent.control_X.drawVar.get()
        draw_Y = self.parent.control_Y.drawVar.get()

        if signal and len(signal) > 1:
            if name == "X" :
                if draw_X:
                    if self.signal_X > -1:
                        self.delete(self.signal_X)
                    plot = [(x*self.width, y*self.height + self.height/2) for (x, y) in signal]
                    self.signal_X = self.create_line(plot, fill=self.color_X, smooth=1, width=3)
                else:
                    self.delete(self.signal_X)
            if name == "Y":
                if draw_Y:
                    if self.signal_Y > -1:
                        self.delete(self.signal_Y)
                    plot = [(x*self.width, y*self.height + self.height/2) for (x, y) in signal]
                    self.signal_Y = self.create_line(plot, fill=self.color_Y, smooth=1, width=3)
                else:
                    self.delete(self.signal_Y)
            if name == 'XY':
                self.delete(self.signal_XY)
                if self.parent.drawXY.get()==1:
                    plot = [(x*self.width+self.width/2, y*self.height + self.height/2) for (x, y) in signal]
                    self.signal_XY = self.create_line(plot, fill=self.color_XY, smooth=1, width=3)

if __name__ == "__main__":
    root = Tk()
    screen = Screen(root)
    screen.pack()
    root.mainloop()
