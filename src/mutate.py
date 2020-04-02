from random import random, randint


# MACHINES_MUTATION_PROBABILITY = 0.2
# MUTATION_PROBABILITY = 0.1

#
# def mutate(chromosome):
#     machines_number = max(map(lambda x: x[1], chromosome))
#     mutated_chromosome = []
#
#     if random() < MACHINES_MUTATION_PROBABILITY:
#         if random() < 0.5:
#             machines_number += 1
#         else:
#             machines_number -= 1
#
#     print(machines_number)
#
#     for gene in chromosome:
#         if gene[1] > machines_number or random() < MUTATION_PROBABILITY:
#             mutated_chromosome.append((gene[0], randint(0, machines_number)))
#         else:
#             mutated_chromosome.append(gene)
#
#     return mutated_chromosome
#



def mutate_in_place(chromosome, MUTATION_PROBABILITY, MACHINES_MUTATION_PROBABILITY):
    max_machines = max(map(lambda x: x[1], chromosome))

    # If we apply this mutation then we either gain a machine or lose one.
    if random() < MACHINES_MUTATION_PROBABILITY:
        if random() < 0.5 or max_machines == 0:
            max_machines += 1
        else:
            max_machines -= 1

    # To reorder the tasks on the new number of machines
    for i in range(len(chromosome)):
        if chromosome[i][1] > max_machines or random() < MUTATION_PROBABILITY:
            chromosome[i][1] = randint(0, max_machines)

    return chromosome
