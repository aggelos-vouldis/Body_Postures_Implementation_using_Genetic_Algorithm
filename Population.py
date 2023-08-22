from DNA import DNA, CrossoverDeniedException
from math import floor
from random import shuffle, randint
from numpy import interp
from Target import Target
from Errors import InvalidSelectionType


class Population():
    "Class that represents a population of DNA sequences"

    def __init__(
        self,
        target,
        other_positions,
        mutationRate,
        crossover_probability,
        population_max,
        crossover_type,
        filename=None,
        show_debug_info=False,
        heuristic_start=None
    ) -> None:
        # setup logger
        if filename is not None:
            self.filename = filename
            self.DEBUG_INFO = show_debug_info

        self.crossover_type = crossover_type
        self.population = list()  # Array to hold the current population
        self.mating_pool = list()  # ArrayList which we will use for our "mating pool"
        self.generations = 0  # number of generations

        self.finished = False  # Boolean that represents whether we have finished evolving
        self.target = target  # Our Target
        self.mutation_rate = mutationRate  # Mutation Rate
        self.crossover_probability = crossover_probability  # Crossover Likelihood
        self.perfect_score = 1

        # save all other positions values
        # 0 -> walking | 1 -> standingUp | 2 -> standing | 3 -> sittingDown
        self.all_other_position_values = other_positions

        # default variables
        self.best = type(DNA)
        self.best_fitness = 0
        self.last_best_fitness = 0
        self.best_overall_fitness = 0
        self.terminate_counter = 0

        if heuristic_start != None:
            self.population = heuristic_start
        else:
            for i in range(population_max):
                self.population.append(DNA())

    # fill the fitness array with a value for every member of the population
    def __calcFitness__(self) -> None:
        "Calculate the fitness of all members of the population"
        for dna in self.population:
            dna.calcFitness(self.target, self.all_other_position_values)

    def generate_mating_pool(self, selection_type: dict) -> None:
        """generate a mating pool with one of 3 possible selection types
        tournament_selection, rank_selection, cost_selection
        """

        if selection_type['type'] == 0:
            self.tournament_selection(selection_type['n_comparisons'])
        elif selection_type['type'] == 1:
            self.rank_selection()
        elif selection_type['type'] == 2:
            self.cost_selection()
        else:
            raise InvalidSelectionType

    # Generate a mating pool
    def tournament_selection(self, n_comparisons) -> None:
        "Implementation for Tournament Selection"

        # Clear the mating_pool
        self.mating_pool = list()

        n_mating_pool = max([100, len(self.population)])

        for j in range(n_mating_pool):
            best_idx = 0
            for i in range(n_comparisons):
                random_idx = randint(0, len(self.population)-1)
                self.population[random_idx]
                if self.population[best_idx].fitness < self.population[random_idx].fitness:
                    best_idx = random_idx
            self.mating_pool.append(self.population[best_idx])
        shuffle(self.mating_pool)

    # Generate a mating pool
    def rank_selection(self) -> None:
        "Implementation for Fitness Proportionate Selection"

        # Clear the mating_pool
        self.mating_pool = list()

        # sort the population based on fitness
        pop_sorted = sorted(self.population, key=lambda x: x.fitness)

        # rank the population of the sorted array
        ranked_dna_dict = list()
        for i, item in enumerate(pop_sorted):
            ranked_dna_dict.append({'rank': len(pop_sorted)-i, 'DNA': item})

        for dna_dict in ranked_dna_dict:
            for i in range(dna_dict['rank'] * 10):
                self.mating_pool.append(dna_dict['DNA'])

    # Generate a mating pool
    def cost_selection(self) -> None:
        "Implementation for Cost-based Roulette Selection"

        # Clear the mating_pool
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
    def generate(self) -> None:
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

                child = parentA.crossover(self.crossover_type, parentB)
                child.mutate(self.mutation_rate)
            except CrossoverDeniedException:
                child = DNA()

            self.population.append(child)
        self.generations += 1

    def __get_best__(self):
        return self.best

    # Compute the current most fit member of the population
    def evaluate(self) -> None:
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

        if self.best_fitness == self.last_best_fitness or (self.best_fitness - self.last_best_fitness) <= 0.01:
            self.terminate_counter += 1
        else:
            self.terminate_counter = 0

        if world_record == self.perfect_score:  # perfect score has reached
            self.finished = True

    def __isFinished__(self) -> bool:
        return self.finished

    def __getGenerations__(self) -> int:
        return self.generation

    def __str__(self) -> str:
        temp_str = ''
        for DNA in self.population:
            temp_str += f"{str(DNA)}\n"
        return temp_str

    def __print__(self) -> None:
        for DNA in self.population:
            print(DNA.__toString__())

    def __printFitness__(self) -> None:
        for dna in self.population:
            print(dna.fitness)

    def __getAverageFitness__(self) -> float:
        total = 0
        for dna in self.population:
            total += dna.fitness

        return total / len(self.population)

    def __terminate__(self) -> bool:
        if self.finished:
            return True

        if self.terminate_counter >= 50:
            return True

        if self.generations >= 1000:
            return True
        return False

    def __print_debug_info__(self, show) -> None:
        if not show:
            return
        temp_str = ''
        temp_str += f"Generation {self.generations} | Average Generation Fitness: {self.__getAverageFitness__()} | Best Fitness: {self.best_fitness} | Population Length: {len(self.population)}"

        print(temp_str)

    def __write_debug_info__(self):
        with open(self.filename, 'a') as f:
            message = ''
            message += f"Generation {self.generations} | Average Generation Fitness: {self.__getAverageFitness__()} | Best Fitness: {self.best_fitness} | Population Length: {len(self.population)}\n"

            f.write(message)


# For testing purposes
if __name__ == '__main__':
    target = Target()
    pop = Population(
        target=target.get_target(),
        other_positions=target.get_other_position_values(),
        mutationRate=0.01,
        crossover_probability=1,
        population_max=5)

    pop.__calcFitness__()
    pop.tournament_selection(3)
