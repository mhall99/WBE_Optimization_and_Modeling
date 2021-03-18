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
No = 1935 #viral load
Nt=No

#input output matrices which are constant for now. may change if we make
#   state space time variant
B=[1, 0]
C=[1,0],[0,1]
D=0

#
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
    t= length/flow
    flowtime.append(t)
    #k represents the half-life/viral decay.
    k=np.log(No-Nt)/flowtime
    
    Nt = No**(k*flowtime)#update Nt to proper viral volume for next iteration
    A= [k, 0],[0, k] #update A matrix
    signal.StateSpace(A,B,C,D)













