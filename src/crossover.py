from random import randint


def crossover(chromosome1, chromosome2):

    n = len(chromosome1)
    crossover_point = randint(0, n)
    new_chromosome = chromosome1[:crossover_point]

    for i in range(n):
        gene = chromosome2[i]
        if not contains_task(new_chromosome, gene[0]):
            new_chromosome.append(gene)
    
    return new_chromosome


def contains_task(chromosome, task):

    for gene in chromosome:
        if gene[0] == task:
            return True
    
    return False
