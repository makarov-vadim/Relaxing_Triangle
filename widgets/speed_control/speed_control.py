from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from widgets.graphic_widget.graphic_widget import GraphicWidget
from widgets.timer_widget.timer_widget import TimerWidget
from widgets.font_scale_label import FontScaleLabel
from widgets.font_scale_button import FontScaleButton

Builder.load_file("widgets/speed_control/speed_control.kv")

class SpeedControl(BoxLayout):
    """Виджет выбора скорости анимации с помощью клавиш «-» и «+»"""
    timer_widget: TimerWidget = ObjectProperty()
    graphic_widget: GraphicWidget = ObjectProperty()

    speed_label: FontScaleLabel = ObjectProperty()
    minus_button: FontScaleButton = ObjectProperty()
    plus_button: FontScaleButton = ObjectProperty()

    def speed_down(self):
        if not self.graphic_widget.is_in_progress:
            self.timer_widget.add_time()

    def speed_up(self):
        if not self.graphic_widget.is_in_progress:
            self.timer_widget.reduce_time()