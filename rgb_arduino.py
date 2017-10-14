from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.core.window import Window


import serial
import math

r = 0
g = 0
b = 0

while True:
    global arduino
    try:
        arduino = serial.Serial("COM4", 115200, timeout=0.01)
        print('Порт: %s' % arduino.name)
        break
    except serial.SerialException:
        print("порт %s ошибка !!!")

def update_r(obj, value):
    global r
    print("r to:" + str(math.floor(obj.value)))
    r = math.floor(obj.value)
    write(b'r%d' % r)



def update_g(obj, value):
    global r
    print("g to:" + str(math.floor(obj.value)))
    g = math.floor(obj.value)
    write(b'r%d' % g)

def update_b(obj, value):
    global r
    print("b to:" + str(math.floor(obj.value)))
    b = math.floor(obj.value)
    write(b'r%d' % b)



def write(data):
    try:
        if arduino.isOpen():
            arduino.write(data)
    except serial.SerialTimeoutException:
        arduino.flushOutput()
        arduino.close()
        arduino.open()
        print("Time out exception !!!")





class MyApp(App):
    def build(self):

        layout = GridLayout(cols=4, spacing=30, padding=30, row_default_height=150)

        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(800, 600), pos=layout.pos)

        rSlider = Slider(orientation='vertical', min=0, max=255, value=r)
        gSlider = Slider(orientation='vertical', min=0, max=255, value=g)
        bSlider = Slider(orientation='vertical', min=0, max=255, value=b)
        btn = Button(text="Exit")
        btn.bind(on_press=self.exitApp)
        rSlider.bind(on_touch_move=update_r)
        gSlider.bind(on_touch_move=update_g)
        bSlider.bind(on_touch_move=update_b)
        layout.add_widget(rSlider)
        layout.add_widget(gSlider)
        layout.add_widget(bSlider)
        layout.add_widget(btn)
        return layout

    def exitApp(self, value):
       self.stop()

if __name__ == '__main__':
    MyApp().run()