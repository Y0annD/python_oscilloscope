#!/usr/bin/python
# -*- coding: utf-8 -*-

import re,  tkFileDialog, tkMessageBox, json
from Tkinter import Tk, Frame, Grid, IntVar

from lissajou import Lissajou
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
        self.master.title("Oscilloscope - Diquélou - Toscer")

        # doit-on afficher la courbe de lissajoux
        self.drawXY = IntVar()
        
        # Modele
        self.time = 0
        # gestion des signaux X et Y
        self.signal_X   = None
        self.signal_Y   = None
        self.signal_XY = None
        # Vues
        self.view = Screen(parent=self)
        self.lissajoux = Screen(parent= self)
        # Controleurs
        self.control_time = TimeBase(parent=self)
        self.control_X = Generator(self,'X')
        self.control_Y = Generator(self, 'Y')



        # menu
        menuBar = MenuBar(self)
        menuBar.pack(fill="x");

        # Affichage Vues, Controleurs
        self.view.pack(fill="both")

        self.control_time.pack(side="left", fill="y")
     
        self.control_X.pack(side="left",fill="y")

        self.lissajoux.pack(fill="both", side="left", expand=1)

        self.control_Y.pack(side="right", fill="both")

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
            self.control_Y.update_signal(None)
            

    def plot_all(self):
        """
        affiche tous les signaux
        """
        self.update_view('X',self.control_X.signal)
        self.update_view('Y',self.control_Y.signal)
        self.update_view('XY',self.control_X.signal)

    def update_view(self, name="X", signal=None):
        """ demande d'affichage de signal

        name : nom de la courbe (X,Y, X-Y)
        signal : liste des couples (temps,elongation) ou (elongation X, elongation Y)
        """
        print("Base de Temps :", self.get_time())
        msdiv = self.get_time()
        if signal :
            if name!='XY':
                signal = signal[0:(len(signal)/msdiv) + 1]
                signal = map(lambda (x, y): (x*msdiv, y), signal)
                
                self.view.plot_signal(name, signal)

            else:
                self.signal_XY = []
                for i in range(0, len(self.control_X.signal)):
                    self.signal_XY.append((self.control_X.signal[i][1],self.control_Y.signal[i][1]))
                self.lissajoux.plot_signal('XY',self.signal_XY)
        return signal


    
    def about(self):
        """
        Affiche les infos des créateurs
        """
        tkMessageBox.showinfo('Super oscilloscope',
                                 'v0.1.5\n\n\tYoann Diquélou\n\tLeïla Toscer\n\n# Copyright (C) 2015 by ENIB-CAI')

    def save(self):
        """
        Sauvegarde la courbe
        sauvegarde au format temps|amplitude|frequence|phase
        """
        print "Oscilloscope.save()"
        saveTxt = {}
        saveTxt["timebase"] = self.time
        saveTxt["graphs"] = []
        saveTxt["graphs"].append( self.getGraphInfos(self.control_X))
        saveTxt["graphs"].append( self.getGraphInfos(self.control_Y))
        filename = tkFileDialog.asksaveasfilename(title="Sauvegarder un graphe", filetypes=[('oscillographe file','.osc'),('all files', '.*')])
        print json.dumps(saveTxt, indent=4)
        if filename:
            file = open(filename,'w')
            file.write(json.dumps(saveTxt, indent=4))
            #file.write(str(self.time)+'|'+str(self.control_X.drawVar.get())+'|'+str(self.control_Y.drawVar.get())+'\n'+str(self.control_X.scale_A.get())+'|'+str(self.control_X.scale_F.get())+'|'+str(self.control_X.scale_P.get())+'|\n'+str(self.control_Y.scale_A.get())+'|'+str(self.control_Y.scale_F.get())+'|'+str(self.control_Y.scale_P.get())+'|\n')
            # fermeture du fichier
            file.close()

    def load(self):
        """
        Charger la courbe
        """
        print "Oscilloscope.load()"
        file = tkFileDialog.askopenfile(title="Ouvrir un graphe", filetypes=[('oscillographe file','.osc'),('all files', '.*')])
        if file:
            #data = file.readline().rstrip('\r\n')
            # vérification que le texte est en accord avec le format
            #            regex = re.compile('^[0-9]{1,2}\|[0-9]{1,2}\|[0-9]{1,2}\|[0-9]{1,2}$')
            # regex = re.compile('^([0-9]{1,2}\|){4}$')
            # if(regex.match(data)):
            #     print "Format ok, loading\n"
            #     a = re.split('\|+', data, flags = re.IGNORECASE)
            #     self.control_time.scale_time.set(int(a[0]))
            #     self.control_X.scale_A.set(int(a[1]))
            #     self.control_X.scale_F.set(int(a[2]))
            #     self.control_X.scale_P.set(int(a[3]))
            # else:
            #     print "Fichier incorrect"
            #     tkMessageBox.showerror('ERREUR',
            # 'Entrez un fichier valide, merci.')
            format = json.load(file)
            self.control_time.scale_time.set( format["timebase"])
            for i in range(0 ,len(format["graphs"])):
                eval('self.control_'+format["graphs"][i]["name"]+'.scale_A.set('+str(format["graphs"][i]["amp"])+')')
                eval('self.control_'+format["graphs"][i]["name"]+'.scale_F.set('+str(format["graphs"][i]["freq"])+')')
                eval('self.control_'+format["graphs"][i]["name"]+'.scale_P.set('+str(format["graphs"][i]["phi"])+')')
                if format["graphs"][i]["active"]==1:
                    eval('self.control_'+format["graphs"][i]["name"]+'.draw.select()')
                else:
                    eval('self.control_'+format["graphs"][i]["name"]+'.draw.deselect()')



                # if format["graphs"][i]["name"] == 'X':
                #     self.control_X.scale_A.set(format["graphs"][i]["amp"])
                #     self.control_X.scale_F.set(format["graphs"][i]["freq"])
                #     self.control_X.scale_P.set(format["graphs"][i]["phi"])
                #     if format["graphs"][i]["active"]==1:
                        
                #         self.control_X.draw.select()
                #     else:
                #         self.control_X.draw.deselect()
                # else:
                #     self.control_Y.scale_A.set(format["graphs"][i]["amp"])
                #     self.control_Y.scale_F.set(format["graphs"][i]["freq"])
                #     self.control_Y.scale_P.set(format["graphs"][i]["phi"])
                #     if format["graphs"][i]["active"]==1:
                #         self.control_Y.draw.select()
                #     else:
                #         self.control_Y.draw.deselect()

            file.close()


    def getGraphInfos(self, graph):
        graphique = {}
        graphique["name"] = graph.name
        graphique["active"] = graph.drawVar.get()
        graphique["amp"] = graph.scale_A.get()
        graphique["freq"] = graph.scale_F.get()
        graphique["phi"] = graph.scale_P.get()
        return graphique
            
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
