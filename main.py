# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyglet
from pyglet import image
from pyglet.window import Window
from pyglet.sprite import Sprite
from pyglet import app
from pyglet.gl import *
from pyglet.window import key


def main():
    # Set alpha blending config
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    batch = pyglet.graphics.Batch()
    background = pyglet.graphics.OrderedGroup(0)
    foreground = pyglet.graphics.OrderedGroup(1)

    sprites = [Sprite(image.load('BACK.png'), batch=batch, x=0, y=0, group=background)]

    keys = key.KeyStateHandler()
    win = Window(width=800, height=600, vsync=False)

    @win.event
    def on_draw():
        win.clear()
        batch.draw()

    @win.event
    def on_key_press(symbol, modifiers):
        current_key = keys
        # Вставка нового изображения
        if current_key[key._1]:

            if len(sprites) == 3:
                sprites[1].delete()
                sprites.pop(1)

            animation = Sprite(pyglet.resource.animation('1_2.gif'), batch=batch, x=50, y=50, group=foreground)
            sprites.insert(1, animation)

        elif current_key[key._2]:
            if len(sprites) == 2:
                sprites[1].delete()
                sprites.pop(1)

            animation = Sprite(pyglet.resource.animation('2_1.gif'), batch=batch, x=50, y=50, group=foreground)
            sprites.insert(1, animation)

        @animation.event
        def on_animation_end():
            print("Гифка закончилась!")
            if len(sprites) == 2:
                sprites[1].delete()
                sprites.pop(1)


    win.push_handlers(on_draw, on_key_press, keys)
    app.run()


if __name__ == '__main__':
    main()
