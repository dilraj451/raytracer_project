"""
A script to trace paraxial rays through a spherical surface to identify the
paraxial focal point of the surface.

Also, traces a non-parallel ray through the spherical surface to confirm that
it is refracted towards the focal point

Author: Dilraj Sidhu
"""

import raytracer as rt
import opticalelements as oe
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#defining the spherical refracting object and output plane object
simple_spherical = oe.SphericalRefraction(100.0,1.0,1.5,100/3,200/3)



# task 9 & 10
ray_tests = []
z_outputs = []

#loop propagates paraxial rays and stores their respective focal points
num_of_rays = 3
for g in range(0,num_of_rays):
    ray_tests.append(rt.Ray(np.array([0.025*(g+1),0.0,0.0]),np.array([0.0,0.0,1.0])))
    simple_spherical.propagate_ray(ray_tests[g])
    iterations = abs(ray_tests[g].p[0]/ray_tests[g].k[0])
    z_outputs.append(ray_tests[g].p[2] + ray_tests[g].k[2]*iterations)
    

#average focal point along z axis is used to define the output plane's position
avg_z_output = np.mean(z_outputs)
print(avg_z_output)
output = oe.OutputPlane(avg_z_output)

#3D plot of the rays
fig = plt.figure()
ax3 = plt.axes(projection='3d')
for h in range(0,num_of_rays):
    output.propagate_ray(ray_tests[h])
    ax3.plot3D(ray_tests[h].vertices()[0],ray_tests[h].vertices()[1],ray_tests[h].vertices()[2])


ax3.set_xlabel('x (mm)')
ax3.set_ylabel('y (mm)')
ax3.set_zlabel('z (mm)')

ax3.xaxis.set_tick_params(labelsize=8)
ax3.yaxis.set_tick_params(labelsize=8)
ax3.zaxis.set_tick_params(labelsize=8)

plt.show()
plt.close(fig)



# task 11

#ray starting at z = 0 plane has non-paraxial direction
ray_angle = rt.Ray(np.array([0.0,0.0,0.0]),np.array([1.0,1.0,10.0]))


#ray is propagated through the refracting surface to the output plane
print(ray_angle.k)
simple_spherical.propagate_ray(ray_angle)
print(ray_angle.k)
output.propagate_ray(ray_angle)


#3D plot of the ray
fig = plt.figure()
ax_angle = plt.axes(projection='3d')
ax_angle.plot3D(ray_angle.vertices()[0],ray_angle.vertices()[1],ray_angle.vertices()[2])


ax_angle.set_xlabel('x (mm)')
ax_angle.set_ylabel('y (mm)')
ax_angle.set_zlabel('z (mm)')

plt.show()
plt.close(fig)

#2D ray plot (in the x-z plane)
plt.plot(ray_angle.vertices()[0],ray_angle.vertices()[2])
plt.xlabel('x (mm)')
plt.ylabel('z (mm)')
plt.show()

#finds distance of ray at the output plane from the x-y plane origin
radius = np.sqrt(output.propagate_ray(ray_angle)[0]*output.propagate_ray(ray_angle)[0]+output.propagate_ray(ray_angle)[1]*output.propagate_ray(ray_angle)[1])
print(radius)