import tkinter
import random
import time

from parametricsurface import ParametricSurface
from functions import *
from vector import V

class Poly3d():
    def __init__(self, parent, size, surfs, eye):
        self.size = size        # screen size
        self.parent = parent    # tkinter parent window
        self.surfindex = 1      # which surface to draw
        self.surfs = surfs      # parametric surfaces
        self.surface = self.surfs[self.surfindex]
        self.eye = eye          # where are we looking from?

        # make canvas
        width, height = size
        self.canvas = tkinter.Canvas(parent, bg='white',
                                     width=width, height=height)
        self.canvas.pack()

        # key bindings
        self.parent.bind('<Left>', self.rotateLeft)
        self.parent.bind('<Right>', self.rotateRight)
        self.parent.bind('<Up>', self.rotateUp)
        self.parent.bind('<Down>', self.rotateDown)
        self.parent.bind('z', self.cameraForward)
        self.parent.bind('x', self.cameraBack)
        self.parent.bind('<Escape>', self.quit)
        self.parent.bind('s', self.changeSurface)

        #draw
        self.draw()

    def changeSurface(self, e=None):
        """change to the next loaded surface"""
        self.surfindex += 1
        self.surfindex %= len(self.surfs)
        self.surface = self.surfs[self.surfindex]
        self.draw()

    def draw(self):
        """draw all the polygons"""
        slow = False
        self.canvas.delete('all')
        self.surface.makePolygons(self.eye,self.size) # project points and make polygons
        #self.surface.scale(self.size)       # scale points to window size
        for p in self.surface.polygons:
            if slow:
                time.sleep(0.001)
            self.canvas.create_polygon(p.points,       # list of 2-tuples
                                       fill=p.color,   # start with 'blue'
                                       outline=p.color # start with 'black'
                                       )
            if slow:
                self.canvas.update()
        self.canvas.update()

    def eyeframe(self):
        """ return 3 orthonormal vectors from eye:
            forward, up, right"""
        forward = -self.eye
        up = V(0,0,1)
        right = forward.cross(up)
        return forward.gram_schmidt(up,right)
        
    def rotateLeft(self, e=None):
        """rotate the camera to the left"""
        fwd, up, right = self.eyeframe()
        d = self.eye.length()
        self.eye += 0.25*right
        self.eye = d*self.eye/self.eye.length()
        self.draw()
        
    def rotateRight(self, e=None):
        """rotate the camera to the right"""
        fwd, up, right = self.eyeframe()
        d = self.eye.length()
        self.eye -= 0.25*right
        self.eye = d*self.eye/self.eye.length()
        self.draw()
        
    def rotateUp(self, e=None):
        """rotate camera up"""
        fwd, up, right = self.eyeframe()
        d = self.eye.length()
        self.eye += 0.25*up
        self.eye = d*self.eye/self.eye.length()
        self.draw()
        
    def rotateDown(self, e=None):
        """rotate camera down"""
        fwd, up, right = self.eyeframe()
        d = self.eye.length()
        self.eye -= 0.25*up
        self.eye = d*self.eye/self.eye.length()
        self.draw()
        
    def cameraBack(self, e=None):
        """move camera farther away"""
        self.eye *= 1.1
        self.draw()
        
    def cameraForward(self, e=None):
        """move camera closer"""
        self.eye *= 0.9
        self.draw()

    def quit(self, e=None):
        """quit application"""
        self.parent.destroy()
            
if __name__ == '__main__':
    root = tkinter.Tk()
    size = (600,400)
    n = 32
    surfs = [ParametricSurface(f, n) for f in functions()]
    eye = V(5,-10,5)
    plot = Poly3d(root, size, surfs, eye)
    root.mainloop()
