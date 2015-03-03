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
        mbuttonFile.pack(side="left")
        menuFile = Menu(mbuttonFile)
        menuFile.add_command(label="Sauvegarder",
                             command=parent.save)
        menuFile.add_command(label="Charger",
                             command=parent.load)
        
        menuFile.add_command(label="Quitter",
                             command=parent.quitter)
        mbuttonFile.configure(menu=menuFile)

        mbuttonFileBis = Menubutton(self, text="?")

        menuFileBis = Menu(mbuttonFileBis)
        menuFileBis.add_command(label="A propos",
                                command=parent.about)
        mbuttonFileBis.configure(menu = menuFileBis)

        mbuttonFileBis.pack(side="left")
