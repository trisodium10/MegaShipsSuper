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

def center_image_x(image):
    image.anchor_x = image.width // 2
#    image.anchor_y = image.height

class game:
    def __init__(self):
        self.board = board()
        
        pyglet.resource.path = ['../resources']
        pyglet.resource.reindex()
        
        # initialize graphic object grouping
        self.objects_group = pyglet.graphics.OrderedGroup(1)
        self.shadows_group = pyglet.graphics.OrderedGroup(0)
        
        self.bullet_batch = pyglet.graphics.Batch() 
        self.splash_batch = pyglet.graphics.Batch()
        
        self.proj3D = matrix_rot3d(0,np.pi/18.0)        
        
        self.players = []
        self.active_player = None
        
        # list of all ships in the board
        self.ships = []
#        self.active_player = players[0]
        
        self.bullets = []
        self.splashes = []
        
    def add_player(self,name=None,base_loc=None):
        if name is None:
            name = 'Player '+str(len(self.players)+1)
        
        if base_loc is None:
            base_loc = base_location(self.board,len(self.players))        
            
        self.players+=[player(name,base_loc)]
        if self.active_player is None:
            self.active_player = self.players[0]
        
        #        self.stage = 'set'  # player sets action
    def next_player(self):
        # change turn to next player in the list
        next_player_index = self.players.index(self.active_player)+1
        if next_player_index >= len(self.players):
            next_player_index = 0
        
        self.active_player = self.players[next_player_index]
        # reset the movement for all of the player's ships
        for s in self.active_player.ships:
            s.reset_movement()
        print(self.active_player)
    
    def set_projection(self,theta,phi):
        self.proj3D = matrix_rot3d(theta,phi)
        
    def add_ship(self,ship_len=3,player_sel=None,loc=None):
        # add a ship to the current active player
        if player_sel is None:
            player_sel = self.active_player
    
        if loc is None:
            loc=((player_sel.base_loc[0][0]-player_sel.base_loc[1][0])*np.random.rand()+player_sel.base_loc[1][0],
                 (player_sel.base_loc[0][1]-player_sel.base_loc[3][1])*np.random.rand()+player_sel.base_loc[3][1])
        
        self.ships+=[ship(loc[0],loc[1],player=player_sel)] # define a default ship
        for ai in range(ship_len):
            self.ships[-1].push_segment(segment(0))
        self.ships[-1].update_ship()
        player_sel.add_ship(self.ships[-1])
        
#        if player_sel is None:
#            self.active_player.add_ship(self.ships[-1])
#        else:
#            player_sel.add_ship(self.ships[-1])
        
    def batch_draw(self):
        for p in self.players:
            p.batch.draw()
        self.bullet_batch.draw()
        self.splash_batch.draw()
            
    def update(self,dt):
        for s in self.ships:
            s.update(dt)
            
        for iobj,obj in enumerate(self.bullets):
            obj.update(dt)
#            print(obj.pos)
            # check for hit ship
            for s in self.ships: 
                # if the ship is at all close to the bullet, evaluate for
                # a hit
                if np.sum((s.coords.flatten()-np.array(obj.pos[:2]))**2) < 20**2:
#                    print(s.coords.flatten())
#                    print(s.test_hit(obj.pos))
                    hit,iseg=s.test_hit(obj.pos)
                    if hit:
                        s.Segments[iseg].apply_damage(obj.damage)
                        print('hit')
                        print(s)
                        print('Segment')
                        print(iseg)
                        self.bullets.remove(obj)
