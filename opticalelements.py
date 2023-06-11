"""
A module to define optical elements, including spherical refracting surface
and the output plane

Author: Dilraj Sidhu
"""

import numpy as np


class OpticalElement:
    
    def propagate_ray(self,ray):
        "propagate a ray through the optical element"
        raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    '''
        Initialisation of the surface object requires the following inputs:
        
        z-intercept with the optical axis (float)
        n1 (float)
        n2 (float)
        Radius of curvature (float)
        Aperture radius (float)'''
    def __init__(self,zintercept,n1,n2,Cradius,Aradius):
        self.__zintercept = zintercept
        self.__n1 = n1
        self.__n2 = n2
        self.__Cradius = Cradius
        self.__curvature = 1.0/self.__Cradius
        self.__Aradius = Aradius
        self.__centre = np.array([0.0,0.0,self.__zintercept+self.__Cradius])
    
       
    def intercept(self,ray):
        '''
        Returns the intercept of input ray object with the surface '''
        
        p = ray.p
        k = ray.k
        
        #condition that surface is spherical
        if self.__curvature != 0:
            r = p - self.__centre
            discriminant = np.dot(r,k)*np.dot(r,k) - np.dot(r,r) + self.__Cradius*self.__Cradius
            
            if discriminant <= 0:
                inter = False
           
            else:
                inter = True
                lm = -np.dot(r,k) - np.sqrt(discriminant)
                lp = -np.dot(r,k) + np.sqrt(discriminant)
                point_m = p + lm*k
                point_p = p + lp*k
                dir_m = (point_m-p)/np.linalg.norm(point_m-p)
                dir_p = (point_p-p)/np.linalg.norm(point_p-p)
                
                if lm <= lp:
                    #condition that point 'lm' is in ray's direction
                    if dir_m[0] == k[0] and dir_m[1] == k[1] and dir_m[2] == k[2]:
                        inte = point_m
                    else:
                        inte = point_p
        
                else:
                    #condition that point 'lp' is in ray's direction
                    if dir_p[0] == k[0] and dir_p[1] == k[1] and dir_p[2] == k[2]:
                        inte = point_p
                    else:
                        inte = point_m
                
        #condition that surface is planar
        else:
            z_diff = self.__zintercept - p[2]
            increments = z_diff/k[2]
            inte = p + increments*k
        
            if np.sqrt(inte[0]*inte[0] + inte[1]*inte[1]) < self.__Aradius:
                inter = True
            else:
                inter = False
        
        #no intercept results in error message
        if inter == False:
            raise ValueError("There is no valid intercept between the ray and surface")
            return None
        
        else:
            return inte
            
        
    def snells(self,intercept,direction):
        '''
        Returns the new direction of the ray after refraction.
        Requires intercept point and the incident direction input as numpy arrays'''
        
        
        #conditional statements determine normal vector at spherical surface intercept
        if self.__curvature != 0:
            if direction[2] > 0:
                if intercept[2] < self.__centre[2]:
                    normal = self.__centre - intercept
                else:
                    normal = intercept - self.__centre
            else:
                if intercept[2] < self.__centre[2]:
                    normal = intercept - self.__centre
                else:
                    normal = self.__centre - intercept
        
        #normal vector is in same z direction as ray if the surface is planar
        else:
            normal = np.array([0.0,0.0,direction[2]])
        
        
        unit_norm = normal/np.linalg.norm(normal)
        theta1 = np.arccos(np.dot(unit_norm,direction))
        self.__nratio = self.__n1/self.__n2
        
        #error message for internal reflection
        if np.sin(theta1) > 1/self.__nratio:
            raise ValueError("Total internal reflection")
            return None
        
        #snell's law is applied and the new direction returned
        else:
            p1 = self.__nratio*(direction-np.cos(theta1)*unit_norm)
            p2 = unit_norm*np.sqrt(1-self.__nratio*self.__nratio*(1-np.cos(theta1)*np.cos(theta1)))
            refracted = p1 + p2
            return(refracted)
    
    #method 'propagate_ray' implements 'intercept' and 'snells' to ray object
    def propagate_ray(self,ray):
        a = self.intercept(ray)
        b = self.snells(a,ray.k)
        ray.append(a,b)

class OutputPlane(OpticalElement):
    '''
    Initialisation of the output plane object requires its z-coordinate to be
    input as a float'''
    def __init__(self,zposition):
        self.__outputP = zposition
    
    #method 'propagate_ray' returns the intercept of the ray and the output plane
    def propagate_ray(self,ray):
        point = ray.p
        direction = ray.k
        diff = self.__outputP - point[2]
        steps = diff/direction[2]
        outputI = point + steps*direction
        ray.append(outputI,np.array([0.0,0.0,1.0]))
        return outputI   