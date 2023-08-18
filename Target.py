import pandas as pd
from sklearn.preprocessing import QuantileTransformer

# This file reads all info from the dataset.csv file and uses the QuantileTransformer on them
# as I did on the last exercise.
# Later it calculates the mean value and transforms the result into a bit array of 1's and 0's

# The last transformation is done by truncating each average value to 10 decimals
# and then converting each number (after the comma) to binary format
# lastly add zeros to the start of each binary number so that the length equals 4 (so that each number has the same length)
#
# ex: Sensor Value: 0.4959 --> Decimal Value:  0    4    9    5    9 -->
#                          --> Binary Value: 0000 0100 1001 0101 1001 --> Finally: 00000100100101011001
#
# Finally we create a string that has all the binary numbers together


def drop_unnecessary_columns(df: pd.DataFrame, columns_to_drop: list()):
    tempDf = pd.DataFrame(df)

    for column in columns_to_drop:
        tempDf = tempDf.drop(column, axis='columns')

    return tempDf


def read_csv_make_changes():
    df = pd.read_csv("dataset.csv", delimiter=';', low_memory=False)

    df = df.loc[df['class'] == 'sitting']
    columns_to_delete = ['user', 'gender', 'age',
                         'how_tall_in_meters', 'weight', 'body_mass_index', 'class']

    df = drop_unnecessary_columns(df, columns_to_delete)
    return df


def transform_data(data):
    transformed_data = QuantileTransformer().fit_transform(data)

    sensor_columns = ['x1', 'y1', 'z1', 'x2', 'y2',
                      'z2', 'x3', 'y3', 'z3', 'x4', 'y4', 'z4']
    return_data = pd.DataFrame(transformed_data, columns=sensor_columns)

    return return_data


def calculate_target():
    df = read_csv_make_changes()
    df = transform_data(data=df)

    sensor_values = list()
    for key in df.keys():
        sensor_values.append({
            'name': key,
            'mean_value': df[key].mean()
        })

    final_values = list()
    for sensor in sensor_values:
        temp_value = '%.10f' % (sensor['mean_value'])
        temp_value = temp_value.replace(".", "")

        temp_binary = ""
        for number in temp_value:
            temp_binary += decimal_to_binary(int(number))

        final_values.append(temp_binary)

        if DEBUG_INFO:
            print(sensor['name'] + ' | Sensor Value: ' + str(sensor['mean_value']) + ' | Decimal Value: ' +
                  str(temp_value) + ' | Binary Value: ' + temp_binary)

    final_str = ''
    for final_value in final_values:
        final_str += final_value
    return final_str


def decimal_to_binary(num: int):
    binary_num = bin(num).replace("0b", "")

    if len(binary_num) != 4:
        for i in range(4 - len(binary_num)):
            binary_num = f"{'0'}{binary_num}"

    return binary_num


def decrypt_target(target: str):
    list_of_values = [target[i:i+44] for i in range(0, len(target), 44)]

    changed_values = list()
    for value in list_of_values:
        list_of_numbers = [value[j:j+4]
                           for j in range(0, len(value), 4)]

        temp_value = str()
        for num in list_of_numbers:
            temp_value += str(binary_to_decimal(int(num)))
        changed_values.append(f"{temp_value[0]}.{temp_value[1:]}")

    return changed_values


def binary_to_decimal(binary: int):
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1

    return decimal


DEBUG_INFO = False

if __name__ == '__main__':
    target = calculate_target()
    print(f"target length: {len(target)}")

    decrypt_target(target)
    if DEBUG_INFO:
        # print the target values splitted
        print(
            f"\nencrypted target values:\n{[target[i:i+44] for i in range(0, len(target), 44)]}")
        print(f"\ndecrypted target values:\n{decrypt_target(target)}")
