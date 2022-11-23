import numpy as np
from manim import *


def vector_to_row(array):
    array = np.expand_dims(
        np.array(array),
        axis=0
    )
    return array


def vectors_3d_angle(array1, array2):
    axis = np.cross(array1, array2)
    cos = np.dot(array1, array2) / (np.linalg.norm(array1) * np.linalg.norm(array2))
    angle = np.arccos(cos)
    return angle, axis


if __name__ == "__main__":
    pass