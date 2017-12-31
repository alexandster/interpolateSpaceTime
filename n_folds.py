#import modules
import random, os

#read data file into 2D array
inFile = open('files/data.txt', 'r')

xyzrList = []

#attach column of random numbers
for i in inFile:

    iStr = i.split(',')

    xyzrList.append([float(iStr[0]),float(iStr[1]),float(iStr[2]),float(iStr[3]),random.random()])

inFile.close()

#sort array according to random number column
k = sorted(xyzrList, key=lambda tup: tup[4])	

#some definitions
numPts = len(xyzrList)		#number of points in dataset
n = 10 						#number of folds
numPts_fold = numPts / n	#number of test points per fold, e.g. 5000

#create folds
j = 0 	#fold number

#create output directory
outDir = 'CV_folds/'
if not os.path.exists(outDir):
    os.makedirs(outDir)


#for each fold
while j < n:
    
    #open output files
    trFile = open(outDir + os.sep + 'training_set_' + str(j) + '.txt', 'w')	#training set
    teFile = open(outDir + os.sep + 'test_set_' + str(j) + '.txt', 'w')		#test set

    tr1_fr = 0
    tr1_to = j * numPts_fold
    te_fr = tr1_to 
    te_to = tr1_to + numPts_fold  
    tr2_fr = te_to
    tr2_to = numPts 
    
    i1 = tr1_fr
    i2 = int(te_fr)
    i3 = int(tr2_fr)

    while i1 < tr1_to:
        trFile.write(str(k[i1][0]) + "," + str(k[i1][1]) + "," + str(k[i1][2]) + "," + str(k[i1][3]) + "\n")
        i1 += 1

    while i2 < te_to:
        teFile.write(str(k[i2][0]) + "," + str(k[i2][1]) + "," + str(k[i2][2]) + "," + str(k[i2][3]) + "\n")
        i2 += 1

    while i3 < tr2_to:
        trFile.write(str(k[i3][0]) + "," + str(k[i3][1]) + "," + str(k[i3][2]) + "," + str(k[i3][3]) + "\n")
        i3 += 1    

    j += 1

trFile.close()
teFile.close()



