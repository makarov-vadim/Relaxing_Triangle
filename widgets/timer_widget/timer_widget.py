from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty

from widgets.font_scale_label import FontScaleLabel


Builder.load_file("widgets/timer_widget/timer_widget.kv")


class TimerWidget(FontScaleLabel):
    start_time = NumericProperty(120)
    current_time = NumericProperty(120)
    time_text = StringProperty()

    def on_kv_post(self, base_widget):
        self.change_time_text()

    def change_time_text(self):
        minutes = int(self.current_time) // 60
        m = str(minutes) if minutes > 9 else f"0{str(minutes)}"
        seconds = int(self.current_time) % 60
        s = str(seconds) if seconds > 9 else f"0{str(seconds)}"
        self.time_text = f"{m}:{s}"

    def add_time(self, sec=30):
        self.current_time += sec - self.current_time % sec
        self.change_time_text()

    def reduce_time(self, sec=30):
        if self.current_time > sec:
            self.current_time -= sec
        else:
            self.current_time = 1
        self.change_time_text()

    def time_step(self, *args):
        if self.current_time > 0:
            self.current_time -= 1
            self.change_time_text()

    def start_timer(self):
        for i in range(int(self.current_time)):
            Clock.schedule_once(self.time_step, i)

    def cancel_timer(self):
        Clock.unschedule(self.time_step)
        self.current_time = self.start_time
        self.change_time_text()
