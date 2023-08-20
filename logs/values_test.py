import os

folder = "logs/selection_crossover_etc_test"
directories = list()
SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}


def ordinal(num: int):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix


for filename in os.listdir(folder):
    f = os.path.join(folder, filename)

    if os.path.isfile(f):
        directories.append(f)

values = list()
for directory in directories:
    with open(directory) as f:
        line = f.readlines()[-3]
        line = line.replace("Best Fitnesses mean: ", "")
        line = line.replace("\n", "")

        values.append({
            'name':  directory,
            'value': float(line)
        })

reordered_values = sorted(values, key=lambda x: x['value'], reverse=True)

results_str = ''
for i, value in enumerate(reordered_values):
    temp_str = ''
    for j, string in enumerate(value['name'].split('-')):
        if j == 0:
            pass
        else:
            temp_str += f"{string} "

    results_str += f"{ordinal(i+1)} | {temp_str} : {value['value']}\n"
    print(f"{ordinal(i+1)} | {temp_str} : {value['value']}")

with open('logs/results_test.txt', 'w') as results:
    results.write(results_str)
