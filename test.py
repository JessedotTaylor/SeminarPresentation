import Particle
import Swarm
import math

def w(x, y):
    return math.sqrt(x**2 + y**2)

def getH(pos, Q=5, H=10, A=2):
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
        # x = x / CLAMPVAL[0]
        # y = y / CLAMPVAL[1]
    else:
        raise ValueError("\nPosition Vector of length {} not implemented!\n".format(dim))

    #h = math.sin(math.sqrt(x**2 + yx**2))
    h = - ((1/Q)**(w(x,y)/H) * A * math.cos(w(x,y)))
    # h = -(x**2 + y**2)+1

    
    return h


# Particle.Particle(getH, 0, 10, 10)
particles = 10
swarm = Swarm.Swarm(particles, getH, -10, 10, dimensions=2)
iteration = 0
n_iterations = 500
target_error = 1e-3

target = min([getH([x, y]) for x in range(-10, 10) for y in range(-10, 10)])

print("Iteration: 0")
print("Target: {}".format(target))
print("Current Best: {}\n".format(swarm.gBest))

while iteration < n_iterations:
    swarm.runStep(0.5, 0.8, 0.9, 1)

    if (abs(swarm.gBest - target) < target_error):
        break

    iteration += 1

    print("Iteration: {}, Current Best: {}".format(iteration, swarm.gBest))
    
    # print()
    # for i in range(10):
    #     pos, vel = swarm.getParticlePos(i)
    #     print("Particle {}: {}".format(i+1, pos))

print("\nSwarm found best position: {}, at actual H value: {}, after {} iterations\n".format(swarm.gBestPos, getH(swarm.gBestPos), iteration))
for i in range(10):
    pos, vel = swarm.getParticlePos(i)
    print("Particle {}: {}".format(i+1, pos))
