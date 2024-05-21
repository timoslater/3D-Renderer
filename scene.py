class Scene:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.objects = []

    def add_object(self, *obj_classes):
        for obj_class in obj_classes:
            self.objects.append(obj_class(self.engine.ctx))

    def get_objects(self):
        def all_objects():
            for obj in self.objects:
                yield obj
        yield from all_objects()

    def destroy_all(self):
        for obj in self.objects:
            obj.destroy()

        self.objects = []
