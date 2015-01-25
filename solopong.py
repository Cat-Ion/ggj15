import pygame, time

from numpy import *
from collision import *

W,H = 640, 480

pygame.init()

screen = pygame.display.set_mode( (W,H) )
pygame.display.set_caption("Pong")
screen.fill((255,255,255))


# Ball
Brad = 10         # Radius
Bcol = (255,0,0) # color
Bx,By = W/2,H/2     # Position
Bvx,Bvy = 100,40 # Velocity


#time step
dt = 0.05    # seconds (real time)
tnext = time.time()

#Barriers
barrier = (500,100),(600,400)

run = 1
mouse_start_pos = None

try:
    while run:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_start_pos = event.pos
                print 'Mouse down at', mouse_start_pos 
            elif event.type == pygame.MOUSEBUTTONUP:
                print 'Mouse up'
                print 'mouse_start_pos:', mouse_start_pos
                if mouse_start_pos != None:
                    mouse_end_pos = event.pos
                    barrier = mouse_start_pos, mouse_end_pos
                    print 'barrier:', barrier
                
        if not run: break

        # Movement integration step
        xnew, ynew = Bx + Bvx*dt, By + Bvy*dt
        if xnew > W: xnew = 2*W - xnew; Bvx = -Bvx
        if xnew < 0: xnew = -xnew; Bvx = -Bvx        
        if ynew > H: ynew = 2*H - ynew; Bvy =- Bvy
        if ynew < 0: ynew = -ynew; Bvy =- Bvy
        ##Bx,By = xnew,ynew        

        # Collision detection
        P = coll_lines( ((Bx,By),(xnew,ynew)), barrier )
        if P != None: 
            xnew,ynew = mirror_point( (xnew,ynew), barrier )
            V = sqrt(Bvx**2+Bvy**2) # velocity absolute
            zout = xnew-P[0],ynew-P[1]
            zout = zout[0]/sqrt(zout[0]**2+zout[1]**2), \
                   zout[1]/sqrt(zout[0]**2+zout[1]**2)
            Bvx,Bvy = V*zout[0],V*zout[1]
        Bx,By = xnew,ynew

        # Update display
        screen.fill((255,255,255))
        pygame.draw.line( screen, (0,0,0), barrier[0], barrier[1], 2 )
        pygame.draw.circle( screen, Bcol, (int(Bx),int(By)), Brad)
        pygame.display.flip()

        # Clock
        tnext += dt
        while time.time()<tnext:
            time.sleep(0.001)

finally:
    pygame.quit()

