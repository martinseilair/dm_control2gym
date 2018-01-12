import pyglet

class DmControlViewer:
    def __init__(self, width, height):
        self.window = pyglet.window.Window(width=width, height=height, display=None)
        self.width = width
        self.height = height

    def update(self, pixel):
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        pyglet.image.ImageData(self.width, self.height, 'RGB', pixel.tobytes(), pitch=self.width * -3).blit(0,0)
        self.window.flip()

    def close(self):
        self.window.close()
