from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from widgets.graphic_widget.graphic_widget import GraphicWidget
from widgets.message_widget.message_widget import MessageWidget
from widgets.speed_control.speed_control import SpeedControl
from widgets.timer_widget.timer_widget import TimerWidget

Builder.load_file("widgets/container/container.kv")

class Container(BoxLayout):
    """Основное окно приложения"""
    message_widget: MessageWidget = ObjectProperty()
    timer_widget: TimerWidget = ObjectProperty()
    graphic_widget: GraphicWidget = ObjectProperty()
    speed_control : SpeedControl = ObjectProperty()