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

    def __init__(self, Markov_matrix, adj_matrix: np.array):
        self.Markov_matrix = Markov_matrix
        self.adj_matrix = adj_matrix

    @staticmethod
    def cal_propagation_prob(pp_matrix: np.array):
        """

        :param pp_matrix: Propagation path Markov matrix in which state '0' is eliminated. Cause what we concern is
                          the head of the congestion propagation which should not interrupt(the cessation of congestion)
                          until the end of the propagation path(destination road segment).
        :return prob: Numpy.array. prob[k]denotes the probability that the head of congestion propagates from
                      road_segment_1 to road_segment_k+2
        """
        assert pp_matrix.shape[0] == pp_matrix.shape[-1], 'Propagation path matrix is not a square'
        num_road_segments = pp_matrix.shape[0]
        element = np.array([(pp_matrix[i][i + 1] / (1 - pp_matrix[i][i])) for i in range(num_road_segments - 1)])
        prob = np.cumprod(element)

        return prob

    def cal_expected_propagation_time(self, pp_matrix: np.array):
        """

        :param pp_matrix:
        :return:
        """
        assert pp_matrix.shape[0] == pp_matrix.shape[-1], 'Propagation path matrix is not a square'
        num_road_segments = pp_matrix.shape[0]

        prob = self.cal_propagation_prob(pp_matrix)

        def cal_numerator(r):
            assert r >= 2, "r must be larger than or equal to 2."
            assert r <= num_road_segments, "r can't be larger than num_road_segments(K)"
            onehot_left = np.eye(r - 1, dtype=int)[0]
            onehot_right = np.transpose(np.eye(r - 1, dtype=int)[-1])
            sub_matrix = pp_matrix[:-(num_road_segments-r+1), :-(num_road_segments-r+1)]
            identity = np.identity(r-1)
            tem = np.linalg.inv(identity - sub_matrix)
            numerator = onehot_left @ tem @ tem @ onehot_right * pp_matrix[r-2][r-1]

            return numerator
        numerator_ = np.array([cal_numerator(r) for r in range(2, num_road_segments + 1, 1)])
        assert numerator_.shape[0] == prob.shape[0], "The numerator and dominator should have the same length."
        expected_time = numerator_ / prob

        return expected_time

    def unfold(self, tree: list):
        """
        Unfold a congestion propagation tree to several propagation paths.

        :param tree: list, the 1st element is the root. i.e.[12, 1, 3, 4, 5, 6]
        :return:
        """
        congestion_propagation_paths = []
        tree_ = copy.deepcopy(tree)

        tree_matrix = np.zeros_like(self.adj_matrix)
        tree_matrix[:, tree] = 1
        tree_matrix[tree, :] = 1
        zeros = np.zeros_like(self.adj_matrix)

        adj_tree = np.where(self.adj_matrix > 0, tree_matrix, zeros)

        # ---------------------- Find Leaves ----------------------
        leaves = []
        parents = [tree[0]]

        while len(tree):
            parents_ = []
            for parent in parents:
                tree.remove(parent)
            for parent in parents:
                indicator = 0  # To indicate whether a parent has a child, it's a leaf if not.
                if len(tree):
                    for child in tree:
                        if adj_tree[parent][child] == 1:
                            parents_.append(child)
                            indicator = 1
                if indicator == 0:
                    leaves.append(parent)
            parents = copy.deepcopy(parents_)

        # ---------------------- Find Paths ----------------------

        def findAllPath(adj_ma, start, end, path=[]):
            if not path:
                path.append(start)
            if start == end:
                paths.append(path[:])
                return

            for node in [i for i, x in enumerate(adj_ma[start]) if x == 1]:
                if node not in path:
                    path.append(node)
                    findAllPath(adj_ma, node, end, path)
                    path.pop()
            return paths

        # --------------------------------------------------------
        for leaf in leaves:
            paths = []
            paths = findAllPath(adj_tree, start=tree_[0], end=leaf)
            for path in paths:
                congestion_propagation_paths.append(path)
        return congestion_propagation_paths

















