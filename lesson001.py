import time
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout

from  plyer import battery
from instruments.serial_custom import SoftSerial
import math


# Builder.load_file('my.kv')

class MyBoxLayout(BoxLayout):
    def get_value(self, value, id):
        if id is 1:
            command = b'r' + (chr(math.floor(value))).encode('utf-8')
        else:
            command = b'g' + (chr(math.floor(value))).encode('utf-8')


        print(command)
        # arduino.change_color((math.floor(value), 0, 0))
        # arduino.ser.write(bytes(command))


class MyApp(App):
    count = NumericProperty()
    val = NumericProperty()
    def build(self):
        return MyBoxLayout()


#arduino = SoftSerial("COM7")

app = MyApp()
app.run()