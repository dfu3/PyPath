import time
import os
from random import randint
import sys
import termios
import contextlib

class MapOBJ:


    def __init__(self, in_Size, in_BLANK): # initializes blank grid using a 2D list
        self.BLANK = in_BLANK
        self.mapSize = in_Size
        self.matrix = list()
        for r in range(self.mapSize/2):
            self.matrix.append(list())
            for c in range(self.mapSize):
                self.matrix[r].append(self.BLANK)


    def drawMatrix(self): # prints current state of grid
        row = ""
        for r in range(self.mapSize/2):
            print(row)
            row = ""
            for c in range(self.mapSize):
                row += self.matrix[r][c]

    def randWall(self): # generates one barrier with variable shape and size

        inMap = False
        coinToss = randint(0, 1)

        while(not inMap):
            startPos = (randint(0,(self.mapSize)/2-1), randint(0,self.mapSize-1))

            if(coinToss == 0):
                if( (startPos[0]+4 < (self.mapSize)/2) and (startPos[1]+10 < self.mapSize+1) ):
                    inMap = True
            else:
                if( (startPos[0]+10 < (self.mapSize)/2) and (startPos[1]+4 < self.mapSize+1) ):
                    inMap = True

        width = randint(2, 4)
        length = randint(8, 10)

        if(coinToss == 0):
            for r in range(width):
                for c in range(length):
                    self.matrix[startPos[0]+r][startPos[1]+c] = " @"
        else:
            for r in range(length):
                for c in range(width):
                    self.matrix[startPos[0]+r][startPos[1]+c] = " @"

class Node:

    def __init__(self, inPos, inId): # creates new node obj with def fields
        self.g = 0
        self.h = 0
        self.f = 0
        self.pos = inPos
        self.isDiag = None
        self.id = inId
        self.parent = None

    def calc_G(self, parentG): # calculates dist traveled

        if(self.isDiag):
            self.g = parentG + 14 #was 10
        else:
            self.g = parentG + 10

    def calc_H(self, tarPos): # calculates the Heuristic cost to goal

        yDist = abs(self.pos[0] - tarPos[0])
        xDist = abs(self.pos[1] - tarPos[1])

        if (xDist < yDist):
            H = (14 * xDist) + (10 * abs(xDist - yDist))
        else:
            H = (14 * yDist) + (10 * abs(yDist - xDist))

        H = 14*(abs(self.pos[1] - tarPos[1]) + abs(self.pos[0] - tarPos[0]))

        self.h = H

    def calc_F(self):
        self.f = self.g + self.h

#-----------------------------------------------------------------
@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)
#-----------------------------------------------------------------

