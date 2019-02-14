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

s1.add_to_board(batch=p1_batch)


win_size = window.get_size()
edge_wid = 10
vertex_list = pyglet.graphics.vertex_list(4,
    ('v2i', (edge_wid, edge_wid, edge_wid, win_size[1]-edge_wid , win_size[0]-edge_wid, win_size[1]-edge_wid, win_size[0]-edge_wid, edge_wid)),
    ('c3B', (0, 0, 155, 0, 0, 175, 0, 0, 205, 0, 0, 255))
    
)


@window.event
def on_draw():
    window.clear()
    vertex_list.draw(pyglet.gl.GL_QUADS)
    p1_batch.draw()
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        pass
    elif button == mouse.RIGHT:
        pass
        
    
pyglet.app.run()
