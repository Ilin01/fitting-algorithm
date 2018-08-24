
'''
This is an example of fitting noisy data.
This program will produce accurate restricted polynomial fitting based on a machine-learning method for the data inputted. A plot of the fit and data will be produced as well. 
The main limitation of this algorithm is that it does not work for data distributions with significant gaps between the points plotted. Read this code and you'll understand why.

'''
import warnings
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
import pandas as pd
import scipy.ndimage

warnings.simplefilter('ignore', np.RankWarning)

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


#function for the y values that takes into account parameters of all possible orders. This will produce an array withe the y values.

def f(x,COEFS,DEG):

    ret1=[]
    for count in range(len(x)):
		
        ret=0
        deg=DEG
        for count1 in range(len(COEFS)):
		
            ret+=COEFS[count1]*(x[count]**(deg))
            deg-=1
        ret1.append(ret)
		
		
		
    return ret1
	
	
#same function as before but it is used to produce y value corresponding to an x value
	
def f_individual_value(x,COEFS,DEG):

	
    ret2=0
    for count2 in range(len(COEFS)):
		
        ret2+=COEFS[count2]*(x**(DEG))
        DEG-=1
		
		
		
		
    return ret2
	
	
#input array of x_values
x_values=np.linspace(0, 5, 1000)#[...]

#input array of y_values
y_values=np.sin(3 * x_values) + .6 * np.sin(7*x_values) - .5 * np.cos(3 * np.cos(10 * x_values))	#[...]
		

		
#fill the gaps in the data distribution for better approximation of the fitting parameters(recommended)

y_values= scipy.ndimage.zoom(y_values, 40)
x_values = scipy.ndimage.zoom(x_values, 40)
		
#create a pandas data frame with the arrays
Dframe=pd.DataFrame({'y_values': y_values, 'x_values': x_values })
		
#order the arrays in the data frame
dataframe = Dframe[['y_values','x_values']]
		
		
#Comment: if an x value crosses the graph line at more than one location (in which case this graph would not represent a function) then the program outputs one of the y values that the graph crosses at the x coordinate inputted or the program outputs a y value in between the y values at which the x value crosses the graph line
		
#the degree of the polynomial fitting (recommended deg=12)
deg=12
		
		

		
#y range decrease percentage (the lower the more accurate the result will be at the cost of the program being slower)
percentage=0.01
		
#calculate the maximum and minimum y values 
y_max=np.array(dataframe)[:,0].max()
y_min=np.array(dataframe)[:,0].min()

x_max=np.array(dataframe)[:,1].max()
x_min=np.array(dataframe)[:,1].min()

		
#calculate the fitting parameters of the first iteration
coefs=np.polyfit(np.array(dataframe)[:,1],np.array(dataframe)[:,0], deg)

progress_control=0

#accuracy = how many linearly spaced x values to calculate between minimum x and maximum x 
accuracy=0.001*abs(x_max-x_min)

X_values=np.arange(x_min,x_max+accuracy,accuracy)

Y_values=[]

percentageX=0.05




for x_value in X_values:
		
    #calculate the y value corresponding to the x value inputted from the first fitting y range
    y_value=f_individual_value(x_value,coefs,deg)
		
    #calculate the value by which the fitting y range decreases each loop
    decreasing_step=-percentage*abs(y_max-y_min)
	
		
    x_length=percentageX*abs(x_max-x_min)

	

    for y_length in np.arange(y_max,y_min,decreasing_step):
			
        time1=time.clock()
		
        #creating a data frame for the new y range of y and x values with the central y value being the one found in the previous iteration and the central x value between x_value-x_length and x_value+x_length
        dataframe_filtered=dataframe[(dataframe.y_values > y_value-y_length) & (dataframe.y_values < y_value+y_length)  & (dataframe.x_values > x_value-x_length) & (dataframe.x_values < x_value+x_length)].values
		
        if len(dataframe_filtered)==0:
          
            break
        else:
        #calculate the new fitting parameters and find the new y value 
            new_coefs=np.polyfit(np.array(dataframe_filtered)[:,1],np.array(dataframe_filtered)[:,0], deg)
            y_value=f_individual_value(x_value,new_coefs,deg)
			
		
			 
		
    Y_values.append(y_value)
	
    progress_control += 1
    progress(progress_control, len(X_values))


	
plt.plot(x_values,y_values,label='graph')
plt.plot(X_values,Y_values,label='fit')
plt.legend()
		
plt.show()
