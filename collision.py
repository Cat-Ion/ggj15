
from math import sqrt

def coll_lines( ((x11,y11), (x12,y12)), ((x21,y21), (x22,y22)) ):
    """Get intersection of two lines.
    Line 1: ((x11,y11), (x12,y12)), Line 2: ((x21,y21), (x22,y22))
    Returns intersection point or None in case of no intersection."""

    # make sure points are sorted by x
    if x11>x12: x11,y11, x12,y12 = x12,y12, x11,y11
    if x21>x22: x21,y21, x22,y22 = x22,y22, x21,y21

    # XXX dirty workaround for infinity slopes
    if x12-x11==0: x12=x11+0.1
    if x22-x21==0: x22=x21+0.1
    
    # slopes
    m1 = float(y12-y11)/(x12-x11)
    m2 = float(y22-y21)/(x22-x21)
    if m1==m2: return None,None  # parallel

    # intersection at x from line equations y11 + m1*(x-x11) == y21 + m2*(x-x21)
    x = float(y21-y11+m1*x11-m2*x21)/(m1-m2)

    # collision outside line endings?
    if x<x11 or x>x12 or x<x21 or x>x22: return None,None

    y = y11+m1*(x-x11)
    return x,y


def mirror_point( (x1,y1), ((x21,y21), (x22,y22)) ):
    """Get position of point x1,y1, mirrored at line (x21,y21),(x22,y22)"""
    
    # make sure points are sorted by x
    if x21>x22: x21,y21, x22,y22 = x22,y22, x21,y21

    if x22-x21==0: x22=x21+0.1
    a = float(y22-y21)/(x22-x21)  # Line slope
    c = y21-a*x21                 # Line y-Offset 

    # Receipe
    d = (x1 + (y1 - c)*a)/(1 + a*a)
    x2 = 2*d - x1
    y2 = 2*d*a - y1 + 2*c
    return x2,y2


def collide_ball( (Bx,By), (Zx,Zy), (Bvx,Bvy), barrier ):
    Px,Py = coll_lines( ((Bx,By),(Zx,Zy)), barrier )  # collision with barrier at P
    if Px != None:
        collision = 1
        Zx,Zy = mirror_point( (Zx,Zy), barrier ) # Z = Reflected position
        PZx, PZy = Zx-Px, Zy-Py     # Reflected direction
        PZabs = sqrt(PZx**2+PZy**2)
        PZx,PZy = PZx/PZabs,PZy/PZabs # Normalized reflected direction
        Bvabs = sqrt(Bvx**2+Bvy**2)  # Absolute velocity
        Bvx,Bvy = Bvabs*PZx, Bvabs*PZy # New velocity after reflection
        Bx,By = Px,Py
    else: collision = 0
    return (Bx,By), (Zx,Zy), (Bvx,Bvy), collision




##A = 100,100
##B = 500,300
##C = 100,500
##D = 500,100
##
####print coll_lines((A,B),(C,D))
##print mirror_point( C, (A,B) )




