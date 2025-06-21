from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty

from widgets.font_scale_label import FontScaleLabel


Builder.load_file("widgets/message_widget/message_widget.kv")


class MessageWidget(FontScaleLabel):
    HELLO = StringProperty("Привет, сначала выбери скорость, а потом нажми на треугольник!")
    RELAX = StringProperty("Расслабься и наблюдай")
    FINISH = StringProperty("Посмотри, как красиво!\nМожешь нажать на треугольник, чтобы начать заново.")

    finish_message_trigger = ObjectProperty()

    def on_kv_post(self, base_widget):
        self.get_hello_message()

    def get_hello_message(self):
        self.text = self.HELLO

    def get_relax_message(self):
        self.text = self.RELAX

    def get_finishing_message(self, *args):
        self.text = self.FINISH

    def run_finishing_message(self, dt):
        Clock.schedule_once(self.get_finishing_message, dt)

    def cancel_finishing_message(self):
        Clock.unschedule(self.get_finishing_message)
        self.get_hello_message()

