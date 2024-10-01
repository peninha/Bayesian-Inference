# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 20:45:38 2022

@author: Pena
There is a bag full of white balls.
Each ball has a fixed unknown chance to break when tested.
This program uses BAYESIAN INFERENCE to estimate the break rate.
From each test, it collects more evidence to update the probability
distribution P(X), where X is the estimated break rate.
"""

import math
import random as rd
import matplotlib.pyplot as plt

### Section I - the bag of balls simulation ###
class ball:
    def __init__(self, color, prob):
        self.color = color
        self.prob = prob
        self.condition = "new"
    
    def test(self):
        if self.condition == "new":
            if rd.random() <= self.prob:
                self.condition = "BROKEN"
                return -1
            return 1
        return 0
    
    def getCondition(self):
        return self.condition
    
    def setCondition(self, condition):
        self.condition = condition

class bagOfBalls:
    def __init__(self, whiteBalls, blackBalls, whiteProb, blackProb):
        self.whiteBalls = whiteBalls
        self.blackBalls = blackBalls #blackballs will be implemented in future
        self.whiteProb = whiteProb
        self.blackProb = blackProb
        self.bag = list()
        self.out = list()
        self.buildBag()
        
    def buildBag(self):
        for _ in range(self.whiteBalls):
            self.bag.append(ball("W", whiteProb))
        for _ in range(self.blackBalls):
            self.bag.append(ball("BLACK", blackProb))
        rd.shuffle(self.bag)
        
    def show(self, list):
        whites, blacks = 0, 0
        for ball in list:
            if ball.color == "W":
                whites += 1
            else:
                blacks += 1
            print("{:5}\t{}".format(ball.color, ball.condition))
        return whites, blacks
        print("The bag has {} Whites and {} Blacks".format(whites, blacks))
    

    def showBag(self):
        print("\nSHOWING BAG:")
        whites, blacks = self.show(self.bag)
        print("The bag has {} Whites and {} Blacks".format(whites, blacks))
    
    def showOut(self):
        print("\nSHOWING OUT:")
        whites, blacks = self.show(self.out)
        print("OUTSITE bag there are {} Whites and {} Blacks".format(whites, blacks))
        
    def pickBalls(self, balls):
        print("\nPICKING BALLS:")
        for _ in range(balls):
            ball = self.bag.pop(0)
            print("picked {}".format(ball.color))
            self.out.append(ball)
    
    def testBalls(self):
        print("\nTESTING BALLS:")
        broken, tested, failed = 0, 0, 0
        for ball in self.out:
            result = ball.test()
            if result == -1:
                tested += 1
                failed += 1
                print("Test... {}".format("FAIL"))
            if result == 0:
                broken += 1
                print("Already BROKEN")
            if result == 1:
                tested += 1
                print("Test... {}".format("new"))
        print("There were {} balls ALREADY BROKEN".format(broken))
        print("Tested {} new balls".format(tested))
        print("{} balls FAILED".format(failed))
        return broken, tested, failed           
    
### Section II - The Bayesian Inference ###
def bayesianInference(tested, failed):
    # main function 
    n = tested
    y = failed
    
    PYinN = 0
    for x in Px:
        PYinN += calcPYinNGivenX(n, y, x)*Px[x]
    
    for x in Px: #computes bayesian inference for each Px
        PXGivenYinN = calcPXGivenYinN(n, y, x, Px[x], PYinN)
        Px[x] = PXGivenYinN #update prior Px to new Px
    return True
    
def calcPYinNGivenX(n, y, x):
    return math.comb(n, y) * (1-x)**(n-y) * x**y
    
def calcPXGivenYinN(n, y, x, px, PYinN):
    #Bayesian Inference is: P(X|YinN) = P(YinN|X)*P(X)/PYinN
    PYinNGivenX = calcPYinNGivenX(n, y, x)
    PXGivenYinN = PYinNGivenX*px/PYinN
    #print("P(YinN|X) = {}".format(PYinNGivenX))
    #print("P(X) = {}".format(px))
    #print("P(YinN) = {}".format(PYinN))
    #print("P(X|YinN) = {}".format(PXGivenYinN))
    return PXGivenYinN
    
def integratePX(): #sum all Px values to check if that adds up 1 (normalized)
    sum = 0
    for x in Px:
        sum += Px[x]
    print("P(X) totals to {}".format(sum))

def plotPX():
    keys = Px.keys()
    values = Px.values()
    plt.plot(keys, values)
    

seed = 4 #seed for random number generator
#rd.seed(seed) 
whiteBalls = 100 #how many white balls are in the bag?
whiteProb = .1 #what is white balls break rate for each test?
blackBalls = 0 #how many black balls are in the bag?
blackProb = .5 #black balls break rate

Px = {  #Prior probability distribution of X (break rate)
      0  : 0.1,
      .1 : 0.1,
      .2 : 0.1,
      .3 : 0.1,
      .4 : 0.1,
      .5 : 0.1,
      .6 : 0.1,
      .7 : 0.1,
      .8 : 0.1,
      .9 : 0.1
     }

bag = bagOfBalls(whiteBalls, blackBalls, whiteProb, blackProb)
bag.showBag()

ballsPicked = 5 #how many balls are picked per round?
testRounds = 10 #how many test rounds?

for _ in range(testRounds):
    bag.pickBalls(ballsPicked)
    broken, tested, failed = bag.testBalls()
    bayesianInference(tested, failed)
    integratePX()

plotPX()