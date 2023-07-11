import random
import numpy as np
from eval import Evaluation


class Individual:

    def __init__(self, items_df, extrac_cost, max_ic):

        self.items_df = items_df
        self.extrac_cost = extrac_cost
        self.gene_size = len(items_df)
        self.evaluation = Evaluation(items_df, extrac_cost)
        self.max_ic = max_ic

        # Short Term Value, fitness 1
        self.stv = 0.0
        # Future Investment, fitness 2
        self.fiv = 0.0
        self.ic = 0.0
        self.fitness = 0.0
        self.genes = []

    def generate_random_genes(self):
        genes = []
        for i in range(self.gene_size):
            genes.append(random.choice([True, False]))
        self.genes = genes
        self.check_valid()

    def crossover(self, partner):
        child = Individual(self.items_df, self.extrac_cost, self.max_ic)
        midpoint = random.randint(0, self.gene_size)
        child.genes = self.genes[:midpoint] + partner.genes[midpoint:]
        child.check_valid()
        return child

    def mutate(self, mutation_rate):
        for elem in enumerate(self.genes):
            if random.uniform(0, 1) < mutation_rate:
                self.genes[elem[0]] = random.choice([True, False])

        if np.sum(self.genes) == 0:
            self.mutate(mutation_rate)
        self.check_valid()

    def check_valid(self):
        self.evaluate()
        while self.ic > self.max_ic:
            rand = random.randint(0, self.gene_size - 1)
            self.genes[rand] = False
            self.evaluate()

    def evaluate(self):
        self.ic = self.evaluation.calculate_ic(np.array(self.genes))
        self.stv, self.fiv = self.evaluation.calculate_fitness(np.array(self.genes))
        self.fitness = self.stv + self.fiv

    def is_greater(self, target):
        if target is None:
            return True
        # if self.stv >= 0.95 * target.stv and self.fiv >= 0.8 * target.fiv:
        if self.stv + self.fiv >= target.stv + target.fiv:
            return True
        return False
