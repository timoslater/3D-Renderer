import numpy as np
from pygame import init 
from camera import Camera
import moderngl as mgl
import glm 

class Base:
    def __init__(self, engine, position=(0, 0, 0)) -> None:
        self.engine = engine
        self.ctx = engine.ctx
        self.vbo = self.get_vbo()
        self.position = position
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.model_mat = np.identity(4)
        self.rotation = [0, 0, 0]
        self.translation = [0, 0, 0]
        self.update()

    def update(self, translation=(0, 0, 0), rotation=(0, 0, 0)):

        for i, c in enumerate(translation):
            self.translation[i] += c

        for i, c in enumerate(rotation):
            self.rotation[i] += c


    def render(self):
        r_x, r_y, r_z = self.rotation

        model = glm.translate(glm.mat4(), glm.vec3(*self.translation))
        model = glm.rotate(model, r_x, glm.vec3(1, 0, 0))
        model = glm.rotate(model, r_y, glm.vec3(0, 1, 0))
        model = glm.rotate(model, r_z, glm.vec3(0, 0, 1))

        self.shader_program['mvp'].write(self.engine.camera.projection_mat * self.engine.camera.view_mat * model)

        self.vao.render(mgl.LINE_STRIP)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()


    def get_vertex_data(self):
        vertex_data = np.array(
            [(-0.6, -0.8, 0.0),
             (0.6, -0.8, 0.0),
             (0.0, 0.8, 0.0)],
            dtype='f4'
        ) 
        return vertex_data

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, self.vbo, 'in_position')
        return vao

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        return program


class Cube(Base):
    def __init__(self, ctx, position=(0, 0, 0)) -> None:
        super().__init__(ctx, position)

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(vertex_data, dtype='f4')
