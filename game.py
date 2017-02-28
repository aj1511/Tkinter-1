# Imports
import tkinter as tk
from turtle import *
from time import *
from operator import itemgetter
import numpy as np
import random


grid = 3
scores = {}
user = ''

# There are two main variables we use here:
# 1. A seperate variable for each line, which allows easier screen drawing and checking for errors
# 2. A seperate variable for each box some belonging to more than one line, which allows for easier win checking
verticals = []
horizontals = []
boxes = []
for i in range(grid):
    for i in range(grid-1):
        verticals.append(0)
for i in range(grid):
    for i in range(grid-1):
        horizontals.append(0)
for i in range(grid-1):
    for i in (range(grid-1)):
        boxes.append(0)
turn = 1

def main():
    # Update Score
    printScore()
    goto(100,100)
    for i in range(1,(grid+1)):
        for i in range(1,(grid + 1)):
            dot(10)
            forward(100)
        goto((xcor() - (grid * 100)),(ycor() + 100))

    # Get input
    onscreenclick(clickHandler)
    mainloop()

def clickHandler(rawx,rawy):
    x = int(rawx//1) # Round click to a full int
    y = int(rawy//1)
    for xnum in range(1,(grid + 1)):
        tempx = (xnum % grid) + 1
        for ynum in range(1,(grid)):
            tempy = (ynum % (grid-1)) + 1
            if ((tempx * 100) + 10) >= x >= ((tempx * 100) - 10) and ((tempy * 100) + 90) >= y >= ((tempy * 100) + 10):
                onscreenclick(None)
                updateVariable(tempx, tempy, True)
    for xnum in range(1,(grid)):
        tempx = (xnum % (grid -1)) + 1
        for ynum in range(1,(grid + 1)):
            tempy = (ynum % grid) + 1
            if ((tempx * 100) + 90) >= x >= ((tempx * 100) + 10) and ((tempy * 100) + 10) >= y >= ((tempy * 100) - 10):
                onscreenclick(None)
                updateVariable(tempx, tempy, False)
    goto((((grid + 1) * 100) / 2),20)
    write("Click a spot", align="center", font=("Arial", 50))


def updateVariable(x, y, isVertical):
    goAgain = False
    global verticals
    global horizontals
    if isVertical:
        verticals[((y - 1) * grid + x)-1] = 1
    else:
        horizontals[((y - 1) * (grid - 1) + x)-1] = 1

    # Draw lines
    clear()
    for xnum in range(1,(grid+1)): # 4
        for ynum in range(1,grid): # 3
            if verticals[((ynum - 1) * grid + xnum) - 1] != 0:
                goto((100 * xnum), (100 * ynum))
                pendown()
                goto((100 * xnum), (100 * (ynum + 1)))
                penup()
    for xnum in range(1,grid):
        for ynum in range(1,(grid + 1)):
            if horizontals[((ynum - 1) * (grid-1) + xnum) - 1] != 0:
                goto((100 * xnum), (100 * ynum))
                pendown()
                goto((100 * (xnum + 1)), (100 * ynum))
                penup()

    # Check for box filled
    boxTotal = len(boxes)
    for i in range(0,boxTotal):
        yMulti = 0
        for z in range(grid-1):
            if (i >= z * (grid-1)):
                yMulti += 1
        if (0 not in itemgetter(i,(i + grid - 1))(horizontals)) and (0 not in itemgetter((i + yMulti-1),(i+ yMulti))(verticals)):
            if boxes[i] == 0:
                boxes[i] = turn
                goAgain = True


    # Draw boxes
    for xnum in range(1,grid):
        for ynum in range(1,grid):
            pos = ((ynum-1) * (grid-1)) + xnum - 1
            if boxes[pos] != 0:
                goto((100 * xnum + 50), (100 * ynum + 20))
                write(boxes[pos], align="center", font=("Arial", 50))

    # Detect a winner
    if not 0 in boxes:
        try:
            scores[user] += 1
        except KeyError:
            scores[user] = 1 # Create new key if empty
        np.save('scores.npy', scores)
        clear()
        goto(grid*50+50,grid*50+100)
        score = countScore()
        if score[0] > score[1]:
            write("Player 1 wins!", align="center", font=("Arial", 50))
        else:
            write("Player 2 wins!", align="center", font=("Arial", 50))
        goto(grid*50+50,grid*50)
        write("Games played: " + str(scores[user]), align="center", font=("Arial", 50))
        goto(100,100)
        write("Play again", align="center", font=("Arial", 50))
        goto(400,100)
        write("Quit", align="center", font=("Arial", 50))
        onscreenclick(endGame)
        mainloop()

    finishUp(goAgain)
def printScore():
    score = countScore()
    goto(((grid+1) * 20), ((grid * 100) + 20))
    if turn == 1:
        write("Player 1: " + str(score[0]), align="center", font=("Arial", 50, "bold"))
        goto(((grid+1) * 80), ((grid * 100) + 20))
        write("Player 2: " + str(score[1]), align="center", font=("Arial", 50))
    if turn == 2:
        write("Player 1: " + str(score[0]), align="center", font=("Arial", 50))
        goto(((grid+1) * 80), ((grid * 100) + 20))
        write("Player 2: " + str(score[1]), align="center", font=("Arial", 50, "bold"))


def endGame(rawx, rawy):
    global verticals
    global horizontals
    global boxes
    global turn
    x = int(rawx//1) # Round click to a full int
    y = int(rawy//1)
    if 150 >= x >= 50 and 150 >= y >= 50:
        onscreenclick(None)
        verticals = [0,0,0,0,0,0,0,0,0,0,0,0] # Read from bottom left to upper right
        horizontals = [0,0,0,0,0,0,0,0,0,0,0,0]
        boxes = [0,0,0,0,0,0,0,0,0]
        turn = 1
        clear()
        finishUp(True)
    if 450 >= x >= 350 and 150 >= y >= 50:
        raise SystemExit

def countScore():
    player1 = 0
    player2 = 0
    for i in range(len(boxes)):
        if boxes[i] == 1:
            player1 += 1
        elif boxes[i] == 2:
            player2 += 1
    return [player1, player2]


def finishUp(again):
    global turn
    if turn == 1 and not again:
        turn = 2
    elif not again:
        turn = 1
    main()

def setup(Username):
    global scores
    global user
    scores = np.load('scores.npy').item()
    user = Username
    screen = getscreen()
    screen.listen()
    title(user)
    hideturtle() # Hide the turtle icon, cuz it's ugly
    tracer(0,0) # Used to remove turtle animation, update() to refresh screen now
    screen.setworldcoordinates(0,0,(grid * 100 + 100),(grid * 100 + 100)) # Set screen cordinates to quadrant 1 only
    penup()
    main()
    screen._root.mainloop() # Stops program from quitting while waiting for input
