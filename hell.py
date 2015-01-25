reflection_start = 1
reflection_count = 1
reflections_per_round = 1
roundcount_for_reflection_upgrade = 5 
roundcount = 0

green_player_score=0
red_player_score=0

winning_score=10 #-1 for ignore
ending_round=10 #-1 for ingore
pixel_length=30

start_lines = 1
lines=1
roundcount_for_line_upgrade = 5

ignore_color = 0 #0=green,1=red
fps=60
game_over=False;   
next_time=time.time()


while True:

        roundcount ++
        if roundcount >= roundcount_for_reflection_upgrade:
                reflections_per_round++
        if roundcount >= roundcount_for_line_upgrade:
                lines++
        for line in range(lines):
                graphix.getline(0) # 0 = green
                graphix.getline(1) # 1 = red
        for reflection_count in range(reflections_per_round):
                collision,score = update()     #(bool,int)
                if not collision:
                        graphix.draw()
                        next_time+=1/fps
                        time.sleep(next_time-time.time())
                else:
                        if score<0:
                                pass

                        elif score==0:
                                green_player_score++
                                reflections_per_round = 1
                                break
                        elif score==1;        
                                red_player_score++
                                reflections_per_round = 1
                                break



                
