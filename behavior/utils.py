import numpy as np


def vector_to_row(array):
    array = np.expand_dims(
        np.array(array),
        axis=0
    )
    return array