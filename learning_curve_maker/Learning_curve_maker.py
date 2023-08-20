from matplotlib import pyplot as plt
from os.path import join, exists
from os import mkdir
from numpy import array_split

population = 20
crossover_probability = 0.1
mutation_rate = 0.01
parent_dir = 'learning_curve_maker/images/'


def ordinal(num: int):
    SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix


with open(f'logs/for_curves/log-Tournament_Selection-single_point_crossover-{population}-{crossover_probability}_{mutation_rate}.log', 'r') as f:
    lines = f.readlines()

final = list()
current_exec_num = int

for line in lines:
    if(line.startswith("Execution")):

        current_exec_num = int(
            line.replace("Execution ", "").replace("\n", "")
        )

        final.append(
            {
                'exec_num': current_exec_num,
                'values': list()
            }
        )

    elif line.startswith("Generation"):
        value_to_append = line.split("|")[2].replace(
            " Best Fitness: ", "").replace(" ", "")
        final[int(current_exec_num-1)]['values'].append(value_to_append)

path = f"{parent_dir}pop_{population}-crossover_{crossover_probability}-mutation_{mutation_rate}"
if not exists(path):
    mkdir(path)

sub_lists = array_split(final, 2)

for execution in final:
    # if execution['exec_num'] != 1:
    #     break
    execution_number = execution['exec_num']

    # Plot Learning Curve
    plt.figure(figsize=(18, 9))

    # splitted_values = array_split(final[execution_number - 1]['values'], 8)

    plt.plot(final[execution_number - 1]['values'], color='blue', marker='o',
             markersize=1, label='Best Fitness')

    plt.title(
        f'Best Fitness Per Generation\npopulation={population}, crossover probability={crossover_probability}, mutation rate={mutation_rate}\n{ordinal(execution_number)} Execution')

    # specifically for population == 20 and crossover_probability == 0.1 and mutation_rate == 0.01
    if population == 20 and crossover_probability == 0.1 and mutation_rate == 0.01:
        for n, label in enumerate(plt.gca().yaxis.get_ticklabels()):
            if n % 20 != 0:
                label.set_visible(False)
        plt.tick_params(labelrotation=45, labelsize='xx-small', grid_alpha=0)

    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')

    plt.grid()
    plt.legend(loc='lower right')

    plt.savefig(f'{path}/{ordinal(execution_number)}_Execution.png',
                bbox_inches='tight')

    plt.close()

    print(f"Execution {execution_number} done")
