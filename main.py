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

    back_img = Sprite(image.load('BACK.png'), x=0, y=0, batch=batch, group=background)
    sprites = [back_img]

    win = Window(width=480, height=1920, vsync=False)


    @win.event
    def on_draw():
        win.clear()
        batch.draw()


    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)  # open serial port
    print(f"Use instance: {ser.name}")  # check which port was really used

    floor_state = ['0', '0']
    ok_list = ('1', '2', '3', '4', '5')
    data_str = []

while True:
    pyglet.clock.tick()

    # обработка UART посылок from MCU
    if ser.inWaiting() > 0:
        # read the bytes and convert from binary array to ASCII
        data_str = ser.read(ser.inWaiting()).decode('ascii')

    if data_str in ok_list:
        floor_state[0] = data_str

        if floor_state[0] is not floor_state[1]:
            sprites.append(Sprite(pyglet.resource.animation(f"{floor_state[0]}.gif"),
                                  x=50, y=50,
                                  batch=batch,
                                  group=foreground))

            temp = sprites[1]


            @temp.event
            def on_animation_end():
                global sprites
                if len(sprites) == 2:
                    temp = sprites.pop(1)
                    sprites[1].delete()
                    sprites.append(temp)


            data_str = ''
            print(floor_state)
            floor_state[1] = floor_state[0]

    # Отрисовка изображения
    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
