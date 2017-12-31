import assignment_CV as ass, settings_CV as sett, os

def decompose(trX, trY, trZ, trP, teX, teY, teZ, teP, xmind, xmaxd, ymind, ymaxd):    # trX: list of x-coordinates \ trY: list of y-coordinates \ trZ: list of z-coordinates \ trP: list of pollen counts
                                                                                                                    # xmind: subdomain lower x boundary \ xmaxd: subdomain upper x boundary \ ymind: subdomain lower x boundary
                                                                                                                    # ymaxd: subdomain upper y boundary \ zmind: subdomain lower x boundary \ zmaxd: subdomain upper z boundary
                                                                                                                    # xybufd: spatial buffer \ zbufd: temporal buffer
                                                                                                                    
    p2, p3, p4, p5, p6, p7, dir1 = sett.p2, sett.p3, sett.p4, sett.p5, sett.p6, sett.p7, sett.dir1   

    sett.sdNum += 1
    
    xminDiff = xmind%p4
    xmaxDiff = xmaxd%p4
    yminDiff = ymind%p4
    ymaxDiff = ymaxd%p4

    xminP = xmind - xminDiff + p4
    xmaxP = xmaxd - xmaxDiff + p4
    yminP = ymind - yminDiff + p4
    ymaxP = ymaxd - ymaxDiff + p4

    xC, yC = 0,0

    xIter = xminP		# for all possible x-coordinates that are within the subdomain (according to xy resolution) 
    while xIter < xmaxP:
        xC += 1
        xIter += sett.p4

    yIter = yminP		# for all possible y-coordinates that are within the subdomain (according to xy resolution)
    while yIter < ymaxP:
        yC += 1
        yIter += sett.p4

    xDim = xmaxd - xmind
    yDim = ymaxd - ymind

    sdArea = xDim * yDim
    bufArea = (xDim + 2 * p2) * (yDim + 2 * p2) 
    bufRatio = sdArea / bufArea

    lentrX = len(trX)
    lenteX = len(teX)

    if lentrX is 0:    # if there are no data points within subdomain, pass
        pass
    elif xC is 0:   #if there are no regular grid points within subdomain, pass
        pass
    elif yC is 0:
        pass
    elif lentrX <= p6 or bufRatio <= p7:

        i = 0      
        
        #open files
        ftr1 = open(dir1 + os.sep + "ptr_1_" + str(sett.sdNum) + ".txt", "w")
        ftr2 = open(dir1 + os.sep + "ptr_2_" + str(sett.sdNum) + ".txt", "w")
        ftr3 = open(dir1 + os.sep + "ptr_3_" + str(sett.sdNum) + ".txt", "w")
        ftr4 = open(dir1 + os.sep + "ptr_4_" + str(sett.sdNum) + ".txt", "w")

        fte1 = open(dir1 + os.sep + "pte_1_" + str(sett.sdNum) + ".txt", "w")
        fte2 = open(dir1 + os.sep + "pte_2_" + str(sett.sdNum) + ".txt", "w")
        fte3 = open(dir1 + os.sep + "pte_3_" + str(sett.sdNum) + ".txt", "w")
        fte4 = open(dir1 + os.sep + "pte_4_" + str(sett.sdNum) + ".txt", "w")

        #write header: boundaries
        ftr1.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.0) + "," + str(0.3209169054441261) + "\n")
        ftr2.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.3209169054441261) + "," + str(0.5444126074498568) + "\n")
        ftr3.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.5444126074498568) + "," + str(0.7679083094555874) + "\n")
        ftr4.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.7679083094555874) + "," + str(1.0) + "\n")

        fte1.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.0) + "," + str(0.3209169054441261) + "\n")
        fte2.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.3209169054441261) + "," + str(0.5444126074498568) + "\n")
        fte3.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.5444126074498568) + "," + str(0.7679083094555874) + "\n")
        fte4.write(str(xmind) + "," + str(xmaxd) + "," + str(ymind) + "," + str(ymaxd) + "," + str(0.7679083094555874) + "," + str(1.0) + "\n")
        
        #write body: training coordinates
        while i < lentrX:
            tCo = trZ[i]
            wData = str(trX[i]) + "," + str(trY[i]) + "," + str(trZ[i]) + "," + str(trP[i]) + "\n"          
            
            if tCo < 0.2349570200573066:
                ftr1.write(wData)
            elif tCo < 0.4068767908309456:
                ftr1.write(wData)
                ftr2.write(wData)
            elif tCo < 0.4584527220630373:
                ftr2.write(wData)
            elif tCo < 0.6303724928366762:
                ftr2.write(wData)
                ftr3.write(wData)
            elif tCo < 0.6819484240687679:
                ftr3.write(wData)
            elif tCo < 0.8538681948424068:
                ftr3.write(wData)
                ftr4.write(wData)
            else:
                ftr4.write(wData)
            i += 1

        i = 0 
        #write body: test coordinates
        while i < lenteX:
            tCo = teZ[i]
            wData = str(teX[i]) + "," + str(teY[i]) + "," + str(teZ[i]) + "," + str(teP[i]) + "\n"          
            
            if tCo < 0.4068767908309456:
                fte1.write(wData)
            elif tCo < 0.6303724928366762:
                fte2.write(wData)
            elif tCo < 0.8538681948424068:
                fte3.write(wData)
            else:
                fte4.write(wData)
            i += 1

        ftr1.close()
        ftr2.close() 
        ftr3.close() 
        ftr4.close()   
        fte1.close()
        fte2.close() 
        fte3.close() 
        fte4.close()            
            
            
    else:   # if number of points in subdomain is higher than threshold, keep decomposing.
        sdXYZ = ass.assign(trX, trY, trZ, trP, teX, teY, teZ, teP, xmaxd, xmind, ymaxd, ymind)        
        decompose(sdXYZ[0], sdXYZ[1], sdXYZ[2], sdXYZ[3], sdXYZ[16], sdXYZ[17], sdXYZ[18], sdXYZ[19], xmind, sdXYZ[-2], ymind, sdXYZ[-1])      # recursive function call 1
        decompose(sdXYZ[4], sdXYZ[5], sdXYZ[6], sdXYZ[7], sdXYZ[20], sdXYZ[21], sdXYZ[22], sdXYZ[23], sdXYZ[-2], xmaxd, ymind, sdXYZ[-1])      # recursive function call 2
        decompose(sdXYZ[8], sdXYZ[9], sdXYZ[10], sdXYZ[11], sdXYZ[24], sdXYZ[25], sdXYZ[26], sdXYZ[27], xmind, sdXYZ[-2], sdXYZ[-1], ymaxd)      # recursive function call 3
        decompose(sdXYZ[12], sdXYZ[13], sdXYZ[14], sdXYZ[15], sdXYZ[28], sdXYZ[29], sdXYZ[30], sdXYZ[31], sdXYZ[-2], xmaxd, sdXYZ[-1], ymaxd)    # recursive function call 4
            
