from deap import creator, base

from src.crossover import crossover_in_place as mate
from src.mutate import mutate_in_place as mutate
from src.schedule_generator import init_generation, makeGraph

# Creating abstract fitness function, with two objective minimizer
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))

# Creating an individual that inherits the list type, with a nb_mach attribute
creator.create("Individual", list, fitness=creator.FitnessMin)

# Initializing variables
NB_POP, MAX_MACH = 10, 10
MACHINES_MUTATION_PROBABILITY = 0.2
MUTATION_PROBABILITY = 0.1

# Let us build the graph only once in order to save time
graph_name = "smallRandom"
task_graph = makeGraph(graph_name)


def initChromosome(icls, content):
    """icls : class of the individual (i.e. "creator.Individual" in this case) """
    return icls(content)


def initPopulation(pcls, ind_init, filename):
    """
    pcls : class of the population (i.e. a toolbox attribute of an individual)
    ind_init : function to initialize individuals
    filename : the name of the graph file we want to use (for now use only smallRandom or mediumRandom)

    return : a list of individuals
    """
    contents = init_generation(NB_POP, MAX_MACH, task_graph)
    return pcls(ind_init(c) for c in contents)


toolbox = base.Toolbox()

toolbox.register("individual_guess", initChromosome, creator.Individual)
toolbox.register("population_guess", initPopulation, list, toolbox.individual_guess, graph_name)
toolbox.register("mutate", mutate, MUTATION_PROBABILITY, MACHINES_MUTATION_PROBABILITY)
toolbox.register("mate", mate)
population = toolbox.population_guess()


# Test
ind1, ind2 = population[0], population[9]

for i in range(20):
    child1, child2 = [toolbox.clone(ind) for ind in (ind1, ind2)]
    toolbox.mate(child1, child2)
    print(f"{i} child1", child1,"\n", " child2", child2)