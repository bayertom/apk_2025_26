from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from math import *
from edge import *
from triangle import *

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
                    
                    #Compute phi
                    phi = self.get2LinesAngle(p_i, p2, p_i, p1)
                    
                    #Update maximum
                    if phi > phi_max:
                        phi_max = phi
                        p_dt = p_i
        return p_dt
                    
    def createDT(self, points):
        #Create Delaunay triangulation                 
        DT = []
        AEL = [] 
        
        #Find pivot
        q = min(points, key = lambda k: k.y())   
        
        #Find point nearest to q
        qn = self.getNearestPoint(q, points)       
        
        #Create new edges
        e = Edge(q, qn)
        es = Edge(qn, q)  
        
        #Edges to AEL
        AEL.append (e)
        AEL.append (es) 
        
        #Repeat until AEL is empty             
        while AEL:
            #Take first edge
            e1 = AEL.pop()
            
            #Switch orientation
            e1s = e1.switchOrientation()
            
            #Find Delaunay point
            p_dt = self.findDelaunayPoint(e1s.getStart(), e1s.getEnd(), points)
            
            #Jump to the next iteration
            if p_dt == None:
                continue
            
            #Create new edges
            e2 = Edge(e1s.getEnd(), p_dt)
            e3 = Edge(p_dt, e1s.getStart())
            
            #Add new edges to DT
            DT.append(e1s)
            DT.append(e2)
            DT.append(e3)
            
            
            #Update AEL
            self.updateAEL(e2,AEL)
            self.updateAEL(e3,AEL)
            
        return DT
    
    
    def updateAEL(self, e, AEL):
        #Verify if e in AEL with diffferent orientation
        es = e.switchOrientation()
        
        #Edge e in AEL, remove
        if es in AEL:
            AEL.remove(es)
            
        #Add e to AEL
        else:
            AEL.append(e) 
            
            
    def getContourPoint(self, p1, p2, z):
        #Intersection line and horizontal plane
        x = (p2.x() - p1.x()) / (p2.z() -p1.z()) * (z - p1.z()) + p1.x()
        y = (p2.y() - p1.y()) / (p2.z() -p1.z()) * (z - p1.z()) + p1.y()

        return QPoint3DF(x, y, z)        
        
            
    def generateContourLines(self, DT, z_min, z_max, dz):
        #Generate contour lines in a given z range and step
        contours = []
        n = len(DT)
        
        #Process al triangles
        for i in range(0, n, 3):
            
            #Get triangle vertices
            p1 = DT[i].getStart()
            p2 = DT[i].getEnd()
            p3 = DT[i + 1].getEnd()
            
            #Create all contour lines
            for z in range(z_min, z_max, dz):
                #Compute height differences
                dz1 = z - p1.z()
                dz2 = z - p2.z()
                dz3 = z - p3.z()
                
                #Coplanar triangle
                if dz1 == 0 and dz2 == 0 and dz3 == 0:
                    continue
                
                #Edge p1, p2 is colinear
                elif dz1 == 0 and dz2 == 0:
                    contours.append(DT[i])

                #Edge p2, p3 is colinear
                elif dz2 == 0 and dz3 == 0:
                    contours.append(DT[i+1])
                    
                #Edge p3, p1 is colinear
                elif dz3 == 0 and dz1 == 0:
                    contours.append(DT[i+2])
                    
                #Edges (p1,p2) and (p2, p3) intersected by line
                elif dz1 * dz2 < 0 and dz2 * dz3 < 0:
                    #Compute intersections
                    a = self.getContourPoint(p1, p2, z)
                    b = self.getContourPoint(p2, p3, z)
                    
                    #Add edge to the list
                    contours.append(Edge(a, b))

                #Edges (p2,p3) and (p3, p1) intersected by line                    
                elif dz2 * dz3 < 0 and dz3 * dz1 < 0:
                    #Compute intersections
                    a = self.getContourPoint(p2, p3, z)
                    b = self.getContourPoint(p3, p1, z)
                    
                    #Add edge to the list
                    contours.append(Edge(a, b))
                    
                #Edges (p3,p1) and (p1, p2) intersected by line
                elif dz3 * dz1 < 0 and dz1 * dz2 < 0:
                    #Compute intersections
                    a = self.getContourPoint(p3, p1, z)
                    b = self.getContourPoint(p1, p2, z)
                    
                    #Add edge to the list
                    contours.append(Edge(a, b))
                    
        return contours
    
    def getSlope(self, p1, p2, p3):
        #Calculate slope of triangle

        #u = p3 - p2
        ux = p3.x() - p2.x()
        uy = p3.y() - p2.y()
        uz = p3.z() - p2.z()

        #v = p1 - p2
        vx = p1.x() - p2.x()
        vy = p1.y() - p2.y()
        vz = p1.z() - p2.z()

        #Cross product
        nx = uy * vz - uz * vy
        ny = - (ux * vz - uz * vx)
        nz = ux * vy - uy * vx
        
        #Norm of n
        norm = sqrt(nx**2 + ny**2 + nz**2)
        
        return acos(nz / norm)
        
    def analyzeDTMSlope(self, DT):
        #Compute slope for DTM
        n = len(DT)

        #Create list of triangles
        triangles = []

        #Process all triangles
        for i in range(0, n, 3):
            
            #Get triangle vertices
            p1 = DT[i].getStart()
            p2 = DT[i].getEnd()
            p3 = DT[i + 1].getEnd()
            
            #Compute slope
            slope = self.getSlope(p1, p2, p3)
            
            #Create new triangle
            triangle = Triangle(p1, p2, p3)

            #Add to list the list
            triangles.append(triangle.setSlope(slope))

        return triangles
    
    
