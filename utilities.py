# @author Metro
# @date 2022/1/7


import heapq
import os
import numpy as np
import pandas as pd

def preprocess():
    path = './raw_data/'
    segments = list(np.array(pd.read_csv(path + 'segment.csv')).squeeze())
    congestion_segments = np.array(pd.read_csv(path + 'congestion_segment.csv').fillna(0)).squeeze()
    congestion_matrix = np.zeros((len(congestion_segments), len(segments)))

    time_indicate = 0
    for sgts in congestion_segments:
        for sgt in sgts:
            if sgt == 0:
                pass
            else:
                congestion_matrix[time_indicate][segments.index(sgt)] = 1
        time_indicate += 1

    print(congestion_matrix)



if __name__ == '__main__':
    preprocess()
