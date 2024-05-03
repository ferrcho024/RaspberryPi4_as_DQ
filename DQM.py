import pandas as pd
import numpy as np


def completeness(data):
    '''Calculates the completeness of a list of values. Sensor acconditioned'''
    
    values = np.array(data)
    
    return np.count_nonzero(~np.isnan(values))/len(data)



def precision(data):
    '''Calculates the precision of a list of values. Sensor acconditioned'''
    
    data = np.nan_to_num(data)
    avg = np.mean(data)

    acum = 0
    for i in data:
        acum += (i - avg)**2

    acum /= (len(data)-1)
    v = np.sqrt(acum)/avg

    return 1 - v

def accuracy(data, ref):
    '''Calculates the accuracy of a list of values according to another reference value'''

    data = np.nan_to_num(data)
    avg = np.mean(data)

    v = np.abs(avg - ref)/ref

    return max(0, 1 - v)


def uncertainty(data1, data2):
    '''Calculates the uncertainty between two lists of values'''

    data1 = pd.Series(data1)
    data2 = pd.Series(data2)

    try:
        if len(data1) == len(data2):
            uncer = np.sqrt(((data1 - data2).pow(2).sum())/(2*(data1 + data2).count()*((data1 + data2).mean())**2))
            uncer = round(1-uncer,2)
            uncer = max(0,uncer)

            rmse = np.sqrt(((data1 - data2).pow(2).sum())/len(data1-data2))
            rmse = round(rmse,2)

            return uncer
        
        else:
            print('UNCERT Something has gone wrong with the data. Check if the dimensions are the same and both are dataset or data series')
            return

    except:
        print('UNCERT Something has gone wrong with the data. Check if the dimensions are the same and both are dataset or data series')
        return

def concordance(data1, data2):
    '''Calculates the concordance between 2 lists of values. Sensor acconditioned'''
 
    data1 = np.nan_to_num(data1)
    data2 = np.nan_to_num(data2)

    try:
        corr = np.corrcoef(data1, data2)
        
        return max(0, corr[0][1])

    except:
        print('CONCORD Something has gone wrong with the data. Check if the dimensions are the same and both are dataset or data series')
        return

def plausability(data1, data2, ref):
    ''''''

    comp_d1 = completeness(data1)
    comp_d2 = completeness(data2)

    prec_d1 = precision(data1)
    prec_d2 = precision(data2)

    acc_d1 = accuracy(data1, ref)
    acc_d2 = accuracy(data2, ref)

    sum_d1 = 0
    sum_d2 = 0

    for dim, val in zip([comp_d1, prec_d1, acc_d1], [0.75, 0.9, 0.9]):
        if dim > val:
            sum_d1 += (dim - val)/(1 - val)
    
    for dim, val in zip([comp_d2, prec_d2, acc_d2], [0.75, 0.9, 0.9]):
        if dim > val:
            sum_d2 += (dim - val)/(1 - val)
    
    a = sum_d1/(sum_d1 + sum_d2)

    return a


def fusion(data1, data2, ref):
    ''''''
    
    coef = plausability(data1, data2, ref)

    fusioned = []
    for x, y in zip(data1, data2):
        fusioned.append((x * coef) + (y * (1 - coef)))
    
    return fusioned


def DQ_Index(dataF, ref, uncer, concor):
    ''''''

    comp = completeness(dataF)
    prec = precision(dataF)
    acc = accuracy(dataF, ref)

    DQ = (0.4*acc) + (0.08*prec) + (0.18*uncer) + (0.16*comp) + (0.18*concor)

    return DQ





    
