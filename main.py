# 11_10_2022 AKIMOV DMITRY, MACH UNIT LLC

import pyglet
from pyglet import image
from pyglet.window import Window
from pyglet.sprite import Sprite
from pyglet.gl import *

import serial

# TODO: 1. try, except на критически важные блоки кода
# TODO: 2. Статические изображения + анимации

if __name__ == '__main__':
    # Set alpha blending config
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    background = pyglet.graphics.OrderedGroup(0)
    foreground = pyglet.graphics.OrderedGroup(1)

    gifs = []
    arrows = []

    for element in range(1, 2):
        gifs.append(Sprite(pyglet.resource.animation(f"{element}.gif"), x=0, y=1030, group=foreground))

    #arrows.append(Sprite(image.load('UP.gif'), x=0, y=550, group=foreground))
    #arrows.append(Sprite(image.load('DOWN.gif'), x=0, y=550, group=foreground))

    animation = gifs[0]
    arrow_img = gifs[0]

    win = Window(width=480, height=1920, fullscreen=True)
    win.set_mouse_visible(visible=False)

    ser = serial.Serial(port='/./dev/ttyAMA0', baudrate=115200)  # open serial port

    floor_state = ['0', '0']
    arrow_state = ['0', '0']
    ok_list = ('1', '2', '3', '4', '5')
    can_refresh = False
    floor_number = ''
    direction = ''
    animation.visible = False
    arrow_img.visible = False

    back_img = Sprite(image.load('BACK.png'), x=0, y=0, group=background)
    logo_img = Sprite(pyglet.resource.animation(f"LOGO.gif"), x=90, y=100, group=foreground)

    def second_thread(dt):
        global animation, arrow_img, floor_number, direction

        # UART message handling from MCU
        if ser.inWaiting() > 0:
            # read the bytes and convert from binary array to ASCII
            data_str = ser.read(ser.inWaiting()).decode('ascii')
            # For debug purposes -- > print(data_str)
            if len(data_str) >= 5:
                floor_number = data_str[1]  # Get floor number
                direction = data_str[3:5]  # Get direction state

        if floor_number in ok_list:
            floor_state[0] = floor_number
            arrow_state[0] = direction

            if floor_state[0] is not floor_state[1]:  # Draw floor number
                idx = int(floor_state[0])
                if idx in range(1, 6):
                    animation.delete()
                    animation = Sprite(pyglet.resource.animation(f"{idx}.gif"), x=0, y=1030, group=foreground)
                    animation.visible = True

            if arrow_state[0] is not arrow_state[1]:  # Draw arrow
                if arrow_state[0] == 'UP':
                    arrow_img.delete()
                    arrow_img = Sprite(pyglet.resource.animation('UP.gif'), x=0, y=550, group=foreground)
                    arrow_img.visible = True
                elif arrow_state[0] == 'DL':
                    arrow_img.delete()
                    arrow_img = Sprite(pyglet.resource.animation('DOWN.gif'), x=0, y=550, group=foreground)
                    arrow_img.visible = True
                elif arrow_state[0] == 'NN':
                    if arrow_img.visible:
                        arrow_img.visible = False

            floor_number = ''
            direction = ''
            floor_state[1] = floor_state[0]
            arrow_state[1] = arrow_state[0]


    def draw_everything(dt):
        win.clear()
        back_img.draw()
        logo_img.draw()
        if arrow_img is not None:
            arrow_img.draw()
        if animation is not None:
            animation.draw()


    @win.event
    def on_draw():
        draw_everything(None)


    @animation.event
    def on_animation_end():
        global can_refresh
        can_refresh = True


    pyglet.clock.schedule_interval(second_thread, 0.5)
    pyglet.clock.schedule_interval(draw_everything, 1 / 60)
    pyglet.app.run()
