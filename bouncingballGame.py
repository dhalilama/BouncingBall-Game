#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 03:32:49 2018
author: Ajay Dhaliwal
"""
import Tkinter as Tk
import random as rd
import math

WIDTH = 800
HEIGHT = 500
RADIUS = 25
color = "black"
MAX_SPEED = 8
MIN_SPEED = 5

class Ball(object):
    def __init__(self, canvas,pos_x, pos_y):
        self.speed = [rd.uniform(MIN_SPEED,MAX_SPEED), 
                      rd.uniform(MIN_SPEED,MAX_SPEED)]
        self.canvas = canvas
        self.shape = self.canvas.create_oval(pos_x, pos_y, 
                                        pos_x+2*RADIUS, pos_y+2*RADIUS, fill=color)
        self.pos = self.canvas.coords(self.shape)
        self.center_x = (self.pos[0]+self.pos[2])*0.5
        self.center_y = (self.pos[1]+self.pos[3])*0.5

    def ball_update(self):
        self.pos = self.canvas.coords(self.shape)
        self.center_x = (self.pos[0]+self.pos[2])*0.5
        self.center_y = (self.pos[1]+self.pos[3])*0.5
        if self.pos[2] >= WIDTH or self.pos[0] <= 0:
            self.speed[0] *= -1
        if self.pos[3] >= HEIGHT or self.pos[1] <= 0:
            self.speed[1] *= -1
        for i in range(2):
            if abs(self.speed[i]) > MAX_SPEED:
                self.speed[i]*= 0.9
            elif abs(self.speed[i]) < MIN_SPEED:
                self.speed[i]*= 1.1
        self.canvas.move(self.shape, self.speed[0], self.speed[1])
        

class BallGame(object):
    def __init__(self, master):
        self.master = master
        self.canvas = Tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="grey")
        self.canvas.pack()
        self.points = 10
        self.label = Tk.Label(master, text="%d points!" % self.points)
        self.label.pack()
        self.label.place(x=170, y=HEIGHT-20)
        self.button = Tk.Button(master, text="Spawn a ball", 
                   command = self.ball_spawner, height = 5, width = 10)
        self.button.pack()
        self.canvas.bind("<Button-1>", self.rectangle)
        self.Ball_group = []
        self.active = True
        self.move_active()
    
    def ball_spawner(self):
        a_ball = Ball(self.canvas, rd.uniform(2*RADIUS,WIDTH-2*RADIUS),rd.uniform(2*RADIUS,HEIGHT-2*RADIUS))
        self.Ball_group.append(a_ball)
        self.points -= 1
        self.update_label()
        
    def update_label(self):
        self.label["text"] = "%d points" % self.points
        self.master.after(50, self.update_label)
        
    def rectangle(self, event):
        hit = self.canvas.create_rectangle(event.x,event.y, event.x+20, event.y+20, fill="red")
        clicked_group = {ball for ball in self.Ball_group if event.x <= ball.pos[2] 
                        and event.x >= ball.pos[0] and event.y <= ball.pos[3] 
                        and event.y >= ball.pos[1]}
        if len(clicked_group):
            print "Got one!"
            self.points +=  1
        else:
            print "You missed!"
            self.points -= 1
            self.canvas.delete(hit)
        self.update_label()

    def dist(self, p, q, speed_p, speed_q):
        center_px = 0.5*(p[0]+p[2])+speed_p[0]
        center_py = 0.5*(p[1]+p[3])+speed_p[1]
        center_qx = 0.5*(q[0]+q[2])+speed_q[0]
        center_qy = 0.5*(q[1]+q[3])+speed_q[1]
        return math.sqrt((center_px - center_qx) ** 2 + (center_py - center_qy) ** 2)    
  
    def collide(self):
        num_balls = len(self.Ball_group)
        for i in range(num_balls):
            for j in range(i+1, num_balls):
                ball1 = self.Ball_group[i]
                ball2 = self.Ball_group[j]
                d =  self.dist(ball1.pos, ball2.pos, ball1.speed, ball2.speed)
                if d < 2*RADIUS:
                    nx = (ball2.center_x-ball1.center_x)/d
                    ny = (ball2.center_y-ball1.center_y)/d
                    p = ball1.speed[0] * nx + ball1.speed[1] * ny 
                    - ball2.speed[0] * nx - ball2.speed[1] * ny
                    ball1.speed[0] -= p * nx
                    ball2.speed[1] -= p * ny
                    ball2.speed[0] += p * nx
                    ball2.speed[1] += p * ny
                    
    def move_active(self):
        if self.active:
            self.collide()
            for ball in self.Ball_group:
                ball.ball_update()
            self.master.after(20, self.move_active)
            
                    
def main(): 
    root = Tk.Tk()
    game = BallGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
