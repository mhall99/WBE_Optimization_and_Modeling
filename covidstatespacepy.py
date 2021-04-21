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


totallength=0


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
    #this makes sure conduits are the only link type at the beginning of 
    #   linksid and linksstr. this is important for conduits to be relative to 
    #   the index of our link length defintion
    #above is desired in event that condutis arent always first in line of links
    #   but the way for link links works means we can't iterate it a second round
    #   so were just gonna pray conduits are always first in the links section
    #for link in links:

     #   count=0
     #   if link.is_conduit() :
     #       linksid.append(links[link.linkid])
     #       linksstr.append(link.linkid)
     #       linkinlets.append(link.inlet_node)
     #       linkoutlets.append(link.outlet_node)
     #       #below gives a node id relative to the string position of the
     #       #   inlet outlet array. string should correspond to 
     #       while(count<nodecount):
     #           if(linkinlets[linkcount]==allnodesstr[count]):
     #               linkinletsid.append(allnodesid[count])
     #               
     #           if(linkoutlets[linkcount]==allnodesstr[count]):
     #               linkoutletsid.append(allnodesid[count])
     #           count=count+1
     #       linkcount=linkcount+1
        
    for link in links:
        #print("hey i exist")
        count=0
        
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




nodespollution=[]
placeholder=[]
timesteps=[]

with pyswmm.Simulation(inp) as sim:
    links = pyswmm.Links(sim)
    nodes = pyswmm.Nodes(sim)
    
    
    get_nodes_and_links(links, nodes)
    length=get_link_length(inp)
    
    for x in length:
        totallength=x+totallength
    
    nextnode=[]
    s2elength=0
    nodestart=allnodesid[1]
    nodeend=allnodesid[5]
    #nextnode=0
    
    #below was an intial attempt at get length of paths. realized 
    #   this prboelm would be better solved through a recursive function
    #   which isbeing worked on in branches
    
    #count=0
    #while not(nextnode==nodeend):
        
        #looking for starting node as an inlet
        #print(count)
        #if linkinletsid[count]==nodestart:
            #get the current conduit and fix nextnode to its outlet since
            #   we found the inlet that starts the chain
            #currentlink=linksid[count]
            #nextnode=currentlink.outlet_node
            
            #s2elength=s2elength+length[count]
            #print('at start', linksstr[count])
            #print(length[count])
            #print('total length', s2elength, nextnode.nodeid, linkoutletsid[count].nodeid)
            #print(linksid[count].linkid, nextnode)
            #nextnode=nodeend
            
            #now we do things until we reach all ends of the sequences
            #newcount=0
            #ranches=0
            #while (newcount<linkcount):
                #print(newcount)
                
                #if :
                    
                #get a count in case of multiple inlets
                #should this be included in some kind of recursion?
                #for node in linkinletsid:
                #    if node=linkinletsid[newcount]:
                #        branches=branches+1
               #print('branches =" branches)
                        
                        
            
            #now we search for a match of the inlet of next node
            #and add lengths but first lets make sure everything strings
            #together appropriately
            #while not (nextnode == nodeend):
            #    print(newcount)
            #    for node in linkinletsid:
                    #print('for loop', node.nodeid, )
                    
            #        if node==linkoutletsid[newcount]:
            #            nextnode=linkoutletsid[newcount]
            #            print('nextnode',nextnode.nodeid)
            #            break
            #    newcount=newcount+1
                #if linkinletsid[newcount]==nextnode:
            #        nextnode=linkoutlets[newcount]
                    
             #   newcount=newcount+1
                
        #count=count+1
        #elif linkinletsid[count]==nextnode:
        #    nextnode=linkoutletsid[count]
            
        #elif nextnode==nodeend:
        #    count=linkcount
            

    #print(nextnode.nodeid)
            
            
            
        
    
    
    
    
    
    
    #***************************************************
    #State Space initialization
    #***************************************************
    No = 1935 #initial viral load based on count/miliLiter
    Nt=No
    #until we can get length from inp this will be a placeholder

     

    n = totallength/10 #number of states in the system
    n=int(n)
    m = 2 #number of inputs
    
    #input output matrices which are constant for now. may change if we make
    #   state space time variant
    A = np.eye(n) #details decay factors of viral load for each state
    B = np.eye(m,n) #details location of viral inputs
    C = np.eye(n) #details location of sensors in the system (assuming all nodes have sensors)
    D=0

    
    
    
    
    
    #steps through the simulation and allows for information to be gathered
    # at each step of the simulation
    for step in sim:
        #print(sim.current_time)
        #cant do below because it is a list object as seen in above print statement
        #timesteps.append(sim.current_time)
        
        count=0
        
        
        while count < nodecount:
            #creates a list of the current pollution values at each node
            placeholder.append(list(allnodesid[count].pollut_quality.values())[0])
            count=count+1
        #applies pollution values to a new row of nodes pollution
        nodespollution.append(placeholder)
        placeholder=[]
    
    #now that all data is out, transpose to make data in rows related to a single node
    #nodespollution=np.transpose(nodespollution)
