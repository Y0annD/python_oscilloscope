#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from Tkinter import Tk, Frame

from screen import Screen
from timebase import TimeBase
from generator import Generator
from MenuBar import MenuBar

class Oscilloscope(Frame):
    """ 
    Modele d'Oscilloscope 

    time : valeur de la base de temps
    signal : liste de couples, (temps,elongation) ou (elongation X, elongation Y)  de signaux
    view : visualisation de signaux
    control_X : controle d'un signal
    control_time : controle de la base de temps
    """
    def __init__(self, parent=None, width=800, height=800):
        """ 
        Initialisation

        parent : une application
        width,height : dimension de l'oscilloscpe
        """
        Frame.__init__(self)
        self.master.title("Oscilloscope")
        # Modele
        self.time = 0
        self.signal = None
        # Vues
        self.view = Screen(parent=self)
        # Controleurs
        self.control_time = TimeBase(parent=self)
        self.control_X = Generator(parent=self)
        # menu
        menuBar = MenuBar(self)
        menuBar.pack();
        # Affichage Vues, Controleurs
        self.view.pack(fill="both", expand=1)
        self.control_time.pack(side="left")
        self.control_X.pack(side="left")
        self.configure(width=width, height=height)
        
        

    def get_time(self):
        """
        recuperer la valeur courante de la base de temps
        """
        return self.control_time.get_time()

    def update_time(self, time):
        """
        calcul de signal si modification de la base de temps

        time : nouvelle valeur de la base de temps
        """
        if self.time != time:
            self.time = time
            self.control_X.update_signal(None)

    def update_view(self, name="X", signal=None):
        """ demande d'affichage de signal

        name : nom de la courbe (X,Y, X-Y)
        signal : liste des couples (temps,elongation) ou (elongation X, elongation Y)
        """
        print("Base de Temps :", self.get_time())
        msdiv = self.get_time()
        if signal :
            signal = signal[0:(len(signal)/msdiv) + 1]
            signal = map(lambda (x, y): (x*msdiv, y), signal)
            self.signal = signal
            self.view.plot_signal(name, signal)
        return signal

    def save(self):
        """
        Sauvegarde la courbe
        """
        print "Oscilloscope.save()"
        file = open("save",'w')
        # sauvegarde au format temps|amplitude|frequence|phase
        file.write(str(self.time)+'|'+str(self.control_X.scale_A.get())+'|'+str(self.control_X.scale_F.get())+'|'+str(self.control_X.scale_P.get())+'\r\n')
        # fermeture du fichier
        file.close()

    def load(self):
        """
        Charger la courbe
        """
        print "Oscilloscope.load()"
        file = open("save",'r')
        data = file.readline().rstrip('\r\n')
        regex = re.compile('^[0-9]{1,2}\|[0-9]{1,2}\|[0-9]{1,2}\|[0-9]{1,2}$')
        if(regex.match(data)):
           print "Format ok, loading\n"
           a = re.split('\|+', data, flags = re.IGNORECASE)
           self.control_time.scale_time.set(int(a[0]))
           self.control_X.scale_A.set(int(a[1]))
           self.control_X.scale_F.set(int(a[2]))
           self.control_X.scale_P.set(int(a[3]))
        else:
            print "Fichier incorrect"

        file.close()
        
if __name__ == "__main__":
    root = Tk()
    oscillo = Oscilloscope(root)
    root.mainloop()
