from functions import *

def hexcolor(color):
    '''given a color like (255,255,255) return #ffffff'''
    digits = '0123456789abcdef'
    s = '#'
    for c in color:
        s += digits[int(c) // 16]
        s += digits[int(c)  % 16]
    return s

class Gradient():
    '''class to compute color from single number in range'''
    def __init__(self, range):
        min,max = range
        self.min = min
        self.max = max
        self.range = max - min

    def color(self, x, shade = 1.0):
        '''return color for x
           optional shade in (0,1) will darken color
        '''
        x = max(self.min, x)
        x = min(self.max, x)
        x = 5*(x-self.min)/self.range
        if x < 1:
            y = 1-x
            return hexcolor((shade*255, shade*x*255, 0))
        elif x < 2:
            x -= 1
            y = 1-x
            return hexcolor((shade*y*255, shade*255, 0))
        elif x < 3:
            x -= 2
            y = 1-x
            return hexcolor((0, shade*255, shade*x*255))
        elif x < 4:
            x -= 3
            y = 1-x
            return hexcolor((0, shade*y*255, shade*255))
        else:
            x -= 4
            y = 1-x
            return hexcolor((shade*x*255, 0, shade*255))

if __name__ == '__main__':
    for c in [(0,0,0), (0,128,0), (255,255,255)]:
        print(c, hexcolor(c))
    
