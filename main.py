from Target import Target
from Population import Population
import logging
from numpy import mean


def run_ga(execution_num=0):
    if DEBUG_INFO:
        logger.debug(f"\nExecution {execution_num + 1}\n")

    # Create a random population of N elements
    pop = Population(
        target=target.get_target(),
        other_positions=target.get_other_position_values(),
        mutationRate=mutation_rate,
        population_max=max_pop,
        logger=logger,
        show_debug_info=DEBUG_INFO,
        crossover_probability=crossover_probability)

    while True:
        # Generate Mating Pool
        pop.cost_selection()
        # Create next Generation
        pop.generate()
        # Calculate Fitness
        pop.__calcFitness__()
        # Evaluate Population
        pop.evaluate()

        # Write to log file
        pop.__write_debug_info__()

        # print(
        #     f"Generation: { pop.generations } | Average Fitness: {round(pop.__getAverageFitness__(), 10)} | Best Fitness: {pop.best_fitness} | Terminate Counter: {pop.terminate_counter}")

        if pop.__terminate__():
            break

    best_fitness_values.append(pop.best_overall_fitness)
    generation_values.append(pop.generations)

    if DEBUG_INFO:
        debug_str = "------------------------------------------------"
        debug_str += f"\nTotal Generations: {pop.generations}\nTotal Population: {max_pop}   ---   Mutation Rate: {mutation_rate}  ---  Crossover Probability: {crossover_probability}\nAverage Fitness: {pop.__getAverageFitness__()}  ---  Best Overall Fitness: {pop.best_overall_fitness}\n"
        debug_str += "------------------------------------------------"

        logger.debug(debug_str)


# number of times to run the genetic algorithm
n_runs = 10

# Debug logging = Log everything
DEBUG_INFO = True

# Basic Variables
max_pop = 200
mutation_rate = 0.00
crossover_probability = 0.6

# setup Logger
logging.basicConfig(filename=f"logs/log_{max_pop}_{crossover_probability}_{mutation_rate}.log",
                    format='%(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


target = Target()
if DEBUG_INFO:
    logger.debug(f"Target string: {target.get_target()}\n")

best_fitness_values = list()
generation_values = list()

for i in range(n_runs):
    run_ga(i)

print("------------------------------------------------\nFINISHED\n------------------------------------------------")
print(f"best fitnesses mean: {mean(best_fitness_values)}")
print(f"generations value mean: {mean(generation_values)}")
