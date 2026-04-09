from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__points =[]
        self.__DT = []
        
        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPoint3DF(x, y, 0)
        
        #Add P to polygon
        self.__points.append(p)
        
        #Repaint
        self.repaint()
        

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        #Create new pen
        pen = QPen()
        
        #Set properties, edges
        pen.setColor(Qt.GlobalColor.green)
        qp.setPen(pen)
        
        #Draw edges
        for e in self.__DT:
            qp.drawLine(e.getStart(), e.getEnd())
        
        #Set properties, points
        pen.setWidth(15)
        pen.setColor(Qt.GlobalColor.black)
        qp.setPen(pen)
   
   
        #Draw points
        qp.drawPoints(self.__points)
        
        #End draw
        qp.end()
        
        
    def setDT(self, DT):
        #Set DT
        self.__DT = DT
        
        
    def getPoints(self):
        #Get points
        return self.__points
    
    
    def clearResult(self):
        #Clear results of analyses
        self.__DT.clear()
           
        #Repaint screen
        self.repaint()
        
        
        
        