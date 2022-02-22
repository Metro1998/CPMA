# @author Metro
# @date 2021/12/29

import numpy as np
import scipy
import copy


class CPMA(object):
    """
    CPMA(Congestion Propagation Modeling Algorithm) is a model able to determine propagation probability
    and expected propagation time for each roads involved in the congestion propagation.
    """

    def __init__(self, pp_matrix):
        self.pp_matrix = pp_matrix

    def cal_propagation_prob(self):
        """

        :param pp_matrix: Propagation path Markov matrix in which state '0' is eliminated. Cause what we concern is
                          the head of the congestion propagation which should not interrupt(the cessation of congestion)
                          until the end of the propagation path(destination road segment).
        :return prob: Numpy.array. prob[k]denotes the probability that the head of congestion propagates from
                      road_segment_1 to road_segment_k+2
        """
        assert self.pp_matrix.shape[0] == self.pp_matrix.shape[-1], 'Propagation path matrix is not a square'
        num_road_segments = self.pp_matrix.shape[0]
        element = np.array([(self.pp_matrix[i][i + 1] / (1 - self.pp_matrix[i][i]))
                            for i in range(num_road_segments - 1)])
        prob = np.cumprod(element)

        return prob

    def cal_expected_propagation_time(self):
        """

        :param pp_matrix:
        :return:
        """
        assert self.pp_matrix.shape[0] == self.pp_matrix.shape[-1], 'Propagation path matrix is not a square'
        num_road_segments = self.pp_matrix.shape[0]

        prob = self.cal_propagation_prob()

        def cal_numerator(r):
            assert r >= 2, "r must be larger than or equal to 2."
            assert r <= num_road_segments, "r can't be larger than num_road_segments(K)"
            onehot_left = np.eye(r - 1, dtype=int)[0]
            onehot_right = np.transpose(np.eye(r - 1, dtype=int)[-1])
            sub_matrix = self.pp_matrix[:-(num_road_segments-r+1), :-(num_road_segments-r+1)]
            identity = np.identity(r-1)
            tem = np.linalg.inv(identity - sub_matrix)
            numerator = onehot_left @ tem @ tem @ onehot_right * self.pp_matrix[r-2][r-1]

            return numerator
        numerator_ = np.array([cal_numerator(r) for r in range(2, num_road_segments + 1, 1)])
        assert numerator_.shape[0] == prob.shape[0], "The numerator and dominator should have the same length."
        expected_time = [numerator_[i] / prob[i] if numerator_[i] != 0 else 0 for i in range(len(numerator_))]
        return expected_time



