#                        self.make_explosion(obj.pos[0],obj.pos[1])
            
            if obj.pos[2] < 0:
                self.bullets.remove(obj)
                self.make_splash(obj.pos[0],obj.pos[1])
        
        for obj in self.splashes:
            obj.update(dt)
            if obj.pos[2] < 0:
                self.splashes.remove(obj)
            
    def make_bullet(self,bullet_pos,bullet_vel,damage):
        self.bullets+=[bullet(bullet_pos,bullet_vel,damage,batch=self.bullet_batch,
                objects_group=self.objects_group,\
                shadows_group=self.shadows_group,proj=self.proj3D)]       
                
    def make_splash(self,x,y,num=10):
        self.splashes+=make_splash(x,y,self.splash_batch,self.objects_group,
                                    self.shadows_group,proj3D=self.proj3D,num=num)
            
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
        self.vertices = (edge_wid, edge_wid, 
                          edge_wid, win_size[1]-edge_wid , 
                          win_size[0]-edge_wid, win_size[1]-edge_wid, 
                          win_size[0]-edge_wid, edge_wid)

        
        self.bg_vertex_list = pyglet.graphics.vertex_list(4,
            ('v2i', self.vertices),
            ('c3B', (80, 80, 235, 110, 110, 225, 140, 140, 225, 110, 110, 175))
            )  
        
class player:
    def __init__(self,name,base_loc):
        self.ships = []     # list of player's ships
        self.money = 10     # initial money player starts with
        self.batch = pyglet.graphics.Batch()  # create a batch object for the player's objects
        self.name = name
        self.base_loc = list(base_loc) # vertex locations of the base
        
    def add_ship(self,ship):
        # Add a ship object to the list of ships belonging to this player
        self.ships+=[ship]
        self.ships[-1].add_to_board(batch = self.batch)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name


#class fire:
#    """
#    Cannon fire animation
#    """
#    def __init__(self,pos,vel,target):
#        """
#        pos - [x,y,z] - initial x,y,z position
#        vel - [vx,vy,vz] velocity vector
#        target - [x,y] - targeted position
#        """
#        self.pos = pos
#        self.vel = vel
#        self.target = target
#        self.spalsh = False
#        self.terminate = False
#        self.sprite = None
#    
#    def start(self,batch=None):
#        bullet_vertex_list = pyglet.graphics.vertex_list(4,
#            ('v2i', (self.pos[0]-bullet_wid, self.pos[1]-bullet_wid,
#                     self.pos[0]-bullet_wid, self.pos[1]+bullet_wid,
#                     self.pos[0]+bullet_wid, self.pos[1]+bullet_wid,
#                     self.pos[0]+bullet_wid, self.pos[1]-bullet_wid)),
#            ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
#        bullet_vertex_list = batch.add(2, pyglet.gl.GL_POINTS, custom_group,
#    ('v2i', (10, 15, 30, 35)),
#    ('c3B', (0, 0, 255, 0, 255, 0))
#)
        
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
        


class projectile(object):
    def __init__(self,pos,vel,batch=None,proj=None,image=None,shadow_image=None,
                 objects_group=None,shadows_group=None,del_obj=None,create_obj=None):
        if proj is None:
            self.proj = np.eye(3)
        else:
            self.proj = proj
            
        if image is None:
            self.image = 'bullet0.png'
            
        self.del_obj = del_obj

        self.pos = pos
        self.vel = vel
        self.accel = np.array([0,0,-g])
        sprite_image = pyglet.resource.image(image)
        center_image_x(sprite_image)
        sprite_pos = np.dot(self.proj,self.pos[np.newaxis].T)[:2,0]
        self.sprite = pyglet.sprite.Sprite(sprite_image, 
                             x=sprite_pos[0], y=sprite_pos[1],
                             batch=batch,group=objects_group)
        if not shadow_image is None:
            shadow_image_obj = pyglet.resource.image(shadow_image)
            center_image(shadow_image_obj)
            self.shadow = pyglet.sprite.Sprite(shadow_image_obj, 
                             x=self.pos[0], y=self.pos[1],
                             batch=batch,group=shadows_group)
        else:
            self.shadow=None
    def update(self,dt):
        if self.pos[2] >= 0:
            self.pos = self.pos+dt*self.vel+0.5*dt**2*self.accel
            self.vel = self.vel+dt*self.accel
            self.sprite.position = np.dot(self.proj,self.pos[np.newaxis].T)[:2,0]
            if not self.shadow is None:
                self.shadow.position = self.pos[:2]
        else:
            self.sprite.visible=False
            if not self.shadow is None:
                self.shadow.visible=False
