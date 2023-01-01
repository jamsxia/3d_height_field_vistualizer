

from functions import *
from vector import V
from gradient import Gradient
from polygon import Polygon

def lerp(x, a, b, c, d):
    return ((x-a)/(b-a))*(d-c) + c

class ParametricSurface():
    def __init__(self, func, n):
        self.func = func.function
        self.n = n
        self.xrange = func.xrange
        self.yrange = func.yrange
        self.gradient = Gradient(func.zrange)
        self.makeHeightfield()

    def makeHeightfield(self):
        self.xmin, self.xmax=self.xrange
        self.ymin,self.ymax=self.yrange
        self.heightfield=dict()
        for i in range(self.n):
            x=lerp(i, 0,self.n-1, self.xmin, self.xmax)
            for j in range(self.n):
                y=lerp(j, 0,self.n-1, self.ymin, self.ymax)
                pt=self.func(x,y)
                self.heightfield[i,j]=pt
        pass

    def projectPoints(self, eye):
        self.points=dict()
        self.distance=dict()
        self.xmin=100000000000000
        self.xmax=-100000000000
        self.ymin=10000000000000
        self.ymax=-100000000000000
        forward=-1*eye
        up=V(0,0,1)
        right=forward.cross(up)
        forward, up, right=forward.gram_schmidt(up,right)
        for i in range (self.n):
            for j in range(self.n):
                pt=self.heightfield[i,j]
                x=right*(pt-eye)
                y=up*(pt-eye)
                d=(pt-eye).length()
                self.points[i,j]=(x/d,y/d)
                self.distance[i,j]=d
                self.xmin=min(self.xmin,x/d)
                self.xmax=max(self.xmax,x/d)
                self.ymin=min(self.ymin,y/d)
                self.ymax=max(self.ymax,y/d)
                
        pass

    def normal(self, i, j):
        
        """find normal to surface at self.heightfield[i,j]
           use cross product of vectors from [i,j] to [i+1,j]
           and from [i,j] to [i,j+1]
        """
        p0=self.heightfield[i,j]
        p1=self.heightfield[i+1,j]
        p2=self.heightfield[i,j+1]
        v1=p1-p0
        v2=p2-p0
        normal=v1.cross(v2)
        normal.normalize()
        return normal
        pass
        
    def makePolygons(self, eye,size):
        n=self.n
        self.projectPoints(eye)
        self.scale(size)
        pts=self.points
        d=self.distance
        color='#0000ff'
        polys=[]
        self.color=dict()
##        print(self.gradient.color(1))
##        print(self.heightfield[1,2].z)
        for i in range(n-1):
            for j in range(n-1):
                normal=self.normal(i,j)
                light=(V(2,1,4)-normal)
                light.normalize()
##                print(light)
##                print(normal*light)
##                print(type(light))
                self.color[i,j]=self.gradient.color(self.heightfield[i,j].z,max(0.25,normal*light))
        
                
                
                
                
        for i in range(n-1):
            for j in range(n-1):
                d1=d[i,j]
                p1=pts[i,j]
##                c1=self.color[i,j]
                d2=d[i+1,j]
                p2=pts[i+1,j]
##                c2=self.color[i+1,j]
                d3=d[i+1,j+1]
                p3=pts[i+1,j+1]
##                c3=self.color[i+1,j+1]
                d4=d[i,j+1]
                p4=pts[i,j+1]
##                c4=self.color[i,j+1]
                dist=(d1+d2+d3+d4)/4
                color=self.color[i,j]
                
                p=Polygon([p1,p2,p3,p4],color,dist)
                polys.append(p)
                self.polygons=polys
##                
##        self.polygons = [Polygon([(100,100), (200,100), (200,200), (100,200)],
##                                 '#0000ff',
##                                 1.0),
##                         Polygon([(150,150), (250,150), (250,250), (150,250)],
##                                 '#ff0000',
##                                 2.0)
##                         ]
        
        
    def scale(self, size):
        w,h=size
        for i in range (self.n):
            for j in range(self.n):
                x,y=self.points[i,j]
                x=lerp(x,self.xmin,self.xmax,0,w-1)
                y=lerp(y,self.ymin,self.ymax,h-1,0)
                self.points[i,j]=(x,y)
                
        pass
    
                
        
        
        
        
        
            
