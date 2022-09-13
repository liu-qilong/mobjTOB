from manim import *

class SingleLayer(object):

    def __init__(self,
                 scene,
                 neural_in,
                 neural_out,
                 central_pos=ORIGIN,
                 scale=1):

        self.scene = scene
        self.neural_in = neural_in
        self.neural_out = neural_out
        self.central_pos = central_pos
        self.scale = scale

        self.is_output_series = False
        self.output_series = []

        # Create input layer, output layer and links between them.

        self.layer_in = [Dot(radius=1/8, stroke_width=2)
                             .shift(n * 5 / self.neural_in * UP) for n in range(self.neural_in)]
        self.layer_in = VGroup(*self.layer_in).move_to(ORIGIN).set_fill(BLACK)

        self.layer_out = [Dot(radius=1/8, stroke_width=2)
                              .shift(n * 5 / self.neural_in * UP) for n in range(self.neural_out)]
        self.layer_out = VGroup(*self.layer_out).next_to(self.layer_in, RIGHT, buff=4).set_fill(BLACK)

        self.links = [Line(start, end) for start in self.layer_in.submobjects for end in self.layer_out]
        self.links = VGroup(*self.links).set_color(GREY).set_stroke(width=1)

        # Pack them as VGroup and do adjustment.

        self.mobj = VGroup(self.layer_in, self.layer_out, self.links)
        self.mobj.move_to(self.central_pos).scale(self.scale)

    def show(self):

        self.scene.play(FadeIn(self.mobj))
    def enable_output_series(self):

        self.is_output_series = True

    def add_output_labels(self, labels, **params):

        out_labels = []

        for it in range(self.neural_out):
            label = MathTex(labels[it], **params)
            label.next_to(self.layer_out.submobjects[it], RIGHT)
            out_labels.append(label)

        self.out_labels = VGroup(*out_labels)
        self.mobj.add(self.out_labels)


    def image_input(self, img):

        img_copy = img.copy()

        self.scene.play(FadeTransform(img_copy, self.layer_in))
        self.scene.remove(img_copy)

        self.arr_input(np.random.rand(self.neural_in))

    def dot_input(self, dot):

        dot_copy = dot.copy()

        self.scene.play(FadeTransform(dot_copy, self.layer_in))
        self.scene.remove(dot_copy)

        self.arr_input(np.random.rand(self.neural_in))

    def arr_input(self, arr):

        values = arr.flatten()
        max_value = values.max()

        for n in range(self.neural_in):
            norm_value = float(values[n] / max_value)
            white_rgb = hex_to_rgb(WHITE)
            norm_color_hex = rgb_to_hex(norm_value * white_rgb)
            self.layer_in.submobjects[n].set_fill(norm_color_hex)

        if self.is_output_series:
            self.move_output_series()

        self.arr_output(np.random.rand(self.neural_out))

    def arr_output(self, arr):

        values = arr.flatten()
        max_value = values.max()

        for n in range(self.neural_out):

            norm_value = float(values[n] / max_value)
            white_rgb = hex_to_rgb(WHITE)
            norm_color_hex = rgb_to_hex(norm_value * white_rgb)
            self.layer_out.submobjects[n].set_fill(norm_color_hex)

    def move_output_series(self):

        if len(self.output_series) == 0:
            new_output = self.layer_out.copy().set_stroke(width=0)
            self.mobj.add(new_output)
            self.output_series.append(new_output)

        else:
            new_output = self.layer_out.copy().set_stroke(width=0)
            self.mobj.add(new_output)
            self.output_series.append(new_output)

            series_move = (mobj.animate.shift(RIGHT/2) for mobj in self.output_series)
            self.scene.play(*series_move)
            self.scene.wait(0.2)

    def get_link(self, start, end):

        index = start * self.neural_out + end
        return self.links.submobjects[index]

    def get_output_seq(self, end):

        return [output.submobjects[end] for output in self.output_series]

    def emphasize_end(self, index_out):

        emp_link = [self.get_link(start, index_out) for start in range(self.neural_in)]
        neg_link = set(self.links.submobjects) - set(emp_link)
        neg_out = set(self.layer_out.submobjects) - set(self.layer_out.submobjects[index_out])

        VGroup(*emp_link).set_color(YELLOW).set_opacity(0.6)
        VGroup(*neg_link).set_opacity(0.4)
        VGroup(*neg_out).set_opacity(0.2)

        if self.is_output_series:

            neg_out_series = [VGroup(*self.get_output_seq(end))
                              for end in range(self.neural_out) if end != index_out]

            VGroup(*neg_out_series).set_opacity(0.2)


