from Particle import *

class Swarm():
    def __init__(self, particleCount, fitnessFunc, lowBound, highBound, dimensions=2, maximizing=False):
        self.particles = [Particle(fitnessFunc, lowBound, highBound, dimensions, maximizing) for _ in range(particleCount)]
        gBest = self.particles[0].pBest
        gBestPos = self.particles[0].pBestPos
        for p in self.particles:
            if maximizing:
                if p.pBest > gBest:
                    gBest = p.pBest
                    gBestPos = p.pos
            else:
                if p.pBest < gBest:
                    gBest = p.pBest
                    gBestPos = p.pBestPos
        self.gBest = gBest
        self.gBestPos = gBestPos
        self.dimensions = dimensions
        self.maximizing = maximizing

    def runStep(self, womega, phi_p, phi_g, lr):
        for p in self.particles:
            for d in range(self.dimensions):
                r_p = random.random()
                r_g = random.random()
                p.vel[d] = womega * p.vel[d] + phi_p * r_p * (p.pBestPos[d] - p.pos[d]) + phi_g * r_g * (self.gBestPos[d] -  p.pos[d])

            pCurr = p.updatePosition(lr)

            if self.maximizing:
                if pCurr > self.gBest:
                    self.gBest = pCurr
                    self.gBestPos = p.pos
            else:
                if pCurr < self.gBest:
                    self.gBest = pCurr
                    self.gBestPos = p.pos

    def getParticlesPos(self, clamp=None):
        retList = []
        for p in self.particles:
            if clamp != None:
                retList.append([[int(abs(i)*clamp[0]*2) for i in p.pos], [int(abs(i)*clamp[0]*2) for i in p.vel]])
            else:
                retList.append([[i for i in p.pos], [i for i in p.vel]])

        return retList
    
    def getParticlePos(self, index):
        return [[i for i in self.particles[index].pos], [i for i in self.particles[index].vel]]


if __name__ == "__main__":
    CLAMPVAL = [680, 384]
    def getH(pos, Q=2, H=10, A=1):
        # x = x / (CENTER[0] // 16)
        dim = len(pos)
        if dim == 2:
            x, y = pos
            x = x / CLAMPVAL[0]
            y = y / CLAMPVAL[1]
            #h = math.sin(math.sqrt(x**2 + yx**2))
            # h = - ((1/Q)**(w(x,y)/H) * A * math.cos(w(x,y)))
            h = -(x**2 + y**2)+1
        else:
            raise ValueError("\nPosition Vector of length {} not implemented!\n".format(dim))
        return h

    swarm = Swarm(10, getH, 0, 1360)
    print(swarm.getParticlePos())