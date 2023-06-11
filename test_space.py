"""
A script to test the classes and their constituent methods from the raytracer
module and the opticalelements module

Author: Dilraj Sidhu
"""

import numpy as np
import raytracer as rt
import opticalelements as oe

#ray class intialisation tested as well as 'p' and 'k' functions
ray1 = rt.Ray(np.array([0.1,0.1,0.0]),np.array([0.0,0.0,1.0]))
print(ray1.p)
print(ray1.k)

#ray class 'append' function tested
ray1.append(np.array([-0.1,0.0,0.0]),np.array([0.0,0.1,11.0]))
print(ray1.p)
print(ray1.k)

#ray class 'vertices' function tested
vertices = ray1.vertices()
print(vertices[1][6])

#spherical refraction object intialisaed and its 'intercept' function is tested
spherical1 = oe.SphericalRefraction(10.0,1.0,1.5,30.0,60.0)
interc = spherical1.intercept(ray1)
print(interc)

#sphericalrefraction class 'snells' method tested
snell1 = spherical1.snells(interc,ray1.k)
print(snell1)

#sphericalrefraction class 'propagate_ray' function tested
ray2 = rt.Ray(np.array([0.1,0.1,0.0]),np.array([0.0,0.0,1.0]))
spherical1.propagate_ray(ray2)
print(ray2.p)
print(ray2.k)

#outputplane class initialised and 'propagate_ray' method tested
output1 = oe.OutputPlane(50)
output1.propagate_ray(ray2)
print(ray2.p)
print(ray2.k)