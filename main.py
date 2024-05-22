import pygame as pg 
import moderngl as mgl
import sys, os
from models import Triangle
from scene import Scene

class Engine:
    def __init__(self, dimensions=(1920, 1080), background_color=(0.196, 0.204, 0.216, 1), max_fps=60) -> None:
        
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(dimensions, flags=pg.OPENGL | pg.DOUBLEBUF)

        self.clock = pg.time.Clock()
        self.MAX_FPS = max_fps
        self.BG_COLOR = background_color

        self.ctx = mgl.create_context()
        self.scene = Scene(self)
        self.scene.add_object(Triangle)
        
        print(self.ctx.info['GL_RENDERER'])

        self.dt = 0


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy_all()
                pg.quit()
                sys.exit(0)

        keys = pg.key.get_pressed()
        speed = 0.005 * self.dt
        if keys[pg.K_w]:
                self.scene.translate_all((0, 1*speed, 0))
        if keys[pg.K_a]:
                self.scene.translate_all((-1*speed, 0, 0))
        if keys[pg.K_s]:
                self.scene.translate_all((0, -1*speed, 0))
        if keys[pg.K_d]:
                self.scene.translate_all((1*speed, 0, 0))

    def render(self):
        self.ctx.clear(color=self.BG_COLOR)
        for obj in self.scene.get_objects():
            obj.render()

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

