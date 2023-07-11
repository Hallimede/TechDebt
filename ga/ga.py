from ga.population import Population
import numpy as np


class GA:

    def __init__(self, items_df, extrac_cost):
        self.population_size = 200
        self.mutation_rate = 0.02
        self.max_generation = 50
        self.crossover_rate = 0.8
        self.items_df = items_df
        self.extrac_cost = extrac_cost
        self.max_ic = 12 * 12.0

    def run(self, verbose=False):
        pop = Population(self.mutation_rate, self.crossover_rate, self.max_generation,
                         self.items_df, self.extrac_cost, self.max_ic)
        pop.create_initial_population(self.population_size)

        while not pop.finished:
            pop.natural_selection()
            pop.generate_population()
            pop.evaluate()
            if verbose:
                pop.print_population_status()

        return np.array(pop.best_individual.genes)
