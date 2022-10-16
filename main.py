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

    gifs = []
    arrows = []

    for element in range(1, 6):
        gifs.append(Sprite(pyglet.resource.animation(f"{element}.gif"), x=50, y=50, group=foreground))

    arrows.append(Sprite(image.load('UP.png'), x=150, y=650, group=foreground))
    arrows.append(Sprite(image.load('DOWN.png'), x=150, y=650, group=foreground))

    animation = gifs[0]
    arrow = arrows[0]

    win = Window(width=480, height=1920, fullscreen=True)
    win.set_mouse_visible(visible=False)

    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)  # open serial port
    print(f"Use instance: {ser.name}")  # check which port was really used

    floor_state = ['0', '0']
    ok_list = ('1', '2', '3', '4', '5')
    can_refresh = False


    def second_thread(dt):
        global animation
        data_str = ''
        # обработка UART посылок from MCU
        if ser.inWaiting() > 0:
            # read the bytes and convert from binary array to ASCII
            data_str = ser.read(ser.inWaiting()).decode('ascii')

        if data_str in ok_list:

            floor_state[0] = data_str

            if floor_state[0] is not floor_state[1]:
                idx = int(floor_state[0])
                if idx in range(0, 5):
                    animation = gifs[idx]

            data_str = ''
            print(floor_state)
            floor_state[1] = floor_state[0]


    def draw_everything(dt):
        win.clear()
        back_img.draw()
        arrow.draw()
        animation.draw()


    @win.event
    def on_draw():
        draw_everything(None)


    @animation.event
    def on_animation_end():
        global can_refresh
        can_refresh = True


    pyglet.clock.schedule_interval(second_thread, 1)
    pyglet.clock.schedule_interval(draw_everything, 1 / 60)
    pyglet.app.run()
