from utilities import *
from cpma import CPMA
from transition import Transition

if __name__ == '__main__':
    congestion_matrix_over_all = prep_congestion_matrix()
    adj_matrix = prep_adj_matrix()
    paths = unfold(tree=[64, 48, 39, 49, 65], adj_matrix=adj_matrix)

    tran = Transition(congestion_matrix=congestion_matrix_over_all, num_days=5)
    for path in paths:
        tran.extract_history(path, time=228)
        tran.generate_seq()
        transition_matrix = tran.construct_transition_matrix()
        tran.clear()
        print(transition_matrix)


