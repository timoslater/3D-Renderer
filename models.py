import numpy as np 

class Triangle:
    def __init__(self, ctx, position=(0, 0, 0)) -> None:
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.position = position
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.model_mat = np.identity(4)

    def update(self, translation=(0, 0, 0)):
        t_x, t_y, t_z = translation 

        translate_mat = np.mat([[1, 0, 0, t_x],
                               [0, 1, 0, t_y],
                               [0, 0, 1, t_z],
                               [0, 0, 0, 1]])

        self.model_mat = self.model_mat * translate_mat
        

        self.shader_program['model_mat'].write(np.asarray(self.model_mat).astype('f4')) 

    def render(self):
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
