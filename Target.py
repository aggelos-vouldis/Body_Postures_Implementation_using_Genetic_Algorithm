import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from Point import TargetPoints, Point


class Target():
    def __init__(self) -> None:
        sitting_mean_values, walking_mean_values, standingUp_mean_values, standing_mean_values, sittingDown_mean_values = calculate_targets()

        self.sitting_tPoints = self.create_point(sitting_mean_values)
        self.walking_tPoints = self.create_point(walking_mean_values)
        self.standingUp_tPoints = self.create_point(standingUp_mean_values)
        self.standing_tPoints = self.create_point(standing_mean_values)
        self.sittingDown_tPoints = self.create_point(sittingDown_mean_values)

    def create_point(self, values: list()):
        temp = TargetPoints(
            Point([values[i] for i in range(0, 3)]),
            Point([values[i] for i in range(3, 6)]),
            Point([values[i] for i in range(6, 9)]),
            Point([values[i] for i in range(9, 12)])
        )
        return temp

    def get_target(self) -> TargetPoints:
        return self.sitting_tPoints

    def get_other_position_values(self):
        return self.walking_tPoints, self.standingUp_tPoints, self.standing_tPoints, self.sittingDown_tPoints


def drop_unnecessary_columns(df: pd.DataFrame, columns_to_drop: list()):
    tempDf = pd.DataFrame(df)

    for column in columns_to_drop:
        tempDf = tempDf.drop(column, axis='columns')

    return tempDf


def read_csv_make_changes():
    df = pd.read_csv("dataset.csv", delimiter=';', low_memory=False)

    # split positions
    sitting_pos = df.loc[df['class'] == 'sitting']
    walking_pos = df.loc[df['class'] == 'walking']
    standingUp_pos = df.loc[df['class'] == 'standingup']
    standing_pos = df.loc[df['class'] == 'standing']
    sittingDown_pos = df.loc[df['class'] == 'sittingdown']

    columns_to_delete = ['user', 'gender', 'age',
                         'how_tall_in_meters', 'weight', 'body_mass_index', 'class']

    # delete unnecessary columns from all positions
    sitting_pos = drop_unnecessary_columns(
        sitting_pos, columns_to_delete
    )
    walking_pos = drop_unnecessary_columns(
        walking_pos, columns_to_delete
    )
    standingUp_pos = drop_unnecessary_columns(
        standingUp_pos, columns_to_delete
    )
    standing_pos = drop_unnecessary_columns(
        standing_pos, columns_to_delete
    )
    sittingDown_pos = drop_unnecessary_columns(
        sittingDown_pos, columns_to_delete
    )

    return sitting_pos, walking_pos, standingUp_pos, standing_pos, sittingDown_pos


def transform_data(data):
    transformed_data = QuantileTransformer().fit_transform(data)

    sensor_columns = ['x1', 'y1', 'z1', 'x2', 'y2',
                      'z2', 'x3', 'y3', 'z3', 'x4', 'y4', 'z4']
    return_data = pd.DataFrame(transformed_data, columns=sensor_columns)

    return return_data


def calculate_targets():
    sitting_pos, walking_pos, standingUp_pos, standing_pos, sittingDown_pos = read_csv_make_changes()

    # transform data with the Quantile Transformer
    sitting_pos = transform_data(sitting_pos)
    walking_pos = transform_data(walking_pos)
    standingUp_pos = transform_data(standingUp_pos)
    standing_pos = transform_data(standing_pos)
    sittingDown_pos = transform_data(sittingDown_pos)

    # calculate the mean values for each position
    # values will be stored in an array like: [x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4]
    sitting_mean_values = calculate_mean_values(sitting_pos)
    walking_mean_values = calculate_mean_values(walking_pos)
    standingUp_mean_values = calculate_mean_values(standingUp_pos)
    standing_mean_values = calculate_mean_values(standing_pos)
    sittingDown_mean_values = calculate_mean_values(sittingDown_pos)

    if DEBUG_INFO:
        print(sitting_mean_values)
        print(walking_mean_values)
        print(standingUp_mean_values)
        print(standing_mean_values)
        print(sittingDown_mean_values)

    return sitting_mean_values, walking_mean_values, standingUp_mean_values, standing_mean_values, sittingDown_mean_values


def calculate_mean_values(df: pd.DataFrame):
    temp_list = list()

    for key in df.keys():
        temp_list.append(df[key].mean())

    return temp_list


DEBUG_INFO = False

if __name__ == '__main__':
    target = Target()

    print(f"Target:\n{target.get_target()}\n")

    print("All the other posible positions:\n")
    for other_value in target.get_other_position_values():
        print(f"{other_value}\n")
