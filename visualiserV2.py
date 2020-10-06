import pygame
import math
import Swarm


# Define some colors
black     = (   0,   0,   0)
white     = ( 255, 255, 255)
green     = (   0, 255,   0)
red       = ( 255,   0,   0)
lightblue = (   0, 100, 255)
tan       = ( 234, 155, 128)
darkblue  = (   0,   0, 255)
grey      = ( 214, 214, 214)
darkgrey  = ( 100, 100, 100)
yellow    = ( 255, 242,   0)

pygame.init()


x_range = [-8, 8]
size = [500] * 2 #1360 768 Screen 1900 1000

PRECISION = 10

step = size[0] // ((abs(x_range[0]) + x_range[1]) * PRECISION)

screen=pygame.display.set_mode(size)

CENTER = [size[0] //2, size[1]//2]
radius = int(math.sqrt(CENTER[0]**2 + CENTER[1]**2))


clock = pygame.time.Clock()

done = False
startFlag = False



def w(x, y):
    return math.sqrt(x**2 + y**2)

def getH(pos, Q=2, H=10, A=2):
    # x = x / (CENTER[0] // 16)
    if type(pos) == list and len(pos) > 1:
        dim = len(pos)
    elif type(pos) == list:
        dim = 1
        pos = pos[0]
    else:
        dim = 1

    if dim == 1:
        x = pos
        y = x

    elif dim == 2:
        x, y = pos
    else:
        raise ValueError("\nPosition Vector of length {} not implemented!\n".format(dim))

    # h = math.sin(math.sqrt(x**2 + y**2))
    # h = math.cos(math.sqrt(x**2 + y**2))
    h = - ((1/Q)**(w(x,y)/H) * A * math.cos(w(x,y)))
    # h = ((1/Q)**(w(x,y)/H) * A * math.cos(w(x,y)))
    # h = -(x**2 + y**2)+1
    return h


def genColour(x):
    x = x / radius * x_range[1] 
    # print(x)
    h = getH(x)
    if h > 1:
        h = 1
    if h < -1:
        h = -1
    colour = [int(124+124*h), 0,int(124+124*-h)]
    return colour

# swarm = Swarm.Swarm(10, getH, -CLAMPVAL[0], CLAMPVAL[0])
swarm = Swarm.Swarm(10, getH, x_range[0], x_range[1], dimensions=2, maximizing=False)

def drawSwarm():
    if swarm.dimensions == 2:
        posList = swarm.getParticlesPos()
        for [x,y], vel in posList:
            x = int((x / x_range[1]) * CENTER[0] + CENTER[0])
            y = int(CENTER[1] - (y / x_range[1]) * CENTER[1])

            pygame.draw.circle(screen, white, [x, y], 5, 1)
            # vel = [0.36*vel[0], 0.36*vel[1]]
            # pygame.draw.lines(screen, yellow, False, [pos, vel], 1)

    elif swarm.dimensions == 1:
        # posList = swarm.getParticlesPos(CLAMP)
        posList = swarm.getParticlesPos()
        for [x], vel in posList: 
            x = int((x / x_range[1]) * CENTER[0] + CENTER[0])
            # print(x)
            pygame.draw.circle(screen, white, [x, CENTER[1]], 5, 1)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # print(getH((CENTER[0] - pos[0], CENTER[1] - pos[1])))
            print("This feature is currently BROKEN")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                swarm.runStep(0.5, 0.8, 0.9, 1.0)
                for pos, vel in swarm.getParticlesPos():
                    print(pos, vel)
                print("Current Best: {}".format(swarm.gBest))  

            if event.key == pygame.K_i:
                for pos, vel in swarm.getParticlesPos():
                    print(pos, vel)
                print("Current Best: {}".format(swarm.gBest))

            if event.key == pygame.K_UP:
                iteration = 0
                startFlag = True


    clock.tick(60)

    screen.fill(black)
    for x in range(step, radius, step):
        pygame.draw.circle(screen, genColour(x), CENTER, x, step)   

    if startFlag == True:
        if iteration == 0:
            n_iterations = 500
            target_error = 1e-3
            target = -2
            print("Max Iterations: {}".format(n_iterations))
            print("Target Point: {}".format(target))
            print("Target Error: {}".format(target_error))
            print("Current Best: {}\n".format(swarm.gBest))
        swarm.runStep(0.5, 0.8, 0.9, 1.0)
        drawSwarm()

        if (abs(swarm.gBest - target) < target_error):
            print("Break Condition: Target Found!")
            print("\nSwarm found best position: {}, at actual H value: {}, after {} iterations\n".format(swarm.gBestPos, getH(swarm.gBestPos), iteration))
            startFlag = False

        if iteration > n_iterations:
            print("Break Condition: Max Loops Exceeded")
            print("Current swarm best: {}".format(swarm.gBest))
            startFlag = False

        iteration += 1

    else:
        drawSwarm()

    pygame.display.flip()

pygame.quit()