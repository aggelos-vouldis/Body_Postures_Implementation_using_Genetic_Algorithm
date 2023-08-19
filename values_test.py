import os

folder = "logs"
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
    print(f"{i+1} | {value['name']} : {value['value']}")
