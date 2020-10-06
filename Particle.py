import random


class Particle():
    def __init__(self, fitnessFunc, lowBound, highBound, dimensions=2, maximizing=False):
        self.fitnessFunc = fitnessFunc
        self.pos = [random.randint(lowBound, highBound) for d in range(dimensions)]
        self.pBest = self.fitnessFunc(self.pos)
        self.pBestPos = self.pos
        self.vel = [random.randint(-abs(highBound - lowBound), abs(highBound -lowBound)) for d in range(dimensions)]
        # self.vel = [random.randint(lowBound, abs(highBound -lowBound)) for d in range(dimensions)]
        self.dimensions = dimensions
        self.maximizing = maximizing


    def updatePosition(self, lr):
        # for d in range(self.dimensions):
        #     pos[d] = self.pos[d] + lr * self.vel[d]
        pos = [self.pos[d] + lr * self.vel[d] for d in range(self.dimensions)]
        pCurr = self.fitnessFunc(pos)

        if self.maximizing:
            if pCurr > self.pBest:
                self.pBest = pCurr
                self.pBestPos = pos
        else:
            if pCurr < self.pBest:
                self.pBest = pCurr
                self.pBestPos = pos

        self.pos = pos
        return pCurr
