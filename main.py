from kivy.app import App
from kivy.config import Config

from widgets.container.container import Container

Config.set("graphics", "resizable", 1)
Config.set("graphics", "height", 510)
Config.set("graphics", "width", 250)


class TriangleApp(App):
    def build(self):
        return Container()


if __name__ == "__main__":
    TriangleApp().run()
