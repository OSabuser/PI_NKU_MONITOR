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

    floor_state = ['', '']
    temp_floor_sprite = Sprite(pyglet.resource.animation(f"1.gif"),
                               x=50,
                               y=50,
                               batch=batch,
                               group=foreground)
    temp_floor_sprite.visible = False

    while True:
        pyglet.clock.tick()
        # обработка UART посылок from MCU
        if ser.inWaiting() > 0:
            # read the bytes and convert from binary array to ASCII
            data_str = ser.read(ser.inWaiting()).decode('ascii')

            match data_str:
                # Floor number updating
                case '0' | '1' | '2' | '3' | '4' | '5':
                    floor_state[0] = data_str
                    if floor_state[0] is not floor_state[1] and floor_state[1] != '':
                        if temp_floor_sprite in sprites:
                            sprites.remove(temp_floor_sprite)
                            temp_floor_sprite.delete()

                        animation = Sprite(pyglet.resource.animation(f"{floor_state[1]}_{floor_state[0]}.gif"),
                                           batch=batch,
                                           x=50, y=50,
                                           group=foreground)
                        sprites.append(animation)
                        test_floor = floor_state[0]

                        @animation.event
                        def on_animation_end():
                            global temp_floor_sprite, animation
                            if animation in sprites:
                                sprites.remove(animation)
                                animation.delete()
                                print("Гифка закончилась!")

                            temp_floor_sprite = Sprite(image.load(f"{test_floor}.gif"),
                                                       x=50, y=50,
                                                       batch=batch,
                                                       group=foreground)
                            sprites.append(temp_floor_sprite)

                    elif floor_state[0] == floor_state[1]:
                        if temp_floor_sprite in sprites:
                            sprites.remove(temp_floor_sprite)
                            temp_floor_sprite.delete()

                        temp_floor_sprite = Sprite(pyglet.resource.animation(f"{test_floor}.gif"),
                                                   x=50, y=50,
                                                   batch=batch,
                                                   group=foreground)
                        sprites.append(temp_floor_sprite)

                    print(floor_state)
                    floor_state[1] = floor_state[0]
                case _:
                    print(data_str)
                    print("Undefined value!!\n")

        # Отрисовка изображения
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()

