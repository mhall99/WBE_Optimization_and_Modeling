clear all
load('swmmSS');
inp = '3tanks.inp'
if A == A'
    disp('Yes')
end
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
PreviousNumberofSegment4Pipes = 235;
NumberofSegment4Pipes = 235;

swmm = SWMM;
%RETRIEVING VARIABLE IDs FROM THE .INP
links = swmm.get_all(inp, swmm.LINK, swmm.NONE);
nodes = swmm.get_all(inp, swmm.NODE, swmm.NONE);
subcatch= swmm.get_all(inp, swmm.SUBCATCH, swmm.NONE);
storage= swmm.get_all(inp, swmm.STORAGE, swmm.NONE);
junction=swmm.get_all(inp, swmm.JUNCTION, swmm.NONE);
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
JunctionCount = size(junction);
JunctionCount = JunctionCount(1,2);
%we are equating subcatchments in swmm to resevoirs in epanet
ReservoirCount=size(subcatch);
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
sensorNumberArray = [1:3]; %[1:JunctionCount] junctioncount=number of nodes, cant be, must < nodecount

NumberofElement=PipeCount+JunctionCount+ValveCount+PumpCount+TankCount+ReservoirCount;
IndexInVar.NumberofElement = NumberofElement;
IndexInVar.Junction_CIndex = junction; %to be imported later 
IndexInVar.Reservoir_CIndex = subcatch;
IndexInVar.Tank_CIndex = storage;
blah = size(links);
blah = blah(1,2);
Pipe_CIndex = zeros(blah, NumberofSegment4Pipes);
v=4;
for j=1:blah
    for i=1:NumberofSegment4Pipes
        Pipe_CIndex(j, i) = v;
        v = v+1;
    end
end

IndexInVar.Pipe_CIndex = Pipe_CIndex;
IndexInVar.Pipe_CStartIndex = 4;
IndexInVar.Pump_CIndex = [];
IndexInVar.Valve_CIndex = [];

IndexInVar.JunctionsIndexInOrder=5;
IndexInVar.ReservoirIndexInOrder=3;
IndexInVar.TankIndexInOrder=8;
IndexInVar.PipeIndexInOrder=9;
IndexInVar.PumpIndexInOrder=[];
IndexInVar.ValveIndexInOrder=[];
IndexInVar.PumpIndex=[];
IndexInVar.ValveIndex=[];


PreviousValue.tInMin = 0;
PreviousValue.X_estimated = x0;
PreviousValue.PreviousNumberofSegment4Pipes = 235;
PreviousValue.IndexInVarOld = IndexInVar;
numberofStep5mins = 5;

%n = size(A,1)
%cvx_begin
    %variable A2(n,n)
    %minimize( norm(A-A2) )
    %subject to 
        %A2+A2' >= 0;
        %A2==A2';
%cvx_end
%CurrentValue.SystemDynamicMatrix.A = A2
sensorSelectionResult = ObtainSensorPlacement2(CurrentValue,aux,ElementCount,PreviousValue,numberofNodes,numberofX,numberofStep5mins,sensorNumberArray)

metric = size(Y);
metric = metric(1,2);
norm_of_diff_N5 = zeros(1,metric);
diff_N5 = zeros(1,metric);
diff_N5(1,:) = Y(1,:) - yid(1,:);
for n=1:metric
    norm_of_diff_N5(1,n) = norm(diff_N5(1,n));
end
total_error = sum(norm_of_diff_N5(:,1), 'all');

text = ['Total error is ', num2str(total_error)];
disp(text)

%d = epanet(inp)
%d.plot

Time = linspace(0,144,metric);
figure
%subplot(2,1,1)
plot(Time, Y(1,:))
hold on
plot(Time, yid(1,:))
xlabel('Time (hours)')
ylabel('Viral load (parts/L)')
legend('SWMM Y(t) for N-5', 'SS Y(t) for N-5')
grid on

%subplot(2,1,2)
%plot(Time,norm_of_diff_N5(1,:))
%grid on
%title('L2 error norm')
%xlabel('Time (hours)')
%ylabel('Error in viral parts/L')

