# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 15:48:44 2023

@author: shikh
"""

import streamlit as st
import main_gp as gp

#gp.GaussianEngine(1,0.014,230,1,"C")
#gp.plot()
st.title("Air dispersion")

st.text("Using Gaussian plume model")

def main():
    st.title("Stack properties:")

    slider_label1 = "Stack height?"
    stack_height = st.slider(slider_label1, 0, 10, 1)

    st.text_label1=("Emission rate (gram per second per meter cube) ?")
    emission_rate = st.text_input(st.text_label1,0.001)
    
    st.title("wind properties:")
    
    slider_label2 = "Wind direction ?"
    wind_direction = st.slider(slider_label2, 0, 360, 60)
    
    st.text_label3=("wind speed (meter/second) ?")
    wind_speed = st.text_input(st.text_label3,1)
    
    options = ['A','B','C','D','E','F']
    
    stability_class = st.selectbox("Select a stability class", options)
    
    #gp.GaussianEngine(stack_height,emission_rate,wind_direction,wind_speed,"C")
    st.title("---------------Model result---------------")
    
    result=gp.GaussianEngine(stack_height,float(emission_rate),wind_direction,float(wind_speed),stability_class)
    gp.plot(result)
    st.text("red point is the source")
if __name__=="__main__":
    main()

        