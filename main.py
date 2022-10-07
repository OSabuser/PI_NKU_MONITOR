# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyglet
from pyglet import image
from pyglet.window import Window
from pyglet import app
from pyglet.gl import *


def main():


    # Set alpha blending config
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    alpha_img_1 = pyglet.resource.image('2.png')
    background = pyglet.resource.image('BACK.png')

    alpha_1 = pyglet.sprite.Sprite(alpha_img_1, x=450, y=250)
    back_1 = pyglet.sprite.Sprite(background, x=0, y=0)

    animation = pyglet.image.load_animation('giphy.gif')
    bina = pyglet.image.atlas.TextureBin()
    animation.add_to_texture_bin(bina)
    sprite = pyglet.sprite.Sprite(img=animation, x=150, y=250)

    win = Window(width=800, height=600)

    @win.event
    def on_draw():


        back_1.draw()
        alpha_1.draw()
        sprite.draw()

    app.run()


if __name__ == '__main__':
    main()
