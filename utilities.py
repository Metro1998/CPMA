# @author Metro
# @date 2022/1/7


import heapq
import os
import numpy as np
import pandas as pd


def convert_rid_2_idx(rid, segment_dict):
    idx = []
    for i in range(len(rid)):
        temp_list = []
        for j in range(len(rid[i])):
            if rid[i][j] != 0:
                temp_list.append(segment_dict[rid[i][j]])
            else:
                break
        idx.append(list(set(temp_list)))
    return idx


def preprocess():
    path = './nostop_speed_SRI/'
    segment = np.array(pd.read_csv(path + 'segment_csv')).squeeze()
    idx = np.arange(len(segment))
    segment_dict = dict(zip(segment, idx))

    longs = np.array(pd.read_csv(path + "longs.csv"))
    lats = np.array(pd.read_csv(path + "lats.csv"))

    children = np.array(pd.read_csv(path + "children.csv").fillna(0))
    children = convert_rid_2_idx(children, segment_dict=segment_dict)
    children = np.array(children)

    parents = np.array(pd.read_csv(path + "parents.csv").fillna(0))
    parents = convert_rid_2_idx(parents, segment_dict)
    parents = np.array(parents)

    longer_pairs = np.array(pd.read_csv(path + "congestion_segment.csv").fillna(0))
    longer_pairs = convert_rid_2_idx(longer_pairs, segment_dict)
    longer_pairs = np.array(longer_pairs)
    time_removed = np.array(pd.read_csv(path + "time_removed.csv"))




if __name__ == '__main__':
    adj_matrix = np.array([[0, 2, 4, 2, 0], [2, 0, 1, 0, 3], [4, 1, 0, 5, 2],
                           [2, 0, 5, 0, 2], [0, 3, 2, 2, 0]])
    g = Graph(adjacent_matrix=adj_matrix, threshold=100, save_path=None)
    print(g.update_shortest_path_matrix())