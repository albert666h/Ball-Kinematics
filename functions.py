import numpy as np


def distance(pos1, pos2):
    pos3 = pos2 - pos1
    return np.sqrt(sum(pos3 * pos3))