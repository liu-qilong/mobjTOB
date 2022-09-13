from manim import *


def centralize(*vmobjects):
    vmobj = VGroup(*vmobjects)
    vmobj.move_to(ORIGIN)
    return vmobj
