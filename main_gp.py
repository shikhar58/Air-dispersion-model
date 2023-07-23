"""
The following example uses Chama to optimize the placement of sensors that 
detects a set of potential plumes from 10 well pads based on 1 hour wind data. 
Simulation data is created using the Gaussian plume model in Chama.
The coverage formulation is used to optimize sensor placement.
Note that this example uses notional wind data, leak rates, and sensor thresholds
along with low resolution simulations for demonstration purposes.
"""
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import chama
from scipy.interpolate import griddata
import streamlit as st

def GaussianEngine(stack_height, emission_rate, wind_direction, wind_speed, stability):
    xsize = 100 # m
    ysize = 100 # m
    zsize = 10 # m
    tsize = 24*60*60 # s (1 day)
    dx = 1 # m
    dy = 1 # m
    dz = 1 # m
    dt = 3600 # s (hourly)
    
    ### Build the x,y,z,t grid
    xar = np.arange(0, xsize, dx)
    yar = np.arange(0, ysize, dy)
    zar = np.arange(0, zsize, dz)
    zar=np.zeros(len(zar))
    tar = np.arange(0, tsize, dt)
    tsteps = int(tsize/dt)
    grid = chama.simulation.Grid(xar, yar, zar)
    
    ### Generate plume signal data (for each wellpad and realization)
    signal = None
    info = []
    
    x = 50
    y = 50
    z = 1                             #source is at a height 0, but it can be changed as well.
    correction=360-90
    leakrate = emission_rate
    wind={}
    
    wind['Wind Direction']=correction-wind_direction
    wind['Wind Speed']=wind_speed
    wind['Stability Class']=stability
    
    wind_data = pd.DataFrame([wind])
    
    
    
    source = chama.simulation.Source(x, y, z, leakrate)
    gauss_plume = chama.simulation.GaussianPlume(grid, source, wind_data)
    gauss_plume.run()
    conc = gauss_plume.conc
    # rename the scenario S to a unique scenario name
    conc = conc.rename(columns={'S': "stack"})
    
    signal = conc
    
                
    del signal['Z']
    
    del signal['T']
                
    signal.to_csv('signal_sn.csv', index=False)
    
    return signal
    
def plot(signal):
    x = signal.iloc[:,0].values
    y = signal.iloc[:,1].values
    z = signal.iloc[:,2].values
    
    # Define the regular grid for interpolation
    xi = np.linspace(x.min(), x.max(), 1000)
    yi = np.linspace(y.min(), y.max(), 1000)
    XI, YI = np.meshgrid(xi, yi)
    
    # Perform 2D interpolation to create a regular grid of z values
    ZI = griddata((x, y), z, (XI, YI), method='linear')
    

    # Create the pcolormesh plot
    fig, ax = plt.subplots()
    pc = ax.pcolormesh(XI, YI, ZI, cmap='viridis')
    plt.colorbar(pc)
    sc=ax.scatter(50,50,c='red')

    
    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    # Set plot title
    #ax.set_title('Continuous 2D Colormap Plot')
    #plt.show()
    # Show the plot
    st.pyplot(fig)
    
    # Show the plot
    #plt.scatter(50,50)
    #plt.show()

    
#result=GaussianEngine(0,0.014,90,1,"C")
#plot(result)