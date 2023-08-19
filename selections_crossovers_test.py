import os

values = [
    {
        'name': 'Cost Selection & Multiple Crossover',
        'value': 0.8291780792638704,
    },
    {
        'name': 'Cost Selection & Single Crossover',
        'value': 0.8284788061032595,
    },
    {
        'name': 'Cost Selection & Uniform Crossover',
        'value': 0.8285344483359122,
    },
    {
        'name': 'Rank Selection & Multiple Crossover',
        'value': 0.8279177848015891,
    },
    {
        'name': 'Rank Selection & Single Crossover',
        'value': 0.8279795915153482,
    },
    {
        'name': 'Rank Selection & Uniform Crossover',
        'value': 0.8275902313460044,
    },
    {
        'name': 'Tournament Selection & Multiple Crossover',
        'value': 0.8331556714136935,
    },
    {
        'name': 'Tournament Selection & Single Crossover',
        'value': 0.833252450763635,
    },
    {
        'name': 'Tournament Selection & Uniform Crossover',
        'value': 0.8332276282336728,
    }
]
folder = "logs\Selection-Crossover-tests"
directories = list()

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

for i, value in enumerate(reordered_values):
    print(
        f"{i+1} | {value['name']} : {value['value']}")
