from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from random import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__points =[]
        self.__DT = []
        self.__contours = []
        
        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Get random z
        z_min = 200
        z_max = 600
        z = random() * (z_max - z_min) + z_min

        #Create new point
        p = QPoint3DF(x, y, z)
        
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
            
        #Set properties, contours
        pen.setColor(Qt.GlobalColor.magenta)
        qp.setPen(pen)
        
        #Draw contour lines
        for e in self.__contours:
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
        
    
    def getDT(self):
        return self.__DT
    

    def getPoints(self):
        #Get points
        return self.__points
    
    
    def clearResult(self):
        #Clear results of analyses
        self.__DT.clear()
           
        #Repaint screen
        self.repaint()
        
        
    def setContours(self, contours):
        #Set contour lines
        self.__contours = contours
        