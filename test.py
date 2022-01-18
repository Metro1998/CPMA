import numpy as np


class Test(object):
    def __init__(self):
        self.route_his_overall = np.array([[[0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
                                            [0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
                                            [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1]
                                            ]])
        self.time_indi = 0
        self.num_days = 1
        self.day_seq = []
        self.max_seg = 3

    def generate_seq(self):
        """

        :return:
        """

        for i in range(self.num_days):
            self.init = [i for i, x in enumerate(self.route_his_overall[i][0]) if x == 1]
            self.begin_again(i)

        print(self.day_seq)

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


if __name__ == '__main__':
    T = Test()
    T.generate_seq()
