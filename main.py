import kivy

kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import serial

# for now, use a global for blink speed (better implementation TBD):
speed = 1.0

# Set up GPIO:
beepPin = 17
ledPin = 27
buttonPin = 22
flashLedPin = 10



while True:
    global arduino
    try:
        arduino = serial.Serial("COM4", 9600, write_timeout=0.0001)
        print('Порт: %s' % arduino.name)
        break
    except serial.SerialException:
        print("порт %s ошибка !!!")


def write(data):
    try:
        if arduino.isOpen():
            arduino.write(data)
    except serial.SerialTimeoutException:
        arduino.flushOutput()
        arduino.close()
        arduino.open()
        print("Time out exception !!!")



# Define some helper functions:

# This callback will be bound to the LED toggle and Beep button:
def press_callback(obj):
    print("Button pressed,", obj.text)
    if obj.text == 'BEEP!':
        # turn on the beeper:
        write(b'b@1')

        # schedule it to turn off:
        Clock.schedule_once(buzzer_off, .1)
    if obj.text == 'LED':
        if obj.state == "down":
            print("button on")
            write(b'l@1')
        else:
            print("button off")
            write(b'l@0')


def buzzer_off(dt):
    if arduino.isOpen():
        arduino.reset_output_buffer()
        write(b'b@0')



# Toggle the flashing LED according to the speed global
# This will need better implementation
def flash(dt):
    global speed
    write(b'c@%d' % speed)
    Clock.schedule_once(flash, 0.2)


# This is called when the slider is updated:
def update_speed(obj, value):
    global speed
    print("Updating speed to:" + str(obj.value))
    speed = obj.value


# Modify the Button Class to update according to GPIO input:
class InputButton(Button):
    def update(self, dt):
        if arduino.isOpen():
            if arduino.read() == b'1':
                self.state = 'normal'
            else:
                self.state = 'down'



class MyApp(App):
    def build(self):
        # Set up the layout:
        layout = GridLayout(cols=5, spacing=30, padding=30, row_default_height=150)

        # Make the background gray:
        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(800, 600), pos=layout.pos)

        # Instantiate the first UI object (the GPIO input indicator):
        inputDisplay = InputButton(text="Input")

        # Schedule the update of the state of the GPIO input button:
        Clock.schedule_interval(inputDisplay.update, 1.0 / 10.0)

        # Create the rest of the UI objects (and bind them to callbacks, if necessary):
        outputControl = ToggleButton(text="LED")
        outputControl.bind(on_press=press_callback)
        beepButton = Button(text="BEEP!")
        beepButton.bind(on_press=press_callback)
        wimg = Image(source='logo.png')
        speedSlider = Slider(orientation='vertical', min=1, max=30, value=speed)
        speedSlider.bind(on_touch_move=update_speed)

        # Add the UI elements to the layout:
        layout.add_widget(wimg)
        layout.add_widget(inputDisplay)
        layout.add_widget(outputControl)
        layout.add_widget(beepButton)
        layout.add_widget(speedSlider)

        # Start flashing the LED
        Clock.schedule_once(flash, 0.2)

        return layout


if __name__ == '__main__':
    MyApp().run()
