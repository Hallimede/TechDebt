from aco.ant import Ant


class Iteration:

    def __init__(self, n_ants, items, extrac_cost, relations):
        self.n_ants = n_ants

        self.ants = [Ant(items, extrac_cost, relations) for _ in range(self.n_ants)]
        self.best_ant = None
        self.best_stv = 0.0
        self.best_fiv = 0.0

        self.ant_paths = []
        self.ant_scores = []

    def execute(self, pheromone, alpha, beta, max_ic, verbose):

        for ant in self.ants:
            ant.explore(pheromone, alpha, beta, max_ic, verbose)
            if self.best_ant is None or ant.is_greater(self.best_ant):
                self.best_stv = ant.stv
                self.best_fiv = ant.fiv
                self.best_ant = ant

            self.ant_paths.append(ant.paths)
            self.ant_scores.append(ant.stv + ant.fiv)

        if verbose:
            print(f"best_stv: {self.best_stv}")
            print(f"best_fiv: {self.best_fiv}")

        return self.best_ant

    def update_pheromone(self, pheromone, decay_rate, Q):
        pheromone *= (1 - decay_rate)
        for ant_path, ant_score in zip(self.ant_paths, self.ant_scores):
            for i in range(len(ant_path) - 1):
                pheromone[ant_path[i]][ant_path[i + 1]] += (Q * ant_score) / 10
        return pheromone
