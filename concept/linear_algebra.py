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
            stroke_width=0.1,
            name_size=48,
            name_buff=0.25,
            name=None,
            **kwargs
    ):
        super(VGroup, self).__init__(**kwargs)

        self.init_len = init_len
        self.color_fill = color_fill
        self.color_border = color_border
        self.color_text = color_text
        self.stroke_width = stroke_width
        self.name_size = name_size
        self.name_buff = name_buff

        self.boxes, self.texts = self.import_array(array)
        self.add(self.boxes, self.texts)

        if name is not None:
            self.name = MathTex(
                name, color=self.color_text, font_size=self.name_size
            ).next_to(self, UP, buff=self.name_buff)
            self.add(self.name)

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

    def import_array(self, array):
        self.array = array
        boxes = VDict()
        texts = VDict()

        for index, value in np.ndenumerate(self.array):
            rec = self.create_rec(index, value)
            text = self.create_text(index, value)
            boxes.add([(str(index), rec)])
            texts.add([(str(index), text)])

        return boxes, texts

    def create_rec(self, index, value):
        pos = self.index_to_pos(index)
        rec = Rectangle(
            fill_color=self.color_fill,
            stroke_color=self.color_border,
            stroke_width=self.stroke_width,
            fill_opacity=1,
            height=self.init_len,
            width=self.init_len
        ).shift(pos)
        return rec

    def create_text(self, index, value):
        pos = self.index_to_pos(index)
        text = Text(
            "{:.1f}".format(value), color=self.color_text
        ).shift(pos)
        return text

    def change_array(self, new_array, align_mode='center'):
        boxes, texts = self.import_array(new_array)

        # scale according to the unit's height
        scale_rate = self.boxes.submobjects[0].height / boxes.submobjects[0].height
        # align according to the center point or the 1st unit
        if align_mode == 'center':
            movement = self.boxes.get_center() - boxes.get_center()
        elif align_mode == '1st':
            movement = self.boxes.submobjects[0].get_center() - boxes.submobjects[0].get_center()
        else:
            movement = ORIGIN
        boxes.scale(scale_rate).shift(movement)
        texts.scale(scale_rate).shift(movement)

        self.remove(self.boxes)
        self.remove(self.texts)
        self.boxes = boxes
        self.texts = texts
        self.add(self.boxes, self.texts)

    def expand_random(self, axis=0):
        """ noted that expand the matrix will remove all the highlighting/lightening """
        expand_shape = list(self.array.shape)
        expand_shape[axis] = 1
        expand_array = np.random.rand(*expand_shape)
        new_array = np.concatenate((self.array, expand_array), axis=axis)
        self.change_array(new_array, align_mode='1st')


    def lighten_cell(self, index, opacity=0.2):
        self.texts[str(index)].set_opacity(opacity)
        self.boxes[str(index)].set_opacity(opacity)

    def cancel_lighten_cell(self, index):
        value = self.array[index]
        origin_text_pos = self.texts[str(index)].get_center()
        origin_box_pos = self.boxes[str(index)].get_center()
        scale_rate = self.boxes[str(index)].height / self.init_len
        new_text = self.create_text(index, value)
        new_box = self.create_rec(index, value)
        self.texts[str(index)].become(
            new_text.move_to(origin_text_pos).scale(scale_rate)
        )
        self.boxes[str(index)].become(
            new_box.move_to(origin_box_pos).scale(scale_rate)
        )

    def highlight_cell(self, id, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            if index != id:
                self.lighten_cell(index, opacity)
            else:
                self.cancel_lighten_cell(index)

    def highlight_rows(self, rows, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            if index[-2] not in rows:
                self.lighten_cell(index, opacity)
            else:
                self.cancel_lighten_cell(index)

    def highlight_columns(self, columns, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            if index[-1] not in columns:
                self.lighten_cell(index, opacity)
            else:
                self.cancel_lighten_cell(index)

    def cancel_lighten_rows(self, rows):
        for index, value in np.ndenumerate(self.array):
            if index[-2] in rows:
                self.cancel_lighten_cell(index)

    def cancel_lighten_columns(self, columns):
        for index, value in np.ndenumerate(self.array):
            if index[-1] in columns:
                self.cancel_lighten_cell(index)

    def lighten_all(self, opacity=0.2):
        self.highlight_columns(list(), opacity)

    def cancel_lighten_all(self, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            self.cancel_lighten_cell(index)


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
            stroke_width=self.stroke_width,
            fill_opacity=self.heat_map(value),
            height=self.init_len,
            width=self.init_len
        ).shift(pos)

        return rec


class Matrix_Box_Heat_3d(Matrix_Box_Heat_2d):
    def __init__(self, text_mode='1st', *args, **kwargs):
        self.text_mode = text_mode
        Matrix_Box_Heat_2d.__init__(self, *args, **kwargs)

    def index_to_pos(self, index):
        # with this coordinates transformation, the vector/matrix/tensor looks just the same as its numpy arrangement
        coord_t = np.array(
            ((0, 0, 1),
             (0, -1, 0),
             (-1, 0, 0))
        ).T
        pos = np.pad(index, (0, 3 - len(index)), 'constant', constant_values=0)  # fill zeros to creat 3d pos
        pos = np.matmul(pos, coord_t) * self.init_len  # coordinates transformation: (Tx)^T = x^T T^T
        return pos

    def create_rec(self, index, value):
        pos = self.index_to_pos(index)
        rec = Cube(
            fill_color=self.color_fill,
            stroke_color=self.color_border,
            stroke_width=self.stroke_width,
            fill_opacity=self.heat_map(value),
            side_length=self.init_len,
        ).shift(pos)
        return rec

    def create_text(self, index, value):
        pos = self.index_to_pos(index) + self.init_len/2 * OUT
        if (self.text_mode == '1st') and (index[-3] == 0):
            text = Text(
                "{:.1f}".format(value), color=self.color_text
            ).shift(pos)
        else:
            text = Text(
                "", color=self.color_text
            ).shift(pos)
        return text

    def lighten_cell(self, index, opacity=0.2):
        if self.text_mode == '1st' and index[-3] == 0:
            self.texts[str(index)].set_opacity(0.5)
        else:
            self.texts[str(index)].set_opacity(0)
        self.boxes[str(index)].set_opacity(opacity)

    def highlight_layers(self, rows, opacity=0.2):
        for index, value in np.ndenumerate(self.array):
            if index[-3] not in rows:
                self.lighten_cell(index, opacity)
            else:
                self.cancel_lighten_cell(index)

    def cancel_lighten_layers(self, rows):
        for index, value in np.ndenumerate(self.array):
            if index[-3] in rows:
                self.cancel_lighten_cell(index)


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
        """ adding lines may slow down rendering drastically """
        self.line_to_origin = Line3D(
            self.coords_to_point(ORIGIN),
            self.pos,
            thickness=0,
            color=color_line
        )
        self.add(self.line_to_origin)

    def add_line_grid(self, color_line=GRAY):
        """ adding lines may slow down rendering drastically """
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


def connect_dot_with_label(dot1, dot2, color_line=GRAY):
    return Line3D(
        dot1.pos,
        dot2.pos,
        thickness=0,
        color=color_line)


def averg_dot_with_label(*dots, text='averg', color_dot=GREEN):
    arr = np.array(dots[0].coord)
    for dot in dots[1:]:
        arr += np.array(dot.coord)
    arr = arr / (len(dot) + 1)

    return Dot_with_Label_3d(
        dots[0].axes,
        arr,
        text=text,
        color_dot=color_dot,
        dot_radius=dots[0].dot_radius
    )