class Overlayer(SingleLayer):

    def __init__(self,
                 scene,
                 front_layer,
                 neural_out,
                 scale=1):

        super().__init__(scene, front_layer.neural_out, neural_out, ORIGIN, scale)
        self.init_neural_in = front_layer.neural_in

        self.layer_in.become(front_layer.layer_out.copy())
        self.layer_out = [Dot(radius=1 / 8, stroke_width=2)
                              .shift(n * 5 / self.init_neural_in * UP) for n in range(self.neural_out)]
        self.layer_out = VGroup(*self.layer_out).next_to(self.layer_in, RIGHT*scale, buff=4).set_fill(BLACK)

        self.links = [Line(start, end) for start in self.layer_in.submobjects for end in self.layer_out]
        self.links = VGroup(*self.links).set_color(GREY).set_stroke(width=1)

        self.mobj = VGroup(self.layer_in, self.layer_out, self.links)


class Convolution(object):

    def __init__(self,
                 scene,
                 arr_A,
                 arr_B,
                 legend_A="A",
                 legend_B="B",
                 legend_C="C",
                 pos=ORIGIN):

        self.arr_A = arr_A
        self.arr_B = arr_B
        self.arr_C = self.convolve(self.arr_A, self.arr_B)
        self.pos = pos

        self.scene = scene
        self.mat_A = Matrix(self.arr_A, left_bracket="[", right_bracket="]").scale(0.7)
        self.star = MathTex("*").next_to(self.mat_A, RIGHT)
        self.mat_B = Matrix(self.arr_B, left_bracket="[", right_bracket="]",
                            include_background_rectangle=True).scale(0.7).next_to(self.star, RIGHT)
        self.mat_B.background_rectangle.set_opacity(0.7)
        self.mat_C = Matrix(self.arr_C, left_bracket="[", right_bracket="]",
                            include_background_rectangle=True).scale(0.7).next_to(self.mat_A, DOWN)
        self.mat_C.background_rectangle.set_opacity(0.7)
        self.equ = MathTex("=").next_to(self.mat_C, LEFT)

        self.legend_A = Text(legend_A, font_size=25).next_to(self.mat_A, UP)
        self.legend_B = Text(legend_B, font_size=25).next_to(self.mat_B, UP)
        self.legend_C = Text(legend_C, font_size=25).next_to(self.mat_C, DOWN)

        self.mobj = VGroup(self.mat_A, self.star, self.mat_B, self.mat_C,
                           self.equ, self.legend_A, self.legend_B, self.legend_C)
        self.mobj.move_to(pos)

    def show(self):

        self.scene.play(FadeIn(self.mobj))

    def demonstrate(self, with_rec=True, pos_dem=ORIGIN):

        slice_B = self.get_mat_slice(self.mat_B,
                                     0, self.arr_B.shape[0] - 1,
                                     0, self.arr_B.shape[1] - 1)

        # Create rectangles for relevant elements.

        self.rec_A = SurroundingRectangle(self.get_mat_slice(self.mat_A,
                                                             0, self.arr_B.shape[0] - 1,
                                                             0, self.arr_B.shape[1] - 1), GOLD)
        self.rec_B = SurroundingRectangle(slice_B, GOLD)
        self.rec_C = SurroundingRectangle(self.get_mat_slice(self.mat_C, 0, 0, 0, 0), GOLD)

        if with_rec:
            self.scene.play(FadeIn(self.rec_A, self.rec_B, self.rec_C))

        for i in range(self.arr_A.shape[0] - self.arr_B.shape[0] + 1):
            for j in range(self.arr_A.shape[1] - self.arr_B.shape[1] + 1):

                # Move rectangles of relevant elements.

                slice_A = self.get_mat_slice(self.mat_A,
                                             i, i + self.arr_B.shape[0] - 1,
                                             j, j + self.arr_B.shape[1] - 1)
                slice_C = self.get_mat_slice(self.mat_C, i, i, j, j)
                rec_A_change = SurroundingRectangle(slice_A, GOLD)
                rec_C_change = SurroundingRectangle(slice_C, GOLD)

                if with_rec:
                    self.scene.play(self.rec_A.animate.become(rec_A_change),
                                    self.rec_C.animate.become(rec_C_change))

                # Show the procedure of convolution.

                math_tex = self.convolve_tex(self.arr_A, self.arr_B, i, j)
                math_group = VGroup(*math_tex)
                math_group.next_to(self.mat_C, RIGHT + pos_dem)
                
                cal_tex_list = []
                A_mov_list = []
                B_mov_list = []

                for m in range(self.arr_B.shape[0]):

                    for n in range(self.arr_B.shape[1]):

                        start = (m * self.arr_B.shape[0] + n) * 4

                        cal_tex_list.append(math_tex[start])
                        cal_tex_list.append(math_tex[start + 2])

                        A_mov_list.append(FadeTransform(self.mat_A.mob_matrix[i + m][j + n].copy(),
                                                        math_tex[start + 1]))
                        B_mov_list.append(FadeTransform(self.mat_B.mob_matrix[m][n].copy(),
                                                        math_tex[start + 3]))

                self.scene.play(FadeIn(*cal_tex_list))
                self.scene.play(*A_mov_list)
                self.scene.play(*B_mov_list)

                self.scene.play(FadeTransform(math_group, slice_C))

    def convolve(self, A, B):

        C = np.zeros([A.shape[0] - B.shape[0] + 1, A.shape[1] - B.shape[1] + 1], dtype='int64')

        for i in range(A.shape[0] - B.shape[0] + 1):
            for j in range(A.shape[1] - B.shape[1] + 1):

                e = [A[i+m, j+n] * B[m, n] for m in range(B.shape[0]) for n in range(B.shape[1])]
                C[i, j] = sum(e)

        return C

    def convolve_tex(self, A, B, i, j):

        math_tex = []

        for m in range(B.shape[0]):
            for n in range(B.shape[1]):

                math_tex.append(MathTex("+", font_size=25, color=GOLD).shift(m * DOWN * 0.8 + n * RIGHT))
                math_tex.append(MathTex(str(A[i + m, j + n]), font_size=25).next_to(math_tex[-1], RIGHT/2))
                math_tex.append(MathTex(r"\times", font_size=25, color=GOLD).next_to(math_tex[-1], RIGHT/2))
                math_tex.append(MathTex(str(B[m, n]), font_size=25).next_to(math_tex[-1], RIGHT/2))

        return math_tex

    def get_mat_slice(self, mat, i_start, i_end, j_start, j_end):

        return VGroup(*(mat.mob_matrix[i][j]
                        for i in range(i_start, i_end+1) for j in range(j_start, j_end+1)))

    def mat_copy_rand_refresh(self, mat):

        mat_shape = [len(mat.get_rows()), len(mat.get_columns())]
        mat_arr = np.random.randint(10, size=mat_shape)

        mat_new = Matrix(mat_arr,  left_bracket="[", right_bracket="]", include_background_rectangle=True)
        mat_new.background_rectangle.set_opacity(0.7)

        mat_new.move_to(mat.get_center())
        mat_new.scale(mat.height / mat_new.height)

        if mat.fill_opacity != 0:
            mat_new.set_opacity(mat.fill_opacity)

        return mat_new