from random import random
from math import floor
from random import randint, random


class DNA():

    def __init__(self, num: int):
        self.genes = ''
        self.fitness = 0

        for i in range(num):
            self.genes += f"{randint(0, 1)}"

    def calcFitness(self, target):
        # 1 = the best fitness
        temp_score = 0
        for i, num in enumerate(target):
            if(num == self.genes[i]):
                temp_score += 1

        self.fitness = temp_score / len(target)

    def crossover(self, partner, crossover_probability):
        if(random() > crossover_probability):
            raise CrossoverDeniedException
        # A new child
        child = DNA(len(self.genes))

        midpoint = randint(0, len(self.genes))

        # half genes from the parentA half from the parentB
        for i in range(len(self.genes)):
            if randint(0, 1) == 0:
                child.genes = self.__change_gen_character__(
                    child.genes, i, self.genes[i])
            else:
                child.genes = self.__change_gen_character__(
                    child.genes, i, partner.genes[i])

        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if(random() < mutation_rate):
                self.genes = self.__change_gen_character__(
                    genes_to_change=self.genes, char_index=i, character=self.genes[i])

    def __toString__(self):
        return self.genes

    def __change_gen_character__(self, genes_to_change: str, char_index: int, character: str):
        # function to change a specific character in the "genes" string
        temp_list = list(genes_to_change)
        temp_list[char_index] = character
        genes_to_change = ''.join(temp_list)

        return genes_to_change


class CrossoverDeniedException(Exception):
    "Raised when a crossover is denied"
    pass
