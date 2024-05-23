import glm
from math import pi

class Camera:
    def __init__(self, engine, fov) -> None:
        self.engine = engine
        self.translation = [0, 0, 0]    
        self.rotation = [0, 0, 0]
        self.fov = fov
        self.aspect_ratio = engine.get_aspect_ratio()
        self.direction = glm.vec3(0)
        self.right = glm.vec3(1, 0, 0)
        self.up = glm.vec3(0, 1, 0)

        self.projection_mat = self.get_projection_matrix()
        self.view_mat = self.get_view_matrix()

    def translate(self, vector):
        for i, c in enumerate(vector):
            self.translation[i] += c

        self.update()

    def rotate(self, vector):
        for i, c in enumerate(vector):
            self.rotation[i] += c

        self.update()

    def update(self):
        mouse_x, mouse_y = self.engine.mouse.get_pos()
        print(mouse_x, mouse_y)
        self.engine.mouse.set_pos(self.engine.dimensions[0]/2, self.engine.dimensions[1]/2)

        self.rotation[2] += self.engine.SENS * self.engine.dt * (self.engine.dimensions[0]/2 - mouse_x)
        self.rotation[1] += self.engine.SENS * self.engine.dt * (self.engine.dimensions[1]/2 - mouse_y)
        self.direction = glm.vec3(glm.cos(self.rotation[1])*glm.sin(self.rotation[2]), glm.sin(self.rotation[1]), glm.cos(self.rotation[1]) * glm.cos(self.rotation[2]))
        self.right = glm.vec3(glm.sin(self.rotation[2] - pi / 2), 0, glm.cos(self.rotation[2] - pi / 2))
        self.up = glm.cross(self.right, self.direction)

        self.view_mat = self.get_view_matrix()
        self.projection_mat = self.get_projection_matrix()




    def get_view_matrix(self):

        return glm.lookAt(glm.vec3(*self.translation), glm.vec3(*self.translation) + self.direction, self.up)

    def get_projection_matrix(self):
        # f = 1 / np.tan(np.radians(self.fov)/2)
        z_far = 100.0
        z_close = 0.1

        # projection = Matrix44([[f/self.aspect_ratio, 0, 0, 0],
        #                     [0, f, 0, 0],
        #                     [0, 0, (z_far + z_close)/(z_close - z_far), (2*z_far*z_close)/(z_close - z_far)],
        #                     [0, 0, -1, 0]], dtype='f4')
        # print(glm.perspective(glm.radians(self.fov), self.aspect_ratio, 0.1, 100))
        # return projection

        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, 0.1, 100)
