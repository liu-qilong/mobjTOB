from manim import *
from manim.utils.color import Colors


class Value(VMobject):
    """
    将价值的概念可视化，包括表示价值量大小的矩形区域、符号说明和示意图.
    特别地，当该价值量表示预付款时，颜色为浅红色，否则为浅蓝色.
    """

    def __init__(
            self,
            value: float = 1.0,
            value_type: str = 'money',
            width_scale: float = 1.0,
            height: float = 1.0,
            mat_tag: str = '',
            **kwargs,
            ):
        self.value = value
        self.value_type = value_type
        self.width_scale = width_scale

        self.rect = Rectangle(height=height,
                              width=value / height / self.width_scale,
                              color=Colors.black.value,
                              fill_opacity=1)
        if self.value_type == 'asset':
            self.rect.set_fill(Colors.blue_e.value)
        elif self.value_type == 'money':
            self.rect.set_fill(Colors.red_e.value)

        self.value_tag = MathTex(str(self.value)).move_to(self.rect.center())
        self.rect_and_tag = VGroup(self.rect, self.value_tag)

        self.mat_tag = MathTex(mat_tag).next_to(self.rect, UP)

        super().__init__(**kwargs)
        self.add(self.rect_and_tag, self.mat_tag)

    def sub_values_devide(self,
                          values: list,
                          value_types: list = [],
                          width_scales: list = [],
                          heights: list = [],
                          mat_tags: list = [],
                          **kwargs,):
        sub_values = ValueGroup(values, value_types, width_scales, heights, mat_tags,
                                self.mat_tag.get_tex_string(), **kwargs)
        sub_values.align_to(self, LEFT)
        sub_values.align_to(self, DOWN)

        return sub_values


class ValueGroup(VMobject):
    def __init__(self,
                 values: list,
                 value_types: list = [],
                 width_scales: list = [],
                 heights: list = [],
                 mat_tags: list = [],
                 mat_tag: str = '',
                 **kwargs,
                 ):
        if value_types == []:
            value_types = ['money', ] * len(values)
        if width_scales == []:
            width_scales = [1.0, ] * len(values)
        if heights == []:
            heights = [1.0, ] * len(values)
        if mat_tags == []:
            mat_tags = ['', ] * len(values)

        value_mobjs = []
        for idx in range(len(values)):
            new_value = Value(value=values[idx],
                              value_type=value_types[idx],
                              width_scale=width_scales[idx],
                              height=heights[idx],
                              mat_tag=mat_tags[idx],
                              )
            if len(value_mobjs) > 0:
                new_value.next_to(value_mobjs[-1], RIGHT, buff=0)
            value_mobjs.append(new_value)
        self.value_mobjs = VGroup(*value_mobjs)

        self.mat_tag = MathTex(mat_tag).next_to(self.value_mobjs, UP)

        super().__init__(**kwargs)
        self.add(self.value_mobjs, self.mat_tag)

    def fade_value(self,
                   idx: int = 0):
        self.value_mobjs.remove(self.value_mobjs.submobjects[idx])
        self.mat_tag.next_to(self.value_mobjs, UP)
