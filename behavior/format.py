import copy
from manim import *


def centralize(*vmobjects):
    vmobj = VGroup(*vmobjects)
    vmobj.move_to(ORIGIN)
    return vmobj


def shadow_mobject(*objs, opacity=0.1):
    obj_group = VGroup(*objs)
    shadow_group = copy.deepcopy(obj_group)
    shadow_group.set_opacity(opacity)
    return shadow_group