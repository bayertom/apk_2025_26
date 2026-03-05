
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Algorithms:
    
    def getPointPolygonPositionRC(self, q:QPointF, pol:QPolygonF):
        #Analyze point and polygon position using ray crossing algorithm
    
        #Intersects
        k = 0  
        #Number of vertices
        n = len(pol) 
        
        #Process all polygon edges
        for i in range(n):
            #Start point of the edge
            xi = pol[i].x() - q.x()
            yi = pol[i].y() - q.y()
            
            #End point of the edge        
            xi1 = pol[(i+1)%n].x() - q.x()
            yi1 = pol[(i+1)%n].y() - q.y()
            
            #Find suitable segment
            if (yi1 > 0) and (yi<= 0) or (yi > 0) and (yi1 <= 0):
                
                #Compute intersection
                xm = (xi1 * yi - xi * yi1) / (yi1 - yi) 
                
                #Correct intersection
                if xm > 0:
                    
                    #Increment number of intersections
                    k = k + 1   
                        
        #Point is inside the polygon
        if k % 2 == 1:
            return 1 
            
        #Point is outside the polygon
        return 0    