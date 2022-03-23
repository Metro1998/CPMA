# @author Metro
# @date 2022/1/7
import csv
import heapq
import os
import numpy as np
import pandas as pd
import copy


def prep_congestion_matrix(time_particle):
    """
    Read segment.csv and congestion_segment.csv
    :return: congestion_matrix
    """
    path = './raw_data/'
    segments = list(np.array(pd.read_csv(path + 'segment.csv')).squeeze())
    if time_particle == 5:
        congestion_segments = np.array(pd.read_csv(path + 'congestion_segment_5min.csv').fillna(0)).squeeze()

    elif time_particle == 1:
        # 这边因为导出来的数据每一天只有1439行（应该只统计了0：00-23：59的数据），所以需要在每天的最后增加一行全零
        congestion_segments = np.array(pd.read_csv(path + 'congestion_segment_1min.csv').fillna(0)).squeeze()
        for i in range(4):
            congestion_segments = \
                np.insert(congestion_segments, 24 * 60 * (i + 1), np.zeros(congestion_segments.shape[1]), axis=0)
        congestion_segments = np.concatenate((congestion_segments,
                                              np.expand_dims(np.zeros(congestion_segments.shape[1]), axis=0)), axis=0)
    else:
        print('Invalid time_particle')
    congestion_matrix = np.zeros((len(congestion_segments), len(segments)))

    t = 0
    for segs in congestion_segments:
        for seg in segs:
            if seg == 0:
                pass
            else:
                congestion_matrix[t][segments.index(seg)] = 1
        t += 1

    return congestion_matrix


def prep_adj_matrix():
    """
    Read children.csv and parents.csv

    :return: adj_matrix
    """
    path = './raw_data/'
    parents = np.array(pd.read_csv(path + 'parents.csv').fillna(0)).squeeze()
    children = np.array(pd.read_csv(path + 'children.csv').fillna(0)).squeeze()
    segments = list(np.array(pd.read_csv(path + 'segment.csv')).squeeze())
    adj_matrix = np.identity(parents.shape[0])

    count = 0
    for ps in parents:
        for seg in ps:
            if seg == 0:
                pass
            else:
                adj_matrix[count][segments.index(seg)] = 1
        count += 1

    count = 0
    for cs in children:
        for seg in cs:
            if seg == 0:
                pass
            else:
                adj_matrix[count][segments.index(seg)] = 1
        count += 1

    return adj_matrix


def unfold(tree: list, adj_matrix):
    """
        Unfold a congestion propagation tree to several propagation paths.

        :param adj_matrix:
        :param tree: list, the 1st element is the root. i.e.[12, 1, 3, 4, 5, 6]
        :return:
        """
    congestion_propagation_paths = []
    tree_ = copy.deepcopy(tree)

    tree_matrix = np.zeros_like(adj_matrix)
    for i in tree:
        for j in tree:
            tree_matrix[i][j] = 1
    zeros = np.zeros_like(adj_matrix)

    adj_tree = np.where(tree_matrix > 0, adj_matrix, zeros)
    leaves = [_ for _ in tree if np.sum(adj_tree, axis=1)[_] == 2]

    """
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
                    if adj_tree[parent][child] == 1 and child not in parents_:
                        parents_.append(child)
                        indicator = 1
            if indicator == 0:
                leaves.append(parent)
        parents = copy.deepcopy(parents_)
    """

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
        for root in leaves:
            if leaf != root:
                paths = []
                paths = findAllPath(adj_tree, start=root, end=leaf)
                for path in paths:
                    congestion_propagation_paths.append(path)

    return congestion_propagation_paths


def write_into_csv(expected_propagation_time, time, time_particle):
    """
    Write the result into .csv
    :param expected_propagation_time:
    :return:
    """
    # translate keys
    path = './raw_data/'
    segments = list(np.array(pd.read_csv(path + 'segment.csv')).squeeze())
    for k, v in copy.deepcopy(expected_propagation_time).items():
        if not isinstance(k, str):
            expected_propagation_time[segments[k]] = expected_propagation_time.pop(k)

    # write
    if time_particle == 5:
        header = ['RID', 'expected_propagation_time(*5min)']
        data = [{'RID': k, 'expected_propagation_time(*5min)': 5 * v} for k, v in expected_propagation_time.items()]
        with open('./result/expected_time_at{}_{}min.csv'.format(time, time_particle), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)

    elif time_particle == 1:
        header = ['RID', 'expected_propagation_time(*1min)']
        data = [{'RID': k, 'expected_propagation_time(*1min)': v} for k, v in expected_propagation_time.items()]
        with open('./result/expected_time_at{}_{}min.csv'.format(time, time_particle), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)

    else:
        print('Invalid Time_Particle')

def prep_visual_data(expected_propagation_time, time, time_particle):

    path = './raw_data/'
    segments = pd.read_csv(path + 'segment.csv')
    rid_list = pd.read_csv(path + 'rid_list.csv')
    segments = pd.merge(segments, rid_list, how='left')

    id_list = list(expected_propagation_time.keys())
    sub = segments.iloc[id_list, [0, 4]].copy()
    sub['id'] = sub.index

    visual_data = []
    for rid in sub.itertuples():
        path = rid[2].split(';')
        link = {'rid': rid[1], 'id': rid[3], 'path': path, 'loc': path[len(path) // 2],
                'proptime': round(expected_propagation_time[rid[3]] * time_particle, 2),
                'time': time, 'unit': time_particle}
        visual_data.append(link)

    visual_data = f'var data = ' + str(visual_data) + ';\n'
    with open('./result/congestion_prop.js', 'w') as file:
        file.write(visual_data)



if __name__ == '__main__':
    prep_adj_matrix()
