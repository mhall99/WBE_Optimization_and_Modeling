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
import re

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
length=[5, 20, 5, 6 ,10]
totallength=0    

for x in length:
    print(x)
    totallength=x+totallength
            

n = totallength/100 #number of states in the system
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
def get_nodes_and_links(links, nodes):
    #str stores the string ids of all nodes found while id stores raw ids which can
    #   be used to find inflow and outflow of any give node
    
    global allnodesstr
    global allnodesid
    global nodecount
    global linksstr
    global linksid
    global linkcount
    #these store the node string of the connection between inlets and outlets
    global linkinlets
    global linkoutlets
    #these store the node id of the connections between inlets and outlets
    global linkinletsid
    global linkoutletsid
    #########################################################################
    #       Initializing all globals within the function
    ##########################################################################
    allnodesstr=[]
    allnodesid=[] 
    nodecount=0

    linksstr=[]
    linksid=[]
    linkcount=0
    #these store the node string of the connection between inlets and outlets
    linkinlets=[]
    linkoutlets=[]
    #these store the node id of the connections between inlets and outlets
    linkinletsid=[]
    linkoutletsid=[]
    count=0

    #counts through each node and performs an action to store
    for node in nodes:
        
        allnodesid.append(nodes[node.nodeid])
        allnodesstr.append(node.nodeid)
       
        nodecount=nodecount+1
    for link in links:
        count=0
        if link.is_conduit() :
            linksid.append(links[link.linkid])
            linksstr.append(link.linkid)
            linkinlets.append(link.inlet_node)
            linkoutlets.append(link.outlet_node)
            #below gives a node id relative to the string position of the
            #   inlet outlet array. string should correspond to 
            while(count<nodecount):
                if(linkinlets[linkcount]==allnodesstr[count]):
                    linkinletsid.append(allnodesid[count])
                    
                if(linkoutlets[linkcount]==allnodesstr[count]):
                    linkoutletsid.append(allnodesid[count])
                count=count+1
            linkcount=linkcount+1
    
def get_link_length(inp):
    
    pattern='Length'
    
    #pattern2='RAIN2'
    #pattern3='RAIN1'
    pattern4='\[ORIFICES\]'
    #below pattern is for whole numbers and for decimal numbers.
    # both require a before and after the start
    lengthpattern=' \d+ '#(" \d+.\d ")
    lengthcheck=0
    length=[]

    with open(inp, 'r') as inpDeck:
        #lines = inpDeck.read()
        #lines = re.findall('Length', lines)
        #print(lines)
        regex = re.compile(pattern)
        #regex2 = re.compile(pattern2)
        #regex3 = re.compile(pattern3)
        regex4=re.compile(pattern4)
        regexlength=re.compile(lengthpattern)
        #searching for match of Length and [ORIFICES] in each line
        for line in inpDeck:
        #   to use as conditions if pattern is found.
            match=regex.search(line)
            match4=regex4.search(line)

        
            #check if match for Length is found then will update 
            #   lengthcheck to 1 to act as true for another if statement
            if(match):
                lengthcheck=1
        #this should find a pattern of a decimal number and a whole number
        #   and then append it to the length array. group 0
        #   should be equivelent in position to length in this pattern
                #check match for [ORIFICES] to signify end of relevant information to
        #   the conduit length search. This means for loop will break
            if(match4):
                lengthcheck=0
                break
            
            if(lengthcheck==1):
            #this checks for pattern of a number with a decimal or a number
            #   with no decimal. both should have a space preceding and
            #   after the end of the number
                lengthmatch=regexlength.search(line)
                if (lengthmatch):
                    #print(lengthmatch.group(0))
                    length.append(int(lengthmatch.group(0)))
                    
    return length

with pyswmm.Simulation(inp) as sim:
    links = pyswmm.Links(sim)
    nodes = pyswmm.Nodes(sim) 

    get_nodes_and_links(links, nodes)
    length=get_link_length(inp)
    print(length)
    #steps through the simulation and allows for information to be gathered
    # at each step of the simulation
    for step in sim:
        count=0
        
        #print the name of the node and the total inflow of it throughout the
        #   simulation. can be used to store the results in various arrays
        while count < nodecount: #linkcount or nodecount
            
            #print(allnodesstr[count], allnodesid[count].total_inflow)
            #if linksid[count].is_conduit and not linksid[count].is_orifice():
                #print(linksstr[count], allnodesid[count], linkoutletsid[count])#linksid[count].get_link_length,
            count=count+1
            



#python dict function to store all our list and big data. savable into a json.
#django web server. has a data model which stores all componenets and measurements
#   possibly use to organziealll data. django
#def get_link_length():
  #  print("nonsense")
  
