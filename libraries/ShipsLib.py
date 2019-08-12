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
import pyglet

g = 9.81  # acceleration of gravity
move_speed = 10

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
    def __init__(self,x,y,width=1,theta=0,player=None):
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
        self.height = 4  # ship height
        
        self.Cannons = []  # list of cannon pairs
        
        self.Shot = []       # no shot loaded
        
        self.mass = 0
        self.propel = 0
        
        self.move_dist = 0 #self.propel/self.mass
        
        self.move_frac = 1.0  # fraction of movement available
        
        
        self.theta = theta # the ship's orientation on the map
        
        self.sprite = None  # pyglet sprite for the ship
        
        self.player=player
        
    def __repr__(self):
        retstr = 'ship class\n'
        retstr+='position (%.2f,%.2f)\n'%(self.coords[0,0],self.coords[1,0])
        retstr+='%d segments\n'%len(self.Segments)
        retstr+='|' 
        for seg in self.Segments:
            retstr+=' %d |'%seg.hp
        retstr+='\n'
        retstr+='%d Cannons\n'%len(self.Cannons)
        shot_count = 0
        for shot_type in self.Shot:
            shot_count+=shot_type.count
        retstr+='%d Shots'%shot_count
        return retstr
    
    def add_to_board(self,batch=None):
#        ship_image = pyglet.resource.image('ship1.png')
        
        self.ship_image_R = pyglet.resource.image('ship1.png')
        self.ship_image_L = flip_image(self.ship_image_R,axis=1)
#        self.ship_image_L = self.ship_image_R.get_region(0, 0, self.ship_image_R.width, self.ship_image_R.height) 
        
        center_image(self.ship_image_R)
        center_image(self.ship_image_L)
        self.sprite = pyglet.sprite.Sprite(self.ship_image_R, 
                             x=self.coords[0,0], y=self.coords[1,0],
                             batch=batch)
#        face_left = image.load('person.png').texture
#        face_right = face_left.get_region(0, 0, face_left.width, face_left.height)        
        
#        center_image(ship_image)
#        self.sprite = pyglet.sprite.Sprite(ship_image, 
#                             x=self.coords[0,0], y=self.coords[1,0],
#                             batch=batch)
        self.opacity = 0
        self.sprite.rotation=self.theta
        self.sprite.scale = 0.05
    
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

    def load_cannon(self,c_index,s_index):
        # load cannon indexed by c_index
        # with shot indexed by s_index
        # assumes c_index and s_index are valid
    
        # To be added to flag illegal indices
#        if c_index >= len(self.Cannons):
#            raise InvalidCannonIndex
#        if s_index >= len(self.Shot):
#            raise InvalidShotIndex
    
        self.Cannons[c_index].load(self.Shot[s_index].load_shot())
    
    def fire_cannon(self,index,x,y):
        # To be added to flag illegal indices
#        if index >= len(self.Cannons):
#            raise InvalidCannonIndex
        coord = np.array([[x],[y]])
        coordship = np.dot(transform(self.theta),coord-self.coords)
        hit_coords,vel_vec,damage = self.Cannons[index].fire(coordship)
        if not hit_coords is None:
            hit_coords = np.dot(transform(-self.theta),hit_coords)+self.coords
            fire_coords = np.concatenate((np.dot(transform(-self.theta),self.Cannons[index].coords)+self.coords,np.array([[self.height]])),axis=0)
            vel_vec = np.dot(transform(-self.theta,dim=3),vel_vec)
            return hit_coords,vel_vec,fire_coords,damage
        else:
            return None,None,None,None
        
    def master_move(self,x_new,y_new):
        # override ship location
        self.coords = np.array([[x_new],[y_new]])
        self.sprite.position = tuple(self.coords.flatten())
        
    def set_angle(self,angle):
        # set the angle of the ship in degrees
        self.theta = angle
        self.sprite.rotation = -self.theta
        if np.abs(self.theta) > 90 and self.sprite.image is self.ship_image_R:
            self.sprite.image = self.ship_image_L
        elif np.abs(self.theta) < 90 and self.sprite.image is self.ship_image_L:
            self.sprite.image = self.ship_image_R
        
    def move(self,x_new,y_new):
        # should we let the ship rotate even if no movement is left?
        if self.move_frac > 0.0:
            c_new = np.array([[x_new],[y_new]])
            self.theta = np.arctan2(c_new[1,0]-self.coords[1,0],c_new[0,0]-self.coords[0,0])*180/np.pi
            self.sprite.rotation = -self.theta
            # set the image based on the orientation of the ship to keep it
            # right-side-up
            if np.abs(self.theta) > 90 and self.sprite.image is self.ship_image_R:
                self.sprite.image = self.ship_image_L
            elif np.abs(self.theta) < 90 and self.sprite.image is self.ship_image_L:
                self.sprite.image = self.ship_image_R

            if np.sqrt(np.sum((c_new-self.coords)**2)) <= self.move_dist*self.move_frac:
                # subtract the distance traveled from the turn allocation
                self.move_frac = 1-np.sqrt(np.sum((c_new-self.coords)**2))/self.move_dist
                # update the ship location
                self.coords = c_new.copy()
                
            else:
                # try to move toward the requested location
                n_move = c_new-self.coords
                n_move = n_move/np.sqrt(np.sum(n_move**2))*self.move_dist*self.move_frac
                self.coords=n_move+self.coords
                self.move_frac = 0.0  # all of the movement allocation for this turn is used up

    def reset_movement(self):
        self.move_frac = 1.0
            
    def update(self,dt):
        # update for animation and motion
        if any(self.sprite.position != self.coords.flatten()):
            self.sprite.position = (move_speed*dt*(self.coords[0,0]-self.sprite.position[0])+self.sprite.position[0],\
                move_speed*dt*(self.coords[1,0]-self.sprite.position[1])+self.sprite.position[1])
    
    def update_ship(self):
        # update ship attributes
        self.update_length()
        self.update_mass()
        self.update_move()
        
        # check if sunk? (any zero hp segments?)
        
    def update_move(self):
        self.move_dist = self.propel*1.0/self.mass
    
    def update_length(self):
        length = 0
        mass_len = 0
        propel = 0
        seg_mass = 0
        for seg in self.Segments:
            length+=seg.length
