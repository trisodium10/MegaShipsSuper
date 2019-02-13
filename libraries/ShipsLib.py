# -*- coding: utf-8 -*-
"""
Spyder Editor

Class definition for ships game.
Ships -
Cannons - 
shot - amunition to fire out of cannons
segments - ship segments to build ships out of
"""

import numpy as np

g = 9.81  # acceleration of gravity

Mseg = 10

m_width = 0.2
b_width = 0.3

default_shot = {'mass':1,'name':'default','damage':1}
heavy_shot = {'mass':3,'name':'heavy','damange':2}

class ship:
    """
    A ship instance with a position on the board coords = (x,y)
    and orientation theta
    A ship consists of Segments and has cannons
    If a segment on a ship runs out of hit points, the ship sinks
    The ship is loaded with shot which is fires in its cannons.
    
    A ship has a move range defined by its propel to mass ratio.  The propel
    property is increased by having more and better masts.  The mass is
    increased by having more segments, cannons and ammunition on the ship.
    """
    def __init__(self,x,y,width=1,theta=0):
        """
        x,y location on board
        """
    #    self.x = x  # x board location
    #    self.y = y  # y board location
        self.coords = np.array([[x],[y]])
        
        self.Segments = []
        
        self.center_of_mass = 0  # ship center of mass from front
        
#        self.Segments = [3]*Nsegments  # list of segments and their health
#        self.z_seg = -np.arange(Nsegments)  # ship coordinate of each segment
        
        self.width = width #Nmasts*m_width+b_width
        self.length = 0  # initial length is zero
        
        self.Cannons = []  # list of cannon pairs
        
        self.Shot = []       # no shot loaded
        
        self.mass = 0
        self.propel = 0
        
        self.move_dist = 0 #self.propel/self.mass
        
        self.theta = theta # the ship's orientation on the map
        
    def __repr__(self):
        retstr = 'ship class\n'
        retstr+='position (%.2f,%.2f)\n'%(self.coords[0,0],self.coords[1,0])
        retstr+='%d segments\n'%len(self.Segments)
        retstr+='|' 
        for seg in self.Segments:
            retstr+=' %d |'%seg.hp
        return retstr

    
    def push_segment(self,new_seg):
        # add a segment to the end of the ship
        new_seg.set_z(self.length)
            
        self.Segments+=[new_seg]
        self.update_length() # update length
        self.update_mass()
        
    def pop_segment(self):
        # remove the end segment
        del self.Segments[-1]
        self.update_length()
        self.update_mass()
        
    def add_cannon(self,new_cannon):
        self.Cannons+=[new_cannon]
    def add_shot(self,new_shot):
        
        # look to see if that shot already exists in the ship
        shot_types = [shot_type.name for shot_type in self.Shot]
        try:
            ishot = shot_types.index(new_shot.name)
            # if we find that shot type, just increase its count
            self.Shot[ishot].add_count(new_shot.count)
            
        except ValueError:
            # if we do not find the shot, add it to the list
            self.Shot+=[new_shot]  # for now don't look for common shot
    
    def fire_cannon(self,index,x,y):
        coord = np.array([[x],[y]])
        coordship = np.dot(transform(self.theta),coord-self.coords)
        hit_coords = self.Cannons[index].fire(coordship)
        hit_coords = np.dot(transform(-self.theta),hit_coords)+self.coords
        return hit_coords
        
    def master_move(self,x_new,y_new):
        # override ship location
        self.coords = np.array([[x_new],[y_new]])
        
    def move(self,x_new,y_new):
        c_new = np.array([[x_new],[y_new]])
        if np.sqrt(np.sum((c_new-self.coords)**2)) <= self.move_dist:
            self.coords = c_new.copy()
        else:
            # try to move toward the requested location
            n_move = c_new-self.coords
            n_move = n_move/np.sqrt(np.sum(n_move**2))*self.move_dist
            self.coords=n_move+self.coords
            
        
    
    def update(self):
        # update everything
        self.update_length()
        self.update_mass()
        self.update_move()
        
    def update_move(self):
        self.move_dist = self.propel*1.0/self.mass
    
    def update_length(self):
        length = []
        mass_len = []
        propel = 0
        for seg in self.Segments:
            length+=[seg.length]
            mass_len+=[seg.mass*seg.length]
            propel+=seg.mast
        self.center_of_mass = np.interp(0.5,np.array(mass_len)/sum(mass_len),np.array(length))
        self.length = sum(length)
        self.propel=propel
    
    def update_mass(self):
        cannon_mass = 0
        for can in self.Cannons:
            cannon_mass+=can.mass
        
        seg_mass = 0
        for seg in self.Segments:
            seg_mass+=seg.mass
            
        shot_mass = 0
        for sh in self.Shot:
            shot_mass+=(sh.mass*sh.count)
            
        self.mass = cannon_mass+seg_mass+shot_mass
        

