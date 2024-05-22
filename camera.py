import numpy as np
import math

class Camera:
    def __init__(self, engine, fov) -> None:
        self.translation = [0, 0, 0]    
        self.rotation = [0, 0, 0]
        self.fov = fov
        self.aspect_ratio = engine.get_aspect_ratio()
        print(self.aspect_ratio)

    def translate(self, vector):
        for i, c in enumerate(vector):
            self.translation[i] += c

        print(self.translation)

        self.update()

    def rotate(self, vector):
        for i, c in enumerate(vector):
            self.rotation[i] += c

        self.update()

    def update(self):
        self.view_mat = self.get_view_matrix()
        self.projection_mat = self.get_projection_matrix()



    def get_view_matrix(self):
        t_x, t_y, t_z = self.translation
        r_x, r_y, r_z = self.rotation

        rotation_x = np.mat([[1, 0, 0, 0],
                           [0, np.cos(r_x), -np.sin(r_x), 0],
                           [0, np.sin(r_x), np.cos(r_x), 0],
                           [0, 0, 0, 1]])

        rotation_y = np.mat([[np.cos(r_y), 0, -np.sin(r_y), 0],
                           [0, 1, 0, 0],
                           [np.sin(r_y), 0, np.cos(r_y), 0],
                           [0, 0, 0, 1]])
        
        rotation_z = np.mat([[np.cos(r_z), -np.sin(r_z), 0, 0],
                           [np.sin(r_z), np.cos(r_z), 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 1]])

        translation = np.mat([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [-t_x, -t_y, -t_z, 1]])

        view_mat = translation * rotation_x * rotation_y * rotation_z

        return view_mat

    def get_projection_matrix(self):
        f = 1 / np.tan(self.fov/2)
        z_far = 100.0
        z_close = 0.1

        projection = np.mat([[f/self.aspect_ratio, 0, 0, 0],
                            [0, f, 0, 0],
                            [0, 0, (z_far + z_close)/(z_close - z_far), (2*z_far*z_close)/(z_close - z_far)],
                            [0, 0, -1, 0]])

        return projection 
