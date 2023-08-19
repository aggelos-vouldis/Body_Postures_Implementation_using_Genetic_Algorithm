from random import random, randint
from Point import TargetPoints
from Errors import CrossoverDeniedException
from typing import Tuple
from Target import Target
from Errors import InvalidCrossoverType


class DNA():
    "Class that represents a DNA sequence"

    def __init__(self) -> None:
        self.genes = TargetPoints()
        self.fitness = 0

    def calcFitness(self, target: TargetPoints, other_positions: Tuple[TargetPoints]) -> None:
        "Calculates the fitness of this DNA (it emphasize the target distance)"

        target_similarity = target.measure_cosine_similarity(self.genes)

        temp_dist = 0
        for other_position in other_positions:
            temp_dist += other_position.measure_cosine_similarity(self.genes)
        temp_dist = 1 - (temp_dist / len(other_positions))

        c = 0.2
        self.fitness = (target_similarity + c * (temp_dist)) / (1 + c)

    def crossover(self, picked_crossover: dict):
        if picked_crossover['type'] == 0:
            child = self.single_point_crossover(
                picked_crossover['partner'], picked_crossover['probability'])
        elif picked_crossover['type'] == 1:
            child = self.multiple_point_crossover(
                picked_crossover['partner'], picked_crossover['probability'], picked_crossover['points'])
        elif picked_crossover['type'] == 2:
            child = self.uniform_crossover(
                picked_crossover['partner'], picked_crossover['probability'])
        else:
            raise InvalidCrossoverType

        return child

    def single_point_crossover(self, partner, crossover_probability: float):
        if random() > crossover_probability:
            raise CrossoverDeniedException
        child = DNA()

        midpoint = randint(0, len(self.genes))

        for i in range(len(self.genes)):
            if(i > midpoint):
                child.genes.set_i(i, self.genes.get_i(i))
            else:
                child.genes.set_i(i, partner.genes.get_i(i))

        return child

    def multiple_point_crossover(self, partner, crossover_probability: float, crossover_points):
        "Multiple point crossover method. It needs a list of crossover points ex [2,3,4,5]"

        if(len(crossover_points) < 2 or len(crossover_points) >= 5):
            raise SyntaxError

        if random() > crossover_probability:
            raise CrossoverDeniedException
        child = DNA()

        if len(crossover_points) == 2:
            for i in range(len(self.genes)):
                if(i < crossover_points[0]):
                    child.genes.set_i(i, self.genes.get_i(i))
                elif i < crossover_points[1]:
                    child.genes.set_i(i, partner.genes.get_i(i))
                else:
                    child.genes.set_i(i, self.genes.get_i(i))

        elif len(crossover_points) == 3:
            for i in range(len(self.genes)):
                if(i < crossover_points[0]):
                    child.genes.set_i(i, self.genes.get_i(i))
                elif i < crossover_points[1]:
                    child.genes.set_i(i, partner.genes.get_i(i))
                elif i < crossover_points[2]:
                    child.genes.set_i(i, self.genes.get_i(i))
                else:
                    child.genes.set_i(i, partner.genes.get_i(i))
        elif len(crossover_points) == 4:
            for i in range(len(self.genes)):
                if(i < crossover_points[0]):
                    child.genes.set_i(i, self.genes.get_i(i))
                elif i < crossover_points[1]:
                    child.genes.set_i(i, partner.genes.get_i(i))
                elif i < crossover_points[2]:
                    child.genes.set_i(i, self.genes.get_i(i))
                elif i < crossover_points[3]:
                    child.genes.set_i(i, partner.genes.get_i(i))
                else:
                    child.genes.set_i(i, self.genes.get_i(i))

        return child

    def uniform_crossover(self, partner, crossover_probability: float):
        if(random() > crossover_probability):
            raise CrossoverDeniedException
        # A new child
        child = DNA()

        for i in range(len(self.genes)):
            if randint(0, 1) == 0:
                child.genes.set_i(i, self.genes.get_i(i))
            else:
                child.genes.set_i(i, partner.genes.get_i(i))

        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if(random() < mutation_rate):
                self.genes.set_i(i, random())

    def __str__(self) -> str:
        return str(self.genes)


if __name__ == '__main__':
    dna1 = DNA()
    dna2 = DNA()

    child = dna1.multiple_point_crossover(dna2, 1, [2, 4, 6, 8])

    t = Target()
    child.calcFitness(t.get_target(), t.get_other_position_values())
    print(f"child:\n{child.fitness}")
