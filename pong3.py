import pygame, time

import pong_physics

pygame.init()

screen = pygame.display.set_mode( pong_physics.field_size )
pygame.display.set_caption("Pong")
screen.fill((255,255,255))

tnext = None
dt = 0.05
run = 1
mouse_start_pos = None


#---- MAIN LOOP ----#

try:
    while run:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print 'Mouse down at', event.pos
                mouse_start_pos = event.pos                 
            elif event.type == pygame.MOUSEBUTTONUP:
                print 'Mouse up at', event.pos
                if mouse_start_pos != None:
                    mouse_end_pos = event.pos
                    pong_physics.barriers = [(mouse_start_pos, mouse_end_pos)]
                    
        if not run: break

        # Physics step
        c,g = pong_physics.step(dt)
        if c: print "Collision"
        if g: print "Goal"

        # Update display
        screen.fill((255,255,255))

        for b in pong_physics.barriers:
            pygame.draw.line( screen, (0,0,0), b[0], b[1], 2 )
            if c: print 'Collision' 

        g1 = pong_physics.goals[0]
        pygame.draw.line( screen, (255,0,0), g1[0], g1[1], 4 )
        
        g2 = pong_physics.goals[1]
        pygame.draw.line( screen, (0,255,0), g2[0], g2[1], 4 )
        
        Bx,By = pong_physics.ball_pos
        Brad = pong_physics.ball_rad
        pygame.draw.circle( screen, (255,0,0), (int(Bx),int(By)), Brad)

        pygame.display.flip()

        # Clock
        if tnext == None: tnext = time.time()
        tnext += dt
        while time.time()<tnext:
            time.sleep(0.001)

finally:
    pygame.quit()

