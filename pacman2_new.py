import pgzrun
import pygame
import random
from sympy import false
import Node
import gameinput
import gamemaps
import graph_and_searchAlgorithms
from random import randint
from datetime import datetime


WIDTH = 600
HEIGHT = 660

player = Actor("pacman_o") # Load in the player Actor image
player.score = 0
player.lives = 3
level = 0
SPEED = 12
pacman_direction = ''
ghost_directions = ['up', 'up', 'up', 'up']
currentNode = ['27','60','45','39']
sum = 0
path=[]
exploredPath='0'
pathGhost=[[],[],[],[]]
pathGhostNode=[[],[],[],[]]
number_of_x=0
number_of_x_ghosts=[0, 0, 0, 0]
number_of_y=0
number_of_y_ghosts=[0, 0, 0, 0]
path_step =0
path_step_ghosts =[0, 0, 0, 0]
numberOfMoves=14
aPixelMove = 5.3
end = exploredPath[path_step]
win = False


def draw(): # Pygame Zero draw function
    global pacDots, player
    screen.blit('header', (0, 0))
    picture = pygame.image.load('images/maze_pacman.PNG')
    picture = pygame.transform.scale(picture, (600, 580))
    rect = picture.get_rect()
    rect = rect.move((0, 80))
    screen.blit(picture, rect)
    # screen.blit('maze_pacman', (0, 80))

    pacDotsLeft = 0
    for a in range(len(pacDots)):
        if pacDots[a].status == 0:
            pacDots[a].draw()
            pacDotsLeft += 1
        if pacDots[a].collidepoint((player.x, player.y)):
            if pacDots[a].status == 0:
                if pacDots[a].type == 2:
                    for g in range(len(ghosts)): ghosts[g].status = 1200
                else:
                    player.score += 10
            pacDots[a].status = 1
    if pacDotsLeft == 0: player.status = 2
    drawGhosts()
    getPlayerImage()
    player.draw()
    drawLives()
    screen.draw.text("LEVEL "+str(level) , topleft=(10, 10), owidth=0.5, ocolor=(0,0,255), color=(255,255,0) , fontsize=40)
    screen.draw.text(str(player.score) , topright=(590, 20), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
    if player.status == 3: drawCentreText("GAME OVER")
    if player.status == 2: drawCentreText("LEVEL CLEARED!\nPress Enter or Button A\nto Continue")
    if player.status == 1: drawCentreText("CAUGHT!\nPress Enter or Button A\nto Continue")
    if win == True : drawCentreText("Pacman Win!\n")

def drawCentreText(t):
    screen.draw.text(t , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)

def update(): # Pygame Zero update function
    global player, moveGhostsFlag, ghosts, sum, pacman_direction, path, number_of_x, number_of_y, path_step,win

    if player.status == 0 and win==False:
        if player.x<574 and player.x>532 and player.y<496 and player.y>459:

            win = True
        if moveGhostsFlag == 4:
            moveGhosts()
        for g in range(len(ghosts)):
            if ghosts[g].status > 0: ghosts[g].status -= 1
            if ghosts[g].collidepoint((player.x, player.y)):
                if ghosts[g].status > 0:
                    player.score += 100
                    animate(ghosts[g], pos=(290, 370), duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)
                else:
                    player.lives -= 1
                    sounds.pac2.play()
                    if player.lives == 0:
                        player.status = 3
                        music.fadeout(3)
                    else:
                        player.status = 1

        if player.inputActive:
            gameinput.checkInput(player, pacman_direction)
            # gameinput.checkInput(ghosts[0],ghost_directions)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                sounds.pac1.play()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)
                if pacman_direction == 'right' or pacman_direction == 'left':
                    number_of_x += 1
                    if number_of_x == numberOfMoves:
                        number_of_x = 0
                        path_step += 1
                        if path_step < len(path):
                            pacman_direction = path[path_step]

                if pacman_direction == 'up' or pacman_direction == 'down':
                    number_of_y += 1
                    if number_of_y == numberOfMoves:
                        number_of_y = 0
                        path_step += 1
                        if path_step < len(path):
                            pacman_direction = path[path_step]
    if player.status == 1:
        i = gameinput.checkInput(player, pacman_direction)
        if i == 1:
            player.status = 0
            player.x = 50
            player.y = 120
    if player.status == 2:
        i = gameinput.checkInput(player, pacman_direction)
        if i == 1:
            init()



def init():
    global player, level
    global pacman_direction, path,exploredPath
    initDots()
    path_ucs, explored_ucs = list(
        graph_and_searchAlgorithms.astar(graph_and_searchAlgorithms.create_ghraph_for_map(), '0', '61'))
    exploredPath = explored_ucs
    print("explored path: ",explored_ucs)
    path = Node.findDirections(explored_ucs, 'astar')
    print(path)
    pacman_direction = path[0]
    initGhosts()
    player.x = 50
    player.y = 120
    player.status = 0
    inputUnLock()
    level += 1
    music.play("pm1")
    music.set_volume(0.2)

def drawLives():
    for l in range(player.lives): screen.blit("pacman_o", (10+(l*32),40))

def getPlayerImage():
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        if a != 180:
            player.image = "pacman_c"
        else:
            player.image = "pacman_cr"
    else:
        if a != 180:
            player.image = "pacman_o"
        else:
            player.image = "pacman_or"
    player.angle = a

def drawGhosts():
    for g in range(len(ghosts)):
        if ghosts[g].x > player.x:
            if ghosts[g].status > 200 or (ghosts[g].status > 1 and ghosts[g].status%2 == 0):
                ghosts[g].image = "ghost5"
            else:
                ghosts[g].image = "ghost"+str(g+1)+"r"
        else:
            if ghosts[g].status > 200 or (ghosts[g].status > 1 and ghosts[g].status%2 == 0):
                ghosts[g].image = "ghost5"
            else:
                ghosts[g].image = "ghost"+str(g+1)
        ghosts[g].draw()

def moveGhosts():
    global moveGhostsFlag
    global player, ghost_directions, path, number_of_x_ghosts, number_of_y_ghosts, path_step_ghosts, path_step,exploredPath,pathGhostNode
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    if path_step<len(exploredPath):
        # pathGhostNode[0], explored_ucs = list(search_algorithms.astar_search(search_algorithms.generate_graph(), '40', exploredPath[path_step]))
        pathGhostNode[1], explored_ucs = list(
            graph_and_searchAlgorithms.astar(graph_and_searchAlgorithms.create_ghraph_for_map(), '60',
                                             exploredPath[path_step]))
        # pathGhostNode[2], explored_ucs = list(search_algorithms.astar_search(search_algorithms.generate_graph(), '45', exploredPath[path_step]))
        pathGhostNode[3], explored_ucs = list(
            graph_and_searchAlgorithms.bfs(graph_and_searchAlgorithms.create_ghraph_for_map(), '39',
                                          exploredPath[path_step]))
        # pathGhost[0] = Node.findDir3(pathGhostNode[0])
        pathGhost[1] = Node.findDirections2(pathGhostNode[1])
        # pathGhost[2] = Node.findDir3(pathGhostNode[2])
        pathGhost[3] = Node.findDirections2(pathGhostNode[3])

    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])
        move(dirs,g)
    moveGhostsFlag = 0
    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])

