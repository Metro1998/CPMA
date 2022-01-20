from utilities import *
from cpma import CPMA
from transition import Transition

if __name__ == '__main__':
    congestion_matrix_over_all = prep_congestion_matrix()
    adj_matrix = prep_adj_matrix()
    paths = unfold(tree=[64, 48, 39, 49, 65], adj_matrix=adj_matrix)
    print('from tree = [64, 48, 39, 49, 65] \n to paths =', paths)

    tran = Transition(congestion_matrix=congestion_matrix_over_all, num_days=5)
    for path in paths:
        tran.extract_history(path, time=228)
        days_seq = tran.generate_seq()
        transition_matrix = tran.construct_transition_matrix(days_seq)
        tran.clear()

        cmpa = CPMA(transition_matrix)
        prob = cmpa.cal_propagation_prob()
        print('propagation probability:\n', prob, '\n')
        expected_time = cmpa.cal_expected_propagation_time()
        print('expected propagation time (*5min):\n', expected_time, '\n')




