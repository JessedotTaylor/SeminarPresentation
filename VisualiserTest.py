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

size = [768, 768] #1360 768 Screen 1900 1000
screen=pygame.display.set_mode(size)

MARGIN = 20 #Pixels
CENTER = [size[0] //2, size[1]//2]

CLAMP = [8] * 2
print("Clamp: {}".format(CLAMP[0]))
CLAMPVAL = [(CENTER[0] / CLAMP[0]), (CENTER[1] / CLAMP[1])]



radius = int(math.sqrt(CENTER[0]**2 + CENTER[1]**2))
# radius = max(size[0], size[1])

clock = pygame.time.Clock()

done = False



def w(x, y):
    return math.sqrt(x**2 + y**2)

def getH(pos, Q=2, H=10, A=1):
    # x = x / (CENTER[0] // 16)
    if type(pos) == list and len(pos) > 1:
        dim = len(pos)
    elif type(pos) == list:
        dim = 1
        pos = pos[0]
    else:
        dim = 1

    if dim == 1:
        x = pos / CLAMPVAL[0]
        y = x

    elif dim == 2:
        x, y = pos
        # x = x / CLAMPVAL[0]
        # y = y / CLAMPVAL[1]
    else:
        raise ValueError("\nPosition Vector of length {} not implemented!\n".format(dim))

    #h = math.sin(math.sqrt(x**2 + yx**2))
    h = - ((1/Q)**(w(x,y)/H) * A * math.cos(w(x,y)))
    # h = -(x**2 + y**2)+1
    return h


def genColour(x, Q=2, H=10, A=1):
    h = getH(x, Q, H, A)
    if h > 1:
        h = 1
    if h < -1:
        h = -1
    colour = [int(124+124*-h), 0,int(124+124*h)]
    return colour

# swarm = Swarm.Swarm(10, getH, -CLAMPVAL[0], CLAMPVAL[0])
swarm = Swarm.Swarm(1, getH, CENTER[0], CENTER[0], dimensions=1)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(getH(CENTER[0] - pos[0]))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                swarm.runStep(0.5, 0.8, 0.9, 1.0)
                for pos, vel in swarm.getParticlesPos():
                    print(pos, vel)
                print("Current Best: {}".format(swarm.gBest))
                print()
            

    clock.tick(60)

    screen.fill(black)
    thickness = 5
    # colour= genColour(485)
    for x in range(thickness, radius, thickness):
        # print(x)
        # h = getH(x)
        # colour = genColour(x)
        pygame.draw.circle(screen, genColour(x), CENTER, x, thickness)

    if swarm.dimensions == 2:
        posList = swarm.getParticlesPos(CLAMP)
        for pos, vel in posList:
            # print(pos, vel)
            pygame.draw.circle(screen, white, pos, 5, 1)
            # vel = [0.36*vel[0], 0.36*vel[1]]
            # pygame.draw.lines(screen, yellow, False, [pos, vel], 1)

    elif swarm.dimensions == 1:
        # posList = swarm.getParticlesPos(CLAMP)
        posList = swarm.getParticlesPos()
        for pos, vel in posList:
            pygame.draw.circle(screen, white, [int(pos[0]), CENTER[1]], 5, 1)


    

    pygame.display.flip()

pygame.quit()