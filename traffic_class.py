import numpy as np
import os
import math
import random
import time

class traffic():

    def __init__(self,length,width,prob):
        self.length = length
        self.width = width+2
        self.prob = prob
        self.road = np.zeros(length*(width+2),dtype='object').reshape(length,width+2) #dimensions of new road. 0 = no car, X = car
        self.cars = []
        self.wall = []
        self.char = [int((length+1)/2)-1, int((width+3)/2)-1]
        self.road[self.char[0],self.char[1]] = '^'
        self.clear = lambda: os.system('cls')
        self.state = 'Pending'
        for i in range(length):
            self.wall.append([i,0])
            self.wall.append([i,self.width-1])
            self.road[i,0] = '|'
            self.road[i,self.width-1] = '|'

        
    
    def reset(self):
        self.road = np.zeros(self.length*self.width,dtype='object').reshape(self.length,self.width)
        self.cars = []
        self.wall = []
        self.char = [int((self.length+1)/2)-1, int((self.width+1)/2)-1]
        self.road[self.char[0],self.char[1]] = '^'
        self.state = 'Pending'
        for i in range(self.length):
            self.wall.append([i,0])
            self.wall.append([i,self.width-1])
            self.road[i,0] = '|'
            self.road[i,self.width-1] = '|'
        return self.road, self.char


    def next(self):

        if self.state == 'Pending':
            
            front_car_danger = False
            
            for c in self.cars:
                self.road[c[0],c[1]] = 0 #removing the visualisation of previous cars
                c[0] = c[0] + 1

                

                

            if random.random() <= self.prob:
                a = random.randint(1,self.width-2)
                self.cars.append([0,a])
                self.road[0,a] = 'X'

            
            self.car_check()
            self.car_add()
            
            self.crash_check(self.char[0],self.char[1])
           
    def crash_check(self,y,x):
        if self.road[y,x] != 0 and self.road[y,x] != '^':
            self.state = 'Fail'
            return True

    def car_check(self):
        for c in self.cars:
            if c[0] == self.length:
                self.cars.remove(c)  

    def car_add(self):
        for c in self.cars:
            self.road[c[0],c[1]] = 'X' #adding new cars

    def visualise(self):
        
        self.clear()
        for row in self.road:
            for item in row:
                print(item,end=' ')
            print()

        #print(self.char)
        #print(self.cars)
        print(self.state)


    def validity_check(self):
        for c in self.cars:
            print(c,self.char)
    


    def make_move(self, move): #movement control of game: 1 move at a time
        y = self.char[0]
        x = self.char[1]
        if move == 'Go right':
            x = self.char[1]+1
        elif move == 'Go left':
            x = self.char[1]-1
        elif move == 'Go straight':
            if self.char[0]-1 >= 0:
                y = self.char[0]-1
        elif move == 'Go back':
            if self.char[0]+1 < self.length:
                y = self.char[0]+1

        if move != 'Do nothing':  #will not do the following unless necessary
            self.crash_check(y,x) #checks for collision with edge of road and cars
            self.road[self.char[0],self.char[1]] = 0
            self.char[0] = y
            self.char[1] = x
            self.road[y,x] = '^'

        return y,x   


    
if __name__ == '__main__':
    test_road = traffic(5,5,1)
    for i in range(10):
        test_road.next()
        test_road.visualise()        
        time.sleep(0.5)
    

