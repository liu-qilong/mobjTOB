""" works on git checkpoint:  """
import numpy as np
from manim import *
from manim.utils.color import Colors
from manim.utils.file_ops import open_file as open_media_file

from concept import linear_algebra
from behavior import utils, format


class Embedding(ThreeDScene):
    def construct(self):
        front_color = BLACK
        back_color = WHITE
        self.camera.background_color = back_color

        arrow = Arrow(start=UP, end=DOWN, color=GOLD)
        arrow_text = Text('Word Embedding', color=GOLD).next_to(arrow, RIGHT).scale(0.8)

        text = linear_algebra.Matrix_Box_2d(
            array=utils.vector_to_row(np.array(('I', 'have', 'a', 'car'))),
            color_fill=back_color,
            color_border=back_color
        ).next_to(arrow, UP)

        embedding = linear_algebra.Matrix_Box_Heat_2d(
            array=np.array(
                ((0.6, 0.9, 0.1),
                 (0.5, 0.8, -0.1),
                 (0.7, -0.1, 0.4),
                 (-0.8, -0.4, -0.5))
            ).T,
            color_fill=Colors.green_e.value,
        ).next_to(arrow, DOWN)
        embedding.lighten_all()

        whole = format.centralize(text, arrow, arrow_text, embedding).scale(0.5)

        self.add(whole)

        select = SurroundingRectangle(
            text.texts['(0, 0)'], color=GOLD
        )
        self.add(select)
        for idx in range(4):
            embedding.highlight_columns((idx,))
            select.become(
                SurroundingRectangle(
                    text.texts['(0, {})'.format(idx)], color=GOLD
                ))
            self.wait()


class Embedding_Space_Similarity(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=2)

        axes_range = [-1, 1, 0.2]
        axes = ThreeDAxes(
            x_range=axes_range, y_range=axes_range, z_range=axes_range,
            x_length=8.5, y_length=8.5,
            tips=False
        )

        group1 = VGroup()
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0.1, 0.8, 0.8), text='plane'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0, 0.8, 0.9), text='drone'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (-0.1, 0.8, 0.7), text='rocket'))
        for obj in group1.submobjects:
            obj.add_line_to_origin()

        group2 = VGroup()
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, 0.1, 0.8), text='goose', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, 0, 0.9), text='eagle', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, -0.1, 0.7), text='bee', color_dot=BLUE))
        for obj in group2.submobjects:
            obj.add_line_to_origin()

        self.add(axes, group1, group2)
        self.wait(1)


class Embedding_Space_Relationship(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=2)

        axes_range = [-1, 1, 0.2]
        axes = ThreeDAxes(
            x_range=axes_range, y_range=axes_range, z_range=axes_range,
            x_length=8.5, y_length=8.5,
            tips=False
        )

        group1 = VGroup()
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0.2, 0.8, 0.8), text='man'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0, 0.8, 0.9), text='king'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (-0.2, 0.8, 0.7), text='actor'))

        group2 = VGroup()
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, 0.1, 0.5), text='woman', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.6, 0.1, 0.6), text='queen', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.4, 0.1, 0.4), text='actress', color_dot=BLUE))

        links = VGroup()
        for idx in range(len(group2.submobjects)):
            links.add(
                group1.submobjects[idx].connect(
                    group2.submobjects[idx]
                )
            )

        self.add(axes, group1, group2, links)
        self.wait(1)


if __name__ == '__main__':
    scenes = (
        Embedding(),
        Embedding_Space_Similarity(),
        Embedding_Space_Relationship(),
    )

    for scene in scenes:
        scene.render(preview=True)