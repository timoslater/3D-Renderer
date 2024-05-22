from math import pi
import pygame as pg 
import moderngl as mgl
import sys, os
from models import Base, Cube
from scene import Scene
from camera import Camera

class Engine:
    def __init__(self, dimensions=(1280, 720), background_color=(0.196, 0.204, 0.216, 1), max_fps=60) -> None:
        
        pg.init()

        self.dimensions = dimensions

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.dimensions, flags=pg.OPENGL | pg.DOUBLEBUF)

        self.clock = pg.time.Clock()
        self.MAX_FPS = max_fps
        self.BG_COLOR = background_color

        self.ctx = mgl.create_context()
        self.scene = Scene(self)
        self.scene.add_object(Cube)
        self.camera = Camera(self, 50*(pi/180)) 

        print(self.ctx.info['GL_RENDERER'])

        self.dt = 0

    def get_aspect_ratio(self):
        return self.dimensions[0] / self.dimensions[1]


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy_all()
                pg.quit()
                sys.exit(0)

        keys = pg.key.get_pressed()
        speed = 0.005 * self.dt
        if keys[pg.K_w]:
                self.camera.translate((0, 0, 1*speed))
        if keys[pg.K_a]:
                self.camera.translate((-1*speed, 0, 0))
        if keys[pg.K_s]:
                self.camera.translate((0, 0, -1*speed)) 
        if keys[pg.K_d]:
                self.camera.translate((1*speed, 0, 0))
            
        if keys[pg.K_n]:
                self.camera.rotate((0, -1*speed, 0)) 
        if keys[pg.K_m]:
                self.camera.rotate((0, 1*speed, 0))

        if keys[pg.K_i]:
                self.scene.translate_all((0, 1*speed, 0))
        if keys[pg.K_j]:
                self.scene.translate_all((-1*speed, 0, 0))
        if keys[pg.K_k]:
                self.scene.translate_all((0, -1*speed, 0))
        if keys[pg.K_l]:
                self.scene.translate_all((1*speed, 0, 0))
        # if keys[pg.K_j]:
        #         self.scene.rotate_all((0, 1*speed, 0))
        # if keys[pg.K_l]:
        #         self.scene.rotate_all((0, -1*speed, 0))

    def render(self):
        self.ctx.clear(color=self.BG_COLOR)
        for obj in self.scene.get_objects():
            obj.render(self.camera)

        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.render()
            self.dt = self.clock.tick(self.MAX_FPS)

if __name__ == "__main__":

    if sys.platform == "linux":
        os.environ['SDL_VIDEODRIVER'] = 'x11'

    engine = Engine()
    engine.run()