class cannon:
    def __init__(self,z=0,w=0,Power=1,MaxRange=10,Accuracy=1,theta=0,position=(0,0),mass=1):

        self.mass = mass   # cannon mass
        self.coords = np.array([[z],[w]])  # position of cannon on ship
        self.Power = Power # cannon power
        self.MaxRange = MaxRange  # range degredation constant
        self.v0n = np.sqrt(self.MaxRange*g)  # nomial exit velocity (standard shot)
        self.Accuracy = Accuracy # overall cannon accuracy (does not change with range)
        
        self.Loaded = False  # is the cannon ready to fire?
        self.Shot = None
        
        self.theta=0  # the cannon's orientation on the ship
        self.position=0 # the cannon's [x,y] position on the ship
        
    def __repr__(self):
        retstr = 'cannon class\n'
        retstr = 'ship position (%.2f,%.2f)\n'%(self.coords[0,0],self.coords[1,0])
        retstr+= 'exit velocity %.2f\n'%self.v0n
        retstr+= 'accuracy %.2f\n'%self.Accuracy
        retstr+= 'loaded: %r'%self.Loaded
        return retstr
        
        
    
    def load(self,shot):
        self.Loaded = True
        self.Shot = shot
        
    def fire(self,t_coords,shot=1):
        # hit success depends on a combination of target range, target size, 
        # cannon range, and cannon accuracy dictated by projectile motion
        # equations
        #
        # accuracy dictates the sigma term in cannon pointing
        # range is a base launch velocity definition
        if self.Loaded:
    
            coord = np.dot(transform(self.theta),t_coords-self.coords)
            t_dist = np.sqrt(np.sum(coord**2))
        
            # shot exit velocity
            v0 =self.v0n/self.Shot.mass
        
##            # round uncertainty space
#            dtheta0 = np.random.rand()*2*np.pi
#            dthetaR = np.random.randn()*self.Accuracy
#            
#            dthetaX = dthetaR*np.cos(dtheta0)
#            dthetaZ = dthetaR*np.sin(dtheta0)
        
            # square uncertainty space
            dthetaX = np.random.randn()*self.Accuracy*np.pi/180
            dthetaZ = np.random.randn()*self.Accuracy*np.pi/180
            
            thetaX = np.arctan2(coord[1,0],coord[0,0])+dthetaX
            thetaZ = 0.5*np.arcsin(t_dist*g/v0**2)+dthetaZ
            if np.isnan(thetaZ):
                thetaZ = np.pi/4
            
            # landing point in cannon coordinate frame
            x_shot = np.cos(thetaX)*v0**2/g*np.sin(2*thetaZ)
            y_shot = np.sin(thetaX)*v0**2/g*np.sin(2*thetaZ)

            coord_out = np.dot(transform(-self.theta),np.array([[x_shot],[y_shot]]))+self.coords
            return coord_out

class shot:
    """
    class definition for cannon ordinance or shot
    the count reflects how much is in the store
    damage is the damage inflicted if it hits its target
    mass is how much the shot contributes to the ship's mass
    name is used to group the types
    """
    def __init__ (self,mass,damage,name,count=10):
        self.damage = damage
        self.count = count
        self.name = name
        self.mass = mass
    
    def __repr__(self):
        retstr = 'shot class: '+self.name+'\n'
        retstr+= 'count %d'%self.count
        return retstr
        
    def add_count(self,count):
        # increase the amount of stored shot
        self.count+=count
    def load_shot(self):
        # return one shot object to laod in the cannon
        # and decrease the shot storage by 1
        self.count-=1
        return shot(self.mass,self.damage,self.name,count=1)
        
def standard_shot(count=10):
    # generate a store of default shot
    new_shot=shot(1,1,'standard',count=count)
    return new_shot
     
def heavy_shot(count=3):
    # generate a store of default shot
    new_shot=shot(3,2,'heavy',count=count)
    return new_shot
        

class segment:
    """
    Class definition for a ship segment
    Each segment has a certain number of hitpoints (hp),
    a position along the ship's length (z)
    a mass
    and a possible mast with value corresponding to the amount it contributes
        to the ship's propel property
    """
    def __init__(self,z,hp=3,length=1,mass=10,mast=10):
        self.hp = hp  # hit points
        self.z = z  # coordinate location along the ship (from the front)
        self.length = length  # length of segment
        self.mass = mass  # mass of the segment
        self.mast = mast  # mast's contribution to ship speed
    def apply_damage(self,damage):
        self.hp-=damage
    def set_z(self,z):
        # set the z location of the segment
        self.z = z
    
    
    

def transform(theta):
    """
    transform gives the transformation matrix into a coordinate
    system defined by the new object orientation theta
    """
    return np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])