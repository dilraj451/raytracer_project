"""
A script that defines a uniform collimated bundle of rays with variable
diameter (set to 5 mm), which is propagated through the spherical surface to 
the output plane at the paraxial focal point. At the output plane, the x 
and y coordinates of each ray are plotted on a scatter graph and the RMS spot
radius of the ray bundle is calculated and printed.

Author: Dilraj Sidhu
"""

import raytracer as rt
import opticalelements as oe
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax3 = plt.axes(projection='3d')


#definition of the refracting object and output plane object
simple_spherical = oe.SphericalRefraction(100.0,1.0,1.5,100/3,200/3)
output = oe.OutputPlane(200.0)#z position found from 'model_testing.py'

rays=[]

#lists to store the x,y coordinates of refracted rays at the output plane
x_coords = []
y_coords = []


#loop that defines uniform collimated rays at z = 0
diameter = 5
for k in range(0,diameter+1):
    if k == 0:
        ray_temp = rt.Ray(np.array([0.0,0.0,0.0]),np.array([0.0,0.0,1.0]))
        rays.append(ray_temp)
    else:
        dots = k*6
        for l in range(0,dots):
            x = 0.5*k*np.sin(l*((2*np.pi)/dots))
            y = 0.5*k*np.cos(l*((2*np.pi)/dots))
            ray_temp = rt.Ray(np.array([x,y,0.0]),np.array([0.0,0.0,1.0]))
            rays.append(ray_temp)

#loop propagates each ray through the refracting surface to the output plane            
for n in range(0,len(rays)):
    simple_spherical.propagate_ray(rays[n])
    output.propagate_ray(rays[n])
    x_coords.append(output.propagate_ray(rays[n])[0])
    y_coords.append(output.propagate_ray(rays[n])[1])
    ax3.plot3D(rays[n].vertices()[0],rays[n].vertices()[1],rays[n].vertices()[2])


#sets 3D axis labels and sizes and plots the rays
ax3.set_xlabel('x (mm)')
ax3.set_ylabel('y (mm)')
ax3.set_zlabel('z (mm)')

ax3.xaxis.set_tick_params(labelsize=8)
ax3.yaxis.set_tick_params(labelsize=8)
ax3.zaxis.set_tick_params(labelsize=8)

plt.show()
plt.close(fig)


#plots rays coordinates in the 2D (y-z) plane
for p in range(0,len(rays)):
    plt.plot(rays[p].vertices()[1],rays[p].vertices()[2])
plt.xlabel('y (mm)')
plt.ylabel('z (mm)')
plt.show()


#plots the coordinates of the rays at the output plane
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.scatter(x_coords,y_coords,s=5)
plt.axis("equal")
plt.axis([-0.005,0.005,-0.005,0.005])
plt.show()


#calculation of the RMS spot radius
total_radius_squared = 0
for t in range(0,len(x_coords)):
    total_radius_squared += x_coords[t]*x_coords[t] + y_coords[t]*y_coords[t]
rms_spot = np.sqrt(total_radius_squared/len(x_coords))
print('The rms spot radius is ',rms_spot)