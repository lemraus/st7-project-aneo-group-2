import random

import matplotlib.pyplot as plt
import numpy
from deap import creator, base, tools
from scoop import futures, shared

from cost_func import cost_func as evaluate
from crossover import crossover_in_place as mate
from mutate import mutate_in_place as mutate
from schedule_generator import init_generation
from construct_graph import construct_graph
from timer import timer
import os

# Creating abstract fitness function, with two objective minimizer
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))

# Creating an individual that inherits the list type, with a nb_mach attribute
creator.create("Individual", list, fitness=creator.FitnessMin)

# Initializing variables
NB_POP, MAX_MACH = 50, 50
MACHINES_MUTATION_PROBABILITY = 0.3
MUTATION_PROBABILITY = 0.2
CXPB = 0.5
MUTPB = 0.5
NGEN = 30


def initChromosome(icls, content):
    """icls : class of the individual (i.e. "creator.Individual" in this case) """
    return icls(content)


def initPopulation(pcls, ind_init):
    """
    pcls : class of the population (i.e. a toolbox attribute of an individual)
    ind_init : function to initialize individuals

    return : a list of individuals
    """
    graph = shared.getConst("graph")
    contents = init_generation(NB_POP, MAX_MACH, graph)
    return pcls(ind_init(c) for c in contents)


# Creating and registering toolbox
toolbox = base.Toolbox()
# toolbox.register("map", futures.map)
toolbox.register("individual_guess", initChromosome, creator.Individual)
toolbox.register("mutate", mutate, MUTATION_PROBABILITY)
toolbox.register("mate", mate)
toolbox.register("select", tools.selTournament, tournsize=3)

# Creating and registering stats
stats_cost = tools.Statistics(key=lambda ind: ind.fitness.values[0])

stats_dur = tools.Statistics(key=lambda ind: ind.fitness.values[1])

mstats = tools.MultiStatistics(cost=stats_cost, duration=stats_dur)
mstats.register("min", numpy.min)
mstats.register("avg", numpy.average)
mstats.register("max", numpy.max)

def genetic_algo():
    # Shared constants
    graph_name = shared.getConst("graph_name")
    graph = shared.getConst("graph")
    max_duration = shared.getConst("max_duration")
    # Extra toolbox registers
    toolbox.register("population_guess", initPopulation, list, toolbox.individual_guess)
    toolbox.register("evaluate", evaluate, graph, max_duration=max_duration)
    # Creating the population
    pop = toolbox.population_guess()

    # Creating a logbook for recording statistics
    logbook = tools.Logbook()

    # To the heart of the genetic algorithm

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = [toolbox.clone(ind) for ind in offspring]

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Recording statistics
        record = mstats.compile(pop)
        logbook.record(gen=g, evals=len(invalid_ind), **record)

    gen = logbook.select("gen")
    fit_mins = logbook.chapters["cost"].select("min")
    duration_mins = logbook.chapters["duration"].select("min")
    duration_maxs = logbook.chapters["duration"].select("max")
    fit_avg = logbook.chapters["cost"].select("avg")

    return gen, fit_mins, fit_avg, duration_mins, duration_maxs

def single_run(index):
    print(f"Starting run number {index}...")
    result = genetic_algo()
    print(f"Finished run number {index}.")
    return result

@timer
def multiple_runs_mean(nb_runs):
    generations = None
    all_fit_mins, all_fit_avg, all_duration_mins, all_duration_maxs = [], [], [], []

    runs_results = futures.map(single_run, range(1, nb_runs + 1))
    for gen, fit_mins, fit_avg, duration_mins, duration_maxs in runs_results:
        if generations == None:
            generations = gen
        all_fit_mins.append(fit_mins)
        all_fit_avg.append(fit_avg)
        all_duration_mins.append(duration_mins)
        all_duration_maxs.append(duration_maxs)

    def mean_values(all_values):
        return [sum(x) / nb_runs for x in zip(*all_values)]

    mean_fit_mins = mean_values(all_fit_mins)
    mean_fit_avg = mean_values(all_fit_avg)
    mean_duration_mins = mean_values(all_duration_mins)
    mean_duration_maxs = mean_values(all_duration_maxs)

    return nb_runs, generations, mean_fit_mins, mean_fit_avg, mean_duration_mins, mean_duration_maxs

def plot_runs_mean(runs_results):
    graph_name = shared.getConst("graph_name")
    max_duration = shared.getConst("max_duration")
    nb_runs, generations, mean_fit_mins, mean_fit_avg, mean_duration_mins, mean_duration_maxs = runs_results
    fig, ax1 = plt.subplots()
    fig.suptitle(f"Mean results over {nb_runs} runs, graph: '{graph_name}', duration constraint: {max_duration}")
    line1 = ax1.plot(generations, mean_fit_mins, "b-", label="Minimum Cost")
    line3 = ax1.plot(generations, mean_fit_avg, "g-", label= "Average Cost")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Cost", color="b")
    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(generations, mean_duration_mins, "r-", label="Minimum Duration")
    line4 = ax2.plot(generations, mean_duration_maxs, "y-", label="Maximum Duration")
    ax2.set_ylabel("Duration", color="r")
    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2 + line3 + line4
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="upper right")

    OUTPUT_DIR = os.environ.get("AZ_BATCH_TASK_DIR", ".")
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{graph_name}_{nb_runs}_runs.png")
    plt.savefig(OUTPUT_FILE)

if __name__ == "__main__":
    graph_name = "MediumComplex"
    task_graph, MAXIMUM_DURATION = construct_graph(graph_name)
    shared.setConst(graph_name=graph_name, graph=task_graph, max_duration=MAXIMUM_DURATION)

    plot_runs_mean(multiple_runs_mean(16))