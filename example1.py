# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 16:06:37 2017

@author: nbody
"""

import math 
from triversity_lib import triversity
import sys


#here an exemple of main to compute other kinds of diversity
#you have to change 3 functions:
    # divs_int (initialise the memory v)
    # divs_add (add the computed diversity)
    # div_return (return what you want to)
#you can use what you want of memory. Here it's name v cause it's a vector (list in python) 


 #auxiliaries functions 
def normalise_by(d,s):
    for x in d.items():
        d[x[0]] = x[1]/ float(s)

def add_default(d,k,n):
    if k in d:
        d[k] += n
    else:
        d[k] = n
def divs(d):
    d0 = 0
    d1 = 0
    d2 = 0 
    dinf = 0
    for x in d.values():
        d0 +=1
        d1 -=x * math.log(x,2)
        d2 += x * x
        dinf = max(x, dinf)
    return [d0,d1,d2,dinf]

#the tree functions to define 

def divs_init(n0,n1):
    #n0 = number of nodes in the first part of the path
    #n1 = number of nodes in the last part of the path
    return [dict(),0,0]


def divs_add(v,d,node):
    #v is the memory 
    # d is the repartition of the node "node" to add
        #it's a dictionnary of all nodes (n2) reachable from the node "node"
        #key : int the node id
        #value: is probability to be reached
    for x in d.items():
        add_default(v[0],x[0],x[1])
    v[1] += 1
    v[2] += divs(d)[1]


def divs_return(v):
    #v is the memory
    normalise_by(v[0],v[1])
    v[2] = 2**(v[2] / float(v[1]))
    di = divs(v[0])
    return (v[1],v[2],di[0],2**di[1],1/float(di[2]),1/(float(di[3])))
    

def main(nbpart,filelist,doSave):
    t = triversity(nbpart)
    t.div_init = divs_init
    t.div_add = divs_add
    t.div_return = divs_return
    for file in filelist:
        t.import_file(file,doRename=True)
        #t.import_file_2(file,100000,"Import "+ file)
    t.normalise_all()
    print("Result for the path(1,2,3)",t.spread_and_divs((1,2,3),doSave)) #spread and compute the div
    print("Result for the path(3,2,1)",t.spread_and_divs((3,2,1),doSave)) #spread and compute the div
    print("Result for the path(1,2)",t.spread_and_divs((1,2),doSave)) #spread and compute the div
    return t


#file = ["data/Automotive/tripartite_automotive_sample_20.csv"]
file = sys.argv[1:]
t = main(3,file,False)

