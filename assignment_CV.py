import settings_CV

def assign(trX, trY, trZ, trP, teX, teY, teZ, teP, xmaxf, xminf, ymaxf, yminf):
    
    p2 = settings_CV.p2

    xr2 = (xmaxf + xminf)/2     # Subdomain division x coordinates (middle of range)
    yr2 = (ymaxf + yminf)/2     # Subdomain division y coordinates (middle of range)
    

    strX1, strX2, strX3, strX4 = [],[],[],[]    #training set: list of data points for each subdomain (X-coordiantes)
    strY1, strY2, strY3, strY4 = [],[],[],[]    #training set: list of data points for each subdomain (Y-coordiantes)
    strZ1, strZ2, strZ3, strZ4 = [],[],[],[]    #training set: list of data points for each subdomain (Z-coordiantes)
    strP1, strP2, strP3, strP4 = [],[],[],[]    #training set: list of data points for each subdomain (pollen counts)

    steX1, steX2, steX3, steX4 = [],[],[],[]    #test set: list of data points for each subdomain (X-coordiantes)
    steY1, steY2, steY3, steY4 = [],[],[],[]    #test set: list of data points for each subdomain (Y-coordiantes)
    steZ1, steZ2, steZ3, steZ4 = [],[],[],[]    #test set: list of data points for each subdomain (Z-coordiantes)
    steP1, steP2, steP3, steP4 = [],[],[],[]    #test set: list of data points for each subdomain (pollen counts)

    for x, y, z, p in zip(trX, trY, trZ, trP):       # assign training points to subdomains
        if x < xr2 - p2:
            if y < yr2 - p2:
                strX1.append(x), strY1.append(y), strZ1.append(z), strP1.append(p)
            elif y < yr2 + p2:
                strX1.append(x), strY1.append(y), strZ1.append(z), strP1.append(p)
                strX3.append(x), strY3.append(y), strZ3.append(z), strP3.append(p)
            else:
                strX3.append(x), strY3.append(y), strZ3.append(z), strP3.append(p)

        elif x < xr2 + p2:                
            if y < yr2 - p2:
                strX1.append(x), strY1.append(y), strZ1.append(z), strP1.append(p)
                strX2.append(x), strY2.append(y), strZ2.append(z), strP2.append(p)
            elif y < yr2 + p2:
                strX1.append(x), strY1.append(y), strZ1.append(z), strP1.append(p)
                strX2.append(x), strY2.append(y), strZ2.append(z), strP2.append(p)
                strX3.append(x), strY3.append(y), strZ3.append(z), strP3.append(p)
                strX4.append(x), strY4.append(y), strZ4.append(z), strP4.append(p)
            else:
                strX3.append(x), strY3.append(y), strZ3.append(z), strP3.append(p)
                strX4.append(x), strY4.append(y), strZ4.append(z), strP4.append(p)
        else:
            if y < yr2 - p2:
                strX2.append(x), strY2.append(y), strZ2.append(z), strP2.append(p)
            elif y < yr2 + p2:
                strX2.append(x), strY2.append(y), strZ2.append(z), strP2.append(p)
                strX4.append(x), strY4.append(y), strZ4.append(z), strP4.append(p)
            else:
                strX4.append(x), strY4.append(y), strZ4.append(z), strP4.append(p)

    for x, y, z, p in zip(teX, teY, teZ, teP):       # assign test points to subdomains
        if x < xr2:
            if y < yr2:
                steX1.append(x), steY1.append(y), steZ1.append(z), steP1.append(p)
            else:
                steX3.append(x), steY3.append(y), steZ3.append(z), steP3.append(p)
        else:
            if y < yr2:
                steX2.append(x), steY2.append(y), steZ2.append(z), steP2.append(p)
            else:
                steX4.append(x), steY4.append(y), steZ4.append(z), steP4.append(p)

    sdXYZd = [strX1, strY1, strZ1, strP1, strX2, strY2, strZ2, strP2, strX3, strY3, strZ3, strP3, strX4, strY4, strZ4, strP4, steX1, steY1, steZ1, steP1, steX2, steY2, steZ2, steP2, steX3, steY3, steZ3, steP3, steX4, steY4, steZ4, steP4, xr2, yr2]

    return sdXYZd 
