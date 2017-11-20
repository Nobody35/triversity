# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 20:31:43 2017

@author: nbody
"""



#auxilaries functions 
import math

def read_file_p (file,separator, fu, step_printer, toprint):
    i = 0 #just to print the progress
    f = open(file,"r")
    for l in f:
        i +=1 
        if (i % step_printer == 0):
            print("\n" + toprint +":" ,i )
        if (not l[0] == "#"):
            v = l.strip().split(separator); #strip is used to remove the "\n"
            fu (v)
    f.close()
    return i
    
def read_file_f (file,separator, fu, step_printer, toprint):
    i = 0 #just to print the progress
    f = open(file,"r")
    for l in f:
        i +=1 
        if (i % step_printer == 0):
            toprint(i)
        if (not l[0] == "#"):
            v = l.strip().split(separator); #strip is used to remove the "\n"
            fu (v)
    f.close()
    return i
    

def read_file (file,separator, fu):
    f = open(file,"r")
    coms = []
    for l in f:
        if (not l[0] == "#"):
            v = l.strip().split(separator);
            #v[-1] = v[-1][:-1]; #remove "/n"
            fu (v)
        else: 
            coms.append(l[1:])
    f.close()
    return coms
    
    
#care if python2 add a "float"
def normalise(d): 
    s = sum(d.values())
    for x in d.items():
        d[x[0]] = x[1]/ float(s)

def normalise_by(d,s):
    for x in d.items():
        d[x[0]] = x[1]/ float(s)

def add_default(d,k,n):
    if k in d:
        d[k] += n
    else:
        d[k] = n



class triversity:
    def __init__(self,nbpart):
        self.nbpart = nbpart +1 
        self.graphs= [[{} for i in range(0,self.nbpart)] for j in range(0,self.nbpart)]
        self.linkedTrees= [dict() for i in range(0,self.nbpart)]
    
    #care it need 2 s its a list of dictionnary (node,linked tree)
    #a linked tree is a dictionnary path -> distribution
    #the path is a tuple
    #a distribution is a dictionnary node -> weight (probability)
        self.res = dict()
        self.saved = set()
        #will save if a result have been spread 
        #it will be in res if the result have been computed (all means etc)
        #the save is just for global, not individual
        
        #for renaming       
        self.ids =  [dict() for i in range(0,self.nbpart)]
        self.revids = [dict() for i in range(0,self.nbpart)]
        self.last_id = [0 for i in range(0,self.nbpart)]
        
        
    #rename node
    def get_default_node(self,pid,n):
        if n in self.ids[pid]:
            return self.ids[pid][n]
        else:
            x= self.last_id[pid]
            self.ids[pid][n] = x
            self.revids[pid][x] = n
            self.last_id[pid] +=1
            return x

        
    #add a link in our graph
    def add_link_d(self,pid1,n1, pid2,n2,w):
        d = self.graphs[pid1][pid2].setdefault(n1,dict())
        add_default(d,n2,w)  

    def add_link(self,pid1,n1, pid2,n2,w,doRename=True):
        if (doRename):
            n1id = self.get_default_node(pid1,n1)
            n2id = self.get_default_node(pid2,n2)
        else:
            n1id = n1
            n2id = n2
        self.add_link_d(pid1,n1id,pid2,n2id,w)
        self.add_link_d(pid2,n2id,pid1,n1id,w)
    
    #get the distribution if the path is of len 2
    def get_distrib_2(self,pid1,pid2,n1):
        return self.graphs[pid1][pid2][n1]
    
    #get the distribution
    #this method is for the user
    def get_distrib(self,path,node):
        try:
            if (len(path) == 2):
                return self.get_distrib_2(path[0],path[1],node)
            else:
                return self.linkedTrees[path[0]][node][path]
        except KeyError as e:
            print("Not computed yet (Keyerror: ", str(e), ")")
        except:
            raise
    
    
    #create a new tree
    def new_tree(self,node,pid):
        d= self.linkedTrees[pid][node] = dict()
        return d
        

   
   #import file
    def import_file(self,file,doRename=True):
        def fread(v):
            try :
                pid1 = int(v[0])
                n1 = v[1]
                pid2 = int(v[2])
                n2 = v[3]
                w = 1 #if there are ponderation add it here
                self.add_link(pid1,n1,pid2,n2,w,doRename)
            except:
                    print("error importing that:",v)
        read_file(file,  " ", fread)
        
    #same thing but print the evolution
    def import_file_2(self,file,stepprinter, toprint,doRename=True):
        def fread(v):
            try :
                pid1 = int(v[0])
                n1 = v[1]
                pid2 = int(v[2])
                n2 = v[3]
                w = 1 #if there are ponderation add it here
                self.add_link(pid1,n1,pid2,n2,w,doRename)
            except:
                    print("error importing that:",v)
        read_file_p(file,  " ", fread, stepprinter, toprint)
   
    #normalise alle distributions
    def normalise_all(self):    
        for gs in self.graphs:
            for g in gs:
                for d in g.values():
                    normalise(d)
    
    
    
    #this compute the last step of a path (pid1,pid2)
    #for an individual begining
    #distribin is the distrib at the previous step
    def compute_spread_one(self,distribin,pid1,pid2): 
        d = {}        
        for x in distribin.items():
            node = x[0]         
            value = x[1]
            for y in self.get_distrib_2(pid1,pid2,node).items():
                add_default(d,y[0],value*y[1])
        return d
        
    
    #this find the last step already computed
    #this is global (all individual have been computed)
    def find_last_saved(self,path):
        i = 3
        n = len(path)
        while ((i <= n) and (path[:i] in self.saved)):
            i += 1 
        i = i-1
        return i

        
    
    #compute what need to be computed
    #for an individual begining
    def compute_spread_one_path(self,d, path1, new_path,doSave,tree,path,i_split):
        #after dosave arguments could be optional cause used just for save
        i0 = path1
        j = i_split #just for save
        for i in new_path:
            j +=1            
            d = self.compute_spread_one(d,i0,i)
            if(doSave):
                tree[path[:j]] = d
            i0 = i
        return d
        
    #here on example of diversity
    def div1(self,d):
        s = 0
        for x in d.values():
            s+= x * math.log(x,2)
        return -s
        
    #the following 3 methods can be changed 
    def div_init(self,n0,n1):
        #n0 = number of nodes in the first part of the path
        #n1 = number of nodes in the last part of the path
        return [0,0,dict()]
    def div_add(self,v,dres,node):
        #this step is the hard to parallelise
        v[0] += 1
        v[1] += self.div1(dres)
        dcol = v[2]
        for x in dres.items():
            add_default(dcol,x[0],x[1])
    def div_return(self,v):
        i = v[0]            
        mi1 = v[1]            
        dcol = v[2]
        normalise_by(dcol,i)
        return  2**(self.div1(dcol)), 2**(mi1/float(i))
            
    #the main function 
    #spread and compute the div on the fly
    #if already spread just compute the div
    #we use find_last_step just one time and not for every nodes.
    def spread_and_divs(self,path,doSave=True):
        if path in self.res:
            print("Already computed")
            return self.res[path]
        v  = self.div_init(self.last_id[path[0]],self.last_id[path[-1]])
        i_split= self.find_last_saved(path)
        if(i_split == 2): #there is no trees
            path0 = path[0]            
            path1 = path[1]
            new_path = path[2:]
            for c in self.graphs[path0][path1].items():
                d = c[1]
                tree = None
                if (doSave and (len(path) > 2) ):
                    tree = self.new_tree(c[0],path0)
                dres = self.compute_spread_one_path(d, path1,new_path,doSave,tree,path,i_split)
                self.div_add(v,dres,c[0])
        else:
            last_path = path[:i_split]
            path1 = last_path[-1]
            new_path = path[i_split:]
            print("Already spread until:" + str(last_path))
            for node,tree in self.linkedTrees[path[0]].items():
                d = tree[last_path]
                dres = self.compute_spread_one_path(d,path1,new_path,doSave,tree,path,i_split)
                self.div_add(v,dres,node)
        res = self.div_return(v)
        self.res[path] = res
        if(doSave):
            for j in range(2,len(path)+1):
                self.saved.add(path[:j])       
        return res
    
    #here a div for the individual spread
    def div_ind(self,d):
        return self.div1(d)
        
    
    def find_last_saved_by_tree(self,path,node,tree):
        i = 3
        n = len(path)
        while ((i <= n) and (path[:i] in tree)):
            i += 1 
        i = i-1
        return i
    
    def build_tree_for_one(self,path,node,doSave):
        lts = self.linkedTrees[path[0]]
        if node in lts:
            return lts[node]
        elif (len(path)>2 and doSave):
            d = lts[node] = dict()
            return d
        else:
            return None
            
        
    

    #main function for individual
    def spread_and_divs_one(self,path,node,doSave=True):
        p0 = path[0]
        p1 = path[1]
        tree = self.build_tree_for_one(path,node,doSave)
        i_split = 2        
        if( not tree == None):
            i_split = self.find_last_saved_by_tree(path,node,tree)
        if (i_split == 2):
            d = self.graphs[p0][p1][node]
        else:
            d = tree[path[:i_split]]
        i0 = path[i_split -1]
        for i in range(i_split,len(path)):
            d = self.compute_spread_one(d,i0,path[i])
            if(doSave):
                tree[path[:(i+2)]] = d
            i0 = path[i]
        return self.div_ind(d)
             

        


