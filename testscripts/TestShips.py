# -*- coding: utf-8 -*-
"""
Spyder Editor

File for testing ships libraries


"""


from ShipsLib import *

import matplotlib.pyplot as plt
import numpy as np


ship_len = 3
s1 = ship(0,0) # define a default ship at the origin
for ai in range(ship_len):
    s1.push_segment(segment(0))

c1 = cannon()  # define a default cannon


s1.add_cannon(c1)  # load the cannon onto the ship

s1.add_shot(standard_shot(count=10))

s1.update()

s1.move(3,5)

target = [12,3]
r_shot = np.zeros((2,10))
r_ship = np.zeros((2,10))
for ai in range(10):
    s1.move(3,5)
#    print('ship mass: %d'%s1.mass)
    s1.Cannons[0].load(s1.Shot[0].load_shot())
    r_shot[:,ai] = s1.fire_cannon(0,target[0],target[1]).flatten()
    r_ship[:,ai] = s1.coords.flatten()
    s1.update()


plt.figure()
plt.scatter(r_shot[0,:],r_shot[1,:])
plt.plot(target[0],target[1],'kx')
plt.plot(r_ship[0,:],r_ship[1,:],'s')
#plt.plot(s1.coords[0],s1.coords[1],'ks')