def move(dirs,ghostNumber):
    global  ghost_directions, path, number_of_x_ghosts, number_of_y_ghosts, path_step_ghosts, path_step, exploredPath,pathGhostNode
    if ghostNumber==0:
        randBits = bool(random.getrandbits(1))
        if randBits == True and dirs[2]==1:
            animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x - aPixelMove, ghosts[ghostNumber].y), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
        elif  dirs[0]==1:
            animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x + aPixelMove, ghosts[ghostNumber].y), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
    elif ghostNumber==2:
        randBits = bool(random.getrandbits(1))
        if randBits == True and dirs[3]==1:
            animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x , ghosts[ghostNumber].y- aPixelMove), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
        elif  dirs[1]==1:
            animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y+ aPixelMove), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)

    else:
        if ghost_directions[ghostNumber] == 'right' or ghost_directions[ghostNumber] == 'left':
            number_of_x_ghosts[ghostNumber] += 1
            if ghost_directions[ghostNumber] == 'right' and dirs[0] == 1:
                if number_of_x_ghosts[ghostNumber] == 14:
                    number_of_x_ghosts[ghostNumber] = 0
                    path_step_ghosts[ghostNumber] += 1
                    if path_step_ghosts[ghostNumber] < len(pathGhost[ghostNumber]):
                        ghost_directions[ghostNumber] = pathGhost[ghostNumber][path_step_ghosts[ghostNumber]]
                        currentNode[ghostNumber] = pathGhostNode[ghostNumber][path_step_ghosts[ghostNumber] + 1]

                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x + aPixelMove, ghosts[ghostNumber].y), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
            elif dirs[2] == 1 and ghost_directions[ghostNumber] == 'left':
                if number_of_x_ghosts[ghostNumber] == 14:
                    number_of_x_ghosts[ghostNumber] = 0
                    path_step_ghosts[ghostNumber] += 1
                    if path_step_ghosts[ghostNumber] < len(pathGhost[ghostNumber]):
                        ghost_directions[ghostNumber] = pathGhost[ghostNumber][path_step_ghosts[ghostNumber]]
                        currentNode[ghostNumber] = pathGhostNode[ghostNumber][path_step_ghosts[ghostNumber] + 1]

                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x - aPixelMove, ghosts[ghostNumber].y), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
            elif dirs[2] == 0 and ghost_directions[ghostNumber] == 'left':
                pathGhostNode[ghostNumber], explored_ucs = list(
                    graph_and_searchAlgorithms.bfs(graph_and_searchAlgorithms.create_ghraph_for_map(),
                                                   currentNode[ghostNumber], exploredPath[path_step]))
                pathGhost[ghostNumber] = Node.findDirections2(pathGhostNode[ghostNumber])
                path_step_ghosts[ghostNumber]=0
                ghost_directions[ghostNumber] = pathGhost[ghostNumber][0]
                number_of_x_ghosts[ghostNumber]=0
                number_of_y_ghosts[ghostNumber]=0
                # animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x+aPixelMove, ghosts[ghostNumber].y), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
            elif dirs[0] == 0 and ghost_directions[ghostNumber] == 'right':
                pathGhostNode[ghostNumber], explored_ucs = list(
                    graph_and_searchAlgorithms.bfs(graph_and_searchAlgorithms.create_ghraph_for_map(),
                                                   currentNode[ghostNumber], exploredPath[path_step]))
                pathGhost[ghostNumber] = Node.findDirections2(pathGhostNode[ghostNumber])
                path_step_ghosts[ghostNumber] = 0
                ghost_directions[ghostNumber] = pathGhost[ghostNumber][0]
                number_of_x_ghosts[ghostNumber]=0
                number_of_y_ghosts[ghostNumber]=0
                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x-aPixelMove , ghosts[ghostNumber].y),duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)
                # animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y),duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)
        if ghost_directions[ghostNumber] == 'up' or ghost_directions[ghostNumber] == 'down':
            if ghost_directions[ghostNumber] == 'up' and dirs[3] == 1:
                number_of_y_ghosts[ghostNumber] += 1
                if number_of_y_ghosts[ghostNumber] == 14:
                    number_of_y_ghosts[ghostNumber] = 0
                    path_step_ghosts[ghostNumber] += 1
                    if path_step_ghosts[ghostNumber] < len(pathGhost[ghostNumber]):
                        ghost_directions[ghostNumber] = pathGhost[ghostNumber][path_step_ghosts[ghostNumber]]
                        currentNode[ghostNumber] = pathGhostNode[ghostNumber][path_step_ghosts[ghostNumber] + 1]
                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y - aPixelMove), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
            elif dirs[1] == 1 and ghost_directions[ghostNumber] == 'down':
                number_of_y_ghosts[ghostNumber] += 1
                if number_of_y_ghosts[ghostNumber] == 14:
                    number_of_y_ghosts[ghostNumber] = 0
                    path_step_ghosts[ghostNumber] += 1
                    if path_step_ghosts[ghostNumber] < len(pathGhost[ghostNumber]):
                        ghost_directions[ghostNumber] = pathGhost[ghostNumber][path_step_ghosts[ghostNumber]]
                        currentNode[ghostNumber] = pathGhostNode[ghostNumber][path_step_ghosts[ghostNumber] + 1]
                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y + aPixelMove), duration=1 / SPEED, tween='linear',on_finished=flagMoveGhosts)
            elif ghost_directions[ghostNumber] == 'up' and dirs[3] == 0:
                pathGhostNode[ghostNumber], explored_ucs = list(
                    graph_and_searchAlgorithms.bfs(graph_and_searchAlgorithms.create_ghraph_for_map(),
                                                   currentNode[ghostNumber], '61'))
                pathGhost[ghostNumber] = Node.findDirections2(pathGhostNode[ghostNumber])
                path_step_ghosts[ghostNumber] = 0
                ghost_directions[ghostNumber] = pathGhost[ghostNumber][0]
                number_of_x_ghosts[ghostNumber]=0
                number_of_y_ghosts[ghostNumber]=0
                # animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y),duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)
                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y+aPixelMove),duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)
            elif ghost_directions[ghostNumber] == 'down' and dirs[1] == 0:
                pathGhostNode[ghostNumber], explored_ucs = list(
                    graph_and_searchAlgorithms.bfs(graph_and_searchAlgorithms.create_ghraph_for_map(),
                                                   currentNode[ghostNumber], exploredPath[path_step]))
                pathGhost[ghostNumber] = Node.findDirections2(pathGhostNode[ghostNumber])
                path_step_ghosts[ghostNumber] = 0
                ghost_directions[ghostNumber] = pathGhost[ghostNumber][0]
                number_of_x_ghosts[ghostNumber]=0
                number_of_y_ghosts[ghostNumber]=0
                animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y -aPixelMove),duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)
                # animate(ghosts[ghostNumber], pos=(ghosts[ghostNumber].x, ghosts[ghostNumber].y ),duration=1 / SPEED, tween='linear', on_finished=flagMoveGhosts)



