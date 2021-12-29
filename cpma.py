# @author Metro
# @date 2021/12/29

import numpy as np


class CPMA(object):
    """
    CPMA(Congestion Propagation Modeling Algorithm) is a model able to determine propagation probability
    and expected propagation time for each roads involved in the congestion propagation.
    """

    def __init__(self, Markov_matrix):
        self.Markov_matrix = Markov_matrix

    def cal_propagation_prob(self, pp_matrix: np.array):
        """

        :param pp_matrix: Propagation path Markov matrix in which state '0' is eliminated. Cause what we concern is
                          the head of the congestion propagation which should not interrupt(the cessation of congestion)
                          until the end of the propagation path(destination road segment).
        :return:
        """
        assert pp_matrix.shape[0] == pp_matrix.shape[-1], 'Propagation path matrix is not a square'
        num_road_segments = pp_matrix.shape[0]
        element = np.array([(pp_matrix[i][i + 1] / (1 - pp_matrix[i][i])) for i in range(num_road_segments - 1)])
        prob = np.cumprod(element)

        return prob

    def cal_expected_propagation_time(self):
        """

        :return:
        """
