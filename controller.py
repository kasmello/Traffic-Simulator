from traffic_class import traffic
from ai_class import ai
import time
import sys
import os

clear = lambda: os.system('cls')

if len(sys.argv) == 1:
    clear()
    test_road = traffic(5,5,0.9)
    test_ai = ai(1, test_road.road, test_road.char)
    try_no = 1

    while test_road.state != 'Success':
        print('Try number ' + str(try_no))
        time.sleep(0.005)

        

        
        test_road.visualise() 
        time.sleep(0.005)
        


        for i in range(100):
            if test_road.state == 'Fail':
                c1, c2, c3 = test_ai.punish()
                print('PUNISHED:')
                print(c1)
                print(c2)
                print(c3)
                road, char = test_road.reset()
                test_ai.reset(road, char)
                print('TRIES LASTED: ' + str(i))
                time.sleep(0.005)
                try_no += 1
                
                
                break
            else:
                
                test_ai.detect_obstacles()

                print('Currently detected obstacles:')
                print(test_ai.return_coord())
                time.sleep(0.005)

                move = test_ai.make_move()
                y,x = test_road.make_move(move)
                test_ai.update_position(y,x)
                if test_road.state != 'Fail':
                    test_road.next()
                test_road.visualise() 
                time.sleep(0.005)
                
            if i == 99 and test_road.state != 'Fail':               
                

                test_road.state = 'Success'
                print('Success')

