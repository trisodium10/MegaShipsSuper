# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 14:34:50 2019

@author: hayman
"""

import pyglet

from ShipsLib import *
import numpy as np

g0 = 9.81

edge_wid = 3

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
                    
                    
class projectile:
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
        self.accel = np.array([0,0,-g0])
        sprite_image = pyglet.resource.image(image)
        center_image_x(sprite_image)
        sprite_pos = np.dot(self.proj,self.pos[np.newaxis].T)[:2,0]
        self.sprite = pyglet.sprite.Sprite(sprite_image, 
                             x=sprite_pos[0], y=sprite_pos[1],
                             batch=batch,group=objects)
        if not shadow_image is None:
            shadow_image_obj = pyglet.resource.image(shadow_image)
            center_image(shadow_image_obj)
            self.shadow = pyglet.sprite.Sprite(shadow_image_obj, 
                             x=self.pos[0], y=self.pos[1],
                             batch=batch,group=shadows)
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

class game:
    def __init__(self,board_x,board_y):
        self.board_x = board_x
        self.board_y = board_y
        self.objects = []
        self.new_obj = []
        self.del_obj = []
        self.splash_list = []
        window = pyglet.window.Window()
        win_size = window.get_size()

        
        bg_vertex_list = pyglet.graphics.vertex_list(4,
            ('v2i', (edge_wid, edge_wid, edge_wid, win_size[1]-edge_wid , win_size[0]-edge_wid, win_size[1]-edge_wid, win_size[0]-edge_wid, edge_wid)),
            ('c3B', (80, 80, 235, 110, 110, 225, 140, 140, 225, 110, 110, 175))    
        )
        
    
    def update(self,dt):
        for obj in del_obj:
            del obj
        
        for obj in objects:
            obj.update(dt)
            
#        for obj in new_obj:
        

class bullet:
    def __init__(self,pos,vel,batch=None,proj=None):
        self.pos = pos
        self.vel = vel
        self.accel = np.array([0,0,-g0])
        self.state = 0  # 0 - projectile, 1 - splash stage
        bullet_image = pyglet.resource.image('bullet0.png')
        center_image(bullet_image)
        self.sprite = pyglet.sprite.Sprite(bullet_image, 
                             x=self.pos[0], y=self.pos[1],
                             batch=batch)
        self.batch = batch
#        self.vertexlist = batch.add(4,pyglet.gl.GL_QUADS,None,
#            ('v2i', (self.pos[0]-bullet_wid, self.pos[1]-bullet_wid,
#                     self.pos[0]-bullet_wid, self.pos[1]+bullet_wid,
#                     self.pos[0]+bullet_wid, self.pos[1]+bullet_wid,
#                     self.pos[0]+bullet_wid, self.pos[1]-bullet_wid)),
#            ('c3B', (20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)))
        
    def update(self,dt):
        if self.pos[2] >= 0:
            self.pos = self.pos+dt*self.vel+0.5*dt**2*self.accel
            self.vel = self.vel+dt*self.accel
            self.sprite.position = self.pos[:2]
#            print(self.pos)
#        else:
#            # delete self
        
#class splash:
#    __init__()
#            self.state += 1
#            if self.state == 1:
#                splash_image = pyglet.resource.image('splash1.png')
#                splash_image.anchor_x = splash_image.width // 2
#                self.sprite = pyglet.sprite.Sprite(splash_image, 
#                             x=self.pos[0], y=self.pos[1],
#                             batch=self.batch)
#            elif self.state < 11:
#                self.state += 1
#                self.sprite.scale_y+=1
#                if self.state > 10:
#                    self.sprite.visible = False
            
#            self.sprite.visible = False
            
            
#        self.vertexlist.verticies = [
#                     np.int(self.pos[0]-bullet_wid), np.int(self.pos[1]-bullet_wid),
#                     np.int(self.pos[0]-bullet_wid), np.int(self.pos[1]+bullet_wid),
#                     np.int(self.pos[0]+bullet_wid), np.int(self.pos[1]+bullet_wid),
#                     np.int(self.pos[0]+bullet_wid), np.int(self.pos[1]-bullet_wid)]
#        print(self.pos)
                     
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

objects = pyglet.graphics.OrderedGroup(1)
shadows = pyglet.graphics.OrderedGroup(0)

proj3D = matrix_rot3d(0,np.pi/18.0)


bullet_wid = 2
bullet_pos = np.array([400,200,1])
bullet_vel = np.array([10,5,40])

window = pyglet.window.Window()
win_size = window.get_size()
edge_wid = 10

bg_vertex_list = pyglet.graphics.vertex_list(4,
    ('v2i', (edge_wid, edge_wid, edge_wid, win_size[1]-edge_wid , win_size[0]-edge_wid, win_size[1]-edge_wid, win_size[0]-edge_wid, edge_wid)),
    ('c3B', (80, 80, 235, 110, 110, 225, 140, 140, 225, 110, 110, 175))    
)

del_obj_list = []   
create_obj_list = []   

bullet_batch = pyglet.graphics.Batch() 
splash_batch = pyglet.graphics.Batch()

#bullet_vertex_list = pyglet.graphics.vertex_list(4,
#            ('v2i', (bullet_pos[0]-bullet_wid, bullet_pos[1]-bullet_wid,
#                     bullet_pos[0]-bullet_wid, bullet_pos[1]+bullet_wid,
#                     bullet_pos[0]+bullet_wid, bullet_pos[1]+bullet_wid,
#                     bullet_pos[0]+bullet_wid, bullet_pos[1]-bullet_wid)),
#            ('c3B', (20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)))

#bullet_vertex_list = bullet_batch.add(4,pyglet.gl.GL_QUADS,None,
#            ('v2i', (bullet_pos[0]-bullet_wid, bullet_pos[1]-bullet_wid,
#                     bullet_pos[0]-bullet_wid, bullet_pos[1]+bullet_wid,
#                     bullet_pos[0]+bullet_wid, bullet_pos[1]+bullet_wid,
#                     bullet_pos[0]+bullet_wid, bullet_pos[1]-bullet_wid)),
#            ('c3B', (20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)))

#  Make a bullet
#b1 = bullet(bullet_pos,bullet_vel,batch=bullet_batch)
b1 = projectile(bullet_pos,bullet_vel,batch=bullet_batch,image='bullet0.png',
                shadow_image = 'bullet0_shadow.png',\
                objects_group=objects,\
                shadows_group=shadows,proj=proj3D,del_obj=del_obj_list)
          
# make a splash
splash_vel0 = 30
splash_velsig = splash_vel0 * 3.0/5
splash_pos = np.array([100,100,0])
#splash_list = []
#for ai in range(10):
#    splash_vel = ((np.random.randn()*splash_velsig+splash_vel0)*\
#            np.dot(matrix_rot3d(np.random.rand()*2*np.pi,np.random.randn()*np.pi/50),np.array([[0],[0],[1]]))).flatten()
#    splash_list+=[projectile(splash_pos,splash_vel,batch=splash_batch,
#                image='splash2.png',
#                shadow_image = 'splash2_shadow.png',
#                objects_group=objects,
#                shadows_group=shadows,proj=proj3D,del_obj=del_obj_list)]
splash_list = []
#splash_list = make_splash(splash_pos[0],splash_pos[1],splash_batch,objects,shadows,proj3D=proj3D,num=10,del_obj_list=del_obj_list,create_obj_list=create_obj_list)  

@window.event
def on_draw():
    window.clear()
    bg_vertex_list.draw(pyglet.gl.GL_QUADS) # draw blue background
#    b1.vertexlist.draw(pyglet.gl.GL_QUADS)
    bullet_batch.draw()
    splash_batch.draw()
#    bullet_vertex_list.draw(pyglet.gl.GL_QUADS)
    
def update(dt):
    print(del_obj_list)
    for iobj,obj in enumerate(del_obj_list):
        del del_obj_list[iobj]        
        
    
    if b1.update(dt):
        splash_list=make_splash(b1.pos[0],b1.pos[1],splash_batch,objects,shadows,proj3D=proj3D,num=10,del_obj_list=del_obj_list,create_obj_list=create_obj_list)  

    
    for splsh in splash_list:
        splsh.update(dt)

    
pyglet.clock.schedule_interval(update, 1/60.)
pyglet.app.run()
