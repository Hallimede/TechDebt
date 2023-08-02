from ga.individual import Individual
import random


class Population:

    def __init__(self, mutation_rate, crossover_rate, max_generation, items_df, extrac_cost, max_ic):
        self.population = []
        self.generation = 0
        self.max_generation = max_generation
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.best_individual = None
        self.finished = False
        self.perfect_score = 1.0
        self.mating_pool = []
        self.items_df = items_df
        self.extrac_cost = extrac_cost
        self.max_ic = max_ic

    def create_initial_population(self, population_size):
        for i in range(population_size):
            ind = Individual(self.items_df, self.extrac_cost, self.max_ic)
            ind.generate_random_genes()

            if ind.is_greater(self.best_individual):
                self.best_individual = ind

            self.population.append(ind)

    def natural_selection(self):
        self.mating_pool = []

        for index, ind in enumerate(self.population):
            prob = int(round(ind.fitness * 100))
            self.mating_pool.extend([index for i in range(prob)])

    def generate_population(self):
        new_population = []
        pop_size = len(self.population)

        # n_elites = round((1 - self.crossover_rate) * pop_size)
        # elites = sorted(self.population, key=lambda ind: ind.fitness, reverse=True)[:n_elites]
        # new_population.extend(elites)

        for i in range(pop_size):
            partner_a, partner_b = self.selection()
            offspring = partner_a.crossover(partner_b)
            new_population.append(offspring)

        for new_ind in new_population:
            new_ind.mutate(self.mutation_rate)

        self.population = new_population
        self.generation += 1

    def selection(self):
        pool_length = len(self.mating_pool)

        i_partner_a = random.randint(0, pool_length - 1)
        i_partner_b = random.randint(0, pool_length - 1)

        i_partner_a = self.mating_pool[i_partner_a]
        i_partner_b = self.mating_pool[i_partner_b]

        return self.population[i_partner_a], self.population[i_partner_b]

    def evaluate(self):
        for ind in self.population:
            if ind.is_greater(self.best_individual):
                self.best_individual = ind

        if self.generation == self.max_generation:
            self.finished = True

    def print_population_status(self):
        print("\nGeneration: " + str(self.generation))
        print("Best individual: " + str(self.best_individual.stv) + ',' + str(self.best_individual.fiv))

    def print_best_individual(self):
        print("Best individual: ")
        self.best_individual.calculate_results()
