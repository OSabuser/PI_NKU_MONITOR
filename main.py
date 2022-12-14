# 11_10_2022 AKIMOV DMITRY, MACH UNIT LLC

import pyglet
from pyglet import image
from pyglet.window import Window
from pyglet.sprite import Sprite
from pyglet.gl import *

import serial
from serial import SerialException

uart0_port_name = '/./dev/ttyS3'
uart0_baud = 115200

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

    for element in range(1, 6):
        gifs.append(Sprite(pyglet.resource.animation("{0}.gif".format(element)), x=0, y=900, group=foreground))

    arrows.append(Sprite(image.load('UP.png'), x=140, y=515, group=foreground))
    arrows.append(Sprite(image.load('DOWN.png'), x=140, y=515, group=foreground))

    animation = gifs[0]
    arrow_img = arrows[0]

    win = Window(width=480, height=1920, fullscreen=False)
    win.set_mouse_visible(visible=True)

    while True:
        try:
            ser = serial.Serial(port=uart0_port_name, baudrate=uart0_baud)  # open serial port
        except SerialException:
            print('Serial port connection error!\n')
            pass
        else:
            break

    floor_state = ['0', '0']
    arrow_state = ['0', '0']
    ok_list = ('1', '2', '3', '4', '5')
    can_refresh = False
    floor_number = ''
    direction = ''
    animation.visible = False
    arrow_img.visible = False

    batch = pyglet.graphics.Batch()
    back_img = Sprite(image.load('BACK.png'), x=0, y=0, group=background, batch=batch)
    logo_img = Sprite(pyglet.resource.animation("LOGO.gif"), x=90, y=1500, group=foreground, batch=batch)
    qr_img = Sprite(image.load("QR.png"), x=80, y=80, group=foreground, batch=batch)


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
                idx = int(floor_state[0]) - 1
                if idx in range(0, 5):
                    animation.visible = True
                    animation = gifs[idx]

            if arrow_state[0] is not arrow_state[1]:  # Draw arrow
                if arrow_state[0] == 'UP':
                    arrow_img.visible = True
                    arrow_img = arrows[0]
                elif arrow_state[0] == 'DL':
                    arrow_img.visible = True
                    arrow_img = arrows[1]
                elif arrow_state[0] == 'NN':
                    arrow_img.visible = False

            floor_number = ''
            direction = ''
            floor_state[1] = floor_state[0]
            arrow_state[1] = arrow_state[0]


    def draw_everything(dt):
        win.clear()
        batch.draw()
        arrow_img.draw()
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
