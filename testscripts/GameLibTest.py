# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:06:49 2019

@author: hayman
"""

import os
import sys

import pyglet
from pyglet.window import mouse
from pyglet.window import key

# set path to megashipsuper libraries
dirP_str = os.path.abspath(__file__+'/../../libraries')
# dirP_str = os.path.abspath('../../libraries')
if dirP_str not in sys.path:
    sys.path.append(dirP_str)
print()
print(dirP_str)
print()

from ShipsLib import *
from GameLib import *

import numpy as np


g1 = game()                     # create the game
g1.add_player()                 # create a player
g1.add_player()                 # create another player

# give each player a ship with cannon and shot
for player in g1.players:
    g1.add_ship(player_sel=player,ship_len=20)  # create a ship for the active player
    player.ships[0].add_cannon(cannon())  # add a default cannon to the ship
    player.ships[0].add_shot(standard_shot())  # load default shot onto the ship
    player.ships[0].load_cannon(0,0)
    
    
#g1.add_ship(400,300,player_sel=None)  # create a ship for the active player
#g1.active_player.ships[0].add_cannon(cannon())  # add a default cannon to the ship
#g1.active_player.ships[0].add_shot(standard_shot())  # load default shot onto the ship

# load the cannon
#g1.active_player.ships[0].load_cannon(0,0)
#g1.active_player.ships[0].Cannons[0].load(g1.active_player.ships[0].Shot[0].load_shot())

for p in g1.players:
    for s in p.ships:
        s.update_ship()

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
        if not g1.active_player.active_ship is None:
            g1.active_player.active_ship.move(x,y)
#            g1.active_player.ships[0].move(x,y)
    elif button == mouse.RIGHT:
        if not g1.active_player.active_ship is None:
            land_coord,bullet_vel,bullet_pos0,bullet_damage=g1.active_player.active_ship.fire_cannon(0,x,y)
#            land_coord,bullet_vel,bullet_pos0,bullet_damage=g1.active_player.ships[0].fire_cannon(0,x,y)
    #        land_coord,bullet_vel=g1.active_player.ships[0].fire_cannon(0,x,y)
            
    #        print(bullet_vel)
         
    # Manual fire definition   
    #        bullet_pos = np.concatenate((g1.active_player.ships[0].coords.flatten(),
    #                                         np.zeros(1)))
    #        bullet_vel = np.array([x-g1.active_player.ships[0].coords[0,0],
    #                                     y-g1.active_player.ships[0].coords[1,0],
    #                                     0])
    #        bullet_vel = bullet_vel/np.sqrt(np.sum(bullet_vel**2))
    #        bullet_vel[2] = 4
    #        bullet_vel = bullet_vel*15
            
            if not bullet_vel is None:   
                bullet_pos = np.array([bullet_pos0[0,0],bullet_pos0[1,0],bullet_pos0[2,0]])
                g1.make_bullet(bullet_pos,bullet_vel.flatten(),bullet_damage)
                # reload the cannon
#                g1.active_player.ships[0].load_cannon(0,0)
            
@g1.board.window.event
def on_key_press(symbol, modifiers):
    if symbol==key.SPACE:
        # give a turn to the next player
        g1.next_player()
    if symbol == key.N:
        # activate the next ship in the player's fleet
        g1.active_player.cycle_ship()
    
    if symbol == key.L:
        # load the current ship if it has sufficient movement and 
        # it's within its base
        print("Load shot request received")
        if not g1.active_player.active_ship is None:
            if g1.active_player.active_ship.test_on_base():
                if g1.active_player.active_ship.move_frac > 0.5:
                    g1.active_player.active_ship.add_shot(standard_shot(count=5))
                    g1.active_player.active_ship.use_move_frac(0.51)
                    print("loading 5 shot onto")
                    print(g1.active_player.active_ship)
                else:
                    print("Insufficient Move Fraction:")
                    print(g1.active_player.active_ship.move_frac) 
            else:
                print("Ship is not currently on base")
                print(g1.active_player.active_ship.coords)
                print(g1.active_player.base_loc)
                
        else:
            print("No active ship")
    
    if symbol == key.C:
        # load another cannon on the ship
        if g1.active_player.active_ship.test_on_base():
            if len(g1.active_player.active_ship.Cannons) < len(g1.active_player.active_ship.Segments):
                if g1.active_player.active_ship.move_frac >= 1.0:
                    g1.active_player.active_ship.add_cannon(cannon())
                    g1.active_player.active_ship.use_move_frac(1.0)
                else:
                    print("Loading a cannon requires the entire move")
            else:
                print("A ship cannot hold more cannons than it has segments")
        else:
            print("Cannot load cannon on ship.  Ship is not currently on base")
            print(g1.active_player.active_ship.coords)
            print(g1.active_player.base_loc)
        
        
pyglet.clock.schedule_interval(update, 1/60.)
#pyglet.clock.schedule_interval(update_splash,1/2.0)
pyglet.app.run()