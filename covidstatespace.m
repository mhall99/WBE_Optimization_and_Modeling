clear all
load('sys_id')
inp = 'Water-Quality-Modeling-and-Sensor-Placement-master\WQSP\3tanks.inp'
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

swmm = SWMM
%RETRIEVING VARIABLE IDs FROM THE .INP
links = swmm.get_all(inp, swmm.LINK, swmm.NONE);
nodes = swmm.get_all(inp, swmm.NODE, swmm.NONE);
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

%sensorSelectionResult = 
%ObtainSensorPlacement2(CurrentValue,aux,ElementCount,PreviousValue,numberofNodes,numberofX,numberofStep5mins,sensorNumberArray)  