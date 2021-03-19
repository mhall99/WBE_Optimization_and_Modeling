# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 17:03:43 2021

@author: Shalk
"""

# Imported modules
import pyswmm  # The SWMM module
import matplotlib.pyplot as plt  # Module for plotting
import scipy.signal as signal
import numpy as np

# ***********************************************************************
#  Declaration of simulation files and variables
# ***********************************************************************

#dont forget to change inp depending on your own hierarchy
inp    = "python module/swmm_files/3tanks.inp"  # Input file

flow   = []

time   = []
flowtime = []


#***************************************************
#State Space initialization
#***************************************************
No = 1935 #initial viral load
Nt=No

#input output matrices which are constant for now. may change if we make
#   state space time variant
length = 5000 #swmm.get_from_input(inp, LINK, LENGTH)
n = length/100 #number of states in the system
m = 2 #number of inputs
A = np.eye(n) #details decay factors of viral load for each state
B = np.eye(m,n) #details location of viral inputs
C = np.eye(n) #details location of sensors in the system (assuming all nodes have sensors)
D = 0

#str stores the string ids of all nodes found while id stores raw ids which can
#   be used to find inflow and outflow of any give node
allnodesstr=[]
allnodesid=[]
nodecount=0

with pyswmm.Simulation(inp) as sim:
    links = pyswmm.Links(sim)
    nodes = pyswmm.Nodes(sim)
    
    #counts through each node and performs an action to store
    for node in nodes:
       
        allnodesid.append(nodes[node.nodeid])
        allnodesstr.append(node.nodeid)
        nodecount= nodecount+1
        
    #steps through the simulation and allows for information to be gathered
    # at each step of the simulation
    for step in sim:
        count=0
        #print the name of the node and the total inflow of it throughout the
        #   simulation. can store the results in various arrays
        while count <nodecount:
            print(allnodesstr[count], allnodesid[count].total_inflow)
            count=count+1









