from kivy.properties import NumericProperty
from kivy.uix.label import Label


class FontScaleLabel(Label):
    font_scale = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.on_size_change)

    def on_size_change(self, instance, value):
        self.font_size = int(value[1] * self.font_scale)