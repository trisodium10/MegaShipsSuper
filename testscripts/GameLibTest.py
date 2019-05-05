# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:06:49 2019

@author: hayman
"""

import pyglet
from pyglet.window import mouse

#from ShipsLib import *
from GameLib import *

import numpy as np


g1 = game()
g1.add_player()
g1.add_ship(400,300,player_sel=None)

@g1.board.window.event
def on_draw():
    g1.board.window.clear()
    g1.board.bg_vertex_list.draw(pyglet.gl.GL_QUADS) # draw blue background
    g1.batch_draw()
    
    
def update(dt):
    g1.update(dt)
#    s1.update(dt)
    
    
@g1.board.window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        g1.active_player.ships[0].move(x,y)
#    elif button == mouse.RIGHT:
#        splash1.position=(x,y)
#        splash1.visible = True
        
pyglet.clock.schedule_interval(update, 1/60.)
#pyglet.clock.schedule_interval(update_splash,1/2.0)
pyglet.app.run()