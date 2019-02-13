# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 18:32:44 2019

@author: hayman
"""

import pyglet


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

vertex_list = pyglet.graphics.vertex_list(3,
    ('v2i', (10, 10, 10, 40 , 20, 20)),
    ('c3B', (0, 0, 255, 0, 255, 0, 0, 255, 0))
    
)

vertex_index = 0
l_vertex = 2
n_vertex = 3

@window.event
def on_draw():
    window.clear()
    vertex_list.draw(pyglet.gl.GL_TRIANGLES)
    
@window.event
def on_mouse_press(x, y, button, modifiers,vertex_index):
    if button == mouse.LEFT:
        vertex_list.vertices[vertex_index*l_vertex:(1+vertex_index)*l_vertex-1] = [x,y]
    elif button == mouse.RIGHT:
        vertex_index+=1
        vertex_index = np.mod(vertex_index,n_vertex)
    return vertex_index
        
    
pyglet.app.run()
