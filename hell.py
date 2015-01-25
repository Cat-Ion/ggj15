import graphics
import pong_physics
import camera
import time
import gamemaths

roundcount_for_reflection_upgrade = 5 
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

graphics.init()
camera.init()
camera.calibrate(graphics.screen)

while True:
        roundcount += 1
        reflections_per_round = roundcount / roundcount_for_reflection_upgrade
        lines = roundcount / roundcount_for_line_upgrade

        for line in range(lines):
                pong_physics.barriers.append(
                        gamemaths.fit_line(camera.get_line(0, graphics.draw_lines), 40))
                pong_physics.barriers.append(
                        gamemaths.fit_line(camera.get_line(0, graphics.draw_lines), 40))


        next_time = time.time()
        for reflection_count in range(reflections_per_round):
                while True:
                        collision,score = pong_physics.step(1./fps)
                        if not collision:
                                graphics.draw()
                                next_time+=1./fps
                                time.sleep(next_time-time.time())
                        else:
                                if score<0:
                                        pass

                                elif score==0:
                                        green_player_score += 1
                                        reflections_per_round = 1
                                        break
                                elif score==1:      
                                        red_player_score += 1
                                        reflections_per_round = 1
                                        break


