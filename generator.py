# -*- coding: utf-8 -*-
from Tkinter import Tk, Frame, Scale
from math import cos, sin, pi


class Generator(Frame):
    """
    Vibration harmonique du type : e=a*sin(2*pi*f*t+p)

    scale_A : controleur d'Amplitude
    scale_F : controleur de Frequence
    scale_P : controleur de Phase

    """
    def __init__(self, parent, name="X"):
        """
        Initialisation

        parent : un oscilloscope
        name : nom du signal
        """
        Frame.__init__(self)
        self.configure(bd=1, relief="sunken")
        self.parent = parent
        self.name = name

        # c
        self.scale_A = Scale(self, length=100, orient="horizontal",
                label=name + " Amplitude", showvalue=1, from_=0, to=10,
                tickinterval=1, command=self.update_signal)
        self.scale_A.pack(expand="yes", fill="both")

        self.scale_F = Scale(self, length=100, orient="horizontal",
                label=name + " Fréquence", showvalue=1, from_=1, to=10,
                tickinterval=1, command=self.update_signal)
        self.scale_F.pack(expand="yes", fill="both")

        self.scale_P = Scale(self, length=100, orient="horizontal",
                label=name + " Phase", showvalue=1, from_=0, to=10,
                tickinterval=1, command=self.update_signal)
        self.scale_P.pack(expand="yes", fill="both")

        
        self.bind("<Configure>",self.update_signal)
        
    def update_signal(self, event):
        """
        Mise a jour de signal si modifications (amplitude, frequence, phase)
        """
        print("Vibration.update_signal()")
        print("Amplitude :", self.scale_A.get())
        scaling=0.05
        amp = scaling*self.scale_A.get()
        signal = self.generate_signal(a=amp,f=self.scale_F.get(),
                                      p=self.scale_P.get())
        if not isinstance(self.parent, Tk):
            self.parent.update_view(self.name, signal)
        return signal

    def generate_signal(self, a=1.0, f=2.0, p=0):
        """
        Calcul de l'elongation : e=a*sin(2*pi*f*t+p) sur une periode
        a : amplitude
        f : frequence
        p : phase
        """
        signal = []
        samples = 1000
        for t in range(0, samples):
            samples = float(samples)
            e = a * sin((2*pi*f*(t/samples)) - p)
            signal.append((t/samples,e))
        return signal


        
if __name__ == "__main__":
    root = Tk()
    Generator(root).pack()
    root.mainloop()
