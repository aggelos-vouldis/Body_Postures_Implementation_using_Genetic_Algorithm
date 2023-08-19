from Target import Target
from Population import Population
import logging
from numpy import mean


def run_GA(execution_num=0):
    if LOGGING:
        logger.debug(f"\nExecution {execution_num + 1}\n")
    if DEBUG_INFO:
        print(f"\nExecution {execution_num + 1}\n")

    # Create a random population of N elements
    pop = Population(
        target=target.get_target(),
        other_positions=target.get_other_position_values(),
        mutationRate=mutation_rate,
        population_max=max_pop,
        logger=logger,
        show_debug_info=LOGGING,
        crossover_probability=crossover_probability)

    while True:
        # Generate Mating Pool
        pop.generate_mating_pool(selection_type=picked_selection)
        # Create next Generation
        pop.generate()
        # Calculate Fitness
        pop.__calcFitness__()
        # Evaluate Population
        pop.evaluate()

        # Write to log file
        pop.__write_debug_info__()
        # Print Information
        pop.__print_debug_info__(DEBUG_INFO)

        if pop.__terminate__():
            break

    best_fitness_values.append(pop.best_overall_fitness)
    generation_values.append(pop.generations)

    if LOGGING:
        debug_str = "------------------------------------------------"
        debug_str += f"\nTotal Generations: {pop.generations}\nTotal Population: {max_pop}   ---   Mutation Rate: {mutation_rate}  ---  Crossover Probability: {crossover_probability}\nAverage Fitness: {pop.__getAverageFitness__()}  ---  Best Overall Fitness: {pop.best_overall_fitness}\n"
        debug_str += "------------------------------------------------"

        logger.debug(debug_str)

    if DEBUG_INFO:
        temp_str = "------------------------------------------------"
        temp_str += f"\nTotal Generations: {pop.generations}\nTotal Population: {max_pop}   ---   Mutation Rate: {mutation_rate}  ---  Crossover Probability: {crossover_probability}\nAverage Fitness: {pop.__getAverageFitness__()}  ---  Best Overall Fitness: {pop.best_overall_fitness}\n"
        temp_str += "------------------------------------------------"

        print(temp_str)

    print(f"Execution { execution_num + 1 } ENDED")


# number of times to run the genetic algorithm
n_runs = 10

LOGGING = True  # Boolean to log information
DEBUG_INFO = False  # Boolean to show information

# Basic Variables
max_pop = 200
crossover_probability = 0.1
mutation_rate = 0.01

selection_types = [{
    'type': 0,
    'name': 'Tournament_Selection',
    'n_comparisons': int(max_pop / 2)
}, {
    'type': 1,
    'name': 'Rank_Selection'
}, {
    'type': 2,
    'name': 'Cost_Selection'
}]
picked_selection = selection_types[0]

# setup Logger
logging.basicConfig(
    filename=f"logs/log-{picked_selection['name']}-single_point_crossover-{max_pop}-{crossover_probability}_{mutation_rate}.log",
    format='%(message)s',
    filemode='w'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


target = Target()
if LOGGING:
    logger.debug(f"Target: \n{target.get_target()}\n")

best_fitness_values = list()
generation_values = list()

print("-------------------------- STARTING --------------------------")

for i in range(n_runs):
    run_GA(i)

if LOGGING:
    logger.debug(f"Best Fitnesses mean: {mean(best_fitness_values)}")
    logger.debug(f"Total Generations mean: {mean(generation_values)}")
    logger.debug("------------------------------------------------")

print(
    f"""-------------------------- FINISHED --------------------------
best fitnesses mean: {mean(best_fitness_values)}
generations value mean: {mean(generation_values)}
------------------------------------------------""")
