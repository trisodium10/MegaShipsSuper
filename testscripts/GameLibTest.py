# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:06:49 2019

@author: hayman
"""

import pyglet
from pyglet.window import mouse

from ShipsLib import *
from GameLib import *

import numpy as np


g1 = game()                     # create the game
g1.add_player()                 # create a player
g1.add_ship(400,300,player_sel=None)  # create a ship for the active player
g1.active_player.ships[0].add_cannon(cannon())  # add a default cannon to the ship

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
    elif button == mouse.RIGHT:
        bullet_pos = np.concatenate((g1.active_player.ships[0].coords.flatten(),
                                     np.zeros(1)))
        bullet_vel = np.array([x-g1.active_player.ships[0].coords[0,0],
                                     y-g1.active_player.ships[0].coords[1,0],
                                     0])
        bullet_vel = bullet_vel/np.sqrt(np.sum(bullet_vel**2))
        bullet_vel[2] = 4
        bullet_vel = bullet_vel*15
                      
        g1.make_bullet(bullet_pos,bullet_vel)
#        splash1.position=(x,y)
#        splash1.visible = True
        
pyglet.clock.schedule_interval(update, 1/60.)
#pyglet.clock.schedule_interval(update_splash,1/2.0)
pyglet.app.run()