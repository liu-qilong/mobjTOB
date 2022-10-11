import numpy as np
import open3d as o3d
from manim import *

class Point_Cloud(PMobject):
    def __init__(self, path, sample_num=int(1e4), load_scale=1, stroke_width=1, **kwargs):
        PMobject.__init__(self, stroke_width=stroke_width, **kwargs)
        mesh = o3d.io.read_triangle_mesh(path).scale(load_scale, center=ORIGIN)
        mesh.compute_vertex_normals()
        pcd = mesh.sample_points_poisson_disk(number_of_points=sample_num, init_factor=5)

        self.vertices = np.asarray(pcd.points)
        self.normals = np.asarray(pcd.normals)
        self.add_points(self.vertices, color=self.color)

    def lightup(self, light_vector=UP):
        # compute the dot product of normal vectors and light vector, and normalize to [0, 1]
        # use them as the lightup weight
        lightup_value = np.expand_dims(
            (np.sum(self.normals * light_vector, axis=1) + 1)/2,
            axis=1
        )
        # concatenate as [point_num, 4] lihtup weight array
        lightup_expand = np.concatenate(
            (
                lightup_value, 
                lightup_value, 
                lightup_value, 
                np.ones((len(self.vertices), 1))
            ),
            axis=1
        )
        # use the lightup weight array to lightup/shadow the rgbs attribute
        # noted that the opacity channel aren't changed
        self.rgbas = lightup_expand * self.rgbas

    
class Mesh(VGroup):
    def __init__(self, path, stroke_width=0, fill_opacity=1, **kwargs):
        VGroup.__init__(self, stroke_width=stroke_width, fill_opacity=fill_opacity, **kwargs)
        mesh = o3d.io.read_triangle_mesh(path)
        mesh.compute_triangle_normals()

        self.vertices = np.asarray(mesh.vertices)
        self.triangles = np.asarray(mesh.triangles)
        self.normals = np.asarray(mesh.triangle_normals)

        faces = VGroup()
        for tri in self.triangles:
            face = ThreeDVMobject()
            face.set_points_as_corners([
                    self.vertices[tri[0]],
                    self.vertices[tri[1]],
                    self.vertices[tri[2]],
                ],
            )
            faces.add(face)
        
        faces.set_fill(color=self.fill_color, opacity=self.fill_opacity)
        faces.set_stroke(
            color=self.stroke_color,
            width=self.stroke_width,
            opacity=self.stroke_opacity,
        )
        self.add(*faces)

    def lightup(self, light_vector=UP):
        # compute the dot product of normal vectors and light vector, and normalize to [0, 1]
        # use them as the lightup weight
        lightup_value = (np.sum(self.normals * light_vector, axis=1) + 1)/2
        # use the lightup weight array to lightup/shadow the face color
        # noted that the opacity channel aren't changed
        for idx in range(len(self.submobjects)):
            face = self.submobjects[idx]
            weight = lightup_value[idx]
            original_rgba = color_to_rgba(face.color)
            
            lightup_rgba = weight * original_rgba
            lightup_rgba[-1] = 1.0
            face.set_fill(color=rgba_to_color(lightup_rgba))