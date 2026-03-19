from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__building = QPolygonF()
        self.__mbr = QPolygonF()
        self.__ch = QPolygonF()

        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPointF(x,y)
        
        #Add P to polygon
        self.__building.append(p)
        
        #Repaint
        self.repaint()
        

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        #Set attributes, building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw building
        qp.drawPolygon(self.__building)
        
        #Set attributes, convex hull
        qp.setPen(Qt.GlobalColor.red)
        
        #Draw convex hull
        qp.drawPolygon(self.__ch)
        
        #Set attributes, MBR
        qp.setPen(Qt.GlobalColor.blue)
        
        #Draw MBR
        qp.drawPolygon(self.__mbr)
        
        #End draw
        qp.end()
        
        
    def setMBR(self, mbr:QPolygonF):
        #Set MBR
        self.__mbr = mbr
        

    def setCH(self, ch:QPolygonF):
        #Set CH
        self.__ch = ch  
        
        
    def getBuilding(self):
        #Get building
        return self.__building
        
        