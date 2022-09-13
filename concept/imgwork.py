from manim import *

class PartialShow(object):

    def __init__(self,
               scene,
               img,
               zoom_rate=10,
               zoom_pos=[0, 0, 0],
               show_pos=RIGHT,
               show_buff=2,
               show_legend="Partial of Image"):
        """This class creates a crop window on the desired image and show it on another place.
        he crop window move in a consistent speed showing the partial pixels of the image.

                :param scene: The scene that rendered the animation.
                :param img: The image mobject to be cropped and showed.
                :param zoom_rate: The image magnification rate.
                :param zoom_pos: The Relative position of the crop window to the left-up corner of the image.
                :param show_buff: The show image will be shown next to the right edge of the image. Here defines the buff.
                :param show_legend: The legend of the show image.
                """

        self.scene = scene
        self.img = img
        self.zoom_rate = zoom_rate
        self.show_buff = show_buff
        self.show_legend = show_legend

        # Define the window and sub window.

        self.window = SurroundingRectangle(img, GOLD)
        self.sub_window = Rectangle(GOLD, img.height / zoom_rate, img.height / zoom_rate)
        self.zoom_pos = zoom_pos\
                      + img.points.min(0) - self.sub_window.points.min(0)\
                      + [0, img.height - self.sub_window.height, 0]
        self.sub_window.shift(self.zoom_pos)

        # Define the show window and the accessories.

        self.img_show = ImageMobject(self.img_crop(self.img, self.sub_window)) \
            .next_to(self.img, show_pos, buff=self.show_buff).set_opacity(0.8)

        self.img_show.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        self.show_scale = self.img.height / self.img_show.height
        self.img_show.scale(self.show_scale)
        self.rec_show = SurroundingRectangle(self.img_show).set_color(GOLD)

        self.legend = Tex(self.show_legend, font_size=20).next_to(self.img_show, UP)

        self.link_right = Line(self.sub_window.points.min(0) + [self.sub_window.width, self.sub_window.width, 0],
                               self.rec_show.points.min(0) + [self.rec_show.width, 0, 0])
        self.link_right.set_color(GOLD).set_opacity(0.4)
        self.link_left = Line(self.sub_window.points.min(0) + [0, self.sub_window.width, 0],
                              self.rec_show.points.min(0))
        self.link_left.set_color(GOLD).set_opacity(0.4)

    def img_crop(self, img, window):

        arr = img.get_pixel_array()
        scale_ld = window.points.min(0) - img.points.min(0)
        scale_ru = img.points.max(0) - window.points.max(0)

        sample_width = window.width / img.width * arr.shape[1]

        x_start = int(scale_ld[0] / img.width * arr.shape[1])
        x_end = int(x_start + sample_width - 1)
        y_start = int(scale_ru[1] / img.height * arr.shape[0])
        y_end = int(y_start + sample_width - 1)

        return arr[y_start:y_end, x_start:x_end]

    def show(self, is_fade_in=True):

        self.scene.add(self.window)
        self.scene.wait(0.5)
        self.scene.play(ReplacementTransform(self.window, self.sub_window))

        if is_fade_in:
            self.scene.play(FadeIn(self.img_show),
                            FadeIn(self.rec_show),
                            FadeIn(self.link_right),
                            FadeIn(self.link_left),
                            Write(self.legend))
        else:
            self.scene.add(self.img_show, self.rec_show, self.link_right, self.link_left, self.legend)


    def move(self, pace, run_time):

        def interpolate(mobj, dt):
            self.sub_window.shift(pace)

            self.link_right.become(
                Line(self.sub_window.points.min(0) + [self.sub_window.width, self.sub_window.width, 0],
                     self.rec_show.points.min(0) + [self.rec_show.width, 0, 0]))
            self.link_right.set_color(GOLD).set_opacity(0.4)
            self.link_left.become(
                Line(self.sub_window.points.min(0) + [0, self.sub_window.width, 0],
                     self.rec_show.points.min(0)))
            self.link_left.set_color(GOLD).set_opacity(0.4)

            last_img_show_center = self.img_show.get_center()
            last_img_show_height = self.img_show.height

            self.img_show.become(ImageMobject(self.img_crop(self.img, self.sub_window))) \
                .move_to(last_img_show_center).set_opacity(0.8)
            self.img_show.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            self.img_show.scale(last_img_show_height / self.img_show.height)

        # Animate all the mobjects

        self.sub_window.add_updater(interpolate)
        self.scene.wait(run_time)
        self.sub_window.remove_updater(interpolate)