#print(timesteps)

    #print(pollution[0])
        #placeholder=list(allnodesid[0].pollut_quality.values())[0]
        #print(placeholder)
#print(nodespollution)



#######################################################
#
#   Experimentation with definitions
#
#######################################################

  
#recursive branches function to account for branches within branches
def branches(currentlink, nextnode, endnode):
    branchcount=0
    #need to know the position of branch in linkinlets
    #   to be able to start from it later
    #   think each position represent child in set of children
    branchposition=[]
    count=0
    oglink=currentlink
    sumoflengths=0
    midsumoflengths=0
    #count branches for current set. if only 1 path then it acts like 1 path.
    #   if no path then everything else is skipped and function returns 0
    for node in linkinletsid:
		if nextnode==node:
            branchposition.append(count)
			branchcount=branchcount+1
        count=count+1
    #now time to check connections per each branch and any additional branches
    #   and if those branches lead to endnode
	x=0
    count=0
    #think checking for children of each child. checking for outlet of each inlet
    while x<branchcount:
        #we need nextnode to be reset to the child of the
        #   current child in the set of children
        nextnode=linkoutletsid[branchposition[x]]
        #here we check if the outlet has an inlet i.e child
        count=0
        while count<linkcount:
            
            #condition for when the end node is equivelent to current node
            #   we want to end the branch and return the sum of lengths found
            #   along the way
            if nextnode==endnode:#or do i use nextnode? yes because linkoutlets[count] would cause this to interact when not desired
                #make sure link is a conduit so we dont go out of bounds
                #   for the count and try added that which doesn't exist
                if linkids[count].is_conduit():
                #since we break below we won't reach end of branch
                #   where midsumoflengths is added to sumoflengths
                #   so we need to add it here. 
                    sumoflengths=length[count]+midsumoflengths
                #break this while loop so that the next branch is calculated
                #   and nothing else happens in this branch
                break
            #condition for when inlet is found i.e child of child is found
            if linkinletsid[count]==nextnode:
                #link with outlet at count is same as link with inlet at count
                #   and therefore should be our current link that we get
                #   a length from
                currentlink=linkids[count]
                #the nextnode here needs to then become the outlet so we can 
                #   check if this outlet acts as an inlet(i.e has children)
                #nextnode=linkoutletsid[count]#is this needs??????? no updates when branch is caolled??
                
                
                #recursively will check for additional branches of current node
                #   the return should be the sumoflengths of the recursed function
                #   the result should be added to our sumlengths in this
                #   of recursion since we know this branch for sure ended in
                #   with appropriate value----something might be wrong here???
                #   should it be midsumoflengths? or is there an event
                #   midsumoflengths is fucky here
                midsumoflengths=branches(currentlink, nextnode,endnode)+midsumoflengths
                #midsumoflengths should also be added from current conduit
                #   and excluding nonconduits
                if currentlink.is_conduit() and not (midsumoflengths==0):
                    #count should still be related to the parent i.e inlet
                    #   of the outlet therefore count should be at right index
                    #   for length....hopefully?
                    midsumoflengths=length[count]+midsumoflengths
                    
             #if x+1=branchcount and midsumoflengths not == 0
                 #midsumoflengths= (length of oglink)+midsumoflengths
                 
                 
                #nextnode=linkoutletsid[count]
            #does below need to be there?? probably not. should be covered
            #   by if nextnode==endnode: at the top
            #condition for when end node is not ever found after
            #   the all indicies are checked
            #if (count==linkcount-1) and not(nextnode==endnode):
                #because the target endnode isn't ever found we have no 
                #   interest in whatever sumsoflengths found in this branch are
                #   therefore the midsumlengths needs to equal 0????
                #   something fucky here too maybe?
                #midsumoflengths=0
                #return 0
                #break
            count=count+1
            sumoflengths=midsumoflengths+sumoflengths
            
        #after everybranch path is resolve the midsumoflengths is added to the
        #   whole sumoflengths. if a branch returns a 0 to its sumoflengths
        #   then the midsumoflengths is equal to 0 and therefore doesnt
        #   change the sumoflengths. a return of 0 means no path ended in the
        #   end node        wrong we want it after every branch since it would
        #       zeroed out and successful anyways. it above now
        #sumoflengths=midsumoflengths+sumoflengths
        
        
        #recursively will check for additional branches of current node
        #   not here thoughntis was just beng held
            #branches(currentlink,nextnode,endnode)
        
        
        x=x+1

    #return sumoflengths after all branches have been accounted for 
    #   which will then be calculated to any midsumoflength
    return sumoflengths



#subcatchment stuff in case we want it
#subcatchments=pyswmm.Subcatchments(sim)
#subbiesid=[]
#subbies=[]
#subbiesoutlets=[]    
    #for subcatchment in subcatchments:
    #   subbiesid.append(subcatchment)
    #   subbies.append(subcatchment.subcatchmentid)
    #   subbiesoutlets.append(subcatchment.connection)



#python dict function to store all our list and big data. savable into a json.
#django web server. has a data model which stores all componenets and measurements
#   possibly use to organziealll data. django
    