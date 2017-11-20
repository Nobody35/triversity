# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:11:26 2017

@author: nbody
"""



#here an other main with different function of diversity
import time
import numpy as np
import math
import os
import sys
from triversity_lib import triversity

def create_folder(path):
    i = 0
    new_path = path
    while (os.path.exists(new_path)):
        i +=1        
        new_path = path+ "." + str(i)
    os.makedirs(new_path)
    return (new_path + "/")

def divs_init(n0,n1):
    return [np.zeros(n1),0,0,0,0,np.zeros((3,n0))]

def divs_v(v):
    d0 = 0
    d1 = 0
    d2 = 0 
    dinf = 0
    for x in v:
        d0 +=1
        d1 -=x * math.log(x,2)
        d2 += x * x
        dinf = max(x, dinf)
    return [d0,d1,d2,dinf]
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

def divs_add(v,d):
    for x in d.items():
        v[0][x[0]] += x[1]
    div = divs(d)
    d1 = div[1]
    v[2] += d1
    d2 = div[2]
    v[3] += d2
    d3 = div[3]
    v[4] += d3
    v[-1][0][v[1]] = 2**(d1)
    v[-1][1][v[1]] = 1/float(d2)
    v[-1][2][v[1]] = 1/float(d3)
    v[1] += 1

def normalise_nump(v,s):
    def f(a):
        a /= s
    f(v)
    
    
def divs_return(v):
    normalise_nump(v[0],v[1])
    v[2] = 2**(v[2] / float(v[1]))
    v[3] = v[1] / float(v[3])
    v[4] = v[1] / float(v[4])
    di = divs_v(v[0])    
    return (v[1],v[2],v[3],v[4],di[0],2**di[1],1/float(di[2]),1/float(di[3]),v[-1])
    

import matplotlib.pyplot as plt

def plotapath(t,p,outs,doSave = False):
    a = t.spread_and_divs(p,doSave)
    #a= t.spread_and_divs((3,2,1),doSave)
    print(a[:-1])
    out1 = open(outs[1],"w")
    out1.write("\nNumber of ind: " + str(a[0]))
    out1.write("\nGlobal div1: " + str(a[1]))
    out1.write("\nGlobal div2: " + str(a[2]))
    out1.write("\nGlobal div_inf: " + str(a[3]))
    out1.write("\nIndividual Mean div0: " + str(a[4]))
    out1.write("\nIndividual Mean div1: " + str(a[5]))
    out1.write("\nIndividual Mean div2: " + str(a[6]))
    out1.write("\nIndividual Mean div_inf: " + str(a[7]))
    out1.close()
    plt.title("Repartition des diversités individuelles sur " + str(p)+ ".")
    plt.xlabel("Valeur de diversité")
    plt.ylabel("Nombre d'individus")
    plt.hist(a[-1][0],bins = 30,label = "div1")
    plt.hist(a[-1][1],bins = 30, label = "div2")
    plt.hist(a[-1][2],bins = 30, label = "div_inf")
    plt.savefig(outs[0]+ str(p) + ".pdf")
    plt.legend()

def main(nbpart,nameout,filelist,doSave):
    folderout = create_folder(nameout)
    ti= time.time()
    t = triversity(nbpart)
    t.div_init = divs_init
    t.div_add = divs_add
    t.div_return = divs_return
    for file in filelist:
        t.import_file_2(file,100000,"Import "+ file)
        print("Time:", time.time()- ti)
    print("End import.")
    print(time.time() -ti)
    t.normalise_all()
    print(time.time() -ti)
    p = (1,2,3)
    out = [""] * 2
    out[0] = folderout+"plot"
    out[1] = folderout+"results.txt"
    plotapath(t,p,out)
    print(time.time() -ti)

    
    return t
    
    
#fortests
file = ["data/Automotive/tripartite_automotive_sample_20.csv"]
bigfile = ["data/Automotive/tripartite_automotive_sample_0.csv"]
#t = main(3,["data/Automotive/tripartite_automotive_sample_0.csv"],False)

files = ["../musi/usefull/triversity/Treatedwith5/tags_5b.txt","../musi/usefull/triversity/Treatedwith5/triplets_tags_5b.txt"
]

files2 = ["../musi/usefull/triversity/Treatedwith6/tags_6.txt","../musi/usefull/triversity/Treatedwith6/triplets_tags_6.txt"
]

#t = main(3,"test",file,False)
main(3,sys.argv[1],sys.argv[2:],False)
#main_2(3,sys.argv[1:],False)
