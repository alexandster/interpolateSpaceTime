#import modules
from datetime import datetime
from scipy import spatial
import glob, os, sys, math
import settings_CV as sett, numpy as np

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#initialize global variables
sett.init()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#parameters
sett.p1 = sys.argv[1]				#fold
p = int(sys.argv[2]) / 1000.0		#parameter p

sett.p2 = 0.2959848493588502       	#bandwidth
sett.p3 = 0

sett.dir1 = 'CV_decomp/fold_' + sett.p1
sett.dir2 = 'CV_result' 

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#create directories
if not os.path.exists(sett.dir1):
    os.makedirs(sett.dir1)
if not os.path.exists(sett.dir2):
    os.makedirs(sett.dir2)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#open output file    
outFile = open(sett.dir2 + os.sep + "st_idw_" + str(p) + "_" + str(sett.p1) + ".txt" , "w")       # Open output file

#performance menasures: Sum of Squared Differences (SSD), Mean Absolute Relative Error (MARE), Root Mean Square Percentage Error (RMSPE)  
SSD = MARE = RMSPE = 0

# loop through all subdomains, compute performance measures
for trData, teData in zip(sorted(glob.glob(sett.dir1 + os.sep + "ptr_*")), sorted(glob.glob(sett.dir1 + os.sep + "pte_*"))):        # Loop through all subdomains

    #open point files
    trFile = open(trData, "r")
    teFile = open(teData, "r")

    #header: boundaries
    r = trFile.readline().split(",")
    e = teFile.readline()
    xmin, xmax, ymin, ymax, zmin, zmax = float(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5].strip())
  
    #read training data
    trX, trY, trZ, trP = [], [], [], []	
    for record in trFile:   
        trX.append(float(record.split(",")[0]))
        trY.append(float(record.split(",")[1]))
        trZ.append(float(record.split(",")[2]))
        trP.append(float(record.split(",")[3]))
    trFile.close()

    tr_xyzp = zip(trX, trY, trZ, trP)
    tr_xyz = zip(trX, trY, trZ)

    #read test data
    te_xyz, te_xyzp = [], []
    teX, teY, teZ, teP = [], [], [], []
    for record in teFile:   		
        teX = float(record.split(",")[0])
        teY = float(record.split(",")[1])
        teZ = float(record.split(",")[2])
        teP = float(record.split(",")[3])
        te_xyz.append([teX, teY, teZ])
        te_xyzp.append([teX, teY, teZ, teP])

    teFile.close()

    i = 0

    while i < len(te_xyz):	#for each test point

        xC, yC, zC = te_xyz[i][0], te_xyz[i][1], te_xyz[i][2]

        distanceSum = 0.0
        productSum = 0.0

        j = 0
        while j < len(tr_xyz):  	#for each training point      
      
            distance = Distance3D(tr_xyzp[j][0], tr_xyzp[j][1], tr_xyzp[j][2], xC, yC, zC) #calculating 3D distance between voxel and known data points
 
            if distance < sett.p2:

                distancePower = (1.0 / distance) ** p	#power parameter p

                distanceSum += distancePower
                productSum += (distancePower) * tr_xyzp[j][3]  
              
            j += 1 
 
        if distanceSum > 0.0:
            estimate = productSum / distanceSum
        else:
            estimate = 0.0

        #keep a running  sum of squared differences between estimate and observed value
        SSD += (estimate - te_xyzp[i][3]) ** 2 	#sum of squared differences
        MARE += abs(estimate - te_xyzp[i][3]) / te_xyzp[i][3]
        RMSPE += MARE ** 2
                   
        i = i + 1
    
outFile.write(str(SSD) + "," + str(MARE) + "," + str(RMSPE))
outFile.close()