#-----------------------------

#import modules
from datetime import datetime
from scipy import spatial
import glob, os, sys, math
import settings_CV as sett, numpy as np

#set recursion limit
sys.setrecursionlimit(3000)

#initialize global variables
sett.init()

#parameters

sett.p1 = sys.argv[1]			#fold
sett.p2 = 0.2959848493588502       	#bandwidth
sett.p3 = 0
sett.p4 = 0.01826823663906559       	#resolution
sett.p5 = 0
sett.p6 = 20       			#max points per sd
sett.p7 = 0.01				#bufRatio
sett.dir1 = 'CV_decomp/fold_' + sett.p1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#create directories
if not os.path.exists(sett.dir1):
    os.makedirs(sett.dir1)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#read input files
trFile = open('CV_folds/training_set_' + sett.p1 + ".txt", "r")
teFile = open('CV_folds/test_set_' + sett.p1 + ".txt", "r")
#point file
trX, trY, trZ, trP, teX, teY, teZ, teP = [], [], [], [], [], [], [], []
xmin, xmax, ymin, ymax, zmin, zmax, pmin, pmax = 0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0
for record in trFile:   
    trX.append(float(record.split(",")[0]))
    trY.append(float(record.split(",")[1]))
    trZ.append(float(record.split(",")[2]))
    trP.append(float(record.split(",")[3]))
trFile.close()
for record in teFile:   
    teX.append(float(record.split(",")[0]))
    teY.append(float(record.split(",")[1]))
    teZ.append(float(record.split(",")[2]))
    teP.append(float(record.split(",")[3]))
teFile.close()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#start decomposition
startTime = datetime.now()
decompose(trX, trY, trZ, trP, teX, teY, teZ, teP, xmin, xmax, ymin, ymax)
endTime = datetime.now()

#record decomposition time
runTime = endTime - startTime
tFile = sett.dir1 + os.sep + "decomp_time_" + sett.p1 + ".txt"
tFile_i=open(tFile, "w")
tFile_i.write(str(runTime))
tFile_i.close()


