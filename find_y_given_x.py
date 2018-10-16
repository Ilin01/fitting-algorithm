
'''
This program will produce accurate restricted polynomial fitting for the data inputted. This program will find the y value for a given x value of a graph.
'''

import numpy.polynomial.polynomial as poly
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import math
from matplotlib.colors import LogNorm
import matplotlib.colors as colors
import scipy
from scipy import stats
from matplotlib.pyplot import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
import scipy.ndimage
import warnings

warnings.simplefilter('ignore', np.RankWarning)

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


#function finding the y value corresponding to an x value based on fitting parameters
def f_individual_value(x,COEFS,DEG):

	
    ret2=0
    for count2 in range(len(COEFS)):
		
        ret2+=COEFS[count2]*(x**(DEG))
        DEG-=1
		
		
		
		
    return ret2


	
#input array of y_values
y_values=[...]
		
#input array of x_values
x_values=[...]	
		
#fill the gaps in the data distribution for better approximation of the fitting parameters(recommended)

y_values= scipy.ndimage.zoom(y_values, 40)
x_values = scipy.ndimage.zoom(x_values, 40)
		
#create a pandas data frame with the arrays
Dframe=pd.DataFrame({'y_values': y_values, 'x_values': x_values })
		
#order the arrays in the data frame
dataframe = Dframe[['y_values','x_values']]
		
		

		
#the degree of the polynomial fitting (recommended deg=12)
deg=12
		
		
#the x value corresponding to the y value to be found
x_value=float(input("Enter x value: "))
		
#y range decrease percentage (the lower the more accurate the result will be at the cost of the program being slower)
percentage=0.001
		
#calculate the maximum and minimum x and y values 
y_max=np.array(dataframe)[:,0].max()
y_min=np.array(dataframe)[:,0].min()
		
x_max=np.array(dataframe)[:,1].max()
x_min=np.array(dataframe)[:,1].min()
		
#calculate the fitting parameters of the first iteration
coefs=np.polyfit(np.array(dataframe)[:,1],np.array(dataframe)[:,0], deg)

		
		
		
#calculate the y value corresponding to the x value inputted from the first fitting y range
y_value=f_individual_value(x_value,coefs,deg)
		
#calculate the value by which the fitting y range decreases each loop
decreasing_step=-percentage*(y_max-y_min)

percentageX=0.05

x_length=percentageX*abs(x_max-x_min)

progress_control=0



for y_length in np.arange(y_max,y_min,decreasing_step):
			
	
    #creating a data frame for the new y range of y and x values with the central y value being the one found in the previous iteration and the central x value between x_value-x_length and x_value+x_length
    dataframe_filtered=dataframe[(dataframe.y_values > y_value-y_length) & (dataframe.y_values < y_value+y_length) & (dataframe.x_values > x_value-x_length) & (dataframe.x_values < x_value+x_length)].values
	
    if len(dataframe_filtered)==0:
 
        break
    else:
        #calculate the new fitting parameters and find the new y value 
        new_coefs=np.polyfit(np.array(dataframe_filtered)[:,1],np.array(dataframe_filtered)[:,0], deg)
        y_value=f_individual_value(x_value,new_coefs,deg)



		
	
    
		

print('The y value corresponding to x = '+str(x_value)+' is y = '+str(y_value))

