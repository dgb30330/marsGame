import pygame

trans = (10,10,10) # use with .set_colorkey()
black = (0,0,0) # Waste

white = (255,255,255) # Habitat
grey = (90,80,80) # Storage
green =  (35,100,35) # Life Support
aqua = (0,240,220) # Recycle
yellow = (255,216,0) # Power
red = (195,0,0) # Extraction
orange = (233,49,0) # Industry
blue = (0,0,135) # Transportation
purple = (160,150,209) # Lab
pink = (255,34,169)# Admin

darkGreen =  (55,130,55) # Organics


#Tile theme
surfaceRed = (154,29,29)
boldRed = (124,10,10)
subRedDark = (79,19,0)
subRed = (103,22,9)
highlightOrange = (255,144,0)
highlightYellow = (255,205,0)
highlightBrown = (114,44,0)
glowYellow = (255,255,194)

panelGrey = (25,10,10)

def darken(color,factor):
    rgb = [0,0,0]
    colorIndex = 0
    for x in color:
        if x - factor > 0:
            rgb[colorIndex] = x - factor
        else:
            pass
        colorIndex+=1
    newColor = (rgb[0],rgb[1],rgb[2])
    return newColor

