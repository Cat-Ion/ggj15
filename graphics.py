import gamemaths
import pong_physics
import pygame

screen = None

def init():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

def clear_screen():
    screen.fill((0,0,0))

def draw_world():
    for line in pong_physics.barriers:
        pygame.draw.line(screen, (128, 128, 128), line[0], line[1], 2)
    pygame.draw.circle(screen, (255, 255, 255),
                       (int(pong_physics.ball_pos[0]),
                        int(pong_physics.ball_pos[1])),
                       int(pong_physics.ball_rad), 0)

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
