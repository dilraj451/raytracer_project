"""
A script that stores the RMS spot radius data from both orientations of the
plano-convex lens for different ray bundle diameters. The data is plot, with
the trends being modelled as quadratic. The models' parameters are optimised
and their errors calculated. The optimised models are graphed with the raw data.

Author: Dilraj Sidhu
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


#arrays to store diameter and respective RMS spot radius data
diameter = np.array([2,4,6,8,10])
pc = np.array([3.66e-4,2.47e-3,7.70e-3,1.75e-2,3.33e-2])
cp = np.array([9.24e-5,6.23e-4,1.94e-3,4.40e-3,8.36e-3])


#plots data in graph
plt.plot(diameter,pc,'x',color='green')
plt.plot(diameter,cp,'x',color='red')

#data fitted as a quadratic function
pc_opt, pc_cov = np.polyfit(diameter,pc,2,cov=True)
cp_opt, cp_cov = np.polyfit(diameter,cp,2,cov=True)

#calculation of quadratic parameters' errors
pc_param_errors = np.sqrt(np.diag(pc_cov))
cp_param_errors = np.sqrt(np.diag(cp_cov))


#generated x and y data for the quadratic model
x = np.linspace(2,10,1000)
pc_y = pc_opt[0]*x*x + pc_opt[1]*x + pc_opt[2]
cp_y = cp_opt[0]*x*x + cp_opt[1]*x + cp_opt[2]

#quadratic model plotted on same graph as raw data
plt.plot(x,pc_y,color='green')
plt.plot(x,cp_y,color='red')

#axis titles and legend added to graph
plt.xlabel('Diameter (mm)')
plt.ylabel('RMS spot radius (mm)')
green_patch = mpatches.Patch (color = 'green', label = 'Convex surface facing output')
red_patch = mpatches.Patch (color = 'red', label = 'Planar surface facing output')
plt.legend(handles=[green_patch]+[red_patch])
plt.show()