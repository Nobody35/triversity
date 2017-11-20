# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:03:37 2017

@author: nbody
"""

from triversity_lib import triversity

#here an exemple of main to compute the diversity
#here it's the collective and the mean of individual of shannon
#but it can be changed (see the example 1)

def main(nbpart,filelist,doSave):
    #nb part : the number of part
    #file list is the list of file of input
    t = triversity(nbpart) #create the object     
    for file in filelist:
        t.import_file(file)

    t.normalise_all() #normalise every dictionnaries (don't forget to do it)
    
    #here is the main function 
    #it compute the new repartition and compute the diversity on fly
    #here it's the collective and the mean of individual of shannon
    #but it can be changed (see the example 1)
    #the first argument is the path (care it's a tuple not a list)
    #doSave if you want to save the already computed (can be Huge in memory but decrease time of execution)
        #if you don't put it it will be set to 

 
    print("Result for the path(1,2,3)",t.spread_and_divs((1,2,3),doSave)) #spread and compute the div
    print("Result for the path(3,2,1)",t.spread_and_divs((3,2,1),doSave)) #spread and compute the div
    print("Result for the path(1,2)",t.spread_and_divs((1,2),doSave)) #spread and compute the div
    
    #you can also just spread and compute the div of oneperson
    print("Result for the path(1,2,3) the node 2",t.spread_and_divs_one((1,2,3),2,doSave)) #spread and compute the div


    #if you want to name of an id use rev id:
    #you have to know the part where he is (here it's 1)
    #here i test the node 2
    x = t.revids[1][2]
    print("rev id of 2:", x)    
    
    #if you want to know the id of a node use id:
    #you have to know the part where he is (here it's 1)
    print("id of ", x, ":", t.ids[1][x])
    
    

    
    
    return t

#for example:
file = ["data/Automotive/tripartite_automotive_sample_20.csv"]
#file = sys.argv[1:]
t = main(3,file,False)
