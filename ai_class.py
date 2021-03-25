import numpy as np
import math
import random
from collections import deque

class ai():

    def __init__(self, d_range, road, pos): #y and x refer to starting coordinates
        self.d_range = d_range
        
        self.sensor_stack = deque()
        
        self.knowledge = {}
        self.road = road
        self.char_pos = pos #position of character
        self.knowledge_learnt_in_round = {}
        


    def detect_obstacles(self):
        curr_obst = []
        for i in range(-self.d_range, self.d_range+1):
            y_coord = self.char_pos[0] - i
            if y_coord >= 0 and y_coord < len(self.road):
                for j in range(-self.d_range, self.d_range+1):
                    x_coord = self.char_pos[1]-j
                    if x_coord >= 0 and x_coord < len(self.road[0]):

                        if self.road[y_coord,x_coord] != '^':
                            curr_obst.append((i,j,self.road[y_coord,x_coord]))
        curr_obst = tuple(curr_obst) #all detected obstacles 

        if self.knowledge.get(hash(curr_obst)) is None: #check if the knowledge bank for has this combo
            new_detection = weights(curr_obst)
            self.knowledge[hash(curr_obst)] = new_detection


        if self.knowledge_learnt_in_round.get(hash(curr_obst)) is None: #check if the knowledge bank for current round has this combo, and will put in temp knowledge bank
            self.knowledge_learnt_in_round[hash(curr_obst)] = self.knowledge[hash(curr_obst)]
                            
                            
        self.sensor_stack.append(self.knowledge.get(hash(curr_obst)))
        if len(self.sensor_stack) == 4:
            ttuple = self.sensor_stack[0].combo        
            self.knowledge_learnt_in_round[hash(ttuple)].actions[0][1] += 0.05 #this gets the played action in according to the obstacle combination and rewards it
            self.sensor_stack.popleft()
            

    
    def make_move(self):
        action_list = self.sensor_stack[-1].actions
        
        return(action_list[0][0])

    def update_position(self,y,x):
        
        self.char_pos[0] = y
        self.char_pos[1] = x

    def punish(self): #punishes the three most recent moves
        combo1 = None
        combo2 = None
        combo3 = None
        if len(self.sensor_stack) > 0:
            combo1 = self.sensor_stack[0].combo
            self.knowledge_learnt_in_round[hash(combo1)].actions[0][1] = 0 #punishes the most recently played move heavily as it guarantees instant death

            

        if len(self.sensor_stack) > 1:
            combo2 = self.sensor_stack[1].combo
            self.knowledge_learnt_in_round[hash(combo2)].actions[0][1] -= 0.7
            if self.knowledge_learnt_in_round[hash(combo2)].actions[0][1] < 0:
                self.knowledge_learnt_in_round[hash(combo2)].actions[0][1] = 0

        if len(self.sensor_stack) > 2:     
            combo3 = self.sensor_stack[2].combo 
            self.knowledge_learnt_in_round[hash(combo3)].actions[0][1] -= 0.45
            
            if self.knowledge_learnt_in_round[hash(combo3)].actions[0][1] < 0:
                self.knowledge_learnt_in_round[hash(combo3)].actions[0][1] = 0

        return combo1, combo2, combo3

        


    def return_coord(self):
        return self.sensor_stack[-1].combo
           

    def reset(self, road, char):

        for hash_combo, weight in self.knowledge_learnt_in_round.items():
            sorted_array = weight.sort_in_place() #sort weighted actions correctly
            self.knowledge[hash_combo].actions = sorted_array        


        for i in range(len(self.sensor_stack)):
            self.sensor_stack.popleft() #pops all values off sensor stack
            

        self.knowledge_learnt_in_round = {}
        self.road = road
        self.char_pos = char
        





class weights(): #stores all possible sensor pickups and rates moves
    def __init__(self, combo):
        self.combo = combo
        self.actions = [['Go straight',1],['Go left',1],['Go right',1],['Go back',1],['Do nothing',1]] #stores all possible actions and their weights


    def sort_in_place(self):
        self.actions.sort(key = lambda x: x[1], reverse=True)
        
        a = self.actions[0][1]
        for i in self.actions:
            if a != 0:
                i[1] = float(i[1] / a) #to regularise and not make numbers too big
            else:
                i[1] = 1
        return self.actions








    
        

    