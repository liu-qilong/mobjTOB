""" works on git checkpoint: 8b50fe7267b5ac2a1b835f955f0b17a55ace4eb1 """
import copy
import scipy
import numpy as np
from manim import *

import sys
sys.path.insert(0, '../mobjTOB')

from concept import linear_algebra
from behavior import utils, format

class Embedding_Averg_Transform(ThreeDScene):
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

        # init
        self.next_section("init", skip_animations=False)

        text_i = linear_algebra.Dot_with_Label_3d(axes, (0.6, 0.9, 0.9), text='I')
        text_have = linear_algebra.Dot_with_Label_3d(axes, (-0.5, 0.8, 0.9), text='have')
        text_a = linear_algebra.Dot_with_Label_3d(axes, (0.7, -0.8, 0.4), text='a')
        text_car = linear_algebra.Dot_with_Label_3d(axes, (0.8, 0.4, 0.5), text='car')

        original_embeddings = VDict(
            [("text_i", text_i), ("text_have", text_have), ("text_a", text_a), ("text_car", text_car)]
        )
        for obj in original_embeddings.submobjects:
            obj.add_line_to_origin()
            self.add_fixed_orientation_mobjects(obj.label)

        self.add(axes, grid, original_embeddings)
        self.wait(0.5)

        # transform
        self.next_section("deform", skip_animations=False)

        shadow_embeddings = format.shadow_mobject(text_i, text_have, text_a, text_car)
        self.add(shadow_embeddings)
        for obj in shadow_embeddings.submobjects:
            self.add_fixed_orientation_mobjects(obj.label)

        text_averg = linear_algebra.averg_dot_with_label(text_i, text_have, text_a, text_car)
        text_averg.add_line_to_origin()
        self.play(
            text_i.dot.animate.move_to(text_averg.pos),
            text_have.dot.animate.move_to(text_averg.pos),
            text_a.dot.animate.move_to(text_averg.pos),
            text_car.dot.animate.move_to(text_averg.pos),
            run_time=0.5
        )
        self.remove(original_embeddings)
        self.add(text_averg)
        self.add_fixed_orientation_mobjects(text_averg.label)
        self.wait(0.5)


class Single_Word(ThreeDScene):
    def construct(self):
        font_color = BLACK
        equations = VGroup()

        # numpy arrays
        array_W_K = np.array(
            ((0.9, 0.1, 0.2),
             (-0.1, 0.8, 0.2),
             (0.1, -0.1, 0.9))
        )
        array_x_j = np.array((0.6, 0.9, 0.9))
        array_W_Q = np.array(
            ((0.1, 0.8, -0.2),
             (0.7, -0.2, 0.1),
             (-0.3, 0.1, 0.9))
        )
        array_x_i = np.array((-0.5, 0.8, 0.9))

        array_k_j_T = utils.vector_to_row(
            np.matmul(array_W_K, array_x_j)
        )
        array_q_i = np.matmul(array_W_Q, array_x_i)

        array_z_ji = np.matmul(array_k_j_T, array_q_i)

        # first row
        coe1 = MathTex(r"\frac{1}{\sqrt{d}}(", color=font_color)
        W_K = linear_algebra.Matrix_Box_Heat(
            array=array_W_K,
            name=r"\boldsymbol{W}_K",
            color_text=font_color,
            color_fill=GOLD).next_to(coe1, RIGHT)
        x_j = linear_algebra.Matrix_Box_Heat(
            array=array_x_j,
            name=r"\boldsymbol{x}_j",
            color_text=font_color).next_to(W_K, RIGHT).align_to(W_K, DOWN)
        equations.add(coe1, W_K, x_j)
        mid1 = MathTex(r")^T \cdot (", color=font_color).next_to(x_j, RIGHT)
        W_Q = linear_algebra.Matrix_Box_Heat(
            array=array_W_Q,
            name=r"\boldsymbol{W}_Q",
            color_text=font_color,
            color_fill=GOLD).next_to(mid1, RIGHT)
        x_i = linear_algebra.Matrix_Box_Heat(
            array=array_x_i,
            name = r"\boldsymbol{x}_i",
            color_text=font_color).next_to(W_Q, RIGHT).align_to(W_Q, DOWN)
        right1 = MathTex(r")", color=font_color).next_to(x_i, RIGHT)
        equations.add(mid1, W_Q, x_i, right1)

        # second row
        coe2 = MathTex(r"= \frac{1}{\sqrt{d}}\,", color=font_color)\
            .next_to(W_K, DOWN, buff=2).align_to(coe1, RIGHT).shift(DOWN)
        k_j_T = linear_algebra.Matrix_Box_Heat(
            array=array_k_j_T,
            name=r"\boldsymbol{k}_j^T",
            color_text=font_color,
            color_fill=BLUE_E).next_to(coe2, RIGHT)
        q_i = linear_algebra.Matrix_Box_Heat(
            array=array_q_i,
            name=r"\boldsymbol{q}_i",
            color_text=font_color,
            color_fill=BLUE_E).next_to(k_j_T, RIGHT)
        equations.add(coe2, k_j_T, q_i)

        # third row
        coe3 = MathTex(r"= \frac{1}{\sqrt{d}}", color=font_color) \
            .next_to(q_i, RIGHT)
        z_ji = linear_algebra.Matrix_Box_Heat(
            array=array_z_ji,
            name=r"z_{ji}",
            color_text=font_color,
            color_fill=TEAL_E).next_to(coe3, RIGHT)
        equations.add(coe3, z_ji)

        equations.move_to(ORIGIN).scale(0.8)
        self.add(equations)


