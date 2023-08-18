import Target
from Population import Population
import logging
from numpy import mean

logging.basicConfig(filename="log.log",
                    format='%(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def run_genetic_algorithm(exec_num=0):
    if DEBUG_INFO:
        logger.debug(f"\nExecution {exec_num + 1}\n")

    # Create a random population of N elements
    pop = Population(target=target, mutationRate=mutation_rate, population_max=max_pop,
                     logger=logger, show_debug_info=DEBUG_INFO, crossover_probability=crossover_probability)

    while(True):
        # Generate mating pool
        pop.naturalSelection()
        # Create next Generation
        pop.generate()
        # Calculate fitness
        pop.__calcFitness__()
        # Check if we reached fitness 1 = 100%
        pop.evaluate()

        # write to log file
        pop.__write_debug_info__()

        print(
            f"Generation: { pop.generations } | Average Fitness: {round(pop.__getAverageFitness__(), 10)} | Best Fitness: {pop.best_fitness} | Terminate Counter: {pop.terminate_counter}")
        if pop.__terminate__():
            break

    best_fitness_values.append(pop.best_overall_fitness)
    generation_values.append(pop.generations)
    if DEBUG_INFO:
        debug_str = ''
        debug_str += "------------------------------------------------"
        debug_str += f"\nTotal Generations: {pop.generations}\nTotal Population: {max_pop}   ---   Mutation Rate: {mutation_rate}  ---  Crossover Probability: {crossover_probability}\nAverage Fitness: {pop.__getAverageFitness__()}  ---  Best Overall Fitness: {pop.best_overall_fitness}\n"
        debug_str += "------------------------------------------------"

        logger.debug(debug_str)


# Debug logging
DEBUG_INFO = True

# Basic Variables
max_pop = 200
mutation_rate = 0.01
crossover_probability = 0.6


# SETUP
target = Target.calculate_target()
# target = '101010101'
if DEBUG_INFO:
    logger.debug(f"Target string: {target}\n")

best_fitness_values = list()
generation_values = list()

for i in range(10):
    run_genetic_algorithm(i)


print("------------------------------------------------\nFINISHED\n------------------------------------------------")
print(f"best fitnesses mean: {mean(best_fitness_values)}")
print(f"generations value mean: {mean(generation_values)}")
