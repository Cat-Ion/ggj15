import gamemaths
#import pong_physics
import pygame

screen = None

def init():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

def clear_screen():
    screen.fill((0,0,0))

def draw_world():
    # Draw ball and lines here
    pass

def draw_lines(lines):
    screen.fill((0,0,0))
    draw_world()
    pygame.draw.lines(screen, (0,255,0), False, lines, 3)
    
    line = gamemaths.fit_line(lines, 100)
    pygame.draw.circle(screen, (0,255,0), line[0], 10, 2)
    pygame.draw.circle(screen, (255,0,0), line[1], 10, 2)

    pygame.display.flip()
  

def draw():
    screen.fill((0,0,0))
    draw_world()
    pygame.display.flip()
