
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import chama
from scipy.interpolate import griddata
import streamlit as st
from scipy.interpolate import interp2d

def GaussianEngine(stack_height, emission_rate, wind_direction, wind_speed, stability):
    xsize = 400 # m
    ysize = 400 # m
    zsize = 10 # m
    tsize = 24*60*60 # s (1 day)
    dx = 3 # m
    dy = 3 # m
    dz = 10 # m
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
    
    x = 200
    y = 200
    z = stack_height                             #source is at a height 0, but it can be changed as well.
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
                
    #signal.to_csv('signal_sn.csv', index=False)
    
    return signal
    
def plot(signal,wind_dir):
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
    sc=ax.scatter(200,200,c='red')

    
    # Set axis labels
    ax.set_xlabel('X (meter)')
    ax.set_ylabel('Y (meter)')
    
    # Set plot title
    ax.set_title('plume concentration (g/m^3)')
    #plt.show()
    # Show the plot
    st.pyplot(fig)

    # Show the plot
    #plt.scatter(50,50)
    st.text("red point is the point source for pollutant emission \n \n")

"""
interp_func= interp2d(x[::10], y[::10], z[::10], kind='cubic')
#interp_func= interp2d(x[z>z.max()*0.01], y[z>z.max()*0.01], z[z>z.max()*0.01], kind='cubic')
#print("FBFE")
#plt.show()
x_arc=np.array([250+i*np.cos(np.deg2rad(90+wind_dir)) for i in range(0,150,1)])
y_arc=np.array([250+i*np.sin(np.deg2rad(90+wind_dir)) for i in range(0,150,1)])
z_arc=np.array([interp_func(x_arc[i],y_arc[i]) for i in range(len(x_arc))])
z_arc[z_arc<0]=0
#print(z_arc)
a=np.array(range(0,150,1))

fig1, ax1 = plt.subplots()
ax1.plot(a,z_arc)

ax1.set_xlabel('Distance from the source (meter)')  # Adding X-axis label
ax1.set_ylabel('Concentration of air pollutant (g/m^3)')  # Adding Y-axis label
plt.title('Concentration of air pollutant along the plume centerline')
st.pyplot(fig1)
plt.clf()

#result=GaussianEngine(0,0.014,60,1,"C")
#plot(result,60)
"""