from kivy.app import App
from kivy.lang import Builder
from instruments.serial_posts import serial_ports
from kivy.uix.actionbar import ActionButton, ActionBar, ActionGroup, ActionView, ActionPrevious
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

Builder.load_file('kv/stile.kv')

import serial
import math

r = 0
g = 0
b = 0

label_text = 'Arduino no connect!!!'






def write(data):
    try:
        global label_text
        if 'arduino' in globals():
            arduino.write(data)
            myApp.label.text = "Connected"
        else:

            myApp.label.text = "No connected"
    except serial.SerialTimeoutException:
        arduino.flushOutput()
        arduino.close()
        arduino.open()
        print("Time out exception !!!")





class MyApp(App):

    def call_back(self, button):
        port = button.text
        global arduino
        try:

            arduino = serial.Serial(port, 115200, timeout=0.01)
            print('Порт: %s' % arduino.name)

        except serial.SerialException:
                print("порт %s ошибка !!!")

    def build(self):

        layout = GridLayout(cols=4, spacing=30, padding=30, row_default_height=150)
        ser_ports = serial_ports()

        self.label = Label(text=label_text)
        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(1023, 840), pos=layout.pos)
        wimg = Image(source='logo.png')
        rSlider = Slider(orientation='vertical', min=0, max=255, value=r)
        gSlider = Slider(orientation='vertical', min=0, max=255, value=g)
        bSlider = Slider(orientation='vertical', min=0, max=255, value=b)
        btn = Button(text="Exit", size_hint_y=None, height=100)
        actionBar = ActionBar(size_hint_x=None, width=150)
        actionView = ActionView(action_previous=ActionPrevious(with_previous=False,))
        actionBar.add_widget(actionView)
        for port in ser_ports:
            actionView.add_widget(ActionButton(text=port, size_hint=(None, 1), width=50, on_release=self.call_back))

        btn.bind(on_press=self.exitApp)
        rSlider.bind(on_touch_move=self.update_r)
        gSlider.bind(on_touch_move=self.update_g)
        bSlider.bind(on_touch_move=self.update_b)

        layout.add_widget(wimg)
        layout.add_widget(rSlider)
        layout.add_widget(gSlider)
        layout.add_widget(bSlider)
        layout.add_widget(actionBar)
        layout.add_widget(btn)
        layout.add_widget(self.label)

        return layout

    def on_status(self, instance, new_value):
        self.label.text = label_text

    def exitApp(self, value):
       self.stop()

    def update_r(self,obj, value):
        global r
        print("r to:" + str(math.floor(obj.value)))
        r = math.floor(obj.value)
        write(b'r%d' % r)


    def update_g(self, obj, value):
        global r
        print("g to:" + str(math.floor(obj.value)))
        g = math.floor(obj.value)
        write(b'r%d' % g)

    def update_b(self, obj, value):
        global r
        print("b to:" + str(math.floor(obj.value)))
        b = math.floor(obj.value)
        write(b'r%d' % b)

if __name__ == '__main__':
    myApp = MyApp()
    myApp.run()