#            mass_len+=[seg.mass*seg.length]
            mass_len+=seg.mass*(seg.z+seg.length*0.5)
            seg_mass+=seg.mass
            propel+=seg.mast
#        self.center_of_mass = np.interp(0.5,np.array(mass_len)/sum(mass_len),np.array(length))
        self.center_of_mass = mass_len/seg_mass
        self.length = length
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
        
    def test_hit(self,obj_coords):
        hit_ship = False
        seg_index = None
        # check if the object is within height range first
        if obj_coords[2] <= self.height:
            obj_new =  np.dot(transform(self.theta),obj_coords[:2].reshape(2,1)-self.coords)
            if obj_new[0] <= self.width and obj_new[1] >= 0 and obj_new[1] < self.length:
                hit_ship = True
                if hit_ship:
                    for iseg,seg in enumerate(self.Segments):
                        if seg.z <= obj_new[1] and seg.z+seg.length >= obj_new[1]:
                            seg_index=iseg
        return hit_ship,seg_index
        

class cannon:
    def __init__(self,z=0,w=0,Power=1,MaxRange=80,Accuracy=4,theta=0,position=(0,0),mass=1):

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
        if not self.Loaded and shot.count > 0:
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
            if t_dist*g <= v0**2:
                thetaZ = 0.5*np.arcsin(t_dist*g/v0**2)+dthetaZ
            else:
                thetaZ = np.pi/4
                
            if np.isnan(thetaZ):
                thetaZ = np.pi/4
            
            # landing point in cannon coordinate frame
            x_shot = np.cos(thetaX)*v0**2/g*np.sin(2*thetaZ)
            y_shot = np.sin(thetaX)*v0**2/g*np.sin(2*thetaZ)
            
            vel_vec = np.array([[np.cos(thetaX)*np.cos(thetaZ)],
                                [np.sin(thetaX)*np.cos(thetaZ)],
                                [np.sin(thetaZ)]])*v0

            coord_out = np.dot(transform(-self.theta),np.array([[x_shot],[y_shot]]))+self.coords
            vel_out = np.dot(transform(-self.theta,dim=3),vel_vec)
            
            damage = self.Shot.damage
            self.Loaded=False
            self.Shot = None
            
            
            return coord_out,vel_out,damage
        else:
            return None,None,None

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
        # return one shot object to load in the cannon
        # and decrease the shot storage by 1
        if self.count > 0:
            self.count-=1
            return shot(self.mass,self.damage,self.name,count=1)
        else:
            return shot(self.mass,self.damage,self.name,count=0)
        
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
    def __init__(self,z,hp=3,length=3,mass=10,mast=1000):
        self.hp = hp  # hit points
        self.z = z  # coordinate location along the ship (from the front)
        self.length = length  # length of segment
        self.mass = mass  # mass of the segment
        self.mast = mast  # mast's contribution to ship speed
    def apply_damage(self,damage):
        self.hp-=damage
    def set_z(self,z):
        # set the z location of the segment
        # (along the ship's length)
        self.z = z
    
    
    

def transform(theta,dim=2):
    """
    transform gives the transformation matrix into a coordinate
    system defined by the new object orientation theta
    set dim = 3 to handle 3d vectors instead of 2d (default)
    """
    if dim == 2:
        return np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    elif dim == 3:
        return np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
    
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    
def flip_image(image,axis=0):
    # flip an image
    # axis = 0: horizontal
    # axis = 1: vertical

    # tex_coords (tuple) – 12-tuple of float, 
    # named (u1, v1, r1, u2, v2, r2, …). u, v, r give the 3D texture coordinates 
    # for vertices 1-4. The vertices are specified in the order 
    # bottom-left, bottom-right, top-right and top-left.
    image_flip = image.get_region(0, 0, image.width, image.height)
    t = image_flip.tex_coords
    if axis == 0:
        image_flip.tex_coords = t[3:6] + t[:3] + t[9:] + t[6:9]
    else:
        image_flip.tex_coords = t[9:] + t[6:9] + t[3:6] + t[:3]
        
    return image_flip