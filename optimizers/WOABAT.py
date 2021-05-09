# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:19:49 2016
@author: hossam
"""
'''
import random
import numpy
import math
from solution import solution
import time




def WOABAT(objf,lb,ub,dim,SearchAgents_no,Max_iter,k,points, metric):


    #dim=30
    #SearchAgents_no=50
    #lb=-100
    #ub=100
    #Max_iter=500
      
    # initialize position vector and score for the leader
    Leader_pos=numpy.zeros(dim)
    Leader_score=float("inf")  #change this to -inf for maximization problems
    
    
    #Initialize the positions of search agents
    Positions = numpy.zeros((SearchAgents_no, dim))
    
    Positions=numpy.random.uniform(0,1,(SearchAgents_no,dim)) *(ub-lb)+lb
    labelsPred=numpy.zeros((SearchAgents_no,len(points)))
    
    #Initialize convergence
    convergence_curve=numpy.zeros(Max_iter)
    
    #bat algorithm addition
    Qmin=0         # Frequency minimum
    Qmax=2         # Frequency maximum
    
    # Initializing arrays
    Q=numpy.zeros(SearchAgents_no)  # Frequency
    v=numpy.zeros((SearchAgents_no,dim))  # Velocities
    Convergence_curve=[];
    
    A1=0.5;      # Loudness  (constant or decreasing)
    r=0.5;      # Pulse rate (constant or decreasing)
    
    # Initialize the population/solutions
    Positions=numpy.random.rand(SearchAgents_no,dim)*(ub-lb)+lb
    labelsPred=numpy.zeros((SearchAgents_no,len(points)))
    fitness=numpy.zeros(SearchAgents_no)

    z=numpy.zeros((SearchAgents_no,dim))
    z=numpy.copy(Positions)

       
    
    
    ############################
    s=solution()

    print("WOABAT is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################
    
    t=0  # Loop counter
    
    # Main loop
    while t<Max_iter:
        for i in range(0,SearchAgents_no):
            
            # Return back the search agents that go beyond the boundaries of the search space
            
            #Positions[i,:]=checkBounds(Positions[i,:],lb,ub)            
            Positions[i,:]=numpy.clip(Positions[i,:], lb, ub)

            
            # Calculate objective function for each search agent
            startpts = numpy.reshape(Positions[i,:], (k,(int)(dim/k)))

            if objf.__name__ == 'SSE' or objf.__name__ == 'SC' or objf.__name__ == 'DI':
                fitnessValue, labelsPredValues=objf(startpts, points, k, metric) 
            else:
                fitnessValue, labelsPredValues=objf(startpts, points, k) 
                
            fitness = fitnessValue
            labelsPred[i,:] = labelsPredValues
            
            # Find the initial best solution
            f = min(fitness)
            fmin = int(f)
            I=numpy.argmin(int(fitness))
            Leader_pos=Positions[I,:]
            bestLabelsPred=labelsPred[I,:]
            
            # Update the leader
            if fitness<Leader_score: # Change this to > for maximization problem
                Leader_score=fitness; # Update alpha
                Leader_pos=Positions[i,:].copy() # copy current whale position into the leader position
                Leader_labels=labelsPred[i,:].copy() # copy current whale position into the leader position
            
            
        
        
        a=2-t*((2)/Max_iter); # a decreases linearly fron 2 to 0 in Eq. (2.3)
        
        # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
        a2=-1+t*((-1)/Max_iter);
        
        # Update the Position of search agents 
        for i in range(0,SearchAgents_no):
            r1=random.random() # r1 is a random number in [0,1]
            r2=random.random() # r2 is a random number in [0,1]
            
            A=2*a*r1-a  # Eq. (2.3) in the paper
            C=2*r2      # Eq. (2.4) in the paper
            
            
            b=1;               #  parameters in Eq. (2.5)
            l=(a2-1)*random.random()+1   #  parameters in Eq. (2.5)
            
            p = random.random()        # p in Eq. (2.6)
            
            for j in range(0,dim):
                
                if p<0.5:
                    if abs(A)>=1 or abs(A)<1:
                        rand_leader_index = math.floor(SearchAgents_no*random.random());
                        X_rand = Positions[rand_leader_index, :]
                        Q[i]=Qmin+(Qmin-Qmax)*random.random()
                        v[i,:]=v[i,:]+(X_rand[j]-Leader_pos[j])*Q[i]
                        z[i,:]=Positions[i,:]+v[i,:]
                        
                        # Check boundaries
                        Positions=numpy.clip(Positions,lb,ub)
                        
                        # Pulse rate
                        if random.random()>r:
                            z[i,:]=Leader_pos[j]+0.001*numpy.random.randn(dim)
                        
                        #Evaluate new solutions
                        Fnew = objf(z[i,:],startpts, points, k)
                        LabelsPrednew = labelsPredValues
          
                        
                        if ((Fnew != numpy.inf) and (Fnew<=Fitness[i]) and (random.random()<A) ):
                           Sol[i,:]=numpy.copy(S[i,:])
                             Fitness[i]=Fnew
                            labelsPred[i,:]=LabelsPrednew
           
                        '''
                        # Update the current best solution
                        '''if Fnew != numpy.inf and Fnew<=fmin:
                best=numpy.copy(S[i,:])
                fmin=Fnew
                bestLabelsPred=LabelsPrednew'''
                        
          
                        #D_X_rand=abs(C*X_rand[j]-Positions[i,j]) 
                        #Positions[i,j]=X_rand[j]-A*D_X_rand 
                
                
                    '''  
                    elif abs(A)<1:
                        Q[i]=Qmin+(Qmin-Qmax)*random.random()
                        v[i,:]=v[i,:]+(Positions[i,:]-Leader_pos[j])*Q[i]
                        z[i,:]=Positions[i,:]+v[i,:]
                        
                        # Pulse rate
                        if random.random()>r:
                            z[i,:]=Leader_pos[j]+0.001*numpy.random.randn(dim)
                        
                        #Evaluate new solutions
                        Fnew = objf(z[i,:])'''
                        
                        #D_Leader=abs(C*Leader_pos[j]-Positions[i,j]) 
                        #Positions[i,j]=Leader_pos[j]-A*D_Leader     
                    
                    
'''                elif p>=0.5:
                  
                    distance2Leader=abs(Leader_pos[j]-Positions[i,j])
                    # Eq. (2.5)
                    Positions[i,j]=distance2Leader*math.exp(b*l)*math.cos(l*2*math.pi)+Leader_pos[j]
                    
      
        
        convergence_curve[t]=Leader_score
        if (t%1==0):
               print(['At iteration '+ str(t)+ ' the best fitness is '+ str(Leader_score)]);
        t=t+1
    
    timerEnd=time.time()  
    s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime=timerEnd-timerStart
    s.convergence=convergence_curve
    s.optimizer="WOABAT"   
    s.objfname=objf.__name__
    s.best = Leader_score
    s.bestIndividual = Leader_pos
    s.labelsPred = numpy.array(Leader_labels, dtype=numpy.int64)
    
    
    
    return s
'''

# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:19:49 2016
@author: hossam
"""
import random
import numpy
import math
from solution import solution
import time




