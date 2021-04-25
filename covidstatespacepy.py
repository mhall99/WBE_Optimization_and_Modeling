# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 11:34:37 2021

@author: Shalk
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 17:03:43 2021

@author: Shalk
"""

# Imported modules
import pyswmm  # The SWMM module
import matplotlib.pyplot as plt
from past.utils import old_div  # Module for plotting
import scipy.signal as signal
import numpy as np
import re
import sippy as sp

# ***********************************************************************
#  Declaration of simulation files and variables
# ***********************************************************************

#dont forget to change inp depending on your own hierarchy
inp    = "swmm_files/3tanks.inp"  # Input file

aeflow   = []
time   = []
flowtime = []


totallength=0

    
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


#recursive branches function to account for branches within branches
#   this will take a start and end node and look for all paths from start
#   which reach the end. it returns the links with duplicates along path
#   and whether or not there was any connecting path
def branches(nextnode, endnode):
    
    branchcount=0
    #need to know the position of branch in linkinlets
    #   to be able to start from it later
    branchposition=[]
    allfoundlinks=[]
    count=0
    pathtoend=False
    pathtoendcounter=0
    #nodeofpath=nextnode
    #count branches for current set. if only 1 path then it acts like 1 path.
    #   if no path then everything else is skipped and function returns 0
    #print(nextnode.nodeid)
    while count<linkcount:
        #print(linkinletsid[count].nodeid)
        if nextnode==linkinletsid[count]:
            branchposition.append(count)
            branchcount=branchcount+1
        count=count+1
            
        
    #print(branchposition)
    #print(branchcount)
    #now time to check connections per each branch and any additional branches
    #   and if those branches lead to endnode
    x=0
    count=0
    # checking for outlet of each inlet
    while x<branchcount:
        #we need nextnode to be reset to the child of the
        #   current child in the set of children
        nextnode=linkoutletsid[branchposition[x]]
        
        #currentlink=linksid[branchposition[x]].linkid
        #print("branch for", nodeofpath.nodeid,"->", nextnode.nodeid,
        #     "has link", currentlink,"at position", branchposition[x])
        gotwhatwewanted=False
        #here we check if the outlet has an inlet i.e child
        count=0
        while gotwhatwewanted==False:
            
            #condition for when the end node is equivelent to current nextnode
            #   count is not related to the link of this path
            if (nextnode==endnode):
                pathtoendcounter=pathtoendcounter+1
                
                #print("found an end", nodeofpath.nodeid,"->", nextnode.nodeid,
                #     "current link", currentlink,"at position", branchposition[x])
                allfoundlinks.append(branchposition[x])
                #if linksid[count].is_conduit():
                    #or is it currentlink= linksid[count] and then
                    #   append it at the end
                    #link with outlet at count is same as link with inlet at count
                    #   and therefore should be our current link that we get
                    #   a length from
                    #print(linksid[count].linkid)
                    #currentlink=linksid[count].linkid
                    #allfoundlinks.append(currentlink)   
                #since this is the endnode we got what we wanted from this branch
                gotwhatwewanted=True
                
            #condition for when inlet is found
            elif linkinletsid[count]==nextnode:
                
                #print(nextnode.nodeid)
                #print("found a path")
                
                #recursively will check for additional branches of current node
                #   the return should be the sumoflengths and whether any path
                #   of the recursed function had an end which was true
                currentlinks,pathtoend=branches(nextnode,endnode)
                
                #midsumoflengths should also be added from current conduit
                #   and excluding nonconduits
                if pathtoend:
                    #reset pathtoend to false so next path can be assesses true
                    #   or false. also add to counter
                    pathtoendcounter=pathtoendcounter+1
                    pathtoend=False
                    #print("true path branch position",branchposition[x])
                    for y in currentlinks:
                        allfoundlinks.append(y)
                    allfoundlinks.append(branchposition[x])
                #since we found our first occurance of inlet and the recursion
                #   takes care of the we got what we wanted from this branch
                gotwhatwewanted=True
                
            #condition for if the number of links is equal to the indicies
            #   of count. 11 links counted so index 0->10 in count
            elif (count==linkcount-1):
                #we know there was nothing to gain from this branch
                #   so we got what we wanted
                #print("path ended with nothing")
                gotwhatwewanted=True
                
            count=count+1
        
        x=x+1
    #if the pathtoendcounter has incremented that means at least 1 path
    #   has been found in the branches which is worth return a value for
    #   making a path to end true.
    if pathtoendcounter > 0:
        pathtoend=True
    
    #print("this is allfoundlinks",allfoundlinks,"for node", nodeofpath.nodeid,"->",nextnode.nodeid)
    #return sumoflengths after all branches have been accounted for 
    #   which will then be calculated to any midsumoflength
    return allfoundlinks, pathtoend

#rows are each inputnode, columns are the length from inputnode
#   to end node corresponding to allnodesid.
#   this yields an m allnodesid by n allnodesid table of lengths from m->n
def allpathlengths(nodeids):
    x=0
    for n in nodeids:
        count=0
        placeholder=[]
        while count<nodecount:
            s2elength=0
            s2epositionsreduced=[]
            s2epositions, waslegit=branches(n,nodeids[count])
            s2epositionsreduced=[i for n,i in enumerate(s2epositions)
                     if i not in s2epositions[:n]]       
            for y in s2epositionsreduced:
                if linksid[y].is_conduit():
                    s2elength=s2elength+length[y]
            placeholder.append(s2elength)
            count=count+1
        lengthsfrominput.append(placeholder)     
    x=0        
    while x<nodecount:
        print(nodeids[x].nodeid, lengthsfrominput[x])
        x=x+1
    return lengthsfrominput

nodesinflow=[]
nodespollution=[]
placeholder=[]
timesteps=[]

with pyswmm.Simulation(inp) as sim:
    links = pyswmm.Links(sim)
    nodes = pyswmm.Nodes(sim)
    systemrouting=pyswmm.SystemStats(sim)
    
    
    get_nodes_and_links(links, nodes)
    length=get_link_length(inp)
    
    for x in length:
        totallength=x+totallength
    
    x=0
    inputnodes=[]
    lengthsfrominput=[]
    
    
    lengthsfrominput=allpathlengths(allnodesid)
    
    
    #steps through the simulation and allows for information to be gathered
    #   at each step of the simulation
    for step in sim:
        #print(sim.current_time)
        #cant do below because it is a list object as seen in above print statement
        #timesteps.append(sim.current_time)
        
        
        count=0
        placeholder=[]
        pholder2=[]
        while count < nodecount:
            #creates a list of the current pollution values at each node
            placeholder.append(list(allnodesid[count].pollut_quality.values())[0])
            if allnodesid[count].lateral_inflow>0:
                pholder2.append(193500/allnodesid[count].lateral_inflow)
            else:
                pholder2.append(allnodesid[count].lateral_inflow)
            count=count+1
        #applies pollution values to a new row of nodes pollution
        nodespollution.append(placeholder)
        nodesinflow.append(pholder2)
        
        #print(nodespollution[0])
        #print(placeholder)
    
    #print(nodespollution)
#print(timesteps)
count=0
rollingtotal=0
Y=[]
#a_file=open("output_pollution","w")
while(count<len(nodespollution)):
    
    Y.append(nodespollution[count])
       
    #np.savetxt(a_file,nodespollution[count])
    #print(nodespollution[count])
    rollingtotal=rollingtotal+1
    count=count+60

Y=np.transpose(Y)
U=[]
count=0
while(count<len(nodesinflow)):
    U.append(nodesinflow[count])
    count=count+60
    
U = np.transpose(U)

ts = 100
tfin = 28600
npts = int(old_div(tfin, ts)) + 1
method = 'PARSIM-K'
id_sys=sp.system_identification(Y, U, method, SS_f=60, SS_p=60, SS_fixed_order=50, tsample=ts, SS_A_stability=False)      
#a_file.close()
xid, yid = sp.functionsetSIM.SS_lsim_process_form(id_sys.A, id_sys.B, id_sys.C, id_sys.D, U, id_sys.x0)
Time = np.linspace(0, tfin, npts)

plt.close("all")
fig0 = plt.figure(0)
plt.subplot(2, 1, 1)

plt.plot(Time, Y[0])
plt.plot(Time, yid[0])
plt.ylabel("y_tot[0]")
plt.grid()
# plt.xlabel("Time")
# plt.title("Ytot[1]")
plt.legend(['Original system', 'Identified system, ' + method])


norm_of_difference_Y0 = np.zeros((287, 1))
#norm_of_difference_Y1_8node = np.zeros((1, 287))
diff = np.zeros((1, 287))
diff[0, :] = (Y[0] - yid[0])
#diff_8node[1, :] = (y_tot_8node[1, :] - yid_8node[1, :])

#norm_of_difference_Y0_eyeC = np.zeros((601, 1))
#norm_of_difference_Y1_eyeC = np.zeros((601, 1))
#diff_eyeC = np.zeros((2, 601))
#diff_eyeC[0, :] = (y_tot_eyeC[0, :] - yid_eyeC[0, :])
#diff_eyeC[1, :] = (y_tot_eyeC[1, :] - yid_eyeC[1, :])

for n in range(0, 287):
    norm_of_difference_Y0[n, 0] = np.linalg.norm(diff[0, n]) #(diff[0, n] * (10 ** 2))
    #norm_of_difference_Y1_8node[n, 0] = np.linalg.norm(diff_8node[1, n] * (10 ** 2))
    #norm_of_difference_Y0_eyeC[n, 0] = np.linalg.norm(diff_eyeC[0, n] * (10 ** 2))
    #norm_of_difference_Y1_eyeC[n, 0] = np.linalg.norm(diff_eyeC[1, n] * (10 ** 2))
    #print(norm_of_difference)
plt.subplot(2,1,2)
plt.plot(Time, norm_of_difference_Y0[:,0])
#plt.plot(Time, norm_of_difference_Y1_eyeC[:, 0])
plt.ylabel("L2 norm between Y & yid")
plt.grid()
plt.xlabel("Time")
