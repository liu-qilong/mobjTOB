import numpy as np
import open3d as o3d
from manim import *


class Point_Cloud(PMobject):
    def load_from_obj(self, path, stroke_width=1, sample_num=int(2e4), scale_rate=3e-3, scale_center=(0, 0, 0)):
        mesh = o3d.io.read_triangle_mesh(path).scale(scale_rate, center=scale_center)
        mesh.compute_vertex_normals()
        pcd = mesh.sample_points_poisson_disk(number_of_points=sample_num, init_factor=5)

        self.points = np.asarray(pcd.points)
        self.normals = np.asarray(pcd.normals)
        self.set_stroke_width(stroke_width)

    def lightup(self, light_vector=UP, texture_color=WHITE):
        # compute the dot product of normal vectors and light vector, and normalize to [0, 1]
        # use them as the lightup weight
        lightup_value = np.expand_dims(
            (np.sum(self.normals * light_vector, axis=1) + 1)/2,
            axis=1
        )
        print(len(self.points))
        # concatenate as [point_num, 4] lihtup weight array
        lightup_expand = np.concatenate(
            (
                lightup_value, 
                lightup_value, 
                lightup_value, 
                np.ones((len(self.points), 1))
            ),
            axis=1
        )
        # use the lightup weight array to lightup/shadow the rgbs attribute
        # noted that the opacity channel aren't changed
        lightup_rgba = lightup_expand * color_to_rgba(texture_color)
        self.rgbas = lightup_rgba