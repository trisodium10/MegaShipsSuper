# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 12:48:50 2019

@author: hayman

game modules for ships

"""
bullet_wid = 1  # bullet radius in pixels

import pyglet
from ShipsLib import *

def matrix_rot3d(theta,phi):
    return np.dot(np.array([[np.cos(theta),np.sin(theta),0],\
                            [-np.sin(theta),np.cos(theta),0],\
                            [0,0,1]]),
                  np.array([[1,0,0],\
                            [0,np.cos(phi),np.sin(phi)],\
                            [0,-np.sin(phi),np.cos(phi)]]),
                  )


class game:
    def __init__(self):
        self.board = board()
        
        pyglet.resource.path = ['../resources']
        pyglet.resource.reindex()
        
        # initialize graphic object grouping
        self.objects_group = pyglet.graphics.OrderedGroup(1)
        self.shadows_group = pyglet.graphics.OrderedGroup(0)
        
        self.proj3D = matrix_rot3d(0,np.pi/18.0)        
        
        self.players = []
        self.active_player = None
        
        # list of all ships in the board
        self.ships = []
#        self.active_player = players[0]
        
    def add_player(self,name=None):
        if name is None:
            name = 'Player '+str(len(self.players)+1)
        self.players+=[player(name)]
        if self.active_player is None:
            self.active_player = self.players[0]
        
        #        self.stage = 'set'  # player sets action
    
    def set_projection(self,theta,phi):
        self.proj3D = matrix_rot3d(theta,phi)
        
    def add_ship(self,x,y,ship_len=3,player_sel=None):
        # add a ship to the current active player
        self.ships+=[ship(400,300)] # define a default ship
        for ai in range(ship_len):
            self.ships[-1].push_segment(segment(0))
        self.ships[-1].update_ship()
        if player_sel is None:
            self.active_player.add_ship(self.ships[-1])
        else:
            player_sel.add_ship(self.ships[-1])
        
    def batch_draw(self):
        for p in self.players:
            p.batch.draw()
            
    def update(self,dt):
        for s in self.ships:
            s.update(dt)
#    def change_stage(self,newstage):
#        """
#        stages:
#            fire - animate a fire event
#            move - animate a move event
#            set - user updates events
#        """
#        self.stage = newstage
        



class board:
    def __init__(self):
#        self.board_x = size[0]
#        self.board_y = size[1]
        self.objects = []
        self.new_obj = []
        self.del_obj = []
        self.splash_list = []
        self.window = pyglet.window.Window()
        win_size = self.window.get_size()
        edge_wid = 10
        self.board_x = win_size[0]
        self.board_y = win_size[1]

        
        self.bg_vertex_list = pyglet.graphics.vertex_list(4,
            ('v2i', (edge_wid, edge_wid, edge_wid, win_size[1]-edge_wid , win_size[0]-edge_wid, win_size[1]-edge_wid, win_size[0]-edge_wid, edge_wid)),
            ('c3B', (80, 80, 235, 110, 110, 225, 140, 140, 225, 110, 110, 175))
            )  
        
class player:
    def __init__(self,name):
        self.ships = []     # list of player's ships
        self.money = 10     # initial money player starts with
        self.batch = pyglet.graphics.Batch()  # create a batch object for the player's objects
        self.name = name
        
    def add_ship(self,ship):
        # Add a ship object to the list of ships belonging to this player
        self.ships+=[ship]
        self.ships[-1].add_to_board(batch = self.batch)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name


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
        
        