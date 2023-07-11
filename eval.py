import numpy as np
import math


class Evaluation:

    def __init__(self, items_df, extrac_cost):
        self.items_df = items_df
        self.n_items = len(items_df)
        self.n_features = len(items_df[items_df['Type'] == 'Feature'])
        self.cost_and_value = items_df.values[:, 5:7]
        self.extrac_cost = extrac_cost

    def calculate_ic(self, selected):
        ic = np.dot(selected, self.cost_and_value[:, 0])

        features_selected = selected[:self.n_features]
        debts_selected = selected[self.n_features:]
        filtered_extra_cost = self.extrac_cost[:self.n_features, ~debts_selected]

        ic += np.dot(features_selected.reshape(-1, 1).T, filtered_extra_cost).sum()
        return ic

    def calculate_fitness(self, selected):
        debts_selected = selected[self.n_features:]
        features_selected = selected[:self.n_features]

        stv = np.dot(features_selected, self.cost_and_value[:self.n_features, 1])
        fiv = np.dot(debts_selected, self.cost_and_value[self.n_features:, 1])

        filtered_extra_cost = self.extrac_cost[:self.n_features, debts_selected]
        fiv += np.dot((~features_selected).reshape(-1, 1).T, filtered_extra_cost).sum()
        return stv, fiv

    def calculate_entropy(self, selected):
        n_features_selected = np.sum(selected[:self.n_features])
        pre_epic = self.items_df.loc[0]['Epic']
        pre_selected = 0
        pre_epic_total = 0
        tmp = 1
        for i in range(self.n_features + 1):
            if self.items_df.loc[i]['Epic'] != pre_epic:
                tmp *= math.comb(pre_epic_total, pre_selected)
                pre_selected = 0
                pre_epic_total = 0
                pre_epic = self.items_df.loc[i]['Epic']

            pre_epic_total += 1
            if selected[i]:
                pre_selected += 1

        p = tmp / math.comb(self.n_features, n_features_selected)
        return - p * math.log2(p)

    def export_report(self, selected, method, filename):

        # ic = self.calculate_ic(selected)
        stv, fiv = self.calculate_fitness(selected)
        entropy = self.calculate_entropy(selected)

        html = '<div style="margin: 20px 8px;">'
        html += f'<h1 style="font-weight: bold; margin: 4px;">{method}</h1>'
        html += '<table style="border-spacing: 24px 2px;">'
        # html += f'<tr><td>Implementation Cost (IC)</td><td>{ic}</td>'
        html += f'<tr><td>Fitness</td><td>{stv + fiv}</td>'
        html += f'<tr><td>Short Term Value (STV)</td><td>{stv}</td>'
        html += f'<tr><td>Future Investment Value (FIV)  </td><td>{fiv}</td>'
        html += f'<tr><td>Selection Entropy</td><td>{entropy}</td>'
        html += f'</table></div>'

        styler = self.items_df.style.apply(
            lambda x: ['background: lightblue' if selected[i] else '' for i in range(len(x))])

        html += styler.to_html(escape=False, index=False)
        with open(filename, 'w') as f:
            f.write(html)
