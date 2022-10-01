import numpy as np
from manim import *


class Matrix_Box_2d(VGroup):
    def __init__(
            self,
            init_len=1.5,
            array=np.array((0, 0, 0)),
            color_fill=GREEN_B,
            color_border=BLACK,
            color_text=BLACK,
            **kwargs
    ):
        super(VGroup, self).__init__(**kwargs)

        self.init_len = init_len
        self.array = array
        self.color_fill = color_fill
        self.color_border = color_border
        self.color_text = color_text

        self.boxes = {}
        self.texts = {}

        for index, value in np.ndenumerate(self.array):
            rec = self.create_rec(index, value)
            text = self.create_text(index, value)

            self.add(rec, text)
            self.boxes[str(index)] = rec
            self.texts[str(index)] = text

    def index_to_pos(self, index):
        # with this coordinates transformation, the vector/matrix looks just the same as its numpy arrangement
        coord_t = np.array(
            ((0, 1, 0),
             (-1, 0, 0),
             (0, 0, 1))
        ).T
        pos = np.pad(index, (0, 3 - len(index)), 'constant', constant_values=0)  # fill zeros to creat 3d pos
        pos = np.matmul(pos, coord_t) * self.init_len  # coordinates transformation: (Tx)^T = x^T T^T
        return pos

    def create_rec(self, index, value):
        pos = self.index_to_pos(index)
        rec = Rectangle(
            fill_color=self.color_fill,
            stroke_color=self.color_border,
            stroke_width=1,
            fill_opacity=1,
            height=self.init_len,
            width=self.init_len
        ).shift(pos)
        return rec

    def create_text(self, index, value):
        pos = self.index_to_pos(index)
        text = Text(
            str(value), color=self.color_text
        ).shift(pos)
        return text

    def lighten_cell(self, index, opacity=0.2):
        self.texts[str(index)].set_opacity(opacity)
        self.boxes[str(index)].set_opacity(opacity)

    def cancel_lighten_cell(self, index, value):
        origin_pos = self.texts[str(index)].get_center()
        scale_rate = self.boxes[str(index)].height / self.init_len
        new_text = self.create_text(index, value)
        new_box = self.create_rec(index, value)
        self.texts[str(index)].become(
            new_text.move_to(origin_pos).scale(scale_rate)
        )
        self.boxes[str(index)].become(
            new_box.move_to(origin_pos).scale(scale_rate)
        )

    def highlight_rows(self, rows, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            if index[0] not in rows:
                self.lighten_cell(index, opacity)
            else:
                self.cancel_lighten_cell(index, value)

    def highlight_columns(self, columns, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            if index[1] not in columns:
                self.lighten_cell(index, opacity)
            else:
                self.cancel_lighten_cell(index, value)

    def lighten_all(self, opacity=0.2):
        self.highlight_columns(list(), opacity)

    def cancel_lighten_all(self, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            self.cancel_lighten_cell(index, value)


class Matrix_Box_Heat_2d(Matrix_Box_2d):
    def heat_map(self, value):
        # map value to (0, 1)
        value_max = self.array.max()
        value_min = self.array.min() - 1  # make sure that the smallest one still have some color
        return (value - value_min) / (value_max - value_min)

    def create_rec(self, index, value):
        pos = self.index_to_pos(index)
        rec = Rectangle(
            fill_color=self.color_fill,
            stroke_color=self.color_border,
            stroke_width=1,
            fill_opacity=self.heat_map(value),
            height=self.init_len,
            width=self.init_len
        ).shift(pos)

        return rec


class Dot_with_Label_3d(VGroup):
    def __init__(
            self,
            axes,
            coord,
            text=None,
            color_dot=GOLD,
            dot_radius=0.05,
            **kwargs):
        super(VGroup, self).__init__(**kwargs)
        self.axes = axes
        self.coord = coord
        self.text = text
        self.color_dot = color_dot
        self.dot_radius = dot_radius

        self.pos = self.coords_to_point(self.coord)
        self.dot = Dot3D(self.pos, color=self.color_dot, radius=self.dot_radius)
        self.label = Text(str(self.text), color=self.color_dot, font_size=20)\
            .next_to(self.dot, OUT)
        self.add(self.dot, self.label)

    def coords_to_point(self, coord):
        return self.axes.coords_to_point(*coord)

    def add_line_to_origin(self, color_line=GRAY):
        self.line_to_origin = Line3D(
            self.coords_to_point(ORIGIN),
            self.pos,
            thickness=0,
            color=color_line
        )
        self.add(self.line_to_origin)

    def add_line_grid(self, color_line=GRAY):
        line_h = Line3D(
            (self.pos[0], self.pos[1], 0),
            self.pos,
            thickness=0,
            color=color_line
        )
        line_hx = Line3D(
            (self.pos[0], self.pos[1], 0),
            (self.pos[0], 0, 0),
            thickness=0,
            color=color_line
        )
        line_hy = Line3D(
            (self.pos[0], self.pos[1], 0),
            (0, self.pos[1], 0),
            thickness=0,
            color=color_line
        )
        self.line_grid = VGroup(line_h, line_hx, line_hy)
        self.add(self.line_grid)

    def connect(self, dot2, color_line=GRAY):
        return Line3D(
            self.pos,
            dot2.pos,
            thickness=0,
            color=color_line)