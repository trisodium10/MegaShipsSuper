# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 18:32:44 2019

@author: hayman
"""

import pyglet

from ShipsLib import *


import numpy as np




window = pyglet.window.Window()


## Hello World
#label = pyglet.text.Label('Hello, world',
#                          font_name='Times New Roman',
#                          font_size=36,
#                          x=window.width//2, y=window.height//2,
#                          anchor_x='center', anchor_y='center')
#@window.event
#def on_draw():
#    window.clear()
#    label.draw()
    


## view image
##image = pyglet.resource.image('kitten.png')
#image = pyglet.image.load('/home/hayman/c/TestConfig/cute_cat.jpg')
#
#@window.event
#def on_draw():
#    window.clear()
#    image.blit(0, 0)


# draw a triangle with a vertex list and different color verticies    
from pyglet.window import mouse

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

p1_batch = pyglet.graphics.Batch()  # player 1 pieces

ship_len = 3
s1 = ship(400,300) # define a default ship
for ai in range(ship_len):
    s1.push_segment(segment(0))
s1.update_ship()
s1.add_to_board(batch=p1_batch)


win_size = window.get_size()
edge_wid = 10
vertex_list = pyglet.graphics.vertex_list(4,
    ('v2i', (edge_wid, edge_wid, edge_wid, win_size[1]-edge_wid , win_size[0]-edge_wid, win_size[1]-edge_wid, win_size[0]-edge_wid, edge_wid)),
    ('c3B', (10, 10, 105, 80, 80, 225, 40, 40, 225, 0, 0, 175))    
)

splash_batch = pyglet.graphics.Batch()  # player 1 pieces
# initialize the splash sequence
splash = pyglet.resource.image('splash0.png')
splash_seq = pyglet.image.ImageGrid(splash, 1, 6)
splash_animation = splash_seq.get_animation(500,loop=True)
#splash1 = pyglet.sprite.Sprite(splash_animation, 
#                             x=200, y=200,batch=splash_batch)
splash1 = pyglet.sprite.Sprite(splash_seq[2], 
                             x=500, y=500,batch=splash_batch)
splash1.scale = 3
splash1.opacity = 0
splash1.visible=True


#texture_grid = pyglet.image.TextureGrid(splash_seq)

@window.event
def on_draw():
    window.clear()
    vertex_list.draw(pyglet.gl.GL_QUADS) # draw blue background
    p1_batch.draw()  # draw all ships in player 1 batch
    splash_batch.draw()
    
    
def update(dt):
    s1.update(dt)
    
    

    
@window.event
def on_mouse_press(x, y, button, modifiers):
    global draw_splash
    if button == mouse.LEFT:
        s1.move(x,y)
    elif button == mouse.RIGHT:
        splash1.position=(x,y)
        splash1.visible = True
        
pyglet.clock.schedule_interval(update, 1/60.)
#pyglet.clock.schedule_interval(update_splash,1/2.0)
pyglet.app.run()
