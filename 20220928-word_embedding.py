""" works on git checkpoint: 114ffc5334b87bf402d8e56bc2a9e27e97b6e400 """
from manim import *
from manim.utils.color import Colors

from concept import linear_algebra
from behavior import utils, format


class Embedding(Scene):
    def construct(self):
        arrow = Arrow(start=UP, end=DOWN, color=GOLD)
        arrow_text = Text('Word Embedding', color=GOLD).next_to(arrow, RIGHT).scale(0.8)

        text = linear_algebra.Matrix_Box_2d(
            array=utils.vector_to_row(np.array(('I', 'have', 'a', 'car'))),
            color_fill=GRAY_A,
            # color_border=GRAY_A
        ).next_to(arrow, UP)

        embedding = linear_algebra.Matrix_Box_Heat_2d(
            array=np.array(
                ((0.6, 0.9, 0.9),
                 (-0.5, 0.8, 0.9),
                 (0.7, -0.8, 0.4),
                 (0.8, 0.4, 0.5))
            ).T,
            color_fill=Colors.green_e.value,
        ).next_to(arrow, DOWN)
        embedding.highlight_columns((0,))

        # init animation
        whole = format.centralize(text, arrow, arrow_text, embedding).scale(1.5)
        select = SurroundingRectangle(
            text.boxes['(0, 0)'], color=GOLD
        )
        self.add(whole, select)

        # following animations
        for idx in range(1, 4):
            self.play(select.animate.become(
                SurroundingRectangle(
                    text.boxes['(0, {})'.format(idx)], color=GOLD
                ))
            )
            embedding.highlight_columns((idx,))

        self.wait()


class Embedding_Space_Similarity(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes_range = [-1.5, 1.5, 0.5]
        axes = ThreeDAxes(
            x_range=axes_range, y_range=axes_range, z_range=axes_range,
            x_length=10, y_length=10, z_length=10,
            tips=False
        )
        grid = NumberPlane(
            x_range=axes_range, y_range=axes_range,
            x_length=10, y_length=10
        )

        group1 = VGroup()
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0.1, 0.8, 0.8), text='plane'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0, 0.8, 0.9), text='drone'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (-0.1, 0.8, 0.7), text='rocket'))
        for obj in group1.submobjects:
            obj.add_line_to_origin()
            self.add_fixed_orientation_mobjects(obj.label)

        group2 = VGroup()
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, 0.1, 0.8), text='goose', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, 0, 0.9), text='eagle', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, -0.1, 0.7), text='bee', color_dot=BLUE))
        for obj in group2.submobjects:
            obj.add_line_to_origin()
            self.add_fixed_orientation_mobjects(obj.label)

        self.add(axes, grid, group1, group2)
        self.move_camera(theta=90 * DEGREES, run_time=1)


class Embedding_Space_Relationship(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes_range = [-1.5, 1.5, 0.5]
        axes = ThreeDAxes(
            x_range=axes_range, y_range=axes_range, z_range=axes_range,
            x_length=10, y_length=10, z_length=10,
            tips=False
        )
        grid = NumberPlane(
            x_range=axes_range, y_range=axes_range,
            x_length=10, y_length=10
        )

        group1 = VGroup()
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0.2, 0.8, 0.8), text='man'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (0, 0.8, 0.9), text='king'))
        group1.add(linear_algebra.Dot_with_Label_3d(axes, (-0.2, 0.8, 0.7), text='actor'))
        for obj in group1.submobjects:
            self.add_fixed_orientation_mobjects(obj.label)

        group2 = VGroup()
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.8, 0.1, 0.5), text='woman', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.6, 0.1, 0.6), text='queen', color_dot=BLUE))
        group2.add(linear_algebra.Dot_with_Label_3d(axes, (0.4, 0.1, 0.4), text='actress', color_dot=BLUE))
        for obj in group2.submobjects:
            self.add_fixed_orientation_mobjects(obj.label)

        links = VGroup()
        for idx in range(len(group2.submobjects)):
            links.add(
                linear_algebra.connect_dot_with_label(
                    group1.submobjects[idx],
                    group2.submobjects[idx]
                )
            )

        self.add(axes, grid, group1, group2, links)
        self.move_camera(theta=90 * DEGREES, run_time=1)


if __name__ == '__main__':
    with tempconfig({
        "format": "png",
        "transparent": True,
        "output_file": "manim-",
        "zero_pad": False,
        "frame_rate": 1,
        "pixel_width": 1024,
        "pixel_height": 1024,
        "preview": True,
    }):
        scenes = (
            Embedding(),
        )

        for scene in scenes:
            scene.render()

    with tempconfig({
        "format": "png",
        #"transparent": True,
        "output_file": "manim-",
        "zero_pad": False,
        "frame_rate": 1,
        "pixel_width": 1024,
        "pixel_height": 1024,
        "preview": True,
    }):
        scenes = (
            Embedding_Space_Similarity(),
            Embedding_Space_Relationship(),
        )

        for scene in scenes:
            scene.render()