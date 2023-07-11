from aco.iteration import Iteration
import numpy as np


class ACO:

    def __init__(self, items_df, extrac_cost, relations):

        self.n_ants = 50 # larger, more exploration
        self.max_iteration = 30
        self.cur_iteration = 1
        self.initial_pheromone = 0.5
        self.decay_rate = 0.5 # larger, more exploration
        self.alpha = 0.1 # larger, more exploitation
        self.beta = 0.5 # larger, more exploration
        self.Q = 50 # larger, more exploitation
        self.max_ic = 12 * 12.0  # 12 developers, 12 points / person

        self.items_df = items_df
        self.relations = relations
        self.extrac_cost = extrac_cost

        self.pheromone = np.full([len(items_df), len(items_df)], self.initial_pheromone)
        self.best_ant = None

    def run(self, verbose=False):
        while self.cur_iteration <= self.max_iteration:
            if verbose:
                print(f"\niteration: {self.cur_iteration}")
            iteration = Iteration(self.n_ants, self.items_df, self.extrac_cost, self.relations)
            ant = iteration.execute(self.pheromone, self.alpha, self.beta, self.max_ic, verbose)
            self.pheromone = iteration.update_pheromone(self.pheromone, self.decay_rate, self.Q)
            if self.best_ant is None or ant.is_greater(self.best_ant):
                self.best_ant = ant
            self.cur_iteration += 1

        if verbose:
            print("\nbest result")
            print(f"best_stv: {self.best_ant.stv}")
            print(f"best_fiv: {self.best_ant.fiv}")
        return self.best_ant.selected