def main():

    map = MapOBJ(65, ' .')
    os.system('clear')
    wallCount = 1
    wallsDone = False
    doneDrawing = False

    sPos = (0, 0)
    fPos = (0, 0)

    open = list()
    closed = list()
    curList = list()
    idCount = 0

    curNode = Node(sPos, idCount)
    tarNode = Node(fPos, -1)

    foundGoal = False

    with raw_mode(sys.stdin):
        try:
            while True:

                if(wallCount < 10):
                    map.randWall()
                    wallCount+=1

                if(wallCount == 10):
                    wallsDone = True


                if(wallsDone):
                    wallsDone = False
                    wallCount+= 1

                    while( (sPos == fPos) or
                         ( (map.matrix[sPos[0]][sPos[1]] != ' .') or (map.matrix[fPos[0]][fPos[1]] != ' .'))):
                        sPos = (randint(0, (map.mapSize/2)-1), randint(1, (map.mapSize)-1))
                        fPos = (randint(0, (map.mapSize/2)-1), randint(1, (map.mapSize)-1))

                    map.matrix[sPos[0]][sPos[1]] = ' S'
                    map.matrix[fPos[0]][fPos[1]] = ' F'

                    curNode.pos = sPos
                    tarNode.pos = fPos

                    open.append(curNode)
                    doneDrawing = True

                #-----------------------------

                if (doneDrawing and not(foundGoal)):

                    # get node with lowest f score
                    curNode = open[0]
                    lowF = min(node.f for node in open)
                    for i in open:
                        if(i.f == lowF):
                            curNode = i
                            open.remove(i) #drop current node from open list

                    #---------------------------------------------------------------------------------------------------
                    #generate successors
                    tempNode = None
                    #0 left
                    if( (curNode.pos[1]-1 >= 0) and
                      ( (map.matrix[curNode.pos[0]][curNode.pos[1]-1] == ' .') or
                        (map.matrix[curNode.pos[0]][curNode.pos[1]-1] == ' F') )):
                        idCount+=1
                        tempNode = Node((curNode.pos[0], curNode.pos[1]-1), idCount)
                        tempNode.isDiag = False
                        tempNode.parent = curNode
                        curList.append(tempNode)

                    #1 left up
                    if( (curNode.pos[0]-1 >= 0) and (curNode.pos[1]-1 >= 0) and
                      ( (map.matrix[curNode.pos[0]-1][curNode.pos[1]-1] == ' .') or
                        (map.matrix[curNode.pos[0]-1][curNode.pos[1]-1] == ' F') )):
                        idCount+=1
                        tempNode = Node((curNode.pos[0]-1, curNode.pos[1]-1), idCount)
                        tempNode.isDiag = True
                        tempNode.parent = curNode
                        curList.append(tempNode)

                    #2 up
                    if( (curNode.pos[0]-1 >= 0) and
                      ( (map.matrix[curNode.pos[0]-1][curNode.pos[1]] == ' .') or
                        (map.matrix[curNode.pos[0]-1][curNode.pos[1]] == ' F') )):
                        idCount+=1
                        tempNode = Node((curNode.pos[0]-1, curNode.pos[1]), idCount)
                        tempNode.isDiag = False
                        tempNode.parent = curNode
                        curList.append(tempNode)

                    #3 right up
                    if( (curNode.pos[0]-1 >= 0) and (curNode.pos[1]+1 < (map.mapSize)) and
                      ( (map.matrix[curNode.pos[0]-1][curNode.pos[1]+1] == ' .') or
                        (map.matrix[curNode.pos[0]-1][curNode.pos[1]+1] == ' F') )):
                        idCount+=1
                        tempNode = Node((curNode.pos[0]-1, curNode.pos[1]+1), idCount)
                        tempNode.isDiag = True
                        tempNode.parent = curNode
                        curList.append(tempNode)

                    #4 right
                    if( (curNode.pos[1]+1 < (map.mapSize)) and
                      ( (map.matrix[curNode.pos[0]][curNode.pos[1]+1] == ' .') or
                        (map.matrix[curNode.pos[0]][curNode.pos[1]+1] == ' F') )):
                        idCount+=1
                        tempNode = Node((curNode.pos[0], curNode.pos[1]+1), idCount)
                        tempNode.isDiag = False
                        tempNode.parent = curNode
                        curList.append(tempNode)

                    #5 right down
                    if( (curNode.pos[0]+1 < ((map.mapSize/2)-1) ) and (curNode.pos[1]+1 < (map.mapSize)) and
                      ( (map.matrix[curNode.pos[0]+1][curNode.pos[1]+1] == ' .') or
                        (map.matrix[curNode.pos[0]+1][curNode.pos[1]+1] == ' F') ) ):
                        idCount+=1
                        tempNode = Node((curNode.pos[0]+1, curNode.pos[1]+1), idCount)
                        tempNode.isDiag = True
                        tempNode.parent = curNode
                        curList.append(tempNode)

                    #6 down
                    if( (curNode.pos[0]+1 < ((map.mapSize/2)-1)) and
                      ( (map.matrix[curNode.pos[0]+1][curNode.pos[1]] == ' .') or
                        (map.matrix[curNode.pos[0]+1][curNode.pos[1]] == ' F') )):
                        idCount+=1
                        tempNode = Node((curNode.pos[0]+1, curNode.pos[1]), idCount)
                        tempNode.isDiag = False
                        tempNode.parent = curNode
                        curList.append(tempNode)

                    #7 left down
                    if( (curNode.pos[0]+1 < ((map.mapSize/2)-1)) and (curNode.pos[1]-1 >= 0) and
                      ( (map.matrix[curNode.pos[0]+1][curNode.pos[1]-1] == ' .') or
                        (map.matrix[curNode.pos[0]+1][curNode.pos[1]-1] == ' F')) ):
                        idCount+=1
                        tempNode = Node((curNode.pos[0]+1, curNode.pos[1]-1), idCount)
                        tempNode.isDiag = True
                        tempNode.parent = curNode
                        curList.append(tempNode)
                    #---------------------------------------------------------------------------------------------------

                    add = True
                    #evaluating list of adj. nodes of current node
                    for i in curList:

                        i.parent = curNode

                        i.calc_G(curNode.g)    #\
                        i.calc_H(tarNode.pos)    #- calculating cost to target
                        i.calc_F()             #/


                        if(map.matrix[i.pos[0]][i.pos[1]] != ' S' and map.matrix[i.pos[0]][i.pos[1]] != ' F'):
                            map.matrix[i.pos[0]][i.pos[1]] = '  '

                        if(i.pos == tarNode.pos): #goal check
                            foundGoal = True
                            tarNode.parent = curNode
                            break

                        for j in closed:
                            if(i.pos == j.pos):
                                add = False

                        for j in open:
                            if(i.pos == j.pos):
                                add = False
                                if(i.g > j.g):
                                    add = False
                                else:
                                    j.parent = i #i.parent = j
                                    i.g = j.g    #j.g = i.g
                                    j.calc_G(curNode.g)
                                    j.calc_H(tarNode.pos)
                                    j.calc_F()

                        if(add):
                            open.append(i)

                    del curList[:] #reset temp list of nodes

                    closed.append(curNode)

                if(foundGoal): #uses stored parent attribute to trace back best route

                    traceNode = tarNode
                    while(map.matrix[traceNode.parent.pos[0]][traceNode.parent.pos[1]] != ' S' ):

                        map.drawMatrix()
                        #ch = sys.stdin.read(1)
                        #time.sleep(.0333)
                        time.sleep(.1)
                        os.system('clear')

                        if(map.matrix[traceNode.parent.pos[0]][traceNode.parent.pos[1]] != ' S'):
                            map.matrix[traceNode.parent.pos[0]][traceNode.parent.pos[1]] = ' +'
                            traceNode = traceNode.parent

                    break

                #-----------------------------
                map.drawMatrix()
                #ch = sys.stdin.read(1)
                #time.sleep(.0666)
                time.sleep(.3)
                os.system('clear')
                ch = '?'
                #-----------------------------

            os.system('clear')
            map.drawMatrix()

        except (KeyboardInterrupt, EOFError):
            pass

if (__name__ == '__main__'):
    main()