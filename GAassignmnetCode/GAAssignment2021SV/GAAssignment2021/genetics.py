#
# GA Assignment 2021
#
import math
import time
import random
import pdb
from copy import copy
from Items import Item, ItemList
import g
from dataclasses import dataclass
import random
import sys
import time


def rnd (rng, lo, hi):  
    #if rng is a random the it returns a float between lo and hi , but never equalling Hi
    retv = (hi - lo) * rng.random() + lo;
    return retv

def rndInt (rng, lo, hi):
    # if rng is a random it returns a int between lo and hi, this is inclusive of lo and Hi val
    retv = (hi - lo+0.99) * rng.random() + lo;
    return int(retv)

@dataclass
class Gene(object):
    truck: int
    item: Item 


class Genome(object):
    # some genome data deletd here .. students to design
    
    def __init__(self,rng, genes=[]):
        #note it populates the new genome with random numbers
        self.score=0       # score of this genome 
        self.generation=0  # counter to know which generation this came from
        self.mutations=0   # counter to know how many mutations were in this genome
        self.genes = genes
    def __repr__(self):
        return(f"score:{self.score}, generation:{self.generation}, mutations:{self.mutations}")

    @classmethod                
    def random_genes(cls, rng):
        new_list = ItemList()
        new_list.setItems()
        new_list = copy(new_list.lst)
        new_genes = [Gene(random.randint(0, 3), i) for i in new_list] 
        print(new_genes[0])
        return(cls(rng, new_genes))



    def getTruck(self, truck):
        truck_genes = list(filter(lambda x: x.truck==truck, self.genes))
        return(truck_genes)


    def calcScore(self, itemList): #ItemList lst
        # student code here   
        importance_scores = {3:1, 2:2, 1:3} 
        importance = 0
        size = 0
        truck1 = self.getTruck(1)
        truck2 = self.getTruck(2)
        truck3 = self.getTruck(3)
        for gene in truck1:
            importance += importance_scores[gene.item.importance]
            size += gene.item.size

        for gene in truck2:
            importance += importance_scores[gene.item.importance]
            size += gene.item.size

        for gene in truck3:
            importance += importance_scores[gene.item.importance]
            size += gene.item.size

        
        diff_from_ideal = 19 - size
        if diff_from_ideal < 0:
            diff_from_ideal * 2
        size_score = 100 - abs(diff_from_ideal)
        score = size_score + importance
        self.score = score
        return(self.score)

            



       
class Population:
        
    # pop=[]    # the genomes of the population

    def __init__(self,rng, item_list):
        self.pop = [Genome(rng)]* g.POPULATION
        self.rng = rng
        self.item_list = item_list
        self.pop = list(map(lambda x:x.random_genes(item_list), self.pop))

        pdb.set_trace()

    def idOfBest(self): # highest score
        #global POPULATION
        #retv = 0;
        #best = pop[0].score;
        #for i in range(1, g.POPULATION):
        #    if (pop[i].score > best):
        #        retv = i;
        #        best = pop[i].score;
        #return retv;
        pass
        

    def calcScore(self, itemList):
        best_score = 0 
        best_id = 0
        for count, genome in enumerate(self.pop):
            score = genome.calcScore(itemList)
            if score > best_score:
                best_score = score
                best_id = count
        g.bestScore = best_score
        g.best = best_id



         # update score for the entire population
         # update        g.best
         # update        g.bestScore 
    def intercourse(self, genome1, genome2): 
        baby = Genome(self.rng)
        for i in range(30):
            coin = rndInt(self.rng, 0, 1)
            if coin == 0:
                inherited = genome1.genes[i]
            else:
                inherited = genome2.genes[i]
            does_mutation_happen = rndInt(self.rng, 1, 100) 
            if does_mutation_happen <= g.MUTATIONPERCENT:
                coin = rndInt(self.rng, 0, 1)
                if coin == 0:
                    inherited.truck = rndInt(self.rng, 0, 3)
                elif coin == 0:
                    inherited.item = self.item_list[rndInt(self.rng, 0, 29)]
            baby.genes.append(inherited)
        return(baby)


    
    def breed(self):
        # Kill some breed from the rest 
        score = sorted(self.pop, key=lambda genome: genome.score)
        best_50 = score[len(score)//2:]
        parents1 = best_50[:len(best_50)//2]
        parents2 = best_50[len(best_50)//2:]
        new_pop = []
        for i in range(4):
            random.shuffle(parents1)
            random.shuffle(parents2)
            new_pop += [self.intercourse(parents1[i], parents2[i]) for i in range(25)] 
        self.pop = new_pop 


if __name__ == "__main__":
    rng = random.Random()
    item_list = ItemList()
    item_list.setItems()
    test  = Population(rng, item_list)
    test.calcScore(rng)
    pdb.set_trace()
    # x.breed()
    for i in test.pop:
        print(i.genes[0])