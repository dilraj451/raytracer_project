"""
A module to define ray objects 

Author: Dilraj Sidhu
"""
import numpy as np

class Ray:

    def __init__(self,point,direction):
        '''Initialization requires the starting point and direction of the ray
        to be input as numpy arrays'''
        self.__point = point 
        self.__direction = direction/np.linalg.norm(direction) 
        self.__points = [self.__point]
        self.__directions = [self.__direction]
    
    @property
    def p(self):
        '''Returns the most recent ray point '''
        return(self.__points[len(self.__points)-1])
    
    @property
    def k(self):
        '''Returns the most recent ray direction '''
        return(self.__directions[len(self.__directions)-1])
       
    def append(self,p,k):
        '''Adds the new position and direction of the ray, input as
        numpy arrays'''
        self.__points.append(p)
        self.__directions.append(k/np.linalg.norm(k))
    
    def vertices(self):
        '''Returns complete set of vertices traversed by array'''
        points_x = []
        points_y = []
        points_z = []
        
        #loop generates 100 equispaced coordinates between consecutive
        #coordinates in points list
        for i in range(0,len(self.__points)-1):
            temp_x = np.linspace(self.__points[i][0],self.__points[i+1][0],100)
            temp_y = np.linspace(self.__points[i][1],self.__points[i+1][1],100)
            temp_z = np.linspace(self.__points[i][2],self.__points[i+1][2],100)
            
            #loop adds generated coordinates to correscponding lists for x,y,z
            for j in range(0,len(temp_x)):
                points_x.append(temp_x[j])
                points_y.append(temp_y[j])
                points_z.append(temp_z[j])
        
        return points_x, points_y, points_z