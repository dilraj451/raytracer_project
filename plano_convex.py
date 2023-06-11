"""
A script that defines a plano-convex lens with the convex surface facing the 
output. A few paraxial rays are traced in order to find the focal point at 
which the output plane is defined. A uniform collimated bundle of rays of 
variable diameter (set to 10 mm) is defined and propagated through the lens. The 
RMS spot radius of the ray bundle is calculated and printed.

Author: Dilraj Sidhu
"""

import raytracer as rt
import opticalelements as oe
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#planar and spherical surfaces declared
plano = oe.SphericalRefraction(100.0,1.0,1.5168,np.Infinity,100.0)
convex = oe.SphericalRefraction(10.0,1.5168,1.0,50.0,100.0)

ray_tests = []
z_outputs = []

#testing the model with paraxial rays to find the focal point
num_of_test_rays = 3
for g in range(0,num_of_test_rays):
    ray_tests.append(rt.Ray(np.array([0.025*(g+1),0.0,0.0]),np.array([0.0,0.0,1.0])))
    plano.propagate_ray(ray_tests[g])
    convex.propagate_ray(ray_tests[g])
    iterations = abs(ray_tests[g].p[0]/ray_tests[g].k[0])
    z_outputs.append(ray_tests[g].p[2] + ray_tests[g].k[2]*iterations)
    

#average focal point along z axis is used to define the output plane's position
avg_z_output = np.mean(z_outputs)
output = oe.OutputPlane(avg_z_output)

x_coords = []
y_coords = []

rays=[]

fig = plt.figure()
ax3 = plt.axes(projection='3d')


#loop that defines uniform collimated rays at z = 0
diameter = 10
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


#loop propgates rays through the lens to the output and plots the 3D ray trajectories            
for n in range(0,len(rays)):
    plano.propagate_ray(rays[n])
    convex.propagate_ray(rays[n])
    output.propagate_ray(rays[n])
    x_coords.append(output.propagate_ray(rays[n])[0])
    y_coords.append(output.propagate_ray(rays[n])[1])
    ax3.plot3D(rays[n].vertices()[0],rays[n].vertices()[1],rays[n].vertices()[2])



ax3.set_xlabel('x (mm)')
ax3.set_ylabel('y (mm)')
ax3.set_zlabel('z (mm)')

ax3.xaxis.set_tick_params(labelsize=8)
ax3.yaxis.set_tick_params(labelsize=8)
ax3.zaxis.set_tick_params(labelsize=8)
plt.show()
plt.close(fig)


#2D ray plot (in y-z plane)
for p in range(0,len(rays)):
    plt.plot(rays[p].vertices()[1],rays[p].vertices()[2])
plt.xlabel('y (mm)')
plt.ylabel('z (mm)')
plt.show()

#scatter plot of ray interceptions with the output plane
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.scatter(x_coords,y_coords,s=5)
plt.axis("equal")
plt.show()

#calculation of the RMS spot radius
total_radius_squared = 0
for t in range(0,len(x_coords)):
    total_radius_squared += x_coords[t]*x_coords[t] + y_coords[t]*y_coords[t]
rms_spot = np.sqrt(total_radius_squared/len(x_coords))
print('The rms spot radius is ',rms_spot)