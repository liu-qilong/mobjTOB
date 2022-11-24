""" works on git checkpoint: 8b50fe7267b5ac2a1b835f955f0b17a55ace4eb1 """

import sys
sys.path.insert(0, '../mobjTOB')

from manim import *
from concept import polieco
from behavior import format

class Scene1(MovingCameraScene):

    def construct(self):
        i_r = polieco.ValueGroup(values=[4000, 1000, 1000],
                                 value_types=['asset', 'money', 'money'],
                                 width_scales=[500, 500, 500],
                                 mat_tags=['I_c', 'I_v', 'I_m'])
        i_l = polieco.Value(6000, width_scale=500, value_type='asset', mat_tag='I').next_to(i_r, DOWN)
        format.centralize(i_r, i_l)

        self.play(FadeIn(i_r, i_l))
        self.wait()

        i_l_d = i_l.sub_values_devide(values=[4000, 2000],
                                      value_types=['asset', 'asset'],
                                      width_scales=[500, 500])
        self.play(FadeTransform(i_l, i_l_d))
        self.wait()

        self.play(FadeOut(i_r.value_mobjs[0],
                          i_l_d.value_mobjs[0]))