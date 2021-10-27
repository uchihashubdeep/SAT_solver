from CNF_Creator import *
import numpy as np
import random
import time

def random_assignment(n):
    assignment=np.empty(n)
    for i in range(n):
        assignment[i]=random.randint(0,1)
    return assignment

def fitness(assignment,sent):
    size=len(sent)
    count=0
    for i in range(size):
        clause=len(sent[i])
        sat=False
        for j in range(clause):
            if(sent[i][j]<0):
                n=sent[i][j]*(-1)
                n=n-1
                val=not bool(assignment[n])
            else:
                n=sent[i][j]-1
                val=bool(assignment[n])
            sat=sat or val
        if(sat):
            count=count+1
    value=(count/size)*100
    
            
    return value;

def convert(best_child):
    final=[]
    for i in range(50):
        if(best_child[i]==1):
            x=i+1
        else:
            x=-(i+1)
        final.append(x)
    return final

def assign_weight(population,sen):
    weight=[]
    for i in range(len(population)):
        weight.append(fitness(population[i],sen)**10)
    return weight

def ga(population,gen,mutation,sen,size):
    start_time = time.monotonic()
    final_ans=[]
    max_fit=0
    max_child=[]
    weight=[]
    new_weight=[]
    count=0
    for i in range(gen):
        weight=assign_weight(population,sen)
        new_pop=[]
        for p in population:
            x=tournament_selection(population,size,sen,weight)
            y=tournament_selection(population,size,sen,weight)
            child=reproduce(x,y)
            num=random.randint(1,10)
            prob=num/10
            if(prob<=mutation):
                child=mutate(child)
            new_pop.append(child)
        population=new_pop
        new_weight=assign_weight(population,sen)
        best,best_child=fitness_freak(population,sen)
        if(best>max_fit):
            max_fit=best
            max_child=best_child
            count=0
        elif(best<max_fit):
            population=new_child(population,max_child,new_weight)
            count=0
        else:
            count=count+1
            if(count>gen/2):
                final_ans=convert(best_child)
                timeval=time.monotonic()-start_time
                return max_fit,final_ans,timeval
        end_time = time.monotonic()
        timeval=end_time-start_time
        if(timeval>42):
            final_ans=convert(best_child)
            timeval=time.monotonic()-start_time
            return max_fit,final_ans,timeval
        if(max_fit==100):
            break
    final_ans=convert(best_child)
       
    timeval=time.monotonic()-start_time
    return max_fit,final_ans,timeval

def new_child(population,max_child,weight):
    weight=np.reciprocal(weight)
    length=len(population)
    c=np.arange(0,length)
    new_in=random.choices(c,weights=weight,k=1)
    population[new_in[0]]=max_child
    return population

def tournament_selection(population,size,sen,weight):
    cap=len(population)
    randomlist = random.choices(population,weights=weight, k=size)
    participants=[[0]*len(population[0])]*size
    for i in range(size):
        index=randomlist[i]
        participants[i]=index
    winner=[]
    value=-1
    for i in range(size):
        temp=fitness(participants[i],sen)
        if(temp>value):
            value=temp
            winner=participants[i]
    return winner
    
def fitness_freak(population,sentence):
    pop=len(population)
    value=-1
    fav_child=[]
    for i in range(pop):
        temp=fitness(population[i],sentence)
        if(temp>value):
            value=temp
            fav_child=population[i]
    return value,fav_child

def reproduce(x,y):
    cap=len(x)
    cross=random.randint(0,cap-1)
    child=[]
    child[0:cross]=x[0:cross]
    child[cross:cap]=y[cross:cap]
    return child
    
def mutate(child):
    cap=len(child)
    mut_point=random.randint(0,cap-1)
    if(child[mut_point]==0):
        child[mut_point]=1
    else:
        child[mut_point]=0
    return child

    
def main():
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    sentence = cnfC.CreateRandomSentence(m=220) # m is number of clauses in the 3-CNF sentence
    sentence = cnfC.ReadCNFfromCSVfile()
    population=[]
    for i in range(50):
        population.append(random_assignment(50))
    
    best,best_child,ti=ga(population,100,0.4,sentence,5) #ga(populattion,generation,mutation_rate,sentence,tournament_size)
    

    print('\n\n')
    print('Number of clauses in CSV file : ',len(sentence))
    print('Best model : ',best_child)
    print('Fitness value of best model :'+ str(best)+'%')
    print('Time taken : '+str(ti)+' seconds')
    print('\n\n')
    
if __name__=='__main__':
    main()

