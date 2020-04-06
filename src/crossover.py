from random import randint


def contains_task(chromosome, task):
    for gene in chromosome:
        if gene[0] == task:
            return True

    return False


def crossover(chromosome1, chromosome2):
    n = len(chromosome1)
    crossover_point = randint(0, n)
    new_chromosome = chromosome1[:crossover_point]

    for i in range(n):
        gene = chromosome2[i]
        if not contains_task(new_chromosome, gene[0]):
            new_chromosome.append(gene)

    return new_chromosome


def crossover_in_place(chromosome1, chromosome2):
    n = len(chromosome1)
    crossover_point = randint(0, n)

    counter1 = crossover_point
    counter2 = crossover_point
    for i in range(n):
        gene1 = chromosome2[i]
        gene2 = chromosome1[i]
        if not contains_task(chromosome1[:crossover_point], gene1[0]):
            chromosome1[counter1] = gene1
            counter1 += 1
        if not contains_task(chromosome2[:crossover_point], gene2[0]):
            chromosome2[counter2] = gene2
            counter2 += 1
    return chromosome1, chromosome2