def followPlayer(g, dirs):
    d = ghosts[g].dir
    if d == 1 or d == 3:
        if player.x > ghosts[g].x and dirs[0] == 1: ghosts[g].dir = 0
        if player.x < ghosts[g].x and dirs[2] == 1: ghosts[g].dir = 2
    if d == 0 or d == 2:
        if player.y > ghosts[g].y and dirs[1] == 1 and not aboveCentre(ghosts[g]): ghosts[g].dir = 1
        if player.y < ghosts[g].y and dirs[3] == 1: ghosts[g].dir = 3


def ambushPlayer(g, dirs):
    d = ghosts[g].dir
    if player.movex > 0 and dirs[0] == 1: ghosts[g].dir = 0
    if player.movex < 0 and dirs[2] == 1: ghosts[g].dir = 2

    if player.movey > 0 and dirs[1] == 1 and not aboveCentre(ghosts[g]): ghosts[g].dir = 1
    if player.movey < 0 and dirs[3] == 1: ghosts[g].dir = 3

def inTheCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 320 and ga.y < 420:
        return True
    return False

def aboveCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 300 and ga.y < 320:
        return True
    return False

def flagMoveGhosts():
    global moveGhostsFlag
    moveGhostsFlag += 1

def ghostCollided(ga,gn):
    for g in range(len(ghosts)):
        if ghosts[g].colliderect(ga) and g != gn:
            return True
    return False
    
