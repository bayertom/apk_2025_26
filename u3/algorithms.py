from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from math import *

class Algorithms:
    
    def __init__(self):
        
        pass
    
    def getPointLinePosition(self, a, b, p):
        #Analyze point and aline position (half plane test)
        tolerance = 1.0e-6
        
        #Components of vectors
        ux = b.x() - a.x()
        uy = b.y() - a.y()
        vx = p.x() - a.x()
        vy = p.y() - a.y()
        
        #Test criterion
        t = ux*vy - vx*uy
        
        #Point in the left half plane
        if t > tolerance:
            return 1
        
        #Point in the right half plane
        if t < -tolerance:
            return 0
    
        #Point on the line
        return -1
        
    
    def getNearestPoint(self, p, points):
        #Find point nearest to p in points
        p_nearest = None
        d_min = inf
        
        #Process all points
        for p_i in points:
            
            #Point p different from p_i
            if p != p_i:            
                #Coordinate differences
                dx = p.x() - p_i.x()
                dy = p.y() - p_i.y()
                      
                #Compute distance          
                dist = sqrt(dx**2 + dy**2)
                
                #Update minimum
                if dist < d_min:
                    d_min = dist
                    p_nearest = p_i
                    
        return p_nearest
    
    
    def get2LinesAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Angle between two lines
        ux = p2.x() - p1.x()    
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()    
        
        #Dot product
        dot = ux*vx + uy*vy
        
        #Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5
        
        #Correct interval
        arg = dot/(nu*nv)
        arg = max(-1, min(1,arg)) 
        
        return acos(arg)
    
    def findDelaunayPoint(self, p1, p2, points):
        #Find Delaunay point to the edge
        p_dt = None
        phi_max = 0

        #Process all points
        for p_i in points:
            
            #Point pi different from p1 and p2
            if p_i != p1 and p_i != p2:
                
                #Point in the left halfplane
                if self.getPointLinePosition (p_i, p1, p2) == 1:
                    pass
        
    
    
