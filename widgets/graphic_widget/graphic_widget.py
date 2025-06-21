from random import choice

from kivy.clock import Clock
from kivy.graphics import Ellipse, Line
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.uix.widget import Widget

from widgets.message_widget.message_widget import MessageWidget
from widgets.timer_widget.timer_widget import TimerWidget
from configs.app_config import AppConfig


Builder.load_file("widgets/graphic_widget/graphic_widget.kv")


class GraphicWidget(Widget):
    message_widget : MessageWidget = ObjectProperty()
    timer_widget : TimerWidget = ObjectProperty()

    peaks = ListProperty()
    v1_x, v1_y, v2_x, v2_y, v3_x, v3_y = (NumericProperty() for i in range(6))
    point = ListProperty()
    count = NumericProperty(AppConfig.COUNT_POINTS)
    rad = NumericProperty(AppConfig.RAD_POINTS)
    is_in_progress = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.bind(pos=self.update)
        self.bind(size=self.update)

    def update(self, *args):
        self.canvas.clear()
        pos_x, pos_y = self.pos
        size_x, size_y = self.size

        self.v1_x = pos_x
        self.v1_y = pos_y

        self.v3_x = pos_x + size_x
        self.v3_y = pos_y

        self.v2_x = (self.v3_x + self.v1_x) / 2
        self.v2_y = (
            (self.v3_x - self.v1_x) ** 2 - ((self.v3_x - self.v1_x) / 2) ** 2
        ) ** 0.5 + self.v1_y

        self.peaks = [
            (self.v1_x, self.v1_y),
            (self.v2_x, self.v2_y),
            (self.v3_x, self.v3_y),
        ]

        with self.canvas:
            Line(points = self.peaks, close=True,)

    def get_new_point(self, dt):
        peak = choice(self.peaks)
        new_point_x = (peak[0] + self.point[0]) / 2
        new_point_y = (peak[1] + self.point[1]) / 2
        self.point = (new_point_x, new_point_y)

        with self.canvas:
            Ellipse(
                pos=(self.point[0] - self.rad / 2, self.point[1] - self.rad / 2),
                size=(self.rad, self.rad),
            )

    def run_new_point(self, i):
        Clock.schedule_once(self.get_new_point, i * (self.timer_widget.current_time / self.count))

    def cancel_new_point(self):
        Clock.unschedule(self.get_new_point)

    def restart_game(self):
        self.cancel_new_point()
        self.timer_widget.cancel_timer()
        self.message_widget.cancel_finishing_message()

        self.update()
        self.is_in_progress = False

    def on_touch_down(self, touch):
        y_1 = (touch.x - self.v1_x) * (self.v2_y - self.v1_y) / (
            self.v2_x - self.v1_x
        ) + self.v1_y
        y_2 = (touch.x - self.v2_x) * (self.v3_y - self.v2_y) / (
            self.v3_x - self.v2_x
        ) + self.v2_y
        y_3 = self.v1_y

        if touch.y < y_1 and touch.y < y_2 and touch.y > y_3:
            self.point = (touch.x, touch.y)
            if not self.is_in_progress:
                self.is_in_progress = True
                self.message_widget.get_relax_message()
                self.timer_widget.start_timer()

                for i in range(self.count):
                    if i != 0:
                        self.run_new_point(i)

                self.message_widget.run_finishing_message(self.timer_widget.current_time)

            else:
                self.restart_game()