def initDots():
    global pacDots
    pacDots = []
    a = x = 0
    while x < 8:
        y = 0
        while y < 8:
            d = gamemaps.checkDotPoint(10+x*72, 10+y*72)
            if d == 1:
                pacDots.append(Actor("dot",(45+x*72, 125+y*72)))
                pacDots[a].status = 0
                pacDots[a].type = 1
                a += 1
            if d == 2:

                pacDots.append(Actor("power",(45+x*72, 130+y*72)))
                pacDots[a].status = 0
                pacDots[a].type = 2
                a += 1
            y += 1
        x += 1

def initGhosts():
    global ghosts, moveGhostsFlag
    moveGhostsFlag = 4
    ghosts = []
    g = 0
    ghosts.append(Actor("ghost" + str(0 + 1), (315, 100)))
    ghosts.append(Actor("ghost" + str(1 + 1), (557, 425)))
    ghosts.append(Actor("ghost" + str(2 + 1), (395, 255)))
    ghosts.append(Actor("ghost" + str(3 + 1), (334, 625)))

    while g < 4:

        # ghosts.append(Actor("ghost"+str(g+1),(270+(g*2), 330)))
        ghosts[g].dir = randint(0, 3)
        ghosts[g].status = 0
        g += 1

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True
    
init()
pgzrun.go()
