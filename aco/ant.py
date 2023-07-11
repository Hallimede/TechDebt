import numpy as np
from eval import Evaluation


class Ant:

    def __init__(self, items_df, extrac_cost, relations):

        # Short Term Value, fitness 1
        self.stv = 0.0
        # Future Investment, fitness 2
        self.fiv = 0.0

        self.n_items = len(items_df)
        self.weights = (relations * 7 + 1)

        self.evaluation = Evaluation(items_df, extrac_cost)

        self.paths = []
        self.selected = np.zeros(self.n_items, dtype=bool)
        self.last_node = None

        self.select()

        # Implementation Cost
        self.ic = self.evaluation.calculate_ic(self.selected)

    def select(self, p=None):
        if p is None:
            next_node = np.random.randint(self.n_items)
        else:
            sub_p = p[~self.selected]
            sub_p /= sum(sub_p)
            false_indices = np.where(self.selected == False)[0]
            next_node = np.random.choice(false_indices, 1, p=sub_p)[0]

        self.selected[next_node] = True
        self.last_node = next_node

        self.paths.append(next_node)

    def explore(self, pheromone, alpha, beta, max_ic, verbose):

        while self.ic < max_ic:
            probabilities = np.zeros(self.n_items)
            for i in range(self.n_items):
                probabilities[i] = (pheromone[self.last_node][i] ** alpha) * (self.weights[self.last_node][i] ** beta)
            self.select(probabilities)
            self.ic = self.evaluation.calculate_ic(self.selected)

        self.stv, self.fiv = self.evaluation.calculate_fitness(self.selected)

    def is_greater(self, target):
        if target is None:
            return True
        # if self.stv >= 0.95 * target.stv and self.fiv >= 0.8 * target.fiv:
        if self.stv + self.fiv >= target.stv + target.fiv:
            return True
        return False
