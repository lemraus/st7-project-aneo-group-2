from random import random, randint

MACHINES_MUTATION_PROBABILITY = 0.2
MUTATION_PROBABILITY = 0.1

def mutate(chromosome):

    machines_number = max(map(lambda x: x[1], chromosome))
    mutated_chromosome = []

    if random() < MACHINES_MUTATION_PROBABILITY:
        if random() < 0.5:
            machines_number += 1
        else : machines_number -= 1
    
    print(machines_number)
    
    for gene in chromosome:
        if gene[1] > machines_number or random() < MUTATION_PROBABILITY:
            mutated_chromosome.append((gene[0], randint(0, machines_number)))
        else:
            mutated_chromosome.append(gene)
    
    return mutated_chromosome
