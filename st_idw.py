import math, os, sys, glob, datetime
import numpy as np
from scipy import spatial
import time

start_time = time.clock()

#parameters
jobNum = int(sys.argv[1])
stdt = 0.2959848493588502 		#bandwidth
res = 0.01826823663906559/2     #resolution
parameterP = 3.4		#power parameter for IDW

#-----------------------------------
#distance function:
#x1: x-coordinate data point (known location), y1: y-coordinate data point (known location), t1: t-coordinate data point (known location)
#x2: x-coordinate regular grid point (unknown location), y2: y-coordinate regular grid point (unknown location), t2: t-coordinate regular grid point (unknown location)
#c: scaling factor space-time
def Distance3D(x1, y1, t1, x2, y2, t2):
    dx = x2 - x1
    dy = y2 - y1
    ti = t2 - t1
    dit = (dx**2 + dy**2 + ti**2) ** 0.5
    return dit
#-----------------------------------

#directories
inDir = "outputs"
outDir = inDir + os.sep + "stIDW"
timeDir = inDir + os.sep + "timeFiles"
	
if not os.path.exists(outDir):
    os.makedirs(outDir)
if not os.path.exists(timeDir):
    os.makedirs(timeDir)

#list input data, sort, index
inFileDataList = glob.glob(inDir + os.sep + "pointFiles" + os.sep + "*")
inFileDataList.sort()
inFileData = inFileDataList[jobNum]

#time results
timeResults = open(timeDir + os.sep + "stIDW_time_" + inFileData.split(os.sep)[-1][4:], 'w')

t1 = datetime.datetime.now()

#open point file
fData = open(inFileData, "r")
inBoundList = [float(i) for i in fData.readline().split(",")]
xList, yList, tList, pList = [], [], [], []		    	# Lists of coordinates    
for line in fData:
    xList.append(float(line.split(",")[0]))      	# x-coordinate variable
    yList.append(float(line.split(",")[1]))        # y-coordinate variable
    tList.append(float(line.split(",")[2]))        # t-coordinate variable                                            
    pList.append(float(line.split(",")[3]))        # pollen count
fData.close()
xytzList = zip(xList, yList, tList, pList)
xytList = zip(xList, yList, tList)


t2 = datetime.datetime.now()

#open output file
outF = outDir + os.sep + "STIDW_" + inFileData.split(os.sep)[-1][4:]     
outFile = open(outF, "w")       # Open output file

xmin = float(inBoundList[0])
xmax = float(inBoundList[1])
ymin = float(inBoundList[2])
ymax = float(inBoundList[3])
zmin = float(inBoundList[4])
zmax = float(inBoundList[5])

xminDiff = xmin%res
xmaxDiff = xmax%res
yminDiff = ymin%res
ymaxDiff = ymax%res
zminDiff = zmin%res
zmaxDiff = zmax%res

xminP = xmin - xminDiff + res
xmaxP = xmax - xmaxDiff + res
yminP = ymin - yminDiff + res
ymaxP = ymax - ymaxDiff + res
zminP = zmin - zminDiff + res
zmaxP = zmax - zmaxDiff + res

#create grid of output points
xytGrid = []
for i in np.arange(xminP,xmaxP,res):
    for j in np.arange(yminP,ymaxP,res):
        for k in np.arange(zminP,zmaxP,res):
            xytGrid.append([i,j,k])

t3 = datetime.datetime.now()

#build k/d tree, NN-query
tree = spatial.cKDTree(xytList)
nList = tree.query_ball_point(xytGrid, stdt)

t4 = datetime.datetime.now()

#loop through NN, compute IDW
i = 0
while i < len(nList):        
      
    xC, yC, zC = xytGrid[i][0], xytGrid[i][1], xytGrid[i][2]

    distanceSum = 0.0
    count = 0
    productSum = 0.0

    if nList[i]:
        for k in nList[i]:
            nindex = int(k)
            distance = Distance3D(xytList[nindex][0], xytList[nindex][1], xytList[nindex][2], xC, yC, zC) #calculating 3D distance between voxel and known data points
 
            distancePower = (1 / distance) ** parameterP

            distanceSum += distancePower
            productSum += (distancePower) * xytzList[nindex][3]                

        estimate = productSum / distanceSum 

    else:
        estimate = 0.0
        
    outFile.write(str(xC) + "," + str(yC) + "," + str(zC) + "," + str(estimate) +"\n")
           
    i = i + 1

t5 = datetime.datetime.now()
outFile.close()

#write time results
delta_t1_2 = t2 - t1
delta_t2_3 = t3 - t2
delta_t3_4 = t4 - t3
delta_t4_5 = t5 - t4
timeResults.write("stkde_" + inFileData.split(os.sep)[-1][4:] + "," + str(delta_t1_2) + "," + str(delta_t2_3) + "," + str(delta_t3_4) + "," + str(delta_t4_5) + "\n")
timeResults.close()

    
