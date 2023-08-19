from Target import Target
from Population import Population
from numpy import mean


def write_to_file(filename, message):
    with open(filename, 'a') as f:
        f.write(message)


def run_GA(filename: str, execution_num=0):
    if LOGGING:
        write_to_file(filename, f"\nExecution {execution_num + 1}\n")
    if DEBUG_INFO:
        print(f"\nExecution {execution_num + 1}\n")

    # Create a random population of N elements
    pop = Population(
        target=target.get_target(),
        other_positions=target.get_other_position_values(),
        mutationRate=mutation_rate,
        population_max=max_pop,
        crossover_type=picked_crossover,
        filename=filename,
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
        # pop.__write_debug_info__()
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

        write_to_file(filename, debug_str)

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
max_populations = [200, 20]
crossover_probabilities = [0.1, 0.6, 0.9]
mutation_rates = [0.01, 0.0, 0.1]

for max_pop in max_populations:
    for crossover_probability in crossover_probabilities:
        for mutation_rate in mutation_rates:

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
            crossover_types = [{
                'type': 0,
                'probability': crossover_probability,
                'name': 'single_point_crossover'
            },
                {
                'type': 1,
                'probability': crossover_probability,
                'points': [2, 3, 4, 5],
                'name': 'multiple_point_crossover'
            },
                {
                'type': 2,
                'probability': crossover_probability,
                'name': 'uniform_crossover'
            }]

            for picked_selection in selection_types:
                for picked_crossover in crossover_types:

                    print()
                    # setup Logger
                    filename = f"logs/log-{picked_selection['name']}-{picked_crossover['name']}-{max_pop}-{crossover_probability}_{mutation_rate}.log"

                    target = Target()
                    if LOGGING:
                        write_to_file(
                            filename, f"Target: \n{target.get_target()}\n")

                    best_fitness_values = list()
                    generation_values = list()

                    print(
                        "-------------------------- STARTING --------------------------")

                    for i in range(n_runs):
                        run_GA(filename, i)

                    if LOGGING:
                        write_to_file(
                            filename, f"\nBest Fitnesses mean: {mean(best_fitness_values)}\n")
                        write_to_file(
                            filename, f"Total Generations mean: {mean(generation_values)}\n")
                        write_to_file(
                            filename, "------------------------------------------------")

                    print(
                        f"""-------------------------- FINISHED --------------------------
best fitnesses mean: {mean(best_fitness_values)}
generations value mean: {mean(generation_values)}
------------------------------------------------""")
