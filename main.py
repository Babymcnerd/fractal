import math
from operator import pos
import random
import time
import colorsys
import pygame, sys
from multiprocessing import Pool
from time import sleep
from pygame.locals import *

pygame.init()
width = 720
height = 720
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space and time all come down!')
red = (255, 0, 0)
blue = (0, 0, 255)
numOfIterations = 150
xLeft = -2.5
xRight = 2.5
yBottom = -2
yTop = 2
currentFractal = "mand"
hVar = .4
widthRatio = (xRight - xLeft) / width
heightRatio = (yBottom - yTop) / height


listOfAllPixels = []
for i in range(width):
    listOfAllPixels.append([])
    for j in range(height):
        listOfAllPixels[i].append((i, j))

def checkComplexNumberDistance(x, y):
    return (x.real - y.real) * (x.real - y.real) + (x.imag - y.imag) * (x.imag - y.imag)

posOne = xLeft, yTop
posTwo = xRight, yBottom

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def getColorAtCoordMand(cordsStart):
    coords = pixelToCoord(cordsStart)
    x0 = coords[0]
    y0 = coords[1]
    x2 = 0
    y2 = 0
    iteration = 0
    x = 0
    y = 0
    while (x2 + y2 <= 4 and iteration < numOfIterations):
        y = 2 * x * y + y0
        x = x2 - y2 + x0
        x2 = x * x
        y2 = y * y
        iteration = iteration + 1
  
    if (iteration == numOfIterations):
        return (0, 0, 0)
    a = .1
    n = float(iteration)
    return ((0.5 * math.sin(a * n) + 0.5) * 255, (0.5 * math.sin(a * n + 2.094) + 0.5) * 255,  (0.5 * math.sin(a * n + 4.188) + 0.5) * 255)


def getColorAtCoordBurning(cordsStart):
    cords = pixelToCoord(cordsStart)
    x = cords[0]
    y = -cords[1]
    zx = 0
    zy = 0
    h = .4
    iteration = 0
    while (zx*zx + zy*zy < 4 and iteration < numOfIterations):
        xtemp = zx*zx - zy*zy + x
        zy = abs(2*zx*zy) + y
        zx = xtemp
        iteration = iteration + 1
    if (iteration == numOfIterations):
        return (0, 0, 0)    
    h-= iteration / numOfIterations
    if h < 0:
        h = 1
    return hsv2rgb(1 -h, 1, 1)


def getColorsOfList(listOfCords):
    if currentFractal == "mand":
        return list(map(getColorAtCoordMand, listOfCords))
    if currentFractal == "burning":
        return (list(map(getColorAtCoordBurning, listOfCords)))
    


def pixelToCoord(x):
    xRatio = x[0] *  widthRatio + xLeft
    yRatio = x[1] * heightRatio + yTop
    return xRatio, yRatio


def reload():
    sT = time.time()
    pool = Pool(processes=16)
    colorsAtAllCoords = list(pool.map(getColorsOfList, listOfAllPixels))
    pool.close()
    for x in range(width):
        for y in range(height):
            display.set_at((x, y), colorsAtAllCoords[x][y])
    pygame.display.flip()
    print("It took this long -->", time.time() - sT)


reload()

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPosition = pygame.mouse.get_pos()
            print(round(pygame.mouse.get_pos()[0] / width * (xRight - xLeft) + xLeft, 2), ", ",
                  round(pygame.mouse.get_pos()[1] / height * (yBottom - yTop) + yTop, 2))
            posOne = list(pygame.mouse.get_pos())
            clickPosition = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            print(round(pygame.mouse.get_pos()[0] / width * (xRight - xLeft) + xLeft, 2), ", ",
                  round(pygame.mouse.get_pos()[1] / height * (yBottom - yTop) + yTop, 2))
            posTwo = list(pygame.mouse.get_pos())
            if posTwo[0] - posOne[0] > posTwo[1] - posOne[1]:
                posTwo[1] = posOne[1] + (posTwo[0] - posOne[0])
            else:
                posTwo[0] = posOne[0] + (posTwo[1] - posOne[1])
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(posOne[0], posOne[1], posTwo[0]-posOne[0], posTwo[1]-posOne[1]), 3)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "return":
                print("LOADING!")
                xLeftO = xLeft
                xRightO = xRight
                yTopO = yTop
                yBottomO = yBottom
                xLeft = posOne[0] / width * (xRightO - xLeftO) + xLeftO
                xRight = posTwo[0] / width * (xRightO - xLeftO) + xLeftO
                yTop = posOne[1] / height * (yBottomO - yTopO) + yTopO
                yBottom = posTwo[1] / height * (yBottomO - yTopO) + yTopO
                print(xLeft, xRight, yTop, yBottom)
                widthRatio = (xRight - xLeft) / width
                heightRatio = (yBottom - yTop) / height
                reload()
            if pygame.key.name(event.key) == "up":
                numOfIterations += 100
                print("Num of iterations -->", numOfIterations)
                reload()
            if pygame.key.name(event.key) == "down":
                numOfIterations -= 100
                print("Num of iterations -->", numOfIterations)
                reload()
            if pygame.key.name(event.key) == "left":
                currentFractal = "mand"
                reload()
            if pygame.key.name(event.key) == "right":
                currentFractal = "burning"
                reload()
            if pygame.key.name(event.key) == "=":
                hVar += .05
                reload()
            if pygame.key.name(event.key) == "-":
                hVar -= .05
                reload()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()