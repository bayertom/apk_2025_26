from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms:
    
    def __init__(self):
        pass
    
    def get2VectorsAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Angle between two vectors
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
    
    
    def createCH(self, pol:QPolygonF):
        #Create Convex Hull using Jarvis Scan
        ch = QPolygonF()
        
        #Find pivot q (minimize y)
        q = min(pol, key = lambda k: k.y())

        #Find left-most point (minimize x)
        s = min(pol, key = lambda k: k.x())
        
        #Initial segment
        pj = q
        pj1 = QPointF(s.x(), q.y())
        
        #Add to CH
        ch.append(pj)
        
        #Find all points of CH
        while True:
            #Maximum and its index
            omega_max = 0
            index_max = -1
            
            #Browse all points
            for i in range(len(pol)):
                
                #Different points
                if pj != pol[i]:
                    
                    #Compute omega
                    omega = self.get2VectorsAngle(pj, pj1, pj, pol[i])
            
                    #Actualize maximum
                    if(omega > omega_max):
                        omega_max = omega
                        index_max = i
                    
            #Add point to the convex hull
            ch.append(pol[index_max])
            
            #Reasign points
            pj1 = pj
            pj = pol[index_max]
            
            # Stopping condition
            if pj == q:
                break
            
        return ch
    
    
    def createMMB(self, pol:QPolygonF):
        # Create min max box and compute its area

        #Points with extreme coordinates        
        p_xmin = min(pol, key = lambda k: k.x())
        p_xmax = max(pol, key = lambda k: k.x())
        p_ymin = min(pol, key = lambda k: k.y())
        p_ymax = max(pol, key = lambda k: k.y())
        
        #Create vertices
        v1 = QPointF(p_xmin.x(), p_ymin.y())
        v2 = QPointF(p_xmax.x(), p_ymin.y())
        v3 = QPointF(p_xmax.x(), p_ymax.y())
        v4 = QPointF(p_xmin.x(), p_ymax.y())
        
        #Create new polygon
        mmb = QPolygonF([v1, v2, v3, v4])
        
        #Area of MMB
        area = (v2.x() - v1.x()) * (v3.y() - v2.y())
        
        return mmb, area
     

    def rotatePolygon(self, pol:QPolygonF, sig:float):
        #Rotate polygon according to a given angle
        pol_rot = QPolygonF()

        #Process all polygon vertices
        for i in range(len(pol)):

            #Rotate point
            x_rot = pol[i].x() * cos(sig) - pol[i].y() * sin(sig)
            y_rot = pol[i].x() * sin(sig) + pol[i].y() * cos(sig)

            #Create QPoint
            vertex = QPointF(x_rot, y_rot)

            # Add vertex to rotated polygon
            pol_rot.append(vertex)

        return pol_rot
    
    
    def createMBR(self, building:QPolygonF):
        #Create minimum bounding rectangle using repeated construction of mmb
        sigma_min = 0
        
        #Convex hull
        ch = self.createCH(building)
        
        #Initialization
        mmb_min, area_min = self.createMMB(ch)
        
        # Process all edges of convex hull
        n = len(ch)
        for i in range(n):
            #Coordinate differences
            dx = ch[(i+1)%n].x() - ch[i].x()
            dy = ch[(i+1)%n].y() - ch[i].y()
            
            # Compute direction
            sigma = atan2(dy, dx)
            
            #Rotate convex hull
            ch_r = self.rotatePolygon(ch, -sigma)
        
            #Compute min-max box
            mmb, area = self.createMMB(ch_r)
            
            #Did we find a better min-max box?
            if area < area_min:    
                #Update minimum
                area_min = area
                mmb_min = mmb
                sigma_min = sigma
                
        #Back rotation
        return  self.rotatePolygon(mmb_min, sigma_min) 

    
    def getArea(self, pol:QPolygonF):
        #Compute area    
        area = 0
        n = len(pol)
        
        # Process all vertices
        for i in range(n):
            area += pol[i].x() * (pol[(i + 1) % n].y() - pol[(i - 1 + n) % n].y())
            
        return abs(area)/2    
    
        
    def resizeRectangle(self, building:QPolygonF, mbr: QPolygonF):
        #Resizing rectangle area to match building area
        
        #Area of the rectangle
        A = self.getArea(mbr)
        
        #Area of the building
        Ab = self.getArea(building)
        
        #Fraction of both areas
        k = Ab / A
        
        #Compute centroid of the rectangle
        x_c = (mbr[0].x()+mbr[1].x()+mbr[2].x()+mbr[3].x()) / 4
        y_c = (mbr[0].y()+mbr[1].y()+mbr[2].y()+mbr[3].y()) / 4
        
        #Compute vectors 
        v1_x = mbr[0].x() - x_c
        v1_y = mbr[0].y() - y_c 
        
        v2_x = mbr[1].x() - x_c
        v2_y = mbr[1].y() - y_c 

        v3_x = mbr[2].x() - x_c
        v3_y = mbr[2].y() - y_c 
        
        v4_x = mbr[3].x() - x_c
        v4_y = mbr[3].y() - y_c
        
        #Resize vectors v1 - v4 
        v1_x_res = v1_x * k
        v1_y_res = v1_y * k
        
        v2_x_res = v2_x * k
        v2_y_res = v2_y * k
        
        v3_x_res = v3_x * k
        v3_y_res = v3_y * k
        
        v4_x_res = v4_x * k
        v4_y_res = v4_y * k
        
        #Compute new vertices
        p1_x = v1_x_res + x_c  
        p1_y = v1_y_res + y_c 
        
        p2_x = v2_x_res + x_c  
        p2_y = v2_y_res + y_c 
        
        p3_x = v3_x_res + x_c  
        p3_y = v3_y_res + y_c 
        
        p4_x = v4_x_res + x_c  
        p4_y = v4_y_res + y_c
        
        # Compute new coordinates
        p1 = QPointF(p1_x,  p1_y)
        p2 = QPointF(p2_x,  p2_y)
        p3 = QPointF(p3_x,  p3_y)
        p4 = QPointF(p4_x,  p4_y)   
        
        #Create polygon
        mbr_res = QPolygonF()
        mbr_res.append(p1)
        mbr_res.append(p2)
        mbr_res.append(p3)
        mbr_res.append(p4)
       
        return mbr_res