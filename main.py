from kivy.app import App
from kivy.config import Config
from random import choice
from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.graphics import Line, Ellipse

Config.set("graphics", "resizable", 1)
Config.set("graphics", "height", 510)
Config.set("graphics", "width", 250)


class MyMessage(Label):
    def get_message(self, text_id, *args):
        messages = [
            "Привет, сначала выбери скорость, а потом нажми на треугольник!",
            "Расслабся и наблюдай",
            "Посмотри, как красиво!\nМожешь нажать на треугольник, чтобы начать заново.",
        ]
        self.message_text = messages[text_id]

    def on_kv_post(self, base_widget):
        self.get_message(0)

    def get_finish_message(self, dt):
        self.finish_message = Clock.create_trigger(partial(self.get_message, 2), dt)
        self.finish_message()

    def cancel_finish_message(self):
        Clock.unschedule(self.finish_message)


class MyTimer(Label):
    my_start_time = NumericProperty(120)
    my_time = NumericProperty(120)

    def change_time_text(self, *args):
        minutes = int(self.my_time) // 60
        m = str(minutes) if minutes > 9 else "0" + str(minutes)
        seconds = int(self.my_time) % 60
        s = str(seconds) if seconds > 9 else "0" + str(seconds)
        self.time_text = m + ":" + s

    def on_kv_post(self, base_widget):
        self.change_time_text()

    def change_time(self, *args):
        if self.my_time > 0:
            self.my_time -= 1
            self.change_time_text()

    def start_timer(self):

        for i in range(int(self.my_time)):
            Clock.schedule_once(self.change_time, i)

    def cancel_timer(self):
        Clock.unschedule(self.change_time)


class MyGraphicWidget(Widget):
    v1_x, v1_y, v2_x, v2_y, v3_x, v3_y = (NumericProperty() for i in range(6))
    peaks = ListProperty()
    point = ListProperty()
    # count = NumericProperty(10000)
    count = NumericProperty(5000)
    rad = NumericProperty(2)
    flag = BooleanProperty(True)

    def on_kv_post(self, base_widget):
        self.bind(pos=self.update)
        self.bind(size=self.update)

    def update(self, *args):
        self.canvas.clear()

        self.v1_x = self.pos[0]
        self.v1_y = self.pos[1]

        self.v3_x = self.pos[0] + self.size[0]
        self.v3_y = self.pos[1]

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
            Line(
                points=(
                    self.v1_x,
                    self.v1_y,
                    self.v2_x,
                    self.v2_y,
                    self.v3_x,
                    self.v3_y,
                ),
                close=True,
            )

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

    def restart_game(self):
        Clock.unschedule(self.get_new_point)
        self.my_message.cancel_finish_message()
        self.my_timer.cancel_timer()

        self.update()
        self.my_message.get_message(0)
        self.my_timer.my_time = self.my_timer.my_start_time
        self.my_timer.change_time_text()
        self.flag = True

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
            if self.flag:
                self.flag = False
                self.my_message.get_message(1)
                self.my_timer.start_timer()
                for i in range(self.count):
                    if i == 0:
                        continue
                        # self.get_touch_point()
                    else:
                        Clock.schedule_once(
                            self.get_new_point, i * (self.my_timer.my_time / self.count)
                        )

                self.my_message.get_finish_message(self.my_timer.my_time)

            else:
                self.restart_game()


class SpeedControl(BoxLayout):
    def speed_down(self):
        if self.my_graphic_widget.flag:
            self.my_timer.my_time += 30 - self.my_timer.my_time % 30
            self.my_timer.change_time_text()

    def speed_up(self):
        if self.my_graphic_widget.flag:
            if self.my_timer.my_time > 30:
                self.my_timer.my_time -= 30
            else:
                self.my_timer.my_time = 1
            self.my_timer.change_time_text()


class Container(BoxLayout):
    pass


class TriangleApp(App):
    def build(self):
        return Container()


if __name__ == "__main__":
    TriangleApp().run()
