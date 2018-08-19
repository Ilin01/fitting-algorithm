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


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
	
	
	

data2=np.load('C:/Users/User/OneDrive/third_year_proj/new method/l-b-vl-vrh-mass-R-rxy.npz')
data = np.load('C:/Users/User/OneDrive/UCLan_internship/maps_code/coords.708main.asc.npz')

age=data['age']
R=data2['R']
vr=data2['vrh']
m=data2['m']
vl=data2['vl']
l=data2['l']
b=data2['b']




time1=time.clock()	




df = pd.DataFrame({'R': R, 'age': age, 'l': l,'b': b})

df = df[['R','age','l','b']]







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
#not recommended for very noisy distributions
y_values= scipy.ndimage.zoom(y_values, 40)
x_values = scipy.ndimage.zoom(x_values, 40)
		
#create a pandas data frame with the arrays
Dframe=pd.DataFrame({'y_values': y_values, 'x_values': x_values })
		
#order the arrays in the data frame
dataframe = Dframe[['y_values','x_values']]
		
		
#Comment: if an x value crosses the graph line at more than one location (in which case this graph would not represent a function) then the program outputs one of the y values that the graph crosses at the x coordinate inputted or the program outputs a y value in between the y values at which the x value crosses the graph line
		
#the degree of the polynomial fitting (recommended deg=12)
deg=12
		
		
#the x value corresponding to the y value to be found
x_value=...
		
#y range decrease percentage (the lower the more accurate the result will be at the cost of the program being slower)
percentage=0.1/100
		
#calculate the maximum and minimum y values 
y_max=np.array(dataframe)[:,0].max()
y_min=np.array(dataframe)[:,0].min()
		
		
		
#calculate the fitting parameters of the first iteration
coefs=np.polyfit(np.array(dataframe)[:,1],np.array(dataframe)[:,0], deg)

		
		
		
#calculate the y value corresponding to the x value inputted from the first fitting y range
y_value=f_individual_value(x_value,coefs,deg)
		
#calculate the value by which the fitting y range decreases each loop
decreasing_step=-percentage*(y_max-y_min)
		
		
progress_control=0



for y_length in np.arange(y_max,y_min,decreasing_step):
			
	time1=time.clock()
	
	#creating a data frame for the new y range of y and x values with the central y value being the one found in the previous iteration
	dataframe_filtered=dataframe[(dataframe.y_values > y_value-y_length) & (dataframe.y_values < y_value+y_length)].values
	
	if np.array(dataframe_filtered)[:,1]==[] or np.array(dataframe_filtered)[:,0]==[]:
		
		break
	else:
		#calculate the new fitting parameters and find the new y value 
		new_coefs=np.polyfit(np.array(dataframe_filtered)[:,1],np.array(dataframe_filtered)[:,0], deg)
		y_value=f_individual_value(x_value,new_coefs,deg)

			 
		
		
	
	progress_control += 1
	progress(progress_control, len(np.arange(y_max,y_min,decreasing_step)))
		

print('The y value corresponding to x ='+str(x_value)+'is y ='+str(y_value))






	

























		



		
