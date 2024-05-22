import numpy as np
from pygame import init 
from camera import Camera

class Base:
    def __init__(self, ctx, position=(0, 0, 0)) -> None:
        self.ctx = ctx
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
        
        t_x, t_y, t_z = self.translation
        r_x, r_y, r_z = self.rotation

        rotation_x = np.mat([[1, 0, 0, 0],
                           [0, np.cos(r_x), -np.sin(r_x), 0],
                           [0, np.sin(r_y), np.cos(r_y), 0],
                           [0, 0, 0, 1]])

        rotation_y = np.mat([[np.cos(r_y), 0, -np.sin(r_y), 0],
                           [0, 1, 0, 0],
                           [np.sin(r_y), 0, np.cos(r_y), 0],
                           [0, 0, 0, 1]])
        
        rotation_z = np.mat([[np.cos(r_z), -np.sin(r_z), 0, 0],
                           [np.sin(r_z), np.cos(r_z), 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 1]])

        translation = np.mat([[1, 0, 0, t_x],
                               [0, 1, 0, t_y],
                               [0, 0, 1, t_z],
                               [0, 0, 0, 1]])

        self.model_mat = np.identity(4) * translation * rotation_x * rotation_y * rotation_z
       

        self.shader_program['model_mat'].write(np.asarray(self.model_mat).astype('f4')) 

    def render(self, camera):
        self.update()
        self.shader_program['view_mat'].write(np.asarray(camera.get_view_matrix()).astype('f4'))
        self.shader_program['projection_mat'].write(np.asarray(camera.get_projection_matrix()).astype('f4'))
        self.vao.render()

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
        # from link
        vertices = [(-0.3, -0.3, 0.3), (0.3, -0.3,  0.3), (0.3,  0.3,  0.3), (-0.3, 0.3,  0.3),
                    (-0.3, 0.3, -0.3), (-0.3, -0.3, -0.3), (0.3, -0.3, -0.3), (0.3, 0.3, -0.3)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]

        triangles = [vertices[ind] for triangle in indices for ind in triangle]
        
        return np.array(triangles, dtype='f4')

