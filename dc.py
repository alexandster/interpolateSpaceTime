from datetime import datetime
import glob, os, sys
import numpy as np
import shutil

sys.setrecursionlimit(2000)

#parameters
sdNum = 0 
p2 = 0.2959848493588502       		#bandwidth
p4 = 0.01826823663906559/2.0       	#resolution
p6 = 20        						#max points per subdomain threshold
p7 = 0.01							#buffer ratio threshold

#directories
mdir = "outputs"
dir1 = mdir + os.sep + "pointFiles"
dir2 = mdir + os.sep + "boundaryFiles"
tdir = mdir + os.sep + "timeFiles"

if not os.path.exists(mdir):
    os.makedirs(mdir)
if not os.path.exists(dir1):
    os.makedirs(dir1)
if not os.path.exists(dir2):
    os.makedirs(dir2)
if not os.path.exists(tdir):
    os.makedirs(tdir)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def assign(inXf, inYf, inZf, inPf, xmaxf, xminf, ymaxf, yminf):
    
    xr2 = (xmaxf + xminf)/2     # Subdomain division x coordinates (middle of range)
    yr2 = (ymaxf + yminf)/2     # Subdomain division y coordinates (middle of range)
    

    sdX1, sdX2, sdX3, sdX4 = [],[],[],[]    #list of data points for each subdomain (X-coordiantes)
    sdY1, sdY2, sdY3, sdY4 = [],[],[],[]    #list of data points for each subdomain (Y-coordiantes)
    sdZ1, sdZ2, sdZ3, sdZ4 = [],[],[],[]    #list of data points for each subdomain (Z-coordiantes)
    sdP1, sdP2, sdP3, sdP4 = [],[],[],[]    #list of data points for each subdomain (pollen counts)

    for x, y, z, p in zip(inXf, inYf, inZf, inPf):       # assign each data point to subdomain
        if x < xr2 - p2:
            if y < yr2 - p2:
                sdX1.append(x), sdY1.append(y), sdZ1.append(z), sdP1.append(p)
            elif y < yr2 + p2:
                sdX1.append(x), sdY1.append(y), sdZ1.append(z), sdP1.append(p)
                sdX3.append(x), sdY3.append(y), sdZ3.append(z), sdP3.append(p)
            else:
                sdX3.append(x), sdY3.append(y), sdZ3.append(z), sdP3.append(p)

        elif x < xr2 + p2:                
            if y < yr2 - p2:
                sdX1.append(x), sdY1.append(y), sdZ1.append(z), sdP1.append(p)
                sdX2.append(x), sdY2.append(y), sdZ2.append(z), sdP2.append(p)
            elif y < yr2 + p2:
                sdX1.append(x), sdY1.append(y), sdZ1.append(z), sdP1.append(p)
                sdX2.append(x), sdY2.append(y), sdZ2.append(z), sdP2.append(p)
                sdX3.append(x), sdY3.append(y), sdZ3.append(z), sdP3.append(p)
                sdX4.append(x), sdY4.append(y), sdZ4.append(z), sdP4.append(p)
            else:
                sdX3.append(x), sdY3.append(y), sdZ3.append(z), sdP3.append(p)
                sdX4.append(x), sdY4.append(y), sdZ4.append(z), sdP4.append(p)
        else:
            if y < yr2 - p2:
                sdX2.append(x), sdY2.append(y), sdZ2.append(z), sdP2.append(p)
            elif y < yr2 + p2:
                sdX2.append(x), sdY2.append(y), sdZ2.append(z), sdP2.append(p)
                sdX4.append(x), sdY4.append(y), sdZ4.append(z), sdP4.append(p)
            else:
                sdX4.append(x), sdY4.append(y), sdZ4.append(z), sdP4.append(p)

    sdXYZd = [sdX1, sdY1, sdZ1, sdP1, sdX2, sdY2, sdZ2, sdP2, sdX3, sdY3, sdZ3, sdP3, sdX4, sdY4, sdZ4, sdP4, xr2, yr2]

    return sdXYZd 

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def decompose(inXd, inYd, inZd, inPd, xmind, xmaxd, ymind, ymaxd):    # inXd: list of x-coordinates \ inYd: list of y-coordinates \ inZd: list of z-coordinates \ inPd: list of pollen counts
                                                                                                                    # xmind: subdomain lower x boundary \ xmaxd: subdomain upper x boundary \ ymind: subdomain lower x boundary
                                                                                                                    # ymaxd: subdomain upper y boundary \ zmind: subdomain lower x boundary \ zmaxd: subdomain upper z boundary
                                                                                                                    # xybufd: spatial buffer \ zbufd: temporal buffer
                                                                                                                    
    global sdNum
    sdNum += 1
    
    xminDiff = xmind%p4
    xmaxDiff = xmaxd%p4
    yminDiff = ymind%p4
    ymaxDiff = ymaxd%p4

    xminP = xmind - xminDiff + p4
    xmaxP = xmaxd - xmaxDiff + p4
    yminP = ymind - yminDiff + p4
    ymaxP = ymaxd - ymaxDiff + p4

    xC = len(np.arange(xminP, xmaxP, p4))             # for all possible x-coordinates that are within the subdomain (according to xy resolution) 
    yC = len(np.arange(yminP, ymaxP, p4))         # for all possible y-coordinates that are within the subdomain (according to xy resolution)

    xDim = xmaxd - xmind
    yDim = ymaxd - ymind

    sdArea = xDim * yDim
    bufArea = (xDim + 2 * p2) * (yDim + 2 * p2) 
    bufRatio = sdArea / bufArea

    leninXd = len(inXd)

    if leninXd is 0:    # if there are no data points within subdomain, pass
        pass
    elif xC is 0:   #if there are no regular grid points within subdomain, pass
        pass
    elif yC is 0:
        pass
    elif leninXd <= p6 or bufRatio <= p7:

        i = 0      

        fn1 = open(dir1 + os.sep + "pts_" + str(sdNum) + "_" + str(1) + ".txt", "w")
        fn2 = open(dir1 + os.sep + "pts_" + str(sdNum) + "_" + str(2) + ".txt", "w")
        fn3 = open(dir1 + os.sep + "pts_" + str(sdNum) + "_" + str(3) + ".txt", "w")
        fn4 = open(dir1 + os.sep + "pts_" + str(sdNum) + "_" + str(4) + ".txt", "w")

        fn1.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.0) + "," + str(0.3209169054441261) + "\n")
        fn2.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.3209169054441261) + "," + str(0.5444126074498568) + "\n")
        fn3.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.5444126074498568) + "," + str(0.7679083094555874) + "\n")
        fn4.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + ","+ str(0.7679083094555874) + "," + str(1.0) + "\n")
        
        while i < leninXd:

            tCo = inZd[i]

            wData = str(inXd[i]) + "," + str(inYd[i]) + "," + str(inZd[i]) + "," + str(inPd[i]) + "\n"
            
            if tCo < 0.2349570200573066:
                fn1.write(wData)
            elif tCo < 0.4068767908309456:
                fn1.write(wData)
                fn2.write(wData)

            elif tCo < 0.4584527220630373:
                fn2.write(wData)

            elif tCo < 0.6303724928366762:
                fn2.write(wData)
                fn3.write(wData)

            elif tCo < 0.6819484240687679:
                fn3.write(wData)

            elif tCo < 0.8538681948424068:
                fn3.write(wData)
                fn4.write(wData)

            else:
                fn4.write(wData)

            i += 1

        fn1.close()
        fn2.close()
        fn3.close()
        fn4.close()            
            
    else:   # if number of points in subdomain is higher than threshold, keep decomposing.
        sdXYZ = assign(inXd, inYd, inZd, inPd, xmaxd, xmind, ymaxd, ymind)        
        decompose(sdXYZ[0], sdXYZ[1], sdXYZ[2], sdXYZ[3], xmind, sdXYZ[-2], ymind, sdXYZ[-1])      # recursive function call 1
        decompose(sdXYZ[4], sdXYZ[5], sdXYZ[6], sdXYZ[7], sdXYZ[-2], xmaxd, ymind, sdXYZ[-1])      # recursive function call 2
        decompose(sdXYZ[8], sdXYZ[9], sdXYZ[10], sdXYZ[11], xmind, sdXYZ[-2], sdXYZ[-1], ymaxd)      # recursive function call 3
        decompose(sdXYZ[12], sdXYZ[13], sdXYZ[14], sdXYZ[15], sdXYZ[-2], xmaxd, sdXYZ[-1], ymaxd)    # recursive function call 4
            
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#read input files
pFile = "files/data.txt"		#data
bFile = "files/data_bds.txt"	#rectangular envelope - domain

pFile_i = open(pFile, "r")
inX, inY, inZ, inP = [], [], [], []
next(pFile_i)
for record in pFile_i:   
    inX.append(float(record.split(",")[0]))
    inY.append(float(record.split(",")[1]))
    inZ.append(float(record.split(",")[2]))
    inP.append(float(record.split(",")[3]))
pFile_i.close()

r = open(bFile, "r").read().split(",")
xmin, xmax, ymin, ymax = float(r[0]), float(r[1]), float(r[2]), float(r[3])

#------------------------------------------------------------------------------
#decompose
startTime = datetime.now()

decompose(inX, inY, inZ, inP, xmin, xmax, ymin, ymax)

endTime = datetime.now()
runTime = endTime - startTime
print(runTime)

tFile = tdir + os.sep + "tdecomp_1.txt"
tFile_i=open(tFile, "w")
tFile_i.write(str(runTime))
tFile_i.close()



