# gamemaps module
aPixelMove = 5.3
from pygame import image, surface, Color
moveimage = image.load('images/maze_pacman_movemap.png')
dotimage = image.load('images/maze_pacman_movemap.png')


def checkMovePoint(p):
    global moveimage
    if p.x+p.movex < 0: p.x = p.x+600
    if p.x+p.movex > 600: p.x = p.x-600

    if p.y+p.movey < 80: p.y = p.y+660
    if p.y+p.movey > 660: p.y = p.y-660
    if moveimage.get_at((int(p.x+p.movex), int(p.y+p.movey-80))) == Color('#d02090'):
        p.movex = p.movey = 0

def checkDotPoint(x,y):
    global dotimage
    if dotimage.get_at((int(x), int(y))) == Color('#d02090'):
        return 1
    if dotimage.get_at((int(x), int(y))) == Color('#ec1c24'):
        return 2
    return False

def getPossibleDirection(g):
    global moveimage
    if g.x-aPixelMove < 0:
        g.x = g.x+600
    if g.x+aPixelMove > 600:
        g.x = g.x-600
    if g.y-(90-aPixelMove) < 0:
        g.x = g.x+660
    if g.x-(80-aPixelMove) > 660:
        g.x = g.x-660
    directions = [0,0,0,0]
    if g.x+aPixelMove < 600:
        if moveimage.get_at((int(g.x+aPixelMove), int(g.y-(85-aPixelMove)))) != Color('#d02090'): directions[0] = 1
    if g.x < 600 and g.x >= 0:
        if moveimage.get_at((int(g.x), int(g.y-(80-aPixelMove)))) != Color('#d02090'): directions[1] = 1
    if g.x-aPixelMove >= 0:
        if moveimage.get_at((int(g.x-aPixelMove), int(g.y-(85-aPixelMove)))) != Color('#d02090'): directions[2] = 1
    if g.x < 600 and g.x >= 0:
        if moveimage.get_at((int(g.x), int(g.y-(90-aPixelMove)))) != Color('#d02090'): directions[3] = 1
    return directions
                        
