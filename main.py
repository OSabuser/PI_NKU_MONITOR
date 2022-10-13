# 11_10_2022 AKIMOV DMITRY, MACH UNIT LLC

import pyglet
from pyglet import image
from pyglet.window import Window
from pyglet.sprite import Sprite
from pyglet.gl import *
import serial

if __name__ == '__main__':
    # Set alpha blending config
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    batch = pyglet.graphics.Batch()
    background = pyglet.graphics.OrderedGroup(0)
    foreground = pyglet.graphics.OrderedGroup(1)

    back_img = Sprite(image.load('BACK.png'), x=0, y=0, group=background)
    src_gif = pyglet.resource.animation(f"1.gif")
    animation = Sprite(src_gif,
                       x=50, y=50,
                       batch=batch,
                       group=foreground)

    win = Window(width=480, height=480, vsync=False, fullscreen=True)
    win.set_mouse_visible(visible=False)

    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)  # open serial port
    print(f"Use instance: {ser.name}")  # check which port was really used

    floor_state = ['0', '0']
    ok_list = ('1', '2', '3', '4', '5')
    data_str = []

    @win.event
    def on_draw():
        win.clear()
       # back_img.draw()
       # animation.draw()
        batch.draw()

    @animation.event
    def on_animation_end():
        animation.visible = False


    def update(dt):
        print("TEST!")
        pyglet.clock.schedule_interval(update, 1)


    pyglet.app.run()






