# -*- coding: utf-8 -*-
"""
Spyder Editor

File for testing ships libraries


"""


from ShipsLib import *


ship_len = 3
s1 = ship(0,0) # define a default ship at the origin
for ai in range(ship_len):
    s1.push_segment(segment(0))

c1 = cannon()  # define a default cannon


s1.add_cannon(c1)  # load the cannon onto the ship

s1.add_shot(default_shot(count=10))

c1.load(s1.Shot[0])
r = s1.fire_cannon(0,[4,4])