class Multiple_Words(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(2)
        font_color = BLACK
        equations = VGroup()

        # numpy arrays
        array_W_K = np.array(
            ((0.9, 0.1, 0.2),
             (-0.1, 0.8, 0.2),
             (0.1, -0.1, 0.9))
        )
        array_x = np.array(
            ((0.6, 0.9, 0.9),
             (-0.5, 0.8, 0.9),
             (0.7, -0.8, 0.4),
             (0.8, 0.4, 0.5))
        ).T
        array_x_r = np.array(
            (0.6, 0.9, 0.9)
        )
        array_W_Q = np.array(
            ((0.1, 0.8, -0.2),
             (0.7, -0.2, 0.1),
             (-0.3, 0.1, 0.9))
        )

        array_k_T = np.matmul(array_W_K, array_x).T
        array_q = np.matmul(array_W_Q, array_x_r)
        array_z = np.matmul(array_k_T, array_q)
        array_w = scipy.special.softmax(array_z)

        # first row
        coe1 = MathTex(r"\frac{1}{\sqrt{d}}(", color=font_color)
        W_K = linear_algebra.Matrix_Box_Heat(
            array=array_W_K,
            name=r"\boldsymbol{W}_K",
            color_text=font_color,
            color_fill=GOLD).next_to(coe1, RIGHT)
        x_l = linear_algebra.Matrix_Box_Heat(
            array=array_x,
            name=r"\boldsymbol{x}",
            color_text=font_color).next_to(W_K, RIGHT).align_to(W_K, DOWN)
        equations.add(coe1, W_K, x_l)
        mid1 = MathTex(r")^T \cdot (", color=font_color).next_to(x_l, RIGHT)
        W_Q = linear_algebra.Matrix_Box_Heat(
            array=array_W_Q,
            name=r"\boldsymbol{W}_Q",
            color_text=font_color,
            color_fill=GOLD).next_to(mid1, RIGHT)
        x_r = linear_algebra.Matrix_Box_Heat(
            array=array_x_r,
            name = r"\boldsymbol{x}_i",
            color_text=font_color).next_to(W_Q, RIGHT).align_to(W_Q, DOWN)
        right1 = MathTex(r")", color=font_color).next_to(x_r, RIGHT)
        equations.add(mid1, W_Q, x_r, right1)

        # second row
        coe2 = MathTex(r"= \frac{1}{\sqrt{d}}\,", color=font_color)\
            .next_to(W_K, DOWN, buff=2).align_to(coe1, RIGHT).shift(DOWN)
        k_T = linear_algebra.Matrix_Box_Heat(
            array=array_k_T,
            name=r"\boldsymbol{k}^T",
            color_text=font_color,
            color_fill=BLUE_E).next_to(coe2, RIGHT)
        q = linear_algebra.Matrix_Box_Heat(
            array=array_q,
            name=r"\boldsymbol{q}_i",
            color_text=font_color,
            color_fill=BLUE_E).next_to(k_T, RIGHT)
        equations.add(coe2, k_T, q)

        # third row
        coe3 = MathTex(r"= \frac{1}{\sqrt{d}}", color=font_color) \
            .next_to(q, RIGHT)
        z = linear_algebra.Matrix_Box_Heat(
            array=array_w,
            name=r"\boldsymbol{z}_i",
            color_text=font_color,
            color_fill=TEAL_E).next_to(coe3, RIGHT)
        equations.add(coe3, z)

        # init highlight
        x_l.highlight_columns((0,), opacity=0)
        k_T.highlight_rows((0,), opacity=0)
        z.highlight_cell((0,), opacity=0)

        # init softmax and output
        arrow_softmax = Arrow(start=2 * LEFT, end=2 * RIGHT, color=GOLD).next_to(z, RIGHT)
        arrow_softmax_text = MathTex(
            r"\boldsymbol w_i = Softmax(\boldsymbol z_i)\\w_{ji} = \frac{exp(\boldsymbol z_{ji})}{\sum\limits_{j} exp("
            r"z_{ji})}",
            color=BLACK).next_to(arrow_softmax, UP).scale(0.8)
        w = linear_algebra.Matrix_Box_Heat(
            array=array_w,
            name=r"\boldsymbol{w}_i",
            color_text=font_color,
            color_fill=MAROON_B).next_to(arrow_softmax, RIGHT).align_to(z, DOWN)
        arrow_output = Arrow(start=2 * LEFT, end=ORIGIN, color=GOLD).next_to(w, RIGHT)
        arrow_output_text = MathTex(
            r"\boldsymbol y_i = \boldsymbol W_V\boldsymbol x\boldsymbol w_i\\"
            r"= \boldsymbol W_V\left[\begin{matrix}\boldsymbol x_1 & ... & \boldsymbol x_n\end{matrix}\right]"
            r"\left[\begin{matrix}w_{1i} \\ ... \\ w_{ni}\end{matrix}\right]\\"
            r"= \boldsymbol W_V\sum\limits_{j} w_{ji}\boldsymbol{x_j}",
            color=BLACK).scale(1.3).next_to(arrow_output, RIGHT)
        format.centralize(
            equations,
            arrow_softmax, arrow_softmax_text, w,
            arrow_output, arrow_output_text,
        )

        self.add(equations)
        self.wait()

        # expand x_l
        self.next_section("expand x_l")
        for n in range(1, 4):
            x_l.cancel_lighten_columns((n,))
            k_T.cancel_lighten_rows((n,))
            z.cancel_lighten_cell((n,))
            self.wait()

        # softmax
        self.next_section("softmax")
        self.add(arrow_softmax, arrow_softmax_text, w)
        self.wait()

        # weighted output
        self.next_section("output")
        self.add(arrow_output, arrow_output_text)
        self.wait()


class Single_Head(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(2.5)
        font_color = BLACK
        equations = VGroup()

        # numpy arrays
        array_W_K = np.array(
            ((0.9, 0.1, 0.2),
             (-0.1, 0.8, 0.2),
             (0.1, -0.1, 0.9))
        )
        array_x = np.array(
            ((0.6, 0.9, 0.9),
             (-0.5, 0.8, 0.9),
             (0.7, -0.8, 0.4),
             (0.8, 0.4, 0.5))
        ).T
        array_W_Q = np.array(
            ((0.1, 0.8, -0.2),
             (0.7, -0.2, 0.1),
             (-0.3, 0.1, 0.9))
        )

        array_k_T = np.matmul(array_W_K, array_x).T
        array_q = np.matmul(array_W_Q, array_x)
        array_z = np.matmul(array_k_T, array_q)
        array_w = scipy.special.softmax(array_z, axis=1)

        # first row
        coe1 = MathTex(r"\frac{1}{\sqrt{d}}(", color=font_color)
        W_K = linear_algebra.Matrix_Box_Heat(
            array=array_W_K,
            name=r"\boldsymbol{W}_K",
            color_text=font_color,
            color_fill=GOLD).next_to(coe1, RIGHT)
        x_l = linear_algebra.Matrix_Box_Heat(
            array=array_x,
            name=r"\boldsymbol{x}",
            color_text=font_color).next_to(W_K, RIGHT).align_to(W_K, DOWN)
        equations.add(coe1, W_K, x_l)
        mid1 = MathTex(r")^T \cdot (", color=font_color).next_to(x_l, RIGHT)
        W_Q = linear_algebra.Matrix_Box_Heat(
            array=array_W_Q,
            name=r"\boldsymbol{W}_Q",
            color_text=font_color,
            color_fill=GOLD).next_to(mid1, RIGHT)
        x_r = linear_algebra.Matrix_Box_Heat(
            array=array_x,
            name = r"\boldsymbol{x}",
            color_text=font_color).next_to(W_Q, RIGHT).align_to(W_Q, DOWN)
        right1 = MathTex(r")", color=font_color).next_to(x_r, RIGHT)
        equations.add(mid1, W_Q, x_r, right1)

        # second row
        coe2 = MathTex(r"= \frac{1}{\sqrt{d}}\,", color=font_color)\
            .next_to(W_K, DOWN, buff=2).align_to(coe1, RIGHT).shift(DOWN)
        k_T = linear_algebra.Matrix_Box_Heat(
            array=array_k_T,
            name=r"\boldsymbol{k}^T",
            color_text=font_color,
            color_fill=BLUE_E).next_to(coe2, RIGHT)
        q = linear_algebra.Matrix_Box_Heat(
            array=array_q,
            name=r"\boldsymbol{q}",
            color_text=font_color,
            color_fill=BLUE_E).next_to(k_T, RIGHT)
        equations.add(coe2, k_T, q)

        # third row
        coe3 = MathTex(r"= \frac{1}{\sqrt{d}}", color=font_color) \
            .next_to(q, RIGHT)
        z = linear_algebra.Matrix_Box_Heat(
            array=array_z,
            name=r"\boldsymbol{z}",
            color_text=font_color,
            color_fill=TEAL_E).next_to(coe3, RIGHT)
        equations.add(coe3, z)

        # init highlight
        x_r.highlight_columns((0,), opacity=0)
        q.highlight_columns((0,), opacity=0)
        z.highlight_columns((0,), opacity=0)

        # init softmax and output
        arrow_softmax = Arrow(start=2 * LEFT, end=2 * RIGHT, color=GOLD).next_to(z, RIGHT)
        arrow_softmax_text = MathTex(
            r"\boldsymbol w = Softmax(\boldsymbol z)",
            color=BLACK).next_to(arrow_softmax, UP).scale(0.8)
        w = linear_algebra.Matrix_Box_Heat(
            array=array_w,
            name=r"\boldsymbol{w}",
            color_text=font_color,
            color_fill=MAROON_B).next_to(arrow_softmax, RIGHT).align_to(z, DOWN)
        arrow_output = Arrow(start=2 * LEFT, end=ORIGIN, color=GOLD).next_to(w, RIGHT)
        arrow_output_text = MathTex(
            r"\boldsymbol y = \boldsymbol W_V\boldsymbol x \boldsymbol w",
            color=BLACK).scale(1.3).next_to(arrow_output, RIGHT)
        format.centralize(
            equations,
            arrow_softmax, arrow_softmax_text, w,
            arrow_output, arrow_output_text,
        )

        self.add(equations)
        self.wait()

        # expand x_r
        self.next_section("expand x_r")
        for n in range(1, 4):
            x_r.cancel_lighten_columns((n,))
            q.cancel_lighten_columns((n,))
            z.cancel_lighten_columns((n,))
            self.wait()

        # softmax
        self.next_section("softmax")
        self.add(arrow_softmax, arrow_softmax_text, w)
        self.wait()

        # weighted output
        self.next_section("output")
        self.add(arrow_output, arrow_output_text)
        self.wait()


class Multi_Head(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(zoom=0.3, focal_distance=1e5)
        font_color = BLACK
        equations = VGroup()

        # numpy arrays
        array_W_K = np.array(
            ((0.9, 0.1, 0.2),
             (-0.1, 0.8, 0.2),
             (0.1, -0.1, 0.9))
        )
        array_x = np.array(
            ((0.6, 0.9, 0.9),
             (-0.5, 0.8, 0.9),
             (0.7, -0.8, 0.4),
             (0.8, 0.4, 0.5))
        ).T
        array_W_Q = np.array(
            ((0.1, 0.8, -0.2),
             (0.7, -0.2, 0.1),
             (-0.3, 0.1, 0.9))
        )

        # P.S. after matrix multiplication, the vectors seem to become tensors
        # though not quite understand why
        array_k_T = np.matmul(array_W_K, array_x).T
        array_q = np.matmul(array_W_Q, array_x)
        array_z = np.matmul(array_k_T, array_q)
        array_w = scipy.special.softmax(array_z, axis=1)

        array_q = np.expand_dims(array_q, 0)
        array_z = np.expand_dims(array_z, 0)
        array_w = np.expand_dims(array_w, 0)
        array_W_K = np.expand_dims(array_W_K, 0)
        array_x = np.expand_dims(array_x, 0)
        array_W_Q = np.expand_dims(array_W_Q, 0)
        array_k_T = np.expand_dims(array_k_T, 0)

        # first row
        coe1 = MathTex(r"\frac{1}{\sqrt{d}}(", color=font_color, font_size=100)
        W_K = linear_algebra.Tensor_Box_Heat(
            array=array_W_K,
            name=r"\boldsymbol{W}_K",
            color_text=font_color,
            color_fill=GOLD,
            name_size=80,
            name_buff=1).next_to(coe1, 5*RIGHT)
        x_l = linear_algebra.Tensor_Box_Heat(
            array=array_x,
            name=r"\boldsymbol{x}",
            color_text=font_color,
            name_size=80,
            name_buff=1).next_to(W_K, 6*RIGHT).align_to(W_K, DOWN)
        mid1 = MathTex(r")^T \cdot (", color=font_color, font_size=100).next_to(x_l, 5*RIGHT)
        W_Q = linear_algebra.Tensor_Box_Heat(
            array=array_W_Q,
            name=r"\boldsymbol{W}_Q",
            color_text=font_color,
            color_fill=GOLD,
            name_size=80,
            name_buff=1).next_to(mid1, 5*RIGHT)
        x_r = linear_algebra.Tensor_Box_Heat(
            array=array_x,
            name = r"\boldsymbol{x}",
            color_text=font_color,
            name_size=80,
            name_buff=1).next_to(W_Q, 6*RIGHT).align_to(W_Q, DOWN)
        right1 = MathTex(r")", color=font_color, font_size=100).next_to(x_r, 5*RIGHT)
        equations.add(coe1, W_K, x_l, mid1, W_Q, x_r, right1)

        # second row
        coe2 = MathTex(r"= \frac{1}{\sqrt{d}}\,", color=font_color, font_size=100)\
            .next_to(W_K, DOWN, buff=2).align_to(coe1, 5*RIGHT).shift(5*DOWN)
        k_T = linear_algebra.Tensor_Box_Heat(
            array=array_k_T,
            name=r"\boldsymbol{k}^T",
            color_text=font_color,
            color_fill=BLUE_E,
            name_size=80,
            name_buff=1).next_to(coe2, 5*RIGHT)
        q = linear_algebra.Tensor_Box_Heat(
            array=array_q,
            name=r"\boldsymbol{q}",
            color_text=font_color,
            color_fill=BLUE_E,
            name_size=80,
            name_buff=1).next_to(k_T, 6*RIGHT)
        equations.add(coe2, k_T, q)

        # third row
        coe3 = MathTex(r"= \frac{1}{\sqrt{d}}", color=font_color, font_size=100) \
            .next_to(q, 5*RIGHT)
        z = linear_algebra.Tensor_Box_Heat(
            array=array_z,
            name=r"\boldsymbol{z}",
            color_text=font_color,
            color_fill=TEAL_E,
            name_size=80,
            name_buff=1).next_to(coe3, 5*RIGHT)
        equations.add(coe3, z)

        # softmax and output
        arrow_softmax = Arrow3D(start=LEFT, end=RIGHT, color=GOLD, resolution=8).next_to(z, 5*RIGHT)
        arrow_softmax_text = MathTex(
            r"softmax",
            color=BLACK, font_size=60).next_to(arrow_softmax, UP)
        w = linear_algebra.Tensor_Box_Heat(
            array=array_w,
            name=r"\boldsymbol{w}",
            color_text=font_color,
            color_fill=MAROON_B,
            name_size=80,
            name_buff=1).next_to(arrow_softmax, 5*RIGHT).align_to(z, DOWN)
        arrow_output = Arrow3D(start=LEFT, end=RIGHT, color=GOLD, resolution=8).next_to(w, 4*RIGHT)
        arrow_output_text = MathTex(
            r"\boldsymbol y = \boldsymbol W_V\boldsymbol x \boldsymbol w",
            color=BLACK, font_size=80).next_to(arrow_output, RIGHT)
        equations.add(
            arrow_softmax, arrow_softmax_text, w,
            arrow_output, arrow_output_text,
        )

        equations.move_to(ORIGIN)
        self.add(equations)

        self.move_camera(
            phi=55 * DEGREES,
            theta=-45 * DEGREES,
            gamma=30 * DEGREES,
            run_time=10
        )
        self.wait()

        # layer expand
        self.next_section("layer expand")
        for n in range(3):
            W_K.expand_random()
            W_Q.expand_random()
            k_T.expand_random()
            q.expand_random()
            z.expand_random()
            w.expand_random()
            self.wait()

        # layer highlight
        self.next_section("layer height")
        for n in range(4):
            W_K.highlight_layers((n,))
            W_Q.highlight_layers((n,))
            k_T.highlight_layers((n,))
            q.highlight_layers((n,))
            z.highlight_layers((n,))
            w.highlight_layers((n,))
            self.wait()


class Test(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(zoom=0.5, focal_distance=1e5)
        self.move_camera(
            phi=55 * DEGREES,
            theta=-45 * DEGREES,
            gamma=30 * DEGREES,
            run_time=0
        )

        font_color = BLACK

        array_W_K = np.array(
            ((0.9, 0.1, 0.2),
             (-0.1, 0.8, 0.2),
             (0.1, -0.1, 0.9))
        )
        array_W_K = np.expand_dims(array_W_K, 0)
        W_K = linear_algebra.Tensor_Box_Heat(
            array=array_W_K,
            name=r"\boldsymbol{W}_K",
            color_text=font_color,
            color_fill=GOLD).shift(RIGHT)
        self.add(W_K)
        self.wait()

        W_K.expand_random(axis=0)
        W_K.highlight_layers((0,))
        self.wait()


if __name__ == '__main__':
    '''
    with tempconfig({
        "format": "png",
        # "transparent": True,
        "output_file": "manim-",
        "zero_pad": False,
        "frame_rate": 10,
        "pixel_width": 1024,
        "pixel_height": 1024,
        "preview": True,
    }):
        scenes = (
            # Embedding_Averg_Transform(),
            # Test(),
        )

        for scene in scenes:
            scene.render()
    '''
    with tempconfig({
        "format": "png",
        "transparent": True,
        "output_file": "manim-",
        "zero_pad": False,
        "frame_rate": 1,
        "pixel_width": 2048,
        "pixel_height": 1024,
        "preview": True,
    }):
        scenes = (
            # Single_Word(),
            # Multiple_Words(),
            # Single_Head(),
            Multi_Head(),
            # Test(),
        )

        for scene in scenes:
            scene.render()