from DNA import DNA
from math import floor
from random import shuffle, randint
from numpy import interp
from DNA import CrossoverDeniedException


class Population():
    def __init__(self, target, mutationRate, crossover_probability, population_max, logger, show_debug_info=False):
        # setup logger
        self.logger = logger
        self.DEBUG_INFO = show_debug_info
        if self.DEBUG_INFO:
            self.logger = logger

        self.population = list()  # Array to hold the current population
        self.mating_pool = list()  # ArrayList which we will use for our "mating pool"
        self.generations = 0  # number of generations

        self.finished = False  # Boolean that represents whether we have finished evolving
        self.target = target  # Target list of numbers
        self.mutation_rate = mutationRate  # Mutation Rate
        self.crossover_probability = crossover_probability  # Crossover Likelihood
        self.perfect_score = 1

        self.best = ''
        self.best_fitness = 0
        self.last_best_fitness = 0
        self.best_overall_fitness = 0
        self.terminate_counter = 0

        for i in range(population_max):
            self.population.append(DNA(len(self.target)))

    # fill the fitness array with a value for every member of the population
    def __calcFitness__(self):
        for dna in self.population:
            dna.calcFitness(self.target)

    # Generate a mating pool
    def naturalSelection(self):
        # Clear the Array List
        self.mating_pool = list()

        # find the minimum fitness of all the population
        min_fitness = 1
        max_fitness = 0
        for dna in self.population:
            if dna.fitness < min_fitness:
                min_fitness = dna.fitness
            if dna.fitness > max_fitness:
                max_fitness = dna.fitness

        temp_overall_fitness = 0
        for dna in self.population:
            temp_overall_fitness += dna.fitness

        # Add each member to the mating pool a certain number of times, based on fitness
        # higher fitness = more entries to mating pool = more likely to be picked as a parent
        # lower fitness = fewer entries to mating pool = less likely to be picked as a parent
        for dna in self.population:
            fitness = interp(dna.fitness, [0, max_fitness], [0, 1])
            n = floor(fitness * 100)
            # print(f"fitness: {fitness} | n: {n} | real fitness: {dna.fitness}")
            for i in range(n):
                self.mating_pool.append(dna)

        shuffle(self.mating_pool)

    # Create a new generation
    def generate(self):
        # Refill the generation with children from the mating pool
        # clear the past population
        last_population = self.population
        self.population = list()

        # Refill the population with children from the mating pool
        for dna in last_population:
            try:
                a = int(floor(randint(0, len(self.mating_pool) - 1)))
                b = int(floor(randint(0, len(self.mating_pool) - 1)))

                parentA = self.mating_pool[a]
                parentB = self.mating_pool[b]

                child = parentA.crossover(
                    parentB, self.crossover_probability)
                child.mutate(self.mutation_rate)
            except CrossoverDeniedException:
                child = DNA(len(self.target))

            self.population.append(child)
        self.generations += 1

    def __get_best__(self):
        return self.best

    # Compute the current most fit member of the population
    def evaluate(self):
        world_record = 0
        idx = 0

        for i, dna in enumerate(self.population):
            if dna.fitness > world_record:
                idx = i
                world_record = dna.fitness

        self.best = self.population[idx].genes

        # change the best fitness and the last best fitness
        self.last_best_fitness = self.best_fitness
        self.best_fitness = world_record

        if self.best_fitness > self.best_overall_fitness:
            self.best_overall_fitness = self.best_fitness

        # print(abs(self.best_fitness - self.last_best_fitness))
        if self.best_fitness == self.last_best_fitness or (self.best_fitness - self.last_best_fitness) <= 0.01:
            self.terminate_counter += 1
        else:
            self.terminate_counter = 0

        if world_record == self.perfect_score:  # perfect score has reached
            self.finished = True

    def __isFinished__(self):
        return self.finished

    def __getGenerations__(self):
        return self.generation

    def __print__(self):
        for DNA in self.population:
            print(DNA.__toString__())

    def __printFitness__(self):
        for dna in self.population:
            print(dna.fitness)

    def __getAverageFitness__(self):
        total = 0
        for dna in self.population:
            total += dna.fitness

        return total / len(self.population)

    def __terminate__(self):
        if self.finished:
            return True

        if self.terminate_counter >= 20:
            return True

        if self.generations >= 1000:
            return True

        return False

    def __write_debug_info__(self):
        debug_str = ''
        debug_str += f"Generation {self.generations} | Average Generation Fitness: {self.__getAverageFitness__()} | Best Fitness: {self.best_fitness} | Population Length: {len(self.population)}"

        self.logger.debug(debug_str)