#            if not self.terminate_fun is None:
#                self.terminate_fun(self.pos[0],self.pos[1])
            if not self.del_obj is None:
                # delete this object
                self.del_obj+=[self]

class bullet(projectile):
    def __init__(self,pos,vel,damage,batch=None,proj=None,objects_group=None,shadows_group=None,del_obj=None,create_obj=None):
        shadow_image = 'bullet0_shadow.png'
        bullet_image = 'bullet0.png'
        super(bullet,self).__init__(pos,vel,batch=batch,proj=proj,image=bullet_image,shadow_image=shadow_image,
                 objects_group=objects_group,shadows_group=shadows_group,del_obj=del_obj,create_obj=create_obj)   
        self.damage = damage

    def update(self,dt):
        super(bullet,self).update(dt)
#        if self.pos[2] <= 0:
#            make_splash(self.pos[0],self.pos[1],splash_batch,objects,shadows,)
        
    
def make_splash(x,y,splash_batch,objects,shadows,proj3D=None,num=10,del_obj_list=None,create_obj_list=None):
    if proj3D is None:
        proj3D = np.eye(3)
        
    splash_vel0 = 50
    splash_velsig = 3
    splash_pos = np.array([x,y,0])
    splash_list = []
    for ai in range(num):
        splash_vel = ((np.random.randn()*splash_velsig+splash_vel0)*\
                np.dot(matrix_rot3d(np.random.rand()*2*np.pi,np.random.randn()*np.pi/50),np.array([[0],[0],[1]]))).flatten()
        splash_list+=[projectile(splash_pos,splash_vel,batch=splash_batch,
                    image='splash2.png',
                    shadow_image = 'splash2_shadow.png',
                    objects_group=objects,
                    shadows_group=shadows,proj=proj3D,del_obj=del_obj_list)]
    return splash_list
    
def base_location(board,player_num,base_len=40):
    # return the verticies of the base location for player number player_num
    # given a board
    # player_num is base zero
    # base_len: length of a side for the base


    if player_num == 0:
        base_vertices = [(board.vertices[0],board.vertices[1])]
        base_vertices+= [(board.vertices[0]+base_len,board.vertices[1])]
        base_vertices+= [(board.vertices[0]+base_len,board.vertices[1]+base_len)]
        base_vertices+= [(board.vertices[0],board.vertices[1]+base_len)]
        
    elif player_num == 1:
        base_vertices = [(board.vertices[4],board.vertices[5])]
        base_vertices+= [(board.vertices[4]-base_len,board.vertices[5])]
        base_vertices+= [(board.vertices[4]-base_len,board.vertices[5]-base_len)]
        base_vertices+= [(board.vertices[4],board.vertices[5]-base_len)]
        
    elif player_num == 2:
        base_vertices = [(board.vertices[2],board.vertices[3])]
        base_vertices+= [(board.vertices[2]+base_len,board.vertices[3])]
        base_vertices+= [(board.vertices[2]+base_len,board.vertices[3]-base_len)]
        base_vertices+= [(board.vertices[2],board.vertices[3]-base_len)]
        
    elif player_num == 3:
        base_vertices = [(board.vertices[6],board.vertices[7])]
        base_vertices+= [(board.vertices[6]-base_len,board.vertices[7])]
        base_vertices+= [(board.vertices[6]-base_len,board.vertices[7]+base_len)]
        base_vertices+= [(board.vertices[6],board.vertices[7]+base_len)]
        
    elif player_num == 4:
        base_vertices = [(board.board_x/2,board.vertices[1])]
        base_vertices+= [(board.board_x/2-base_len,board.vertices[1])]
        base_vertices+= [(board.board_x/2-base_len,board.vertices[1]+base_len)]
        base_vertices+= [(board.board_x/2,board.vertices[1]+base_len)]
        
    elif player_num == 5:
        base_vertices = [(board.board_x/2,board.vertices[3])]
        base_vertices+= [(board.board_x/2-base_len,board.vertices[3])]
        base_vertices+= [(board.board_x/2-base_len,board.vertices[3]+base_len)]
        base_vertices+= [(board.board_x/2,board.vertices[3]+base_len)]
        
    return base_vertices
        