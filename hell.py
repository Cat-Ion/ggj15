import graphics
import pong_physics
import camera
import time
import gamemaths
import random
import pygame

roundcount_for_reflection_upgrade = 1
roundcount_for_line_upgrade = 5
roundcount = 0

reflection_count = 1
reflections_per_round = 1

green_player_score=0
red_player_score=0

winning_score=10 #-1 for ignore
ending_round=10 #-1 for ingore
pixel_length=30

lines=1

ignore_color = 0 #0=green,1=red
fps=60
game_over=False;   

if __name__ == '__main__':
        graphics.init()
        camera.init()
        camera.calibrate(graphics.screen)
        graphics.draw()
        pygame.mixer.init(buffer = 256)
        tock = [
                pygame.mixer.Sound("tock1.wav"),
                pygame.mixer.Sound("tock2.wav") ]

        while True:
                roundcount += 1
                reflections_per_round = 1 + roundcount / roundcount_for_reflection_upgrade
                lines = 1 + roundcount / roundcount_for_line_upgrade
                
                for line in range(lines):
                        pong_physics.barriers.append(
                                gamemaths.fit_line(camera.get_line(0, graphics.draw_lines), 100))
                        graphics.draw()
                        pong_physics.barriers.append(
                                gamemaths.fit_line(camera.get_line(1, graphics.draw_lines), 100))
                        graphics.draw()


                next_time = time.time()
                for reflection_count in range(reflections_per_round):
                        while True:
                                collision,score = pong_physics.step(1./fps)
                                if not collision:
                                        graphics.draw()
                                        next_time+=1./fps
                                        time.sleep(next_time-time.time())
                                else:
                                        tock[random.randint(0,1)].play()
                                        if score<0:
                                                break

                                        pong_physics.barriers[:] = []
                                        graphics.draw()
                                        
                                        if score==1:
                                                green_player_score += 1
                                                reflections_per_round = 1
                                                graphics.set_scores([green_player_score, red_player_score])
                                                break
                                        elif score==0:      
                                                red_player_score += 1
                                                reflections_per_round = 1
                                                graphics.set_scores([green_player_score, red_player_score])
                                                break
                        if score >= 0:
                                pong_physics.ball_pos = (320,240)
                                graphics.draw()
                                break
                                
