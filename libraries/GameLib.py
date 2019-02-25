# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 12:48:50 2019

@author: hayman

game modules for ships

"""
bullet_wid = 1  # bullet radius in pixels

import pyglet
from ShipsLib import *


class game:
    def __init__(self,size,players):
        self.board = board(size)
        self.players = players
        self.stage = 'set'  # player sets action
    def change_stage(self,newstage):
        """
        stages:
            fire - animate a fire event
            move - animate a move event
            set - user updates events
        """
        self.stage = newstage

class board:
    def __init__(self,size):
        self.size = size


class fire:
    """
    Cannon fire animation
    """
    def __init__(self,pos,vel,target):
        """
        pos - [x,y,z] - initial x,y,z position
        vel - [vx,vy,vz] velocity vector
        target - [x,y] - targeted position
        """
        self.pos = pos
        self.vel = vel
        self.target = target
        self.spalsh = False
        self.terminate = False
        self.sprite = None
    
    def start(self,batch=None):
        bullet_vertex_list = pyglet.graphics.vertex_list(4,
            ('v2i', (self.pos[0]-bullet_wid, self.pos[1]-bullet_wid,
                     self.pos[0]-bullet_wid, self.pos[1]+bullet_wid,
                     self.pos[0]+bullet_wid, self.pos[1]+bullet_wid,
                     self.pos[0]+bullet_wid, self.pos[1]-bullet_wid)),
            ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
        bullet_vertex_list = batch.add(2, pyglet.gl.GL_POINTS, custom_group,
    ('v2i', (10, 15, 30, 35)),
    ('c3B', (0, 0, 255, 0, 255, 0))
)
        
#        bullet_image = pyglet.resource.image('bullet0.png')
#        shadow_image = pyglet.resource.image('bullet_shadow0.png')
#        center_image(bullet_image)
#        center_image(shadow_image)
#        self.sprite = pyglet.sprite.Sprite(ship_image, 
#                             x=self.coords[0,0], y=self.coords[1,0],
#                             batch=batch)
#        self.opacity = 0
#        self.sprite.rotation=self.theta
#        self.sprite.scale = 0.05
#        self.visible = True
        
    def update(self,dt):
        if self.Terminate:
            self.sprite = update
        else:
            self.pos += self.vel*dt
            if self.pos[2] <= 0:
                self.terminate = True
        
        