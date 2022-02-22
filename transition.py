# @author Metro
# @date 2022/1/18

import numpy as np
from utilities import *


class Transition(object):
    """
    From the congestion state history, extract the transition matrix.

    """

    def __init__(self, congestion_matrix, num_days=5):
        self.congestion_matrix = congestion_matrix
        self.path_his_overall = []
        self.num_days = num_days
        self.time_indi = 0
        self.num_segs = 0
        self.max_time = 11
        self.day_seq = []
        self.init = []

    def extract_history(self, path: list, time: int, time_particle: int):
        """
        According to the route, extract the state history, for 1 hour for specific.

        :param time_particle:
        :param time: Time(in min) of a day. i.e. 120 means 2:00 in a.m.
        :param path:
        :return:
        """
        assert len(path) > 1, 'The length of the route must be larger than 1'
        assert 0 <= time <= 1440, 'The time must be confined in [0, 1440]'
        # review 1 hour ahead in the history(self.num_days)
        interval = int(60 / time_particle)
        time = int(time / time_particle)

        for i in range(self.num_days):
            path_ = copy.deepcopy(path)
            path_his = np.expand_dims(self.congestion_matrix[time:time + interval, path_[0]], axis=0)
            path_.pop(0)
            for road_seg in path_:
                path_his = np.concatenate(
                    (path_his, np.expand_dims(self.congestion_matrix[time:time + interval, road_seg], axis=0)), axis=0)
            time += interval * 24
            self.path_his_overall.append(path_his)
        self.num_segs = len(path)

    def generate_seq(self):
        """

        :return:
        """
        days_seq = []
        for j in range(self.num_days):
            self.day_seq.clear()
            self.init = [i for i, x in enumerate(self.path_his_overall[j][0]) if x == 1]
            if len(self.init) == 0:  # Enforce
                self.init = [1]
            self.begin_again(j)
            tem = copy.deepcopy(self.day_seq)
            days_seq.append(tem)
            print('day', j, 'path_seq = ', tem, '\n')

        return days_seq

    def begin_again(self, day_th):
        t = self.init[0]
        self.init.pop(0)
        self.day_seq.append(0)

        self.search(day_th, 0, t)

    def search(self, day_th, seg_th, t_th):
        # -------- 结束或重新开始的条件 ---------
        if seg_th >= self.num_segs - 1:
            if len(self.init) > 0:
                # 当搜索完所有路径之后重新开始
                self.begin_again(day_th)
            else:
                pass

        elif t_th >= 60/5 - 1:
            # 当时间步大于11，跳出搜索
            pass

        # --------- 接下来就是正常的判断 ----------
        else:
            if self.path_his_overall[day_th][seg_th + 1][t_th + 1] == 1:
                self.day_seq.append(seg_th + 1)
                t_th += 1
                seg_th += 1
                self.search(day_th, seg_th, t_th)

            else:
                if self.path_his_overall[day_th][seg_th][t_th + 1] == 1:
                    self.day_seq.append(seg_th)
                    t_th += 1
                    # 延续的拥堵不认为是新的拥堵产生
                    if seg_th == 0:
                        self.init.pop(0)
                    self.search(day_th, seg_th, t_th)

                else:
                    self.day_seq.append(-1)
                    # 当拥堵消散且没有传播出去，重新开始
                    if len(self.init) > 0:
                        self.begin_again(day_th)

    def construct_transition_matrix(self, days_seq):
        count_matrix_over_all = np.zeros((self.num_segs, self.num_segs + 1))
        for day_seq in days_seq:
            count_matrix = np.zeros((self.num_segs, self.num_segs + 1))
            # Initialization
            idx = 0
            while idx < len(day_seq) - 1:
                # 如果当前就是消散状态，跳过
                if day_seq[idx] == -1:
                    pass
                else:
                    # 拥堵驻留
                    if day_seq[idx] == day_seq[idx + 1]:
                        count_matrix[day_seq[idx]][day_seq[idx]] += 1
                    # 拥堵传播
                    if day_seq[idx] == day_seq[idx + 1] - 1:
                        count_matrix[day_seq[idx]][day_seq[idx] + 1] += 1
                    # 拥堵消散
                    if day_seq[idx + 1] == -1:
                        count_matrix[day_seq[idx]][-1] += 1

                idx += 1

            count_matrix_over_all += count_matrix

        transition_matrix = np.zeros((self.num_segs, self.num_segs))
        division = np.sum(count_matrix_over_all, axis=1)
        division = [1 if i == 0 else i for i in division]  # avoid zero

        for i in range(self.num_segs - 1):
            transition_matrix[i][i] = count_matrix_over_all[i][i] / division[i]
            transition_matrix[i][i + 1] = count_matrix_over_all[i][i + 1] / division[i]

        print('transition_matrix:\n', transition_matrix, '\n')
        return transition_matrix

    def clear(self):
        self.path_his_overall.clear()

