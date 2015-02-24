#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Menu, Menubutton

class MenuBar(Frame):
    """
    classe représentant une barre de menu
    """
    def __init__(self, parent=None):
        Frame.__init__(self, borderwidth=2)
        mbuttonFile = Menubutton(self, text="Fichier")
        mbuttonFile.pack()
        menuFile = Menu(mbuttonFile)
        menuFile.add_command(label="Sauvegarder",
                             command=parent.save)
        menuFile.add_command(label="Charger",
                             command=parent.load)
        
        menuFile.add_command(label="Quitter",
                             command=parent.quit)
        mbuttonFile.configure(menu=menuFile)
        
