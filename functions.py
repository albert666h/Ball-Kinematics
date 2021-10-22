import numpy as np


def distance(pos1, pos2):
    pos3 = pos2 - pos1
    return np.sqrt(sum(pos3 * pos3))


def angle(pos1, pos2):
    d = distance(pos1, pos2)
    res = np.arccos((pos2[0] - pos1[0]) / d) * 180 / np.pi
    if pos1[1] < pos2[1]:
        res = 360 - res
    return res
