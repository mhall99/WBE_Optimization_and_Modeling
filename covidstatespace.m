clear all
load('swmmSS');
inp = '3tanks.inp'

CurrentValue.SystemDynamicMatrix.A = A;
CurrentValue.SystemDynamicMatrix.C = C;
CurrentValue.tInMin = 0;
CurrentValue.Np = 140;
CurrentValue.PipeReactionCoeff = -0.00000001;
CurrentValue.delta_t = 10;
CurrentValue.CurrentValue = 10;
CurrentValue.CurrentFlow = 10;
CurrentValue.CurrentNodeTankVolume = 10;
CurrentValue.CurrentVelocityPipe = 10;

aux.NumberofSegment4Pipes = 10;
%massenergymatrix for aux nevermind

swmm = SWMM;
%RETRIEVING VARIABLE IDs FROM THE .INP
links = swmm.get_all(inp, swmm.LINK, swmm.NONE);
nodes = swmm.get_all(inp, swmm.NODE, swmm.NONE);
subcatch= swmm.get_all(inp, swmm.SUBCATCH, swmm.NONE);
storage= swmm.get_all(inp, swmm.STORAGE, swmm.NONE);
%aux.NumberofSegment
%aux.NumberofSegment4Pipes
%aux.LinkLengthPipe
%aux.LinkDiameterPipe
%aux.TankBulkReactionCoeff
%aux.TankMassMatrix
%aux.JunctionMassMatrix
%aux.MassEnergyMatrix
%aux.NodeNameID
%aux.LinkNameID
%aux.NodesConnectingLinksID
%aux.COMPARE
JunctionCount = size(nodes);
JunctionCount = JunctionCount(1,2);
%we are equating subcatchments in swmm to resevoirs in epanet
ReservoirCount=size(subcatch)
ReservoirCount= ReservoirCount(1,2);
ElementCount.ReservoirCount = ReservoirCount;

numberofNodes = JunctionCount;
ElementCount.JunctionCount = JunctionCount;
%we are equating conduits in swmm to pipes in epanet
PipeCount=size(links);
PipeCount= PipeCount(1,2);
ElementCount.PipeCount=PipeCount;
%valves have no real swmm equivalent
ValveCount=0;
ElementCount.ValveCount=ValveCount;
%pumps in swmm can be equated to pumps in epanet however
%   it might be best to run swmm as though the pumps aren't going/existing
PumpCount=0;
ElementCount.PumpCount=0;
%we are equating storage units in swmm to tanks in epanet
TankCount=size(storage);
TankCount=TankCount(1,2);
ElementCount.TankCount=TankCount;

numberofX = size(x0);
numberofX = numberofX(1,1);
numberofStep5mins = 100; %not sure what this should be
IndexInVar.NumberofX = numberofX;
sensorNumberArray = [1:9] %[1:JunctionCount] junctioncount=number of nodes, cant be, must < nodecount

NumberofElement=PipeCount+JunctionCount+ValveCount+PumpCount+TankCount+ReservoirCount;
IndexInVar.NumberofElement = NumberofElement;
IndexInVar.Junction_CIndex = allnodesstr; %to be imported later 
IndexInVar.Reservoir_CIndex = subcatch;
IndexInVar.Tank_CIndex = storage;
blah = size(links)
blah = blah(1,2)
Pipe_CIndex = zeros(blah, NumberofSegments4Pipes)

IndexInVar.Pipe_CIndex = 

PreviousValue.tInMin = 0;
PreviousValue.X_estimated = x0;
PreviousValue.PreviousNumberofSegment4Pipes = 235;
PreviousValue.IndexInVarOld = IndexInVar;
%sensorSelectionResult = 
%ObtainSensorPlacement2(CurrentValue,aux,ElementCount,PreviousValue,numberofNodes,numberofX,numberofStep5mins,sensorNumberArray)

