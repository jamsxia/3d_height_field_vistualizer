import math

class V:
    """3d vectors"""

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x,y,z
    def __str__(self):
        return 'V(%s, %s, %s)' % (str(self.x), str(self.y), str(self.z))

    def copy(self):
        return V(self.x, self.y, self.z)

    def __mul__(self, other):
        if isinstance(other, V):
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
            return x+y+z
        else:
            return V(self.x*other, self.y*other, self.z*other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return (1/other)* self

    def __add__(self, other):
        return V(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return self + (-1*other)

    def __neg__(self):
        return -1*self

    def length(self):
        return math.sqrt(self * self)

    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length
        self.z /= length

    def project(v, w):
        return ((v * w)/(w*w)) * w

    def gram_schmidt(v1, v2, v3):
        u1 = v1.copy()
        u1.normalize()
        u2 = v2 - v2.project(u1)
        u2.normalize()
        u3 = v3 - v3.project(u1) - v3.project(u2)
        u3.normalize()
        return u1,u2,u3

    def cross(self, other):
        a1, a2, a3 = self.x, self.y, self.z
        b1, b2, b3 = other.x, other.y, other.z
        s1 = a2*b3 - a3*b2
        s2 = a3*b1 - a1*b3
        s3 = a1*b2 - a2*b1
        return V(s1,s2,s3)


if __name__ == '__main__':
    v1 = V(1,0,0)
    v2 = V(5, 9, 0)
    v3 = V(12,3,1)
    gs = v1.gram_schmidt(v2, v3)
    for u in gs:
        print(u)
    for u in gs:
        for v in gs:
            print(u*v, end=' ')
        print()
        
    
        
        
