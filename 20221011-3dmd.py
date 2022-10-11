""" works on git checkpoint:  """
from manim import *

from concept import point_cloud
from behavior import utils, format

class Test(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES)

        pcd = point_cloud.Point_Cloud()
        pcd.load_from_obj("gallery/material/obj_sample.obj")
        pcd.lightup()
        pcd.rotate(90*DEGREES, RIGHT)

        self.add(pcd)
        self.begin_ambient_camera_rotation(rate=4)
        self.wait()


if __name__ == "__main__":
    with tempconfig({
        # "format": "png",
        # "transparent": True,
        # "output_file": "manim-",
        # "zero_pad": False,
        "frame_rate": 24,
        #"pixel_width": 2048,
        # "pixel_height": 1024,
        "preview": True,
    }):
        scenes = (
            Test(),
        )

        for scene in scenes:
            scene.render()