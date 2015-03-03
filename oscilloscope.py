#!/usr/bin/python
# -*- coding: utf-8 -*-

import re,  tkFileDialog, tkMessageBox
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
        # gestion des signaux X et Y
        self.signal_X = None
        self.signal_Y = None
        # Vues
        self.view = Screen(parent=self)
        # Controleurs
        self.control_time = TimeBase(parent=self)
        self.control_X = Generator(self,'X')
        self.control_Y = Generator(self, 'Y')


        # menu
        menuBar = MenuBar(self)
        menuBar.pack(fill="both");


        # Affichage Vues, Controleurs
        self.view.pack(fill="both", expand=1)
        self.control_time.pack(side="left")
        self.control_X.pack(side="left")
        self.control_Y.pack(side="left")
        self.configure(width=width, height=height)
        self.master.protocol("WM_DELETE_WINDOW", self.quitter)

        
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


    def plot_all(self):
        """
        affiche tous les signaux
        """
        self.update_view('X',self.control_X.signal)
        self.update_view('Y',self.control_Y.signal)

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


    
    def about(self):
        """
        Affiche les infos des créateurs
        """
        tkMessageBox.showinfo('Super oscilloscope',
                                 'v0.1.3\n\n\tYoann Diquélou\n\tLeïla Toscer\n\n# Copyright (C) 2015 by ENIB-CAI')

    def save(self):
        """
        Sauvegarde la courbe
        sauvegarde au format temps|amplitude|frequence|phase
        """
        print "Oscilloscope.save()"

        filename = tkFileDialog.asksaveasfilename(title="Sauvegarder un graphe", filetypes=[('oscillographe file','.osc'),('all files', '.*')])
        file = open(filename,'w')
    
        file.write(str(self.time)+'|'+str(self.control_X.scale_A.get())+'|'+str(self.control_X.scale_F.get())+'|'+str(self.control_X.scale_P.get())+'|\r\n')
        # fermeture du fichier
        file.close()

    def load(self):
        """
        Charger la courbe
        """
        print "Oscilloscope.load()"
        file = tkFileDialog.askopenfile(title="Ouvrir un graphe", filetypes=[('oscillographe file','.osc'),('all files', '.*')])
        if file:
            data = file.readline().rstrip('\r\n')
            # vérification que le texte est en accord avec le format
#            regex = re.compile('^[0-9]{1,2}\|[0-9]{1,2}\|[0-9]{1,2}\|[0-9]{1,2}$')
            regex = re.compile('^([0-9]{1,2}\|){4}$')
            if(regex.match(data)):
                print "Format ok, loading\n"
                a = re.split('\|+', data, flags = re.IGNORECASE)
                self.control_time.scale_time.set(int(a[0]))
                self.control_X.scale_A.set(int(a[1]))
                self.control_X.scale_F.set(int(a[2]))
                self.control_X.scale_P.set(int(a[3]))
            else:
                print "Fichier incorrect"
                tkMessageBox.showerror('ERREUR',
            'Entrez un fichier valide, merci.')
                
            file.close()


    def quitter(self):
        """
        Affiche une boite de dialogue pour que l'utilisateur confirme son souhait de quitter
        """
        if tkMessageBox.askyesno('Quitter',
                                 'voulez-vous quitter?'):
            print "Oscilloscope.quitter()"
            self.quit()


if __name__ == "__main__":
    root = Tk()
    oscillo = Oscilloscope(root)

    root.mainloop()
