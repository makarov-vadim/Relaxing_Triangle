from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from widgets.graphic_widget.graphic_widget import GraphicWidget
from widgets.timer_widget.timer_widget import TimerWidget

Builder.load_file("widgets/speed_control/speed_control.kv")

class SpeedControl(BoxLayout):
    timer_widget: TimerWidget = ObjectProperty()
    graphic_widget: GraphicWidget = ObjectProperty()

    def speed_down(self):
        if not self.graphic_widget.is_in_progress:
            self.timer_widget.add_time()

    def speed_up(self):
        if not self.graphic_widget.is_in_progress:
            self.timer_widget.reduce_time()