def WOA(objf,lb,ub,dim,SearchAgents_no,Max_iter,k,points, metric):


    #dim=30
    #SearchAgents_no=50
    #lb=-100
    #ub=100
    #Max_iter=500
      
    # initialize position vector and score for the leader
    Leader_pos=numpy.zeros(dim)
    Leader_score=float("inf")  #change this to -inf for maximization problems
    
    
    #Initialize the positions of search agents
    Positions = numpy.zeros((SearchAgents_no, dim))
    
    Positions=numpy.random.uniform(0,1,(SearchAgents_no,dim)) *(ub-lb)+lb
    labelsPred=numpy.zeros((SearchAgents_no,len(points)))
    
    #Initialize convergence
    convergence_curve=numpy.zeros(Max_iter)
    
    
    ############################
    s=solution()

    print("WOA is optimizing  \""+objf.__name__+"\"")    

    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    ############################
    
    t=0  # Loop counter
    
    # Main loop
    while t<Max_iter:
        for i in range(0,SearchAgents_no):
            
            # Return back the search agents that go beyond the boundaries of the search space
            
            #Positions[i,:]=checkBounds(Positions[i,:],lb,ub)            
            Positions[i,:]=numpy.clip(Positions[i,:], lb, ub)

            
            # Calculate objective function for each search agent
            startpts = numpy.reshape(Positions[i,:], (k,(int)(dim/k)))

            if objf.__name__ == 'SSE' or objf.__name__ == 'SC' or objf.__name__ == 'DI':
                fitnessValue, labelsPredValues=objf(startpts, points, k, metric) 
            else:
                fitnessValue, labelsPredValues=objf(startpts, points, k) 
                
            fitness = fitnessValue
            labelsPred[i,:] = labelsPredValues
            
            # Update the leader
            if fitness<Leader_score: # Change this to > for maximization problem
                Leader_score=fitness; # Update alpha
                Leader_pos=Positions[i,:].copy() # copy current whale position into the leader position
                Leader_labels=labelsPred[i,:].copy() # copy current whale position into the leader position
            
            
        
        
        a=2-t*((2)/Max_iter); # a decreases linearly fron 2 to 0 in Eq. (2.3)
        
        # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
        a2=-1+t*((-1)/Max_iter);
        
        # Update the Position of search agents 
        for i in range(0,SearchAgents_no):
            r1=random.random() # r1 is a random number in [0,1]
            r2=random.random() # r2 is a random number in [0,1]
            
            A=2*a*r1-a  # Eq. (2.3) in the paper
            C=2*r2      # Eq. (2.4) in the paper
            
            
            b=1;               #  parameters in Eq. (2.5)
            l=(a2-1)*random.random()+1   #  parameters in Eq. (2.5)
            
            p = random.random()        # p in Eq. (2.6)
            
            for j in range(0,dim):
                
                if p<0.5:
                    if abs(A)>=1:
                        rand_leader_index = math.floor(SearchAgents_no*random.random());
                        X_rand = Positions[rand_leader_index, :]
                        D_X_rand=abs(C*X_rand[j]-Positions[i,j]) 
                        Positions[i,j]=X_rand[j]-A*D_X_rand      
                        
                    elif abs(A)<1:
                        D_Leader=abs(C*Leader_pos[j]-Positions[i,j]) 
                        Positions[i,j]=Leader_pos[j]-A*D_Leader      
                    
                    
                elif p>=0.5:
                  
                    distance2Leader=abs(Leader_pos[j]-Positions[i,j])
                    # Eq. (2.5)
                    Positions[i,j]=distance2Leader*math.exp(b*l)*math.cos(l*2*math.pi)+Leader_pos[j]
                    
      
        
        convergence_curve[t]=Leader_score
        if (t%1==0):
               print(['At iteration '+ str(t)+ ' the best fitness is '+ str(Leader_score)]);
        t=t+1
    
    timerEnd=time.time()  
    s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime=timerEnd-timerStart
    s.convergence=convergence_curve
    s.optimizer="WOA"   
    s.objfname=objf.__name__
    s.best = Leader_score
    s.bestIndividual = Leader_pos
    s.labelsPred = numpy.array(Leader_labels, dtype=numpy.int64)
    
    
    
    return s
