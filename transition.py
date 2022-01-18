# @author Metro
# @date 2022/1/18

import numpy as np
from utilities import *


class Transition(object):
    """

    """

    def __init__(self, congestion_matrix, num_days=5):
        self.congestion_matrix = congestion_matrix
        self.route_his_overall = []
        self.num_days = num_days
        self.time_indi = 0
        self.max_seg = 0
        self.max_time = 11
        self.day_seq = []
        self.days_seq = []
        self.init = []

    def extract_history(self, route: list, time: int):
        """

        :param num_days:
        :param time: Time(in min) of a day divided by 5(min), i.e. 24 means 2:00
        :param route:
        :return:
        """
        assert len(route) > 1, 'The length of the route must be larger than 1'
        assert 0 <= time <= 276, 'The time must be confined in [0, 276]'

        for i in range(self.num_days):
            route_his = np.expand_dims(self.congestion_matrix[:, route[0]], axis=0)
            route.pop(0)
            for road_seg in route:
                route_his = np.concatenate(
                    (route_his, np.expand_dims(self.congestion_matrix[time:time + 12, road_seg], axis=0)), axis=0)
            self.route_his_overall.append(route_his)
        self.max_seg = np.array(self.route_his_overall).shape[1]

    def generate_seq(self):
        """

        :return:
        """

        for i in range(self.num_days):
            self.init = [i for i, x in enumerate(self.route_his_overall[i][0]) if x == 1]
            self.begin_again(i)

        self.days_seq.append(self.day_seq)

    def begin_again(self, day_th):
        t = self.init[0]
        self.init.pop(0)
        self.day_seq.append(0)

        self.search(day_th, 0, t)

    def search(self, day_th, seg_th, t_th):
        print(self.day_seq)
        # -------- 结束或重新开始的条件 ---------
        if seg_th >= self.max_seg - 1:
            if len(self.init) > 0:
                # 当搜索完所有路径之后重新开始
                self.begin_again(day_th)
            else:
                pass

        elif t_th >= 11:
            # 当时间步大于11，跳出搜索
            pass

        # --------- 接下来就是正常的判断 ----------
        else:
            if self.route_his_overall[day_th][seg_th + 1][t_th + 1] == 1:
                print('传播')
                self.day_seq.append(seg_th + 1)
                t_th += 1
                seg_th += 1
                self.search(day_th, seg_th, t_th)

            else:
                if self.route_his_overall[day_th][seg_th][t_th + 1] == 1:
                    print('驻留')
                    self.day_seq.append(seg_th)
                    t_th += 1
                    # 延续的拥堵不认为是新的拥堵产生
                    if seg_th == 0:
                        self.init.pop(0)
                    self.search(day_th, seg_th, t_th)

                else:
                    print('重新开始')
                    self.day_seq.append(-1)
                    # 当拥堵消散且没有传播出去，重新开始
                    if len(self.init) > 0:
                        self.begin_again(day_th)

