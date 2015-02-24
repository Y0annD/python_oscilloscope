# -*- coding: utf-8 -*-
from Tkinter import Tk, Frame, Scale


class TimeBase(Frame):
    """
    Base de temps

    scale_time : controle  de la base de temps
    """
    def __init__(self, parent=None):
        """
        Initialisation

        parent : oscilloscope
        """
        Frame.__init__(self)
        self.configure(bd=1, relief="sunken")
        self.parent = parent
        self.scale_time = Scale(self, length=100, orient="horizontal",
                label="Temps", showvalue=1, from_=1, to=10,
                tickinterval=1, command=self.update)
        self.scale_time.pack(expand="yes", fill="both")

    def get_time(self):
        """
        recuperer la valeur courante de la base de temps
        """
        return self.scale_time.get()

    def update(self, event):
        """mise a jour de la base de temps"""
        print("TimeBase.update_time_base()")
        print("Base de temps : ", self.scale_time.get())
        if not isinstance(self.parent, Tk):
            self.parent.update_time(self.scale_time.get())


if __name__ == "__main__":
    root = Tk()
    TimeBase(root).pack()
    root.mainloop()
