# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 17:03:43 2021

@author: Shalk
"""

# Imported modules
import swmm  # The SWMM module
import matplotlib.pyplot as plt  # Module for plotting
import scipy.signal as signal
import numpy as np

# ***********************************************************************
#  Declaration of simulation files and variables
# ***********************************************************************
LINK=swmm.LINK
LENGTH=swmm.LENGTH
FLOW=swmm.FLOW

inp    = "swmm_files/3tanks.inp"  # Input file
flow   = []

time   = []
flowtime = []

swmm.initialize(inp)

#***************************************************
#State Space initialization
#***************************************************
No = 1935 #initial viral load
Nt=No

#input output matrices which are constant for now. may change if we make
#   state space time variant
length = swmm.get_from_input(inp, LINK, LENGTH)
n = length/100 #number of states in the system
m = 2 #number of inputs
A = np.eye(n) #details decay factors of viral load for each state
B = np.eye(m,n) #details location of viral inputs
C = np.eye(n) #details location of sensors in the system (assuming all nodes have sensors)
D = 0

while( not swmm.is_over() ): 
    
	# ----------------- Run step and retrieve simulation time -----------
	
    time.append( swmm.get_time() )
    swmm.run_step()  # Step 2
    
    length = swmm.get_from_input(inp, LINK, LENGTH)
    
    
	# --------- Retrieve & modify information during simulation ---------
	# Retrieve information about flow in C-5
    f = swmm.get('C-5', FLOW, swmm.SI)
	# Stores the information in the flow vector
    flow.append(f)
    #flow represents velocity. time derived from here describes time of viral
    #   travel from the last point. dividing length of current link by flow
    #   should give that time.
    t = length/flow
    flowtime.append(t)
    #k represents the half-life/viral decay.
    k = np.log(No-Nt)/flowtime
    
    Nt = No**(k*flowtime)#update Nt to proper viral volume for next iteration
    A = k*A #update A matrix
    signal.StateSpace(A.T,B.T,C.T,D)

