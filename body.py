from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class body():
    def __init__(self,mass,H_cap,Temp):
        self.mass_body = float(mass)
        self.Temprature_body = float(Temp)
        self.H_Cap_Body = float(H_cap)

    def add_heat(self,Q_add):
        self.Q_addition = float(Q_add)
        self.add_Temp = (self.Q_addition)/(self.mass_body*self.H_Cap_Body)
        self.Temprature_body+=self.add_Temp
        return self.Q_addition

