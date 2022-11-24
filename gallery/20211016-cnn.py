""" works on git checkpoint: 8d0dfb3877ebd45ff122e7a0e774085bd40644e0 """

import sys
sys.path.insert(0, '../mobjTOB')

from manim import *
from concept import imgwork, neuralwork

class SceneCNN(MovingCameraScene):
    def construct(self):
        # Section 1. What happens when putting image into neural network.
        # Section 1.1. Input the whole picture to the network.
        
        self.SectionShow("1 What happens when putting image into neural network", ORIGIN)
        
        img = ImageMobject('material/cat.jpeg').set_opacity(0.8).scale(0.6)
        rec_img = SurroundingRectangle(img, WHITE).set_stroke(width=2)
        img_and_rec = Group(img, rec_img)
        self.play(FadeIn(img_and_rec))
        self.wait()

        single = neuralwork.SingleLayer(self, 8, 5, RIGHT, 1)
        self.play(img_and_rec.animate.next_to(single.mobj, LEFT))
        single.show()
        single.image_input(img)
        self.wait()

        # Section 1.2. What it actually is.

        arr_A_single = np.random.randint(10, size=(2, 2))
        arr_B_single = np.random.randint(10, size=(2, 2))

        conv_show_single = neuralwork.Convolution(self, arr_A_single, arr_B_single,
                                                  legend_A="Input", legend_B="Weights", legend_C="Output")
        conv_show_single.mobj.scale(0.8).next_to(single.mobj, 1.1*RIGHT)

        single.emphasize_end(2)
        self.wait()

        self.play(single.mobj.animate.scale(0.8))
        conv_show_single.show()

        emp_links = [single.get_link(start, 2) for start in range(single.neural_in)]
        self.play(FadeTransform(single.layer_in.copy(), conv_show_single.mat_A))
        self.wait()
        self.play(FadeTransform(VGroup(*emp_links).copy(), conv_show_single.mat_B))
        self.wait()
        self.play(FadeTransform(single.layer_out[2].copy(), conv_show_single.mat_C))
        self.wait()

        conv_show_single.demonstrate(False, 0.5*DOWN)

        self.play(FadeOut(conv_show_single.mobj))
        
        self.play(single.mobj.animate.move_to(RIGHT))
        self.play(single.mobj.animate.scale(1 / 0.8))

        self.wait(3)
        
        # Section 2. Better way to imitate human visual system.

        self.SectionShow("2 Better way to imitate human visual system")
        
        self.play(img.animate.shift(2*DOWN),
                  rec_img.animate.shift(2*DOWN))
        img_crop = imgwork.PartialShow(self, img, zoom_rate=30, zoom_pos=DOWN + RIGHT, show_pos=UP)
        img_crop.show()

        for n in range(8):
            img_crop.move(0.002*RIGHT, 0.1)

        for n in range(8):
            img_crop.move(0.002*RIGHT, 1)

        self.wait()
        single.enable_output_series()

        for n in range(8):
            img_crop.move(0.002 * RIGHT, 0.1)
            single.image_input(img_crop.img_show)
        
        # Section 3. How to realize such ideas in a concise math form.
        # Section 3.1. Show convolution.

        self.SectionShow("3 How to realize such ideas in a concise math form")

        self.play(FadeOut(single.mobj))

        arr_A = np.random.randint(10, size=(4, 4))
        arr_B = np.random.randint(10, size=(2, 2))

        conv_show = neuralwork.Convolution(self, arr_A, arr_B,
                                           legend_A="Matrix", legend_B="Filter", legend_C="Result",
                                           pos= RIGHT * 2.3)
        conv_show.show()
        conv_show.demonstrate()

        active_1 = MathTex("\sigma(", font_size=50).next_to(conv_show.mat_A, LEFT)
        active_2 = MathTex(")", font_size=50).next_to(conv_show.mat_B, RIGHT)
        active_3 = MathTex("\sigma(", font_size=50).next_to(conv_show.mat_C, LEFT)
        active_4 = MathTex(")", font_size=50).next_to(conv_show.mat_C, RIGHT)

        self.play(FadeIn(active_1, active_2, active_3, active_4),
                  conv_show.equ.animate.next_to(active_3, LEFT))
        self.wait(3)

        # Section 3.2 Unify the two forms
        # The emphasized neural links.

        img_crop_group = VGroup(img_crop.rec_show, img_crop.sub_window,
                                img_crop.link_right, img_crop.link_left)
        self.remove(img_crop.show_legend)
        self.play(FadeTransform(img_crop_group, conv_show.rec_A),
                  FadeOut(img_crop.img_show, img_crop.legend))

        self.wait(3)

        self.play(FadeTransform(conv_show.mat_A, img_crop.img),
                  FadeOut(conv_show.rec_A, conv_show.rec_B, conv_show.rec_C, conv_show.legend_A))

        self.wait(3)

        active_1_2 = VGroup(active_1, active_2)
        active_star = MathTex("\sigma", font_size=35).next_to(conv_show.star, UP)
        conv_show.star = VGroup(active_star, conv_show.star).next_to(conv_show.mat_B, LEFT)
        self.play(FadeTransform(active_1_2, active_star))

        self.wait(3)

        single.mobj.scale(0.7).next_to(img, UP).shift(0.5*RIGHT + 0.1*UP)
        self.play(FadeIn(single.mobj))

        self.wait(3)

        self.play(FadeTransform(VGroup(*single.get_output_seq(2)), conv_show.mat_C))

        links_group = [single.get_link(start, 2) for start in range(single.neural_in)]
        self.play(FadeTransform(VGroup(*links_group), conv_show.mat_B),
                  FadeOut(conv_show.legend_B, conv_show.legend_C))

        self.wait(3)

        # The other neural links.

        filters = VGroup(conv_show.mat_B)
        results = VGroup(conv_show.mat_C)

        for n in range(single.neural_out):
            if n != 2:

                new_filter = Matrix(np.random.randint(10, size=(2, 2)),
                                    include_background_rectangle=True)
                new_filter.scale(0.7 * 0.8**(len(filters)))\
                          .move_to(filters.submobjects[0].get_center() + DOWN/2 + RIGHT/2)\
                          .set_opacity(0.8**(len(filters)))
                new_filter.background_rectangle.set_opacity(0.7)

                self.remove(filters)
                filters.submobjects.reverse()
                filters.add(new_filter)
                filters.submobjects.reverse()
                self.add(filters)

                filters_center = filters.get_center()
                self.play(filters.animate.shift([0, -filters_center[1], 0]))
                self.play(conv_show.star.animate.next_to(filters, LEFT))

                new_result = Matrix(np.random.randint(10, size=(3, 3)),
                                    include_background_rectangle=True)
                new_result.scale(0.7 * 0.8**(len(results)))\
                    .move_to(results.submobjects[0].get_center() + DOWN / 2 + RIGHT / 2) \
                    .set_opacity(0.8**(len(results)))
                new_result.background_rectangle.set_opacity(0.7)

                self.remove(results)
                results.submobjects.reverse()
                results.add(new_result)
                results.submobjects.reverse()
                self.add(results)

                new_result_center = new_result.get_center()
                self.play(results.animate.shift([0, -3 - new_result_center[1], 0]),
                          active_3.animate.shift([0, -3 - new_result_center[1], 0]),
                          active_4.animate.shift([0, -3 - new_result_center[1], 0]))

                self.play(active_3.animate.next_to(results, LEFT),
                          active_4.animate.next_to(results, RIGHT))
                self.play(conv_show.equ.animate.next_to(active_3, LEFT))

                single.emphasize_end(n)
                links_group = [single.get_link(start, n) for start in range(single.neural_in)]
                self.play(FadeTransform(VGroup(*links_group), filters.submobjects[0]),
                          FadeOut(VGroup(*single.get_output_seq(n))))
                self.play(FadeTransform(VGroup(*single.get_output_seq(n)), results.submobjects[0]))

        self.play(FadeOut(single.mobj))

        self.wait(3)

        # New layout.

        results.add(conv_show.equ, active_3, active_4)
        filters.add(conv_show.star)

        img_center = img_crop.img.get_center()
        img_move = [-1.5, -img_center[1] + 1, 0]
        self.play(img_crop.img.animate.scale(1/2).shift(img_move),
                  rec_img.animate.scale(1/2).shift(img_move))

        self.play(filters.animate.next_to(img_crop.img, RIGHT))
        self.play(results.animate.next_to(filters, RIGHT))

        self.wait(3)
        
        # Section 4. Deep Learning: Placing them layer by layer.

        self.SectionShow("4 Deep Learning: Placing them layer by layer")

        txt1 = Text("Convolutional Neural Network (CNN)",
                     disable_ligatures=True,
                     t2c={'C': GOLD, 'N': GOLD}).shift(DOWN*1.3)
        txt2 = Tex("* CNN also contains pooling layers and full-connection layers,",
                     font_size=25).next_to(txt1, DOWN)
        txt3 = Tex("which are dismissed for concision.",
                   font_size=25).next_to(txt2, DOWN)

        self.play(FadeOut(results, conv_show.equ),
                  filters.animate.scale(0.7).next_to(img_crop.img))

        filters_l2 = filters.copy().next_to(filters, 0.9*RIGHT)

        for n in range(len(filters_l2.submobjects) -1):
            filters_l2.submobjects[n] = conv_show.mat_copy_rand_refresh(filters_l2.submobjects[n])

        self.play(FadeIn(filters_l2))

        filters_l3 = filters.copy().next_to(filters_l2, RIGHT)

        for n in range(len(filters_l2.submobjects) - 1):
            filters_l3.submobjects[n] = conv_show.mat_copy_rand_refresh(filters_l3.submobjects[n])

        self.play(FadeIn(filters_l3))

        filters_l4 = filters.copy().next_to(filters_l3, RIGHT)

        for n in range(len(filters_l4.submobjects) - 1):
            filters_l4.submobjects[n] = conv_show.mat_copy_rand_refresh(filters_l4.submobjects[n])

        self.play(FadeIn(filters_l4))
        self.play(Write(txt1), Write(txt2), Write(txt3))

        self.wait(3)


    def SectionShow(self, title, pos=4*UP):

        sec = Text(title, font_size=50).shift(pos)
        self.play(self.camera.frame.animate.scale(2))
        self.play(FadeIn(sec))
        self.wait(3)
        self.play(FadeOut(sec))
        self.play(self.camera.frame.animate.scale(0.5))