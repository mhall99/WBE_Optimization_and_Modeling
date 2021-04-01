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
inp    = "swmm_files/3tanks.inp"  # Input file

aeflow   = []
time   = []
flowtime = []


#***************************************************
#State Space initialization
#***************************************************
No = 1935 #initial viral load
Nt=No
#until we can get length from inp this will be a placeholder
length=5000
n = length/100 #number of states in the system
n=int(n)
m = 2 #number of inputs

#input output matrices which are constant for now. may change if we make
#   state space time variant
A = np.eye(n) #details decay factors of viral load for each state
B = np.eye(m,n) #details location of viral inputs
C = np.eye(n) #details location of sensors in the system (assuming all nodes have sensors)
D=0



#sample methodlolgy for updating A matrix

#k represents the half-life/viral decay.
#k=np.log(No-Nt)/flowtime

#Nt = No**(k*flowtime)#update Nt to proper viral volume for next iteration

#transpose to invert row and column for sake of signals needs
#signal.StateSpace(A.T,B.T,C.T,D)

#dx = A*x + B*u
#y = C*x
#def dx(t,x):
        #u = 100
        #dx = A*x + B*u
    #xs = np.linspace(0,5,100)
    #ys = odeint(dx, No, xs)
    #tspan = np.linspace(0,1000)
    #plt.plot(tspan, y)


#str stores the string ids of all nodes found while id stores raw ids which can
#   be used to find inflow and outflow of any give node
allnodesstr=[]
allnodesid=[] 
nodecount=0

linksstr=[]
linksid=[]
linkcount=0

with pyswmm.Simulation(inp) as sim:
    links = pyswmm.Links(sim)
    nodes = pyswmm.Nodes(sim)
    
    #counts through each node and performs an action to store
    for node in nodes:
       
        allnodesid.append(nodes[node.nodeid])
        allnodesstr.append(node.nodeid)
        nodecount=nodecount+1
    for link in links:
        
        linksid.append(links[link.linkid])
        linksstr.append(link.linkid)
        linkcount=linkcount+1
        
        
    #steps through the simulation and allows for information to be gathered
    # at each step of the simulation
    for step in sim:
        count=0
        
        #print the name of the node and the total inflow of it throughout the
        #   simulation. can be used to store the results in various arrays
        while count < linkcount: #linkcount or nodecount
            #print(allnodesstr[count], allnodesid[count].total_inflow)
            if linksid[count].is_conduit:
                print(linksstr[count], linksid[count].get_link_length, linksid[count].volume)
            count=count+1
            


#python dict function to store all our list and big data. savable into a json.
#django web server. has a data model which stores all componenets and measurements
#   possibly use to organziealll data. django

