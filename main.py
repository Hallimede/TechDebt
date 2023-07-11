import time

from aco.aco import ACO
from eval import Evaluation
from ga.ga import GA
import pandas as pd
import numpy as np


if __name__ == '__main__':

    file = pd.ExcelFile('sem.xlsx')
    items_df = file.parse('Sheet1')

    extrac_cost = items_df.values[:, 7:]

    relation_df = file.parse('Sheet3')
    relations = relation_df.values[:, 1:]
    items_df = items_df[['Type', 'Epic', 'Epic_Name', 'No', 'Name', 'Cost', 'Value']]

    evaluation = Evaluation(items_df, extrac_cost)

    ga = GA(items_df, extrac_cost)
    # res = ga.run(verbose=True)
    res = ga.run()

    print('\nGA Entropy:', evaluation.calculate_entropy(res))
    print('GA SIV,FIV:', evaluation.calculate_fitness(res))
    evaluation.export_report(res, 'Genetic Algorithm', 'report/ga_output.html')

    aco = ACO(items_df, extrac_cost, relations)
    # res = aco.run(verbose=True)
    res = aco.run()

    print('\nACO Entropy:', evaluation.calculate_entropy(res))
    print('ACO SIV,FIV:', evaluation.calculate_fitness(res))
    evaluation.export_report(res, 'Ant Colony Optimization', 'report/aco_output.html')
    n_node = np.sum(res)
    arr = np.concatenate((np.ones(n_node, dtype=bool), np.zeros(len(items_df) - n_node, dtype=bool)))
    np.random.shuffle(arr)

    print('\nRAND Entropy:', evaluation.calculate_entropy(arr))
    print('RAND SIV,FIV:', evaluation.calculate_fitness(arr))
    evaluation.export_report(arr, 'Random Selection', 'report/rand_output.html')
