import os

#determine n - the number of training observations
nFile = open('CV_folds/training_set_0.txt','r')
n = 0.0
for i in nFile:
    n += 1

#determine the number of folds
#nFolds = sum(os.path.isdir(i) for i in os.listdir('CV_decomp'))
nFolds = len(os.listdir('CV_decomp'))
print nFolds

#determine values of p
inList = os.listdir('CV_result')
numList = []
for i in inList:
    numList.append(float(i.split("_")[2]))

print "p SSD MARE RMSPE"

#for each value of p
for j in set(numList):

    i = 0
    SSDsum = MAREsum = RMSPEsum = 0

    #for each fold
    while i < nFolds:
    
        #compute sum of errors
        inFile = open('CV_result/st_idw_' + str(j) + "_" + str(i) + ".txt", 'r')
        r = inFile.readline().split(",")
        
        SSD, MARE, RMSPE = float(r[0]),float(r[1]),float(r[2])         

        SSDsum += SSD
        MAREsum += MARE
        RMSPEsum += RMSPE


        i += 1

    print j, ((SSDsum/n) ** 0.5) / 10.0, (MAREsum/n)/10.0, (((RMSPEsum/n) ** 0.5) * 100.0) / 10.0
    

