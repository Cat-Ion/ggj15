from math import sqrt

from collision import *

# Field
field_size = 640, 480

# Ball
ball_rad = 10
ball_pos = field_size[0]/2, field_size[1]/2
ball_vel = 100,40

#Barriers
barriers = [] ## [ ((500,100),(600,400)) ]

#Goals
goals = [ ((2,field_size[1]/3),(2,field_size[1]*2/3)),
          ((field_size[0]-1-2,field_size[1]/3),(field_size[0]-1-2,field_size[1]*2/3)) ]



def step(dt):
    global ball_pos, ball_vel, field_size
    Bx,By = ball_pos
    Bvx,Bvy = ball_vel
    W,H = field_size
    
    # Motion integration step
    Zx, Zy = Bx + Bvx*dt, By + Bvy*dt  # Z = new position 

    # Barrier collisions
    collision = 0
    for barr in barriers:
        (Bx,By), (Zx,Zy), (Bvx,Bvy), collection = collide_ball( (Bx,By), (Zx,Zy), (Bvx,Bvy), barr )
        collision |= collection
    
    # Wall collisions
    if Zx > W: Zx = 2*W - Zx; Bvx = -Bvx; collision = 1
    if Zx < 0: Zx = -Zx; Bvx = -Bvx; collision = 1        
    if Zy > H: Zy = 2*H - Zy; Bvy =- Bvy; collision = 1
    if Zy < 0: Zy = -Zy; Bvy =- Bvy; collision = 1

    # Goal collisions
    g1,g2 = 0,0
    (Bx,By), (Zx,Zy), (Bvx,Bvy), g1 = collide_ball( (Bx,By), (Zx,Zy), (Bvx,Bvy), goals[0] )
    (Bx,By), (Zx,Zy), (Bvx,Bvy), g2 = collide_ball( (Bx,By), (Zx,Zy), (Bvx,Bvy), goals[1] )
    if g1:
        goal = 0
        collision = 1
    elif g2:
        goal = 1
        collision = 1
    else: goal = -1

    ball_pos = Zx,Zy
    ball_vel = Bvx,Bvy
    return collision, goal 



