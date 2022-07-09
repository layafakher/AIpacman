# gameinput Module

from pygame import joystick, key
from pygame.locals import *

aPixelMove = 5.3
joystick.init()
joystick_count = joystick.get_count()

if(joystick_count > 0):
    joyin = joystick.Joystick(0)
    joyin.init()

def checkInput(p,path=None):
    global joyin, joystick_count
    xaxis = yaxis = 0
    if p.status == 0:
        if joystick_count > 0:
            xaxis = joyin.get_axis(0)
            yaxis = joyin.get_axis(1)
        if key.get_pressed()[K_LEFT] or xaxis < -0.8 or path == 'left':
            p.angle = 180
            p.movex = -aPixelMove
        if key.get_pressed()[K_RIGHT] or xaxis > 0.8 or path == 'right':
            p.angle = 0
            p.movex = aPixelMove
        if key.get_pressed()[K_UP] or yaxis < -0.8 or path == 'up':
            p.angle = 90
            p.movey = -aPixelMove
        if key.get_pressed()[K_DOWN] or yaxis > 0.8 or path == 'down':
            p.angle = 270
            p.movey = aPixelMove
    if joystick_count > 0:
        jb = joyin.get_button(1)
    else:
        jb = 0
    if p.status == 1:
        if key.get_pressed()[K_RETURN] or jb:
            return 1
    if p.status == 2:
        if key.get_pressed()[K_RETURN] or jb:
            return 1


def checkInputGhost(p, path=None):
    global joyin, joystick_count
    xaxis = yaxis = 0
    if p.status == 0:
        if joystick_count > 0:
            xaxis = joyin.get_axis(0)
            yaxis = joyin.get_axis(1)
        if key.get_pressed()[K_LEFT] or xaxis < -0.8 or path == 'left':
            p.angle = 180
            p.x = -aPixelMove
        if key.get_pressed()[K_RIGHT] or xaxis > 0.8 or path == 'right':
            p.angle = 0
            p.x = aPixelMove
        if key.get_pressed()[K_UP] or yaxis < -0.8 or path == 'up':
            p.angle = 90
            p.y = -aPixelMove
        if key.get_pressed()[K_DOWN] or yaxis > 0.8 or path == 'down':
            p.angle = 270
            p.y = aPixelMove
    if joystick_count > 0:
        jb = joyin.get_button(1)
    else:
        jb = 0
    if p.status == 1:
        if key.get_pressed()[K_RETURN] or jb:
            return 1
    if p.status == 2:
        if key.get_pressed()[K_RETURN] or jb:
            return 1



