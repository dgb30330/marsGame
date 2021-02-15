import pygame

import color as c

background = pygame.image.load('img/stars.jpg').convert()

#launch assets
blank = pygame.Surface((24,24))
blank.fill(c.trans)
blank.set_colorkey(c.trans)

earthIcon = blank.copy()
marsIcon = blank.copy()
spaceIcon = blank.copy()
pygame.draw.circle(earthIcon,c.blue,(12,12),11)
pygame.draw.circle(marsIcon,c.red,(12,12),11)
pygame.draw.circle(spaceIcon,c.grey,(12,12),8)
pygame.draw.circle(spaceIcon,c.trans,(12,12),5)
spaceIcon.set_colorkey(c.trans)


blankLaunch = pygame.Surface((300,24))
blankLaunch.fill(c.trans)
blankLaunch.set_colorkey(c.trans)
blankLaunch.blit(earthIcon,(0,0))
blankLaunch.blit(marsIcon,(300-marsIcon.get_width(),0))

blankOrbitalLaunch = pygame.Surface((300,24))
blankOrbitalLaunch.fill(c.trans)
blankOrbitalLaunch.set_colorkey(c.trans)
blankOrbitalLaunch.blit(spaceIcon,(0,0))
blankOrbitalLaunch.blit(marsIcon,(300-marsIcon.get_width(),0))

#map images 64X64
tile = pygame.image.load('img/tile/marsTile.png').convert()
tile.set_colorkey(c.trans)
tileSelected = pygame.image.load('img/tile/marsTileSelected.png').convert()
tileSelected.set_colorkey(c.trans)
tileMO = pygame.image.load('img/tile/marsTileMO.png').convert()
tileMO.set_colorkey(c.trans)

noTile = pygame.image.load('img/tile/noTile.png').convert()
noTile.set_colorkey(c.trans)

debris1 = pygame.image.load('img/tile/debris1.png').convert()
debris1.set_colorkey(c.trans)

debris2 = pygame.image.load('img/tile/debris2.png').convert()
debris2.set_colorkey(c.trans)

debris3 = pygame.image.load('img/tile/debris3.png').convert()
debris3.set_colorkey(c.trans)

crater = pygame.image.load('img/tile/debCrater.png').convert()
crater.set_colorkey(c.trans)

grave = pygame.image.load('img/tombstone.png').convert()
grave.set_colorkey(c.trans)

naut = pygame.image.load('img/astronautL.png').convert()
naut.set_colorkey(c.trans)

nautBad = pygame.image.load('img/astronautLB.png').convert()
nautBad.set_colorkey(c.trans)

bot = pygame.image.load('img/astrobotL.png').convert()
bot.set_colorkey(c.trans)

botBad = pygame.image.load('img/astrobotLDead.png').convert()
botBad.set_colorkey(c.trans)

nautKid = pygame.image.load('img/astronautLC.png').convert()
nautKid.set_colorkey(c.trans)

nautShadow = pygame.image.load('img/astronautShadowL.png').convert()
nautShadow.set_colorkey(c.trans)
nautShadow.set_alpha(100)

mininaut = pygame.image.load('img/astronaut.png').convert()
mininaut.set_colorkey(c.trans)

blackout = pygame.Surface((800,600))
blackout.fill(c.black)

#building overlays 64x47
buildRocket = pygame.image.load('img/build/rocket.png').convert_alpha()

buildXSD = pygame.image.load('img/build/buildXS-d.png').convert_alpha()
buildXSU = pygame.image.load('img/build/buildXS-u.png').convert_alpha()
buildXSR = pygame.image.load('img/build/buildXS-r.png').convert_alpha()
buildXSL = pygame.image.load('img/build/buildXS-l.png').convert_alpha()

buildSD = pygame.image.load('img/build/buildS-d.png').convert_alpha()
buildSU = pygame.image.load('img/build/buildS-u.png').convert_alpha()
buildSR = pygame.image.load('img/build/buildS-r.png').convert_alpha()
buildSL = pygame.image.load('img/build/buildS-l.png').convert_alpha()

buildMDR = pygame.image.load('img/build/buildM-dr.png').convert_alpha()
buildMUR = pygame.image.load('img/build/buildM-ur.png').convert_alpha()
buildMDL = pygame.image.load('img/build/buildM-dl.png').convert_alpha()
buildMUL = pygame.image.load('img/build/buildM-ul.png').convert_alpha()

buildMLDR = pygame.image.load('img/build/buildML-dr.png').convert_alpha()
buildMLUR = pygame.image.load('img/build/buildML-ur.png').convert_alpha()
buildMLDL = pygame.image.load('img/build/buildML-dl.png').convert_alpha()
buildMLUL = pygame.image.load('img/build/buildML-ul.png').convert_alpha()

buildL = pygame.image.load('img/build/buildL.png').convert_alpha()

buildXL = pygame.image.load('img/build/buildXL.png').convert_alpha()

shadowSD = pygame.image.load('img/tile/shadowSD.png').convert()
shadowSD.set_colorkey(c.trans)
shadowSU = pygame.image.load('img/tile/shadowSU.png').convert()
shadowSU.set_colorkey(c.trans)
shadowSR = pygame.image.load('img/tile/shadowSR.png').convert()
shadowSR.set_colorkey(c.trans)
shadowSL = pygame.image.load('img/tile/shadowSL.png').convert()
shadowSL.set_colorkey(c.trans)

#color bases
under = pygame.Surface((64,47))
transUnder = under.copy() # Under Construction
transUnder.fill(c.trans)
whiteUnder = under.copy()
whiteUnder.fill(c.white) # Habitat / CONCRETE
greyUnder = under.copy() 
greyUnder.fill(c.grey) # Storage / METAL
greenUnder = under.copy() 
greenUnder.fill(c.green) # Life Support / FOOD
aquaUnder = under.copy() 
aquaUnder.fill(c.aqua) # Recycle / AIR
yellowUnder = under.copy() 
yellowUnder.fill(c.yellow)# Power / POWER
redUnder = under.copy()
redUnder.fill(c.red) # Extraction / ORE
orangeUnder = under.copy()
orangeUnder.fill(c.orange) # Industry / FUEL
blueUnder = under.copy()
blueUnder.fill(c.blue) # Transportation / WATER
purpleUnder = under.copy()
purpleUnder.fill(c.purple) # Lab / MEDS
pinkUnder = under.copy()
pinkUnder.fill(c.pink) # Admin / RARE
dGreenUnder = under.copy()
dGreenUnder.fill(c.darkGreen) # ORGANICS
dRedUnder = under.copy()
dRedUnder.fill(c.boldRed) # REGOLITH
hYellowUnder = under.copy()
hYellowUnder.fill(c.highlightYellow) # ELECTRONICS
hOrangeUnder = under.copy()
hOrangeUnder.fill(c.highlightOrange) # PLASTICS

blankTile = transUnder.copy()
blankTile.set_colorkey(c.trans)

#rockets
whiteRocket = whiteUnder.copy()
whiteRocket.blit(buildRocket,(0,0))
whiteRocket.set_colorkey(c.trans)

greyRocket = greyUnder.copy()
greyRocket.blit(buildRocket,(0,0))
greyRocket.set_colorkey(c.trans)

greenRocket = greenUnder.copy()
greenRocket.blit(buildRocket,(0,0))
greenRocket.set_colorkey(c.trans)

aquaRocket = aquaUnder.copy()
aquaRocket.blit(buildRocket,(0,0))
aquaRocket.set_colorkey(c.trans)

blueRocket = blueUnder.copy()
blueRocket.blit(buildRocket,(0,0))
blueRocket.set_colorkey(c.trans)

hYellowRocket = hYellowUnder.copy()
hYellowRocket.blit(buildRocket,(0,0))
hYellowRocket.set_colorkey(c.trans)

redRocket = redUnder.copy()
redRocket.blit(buildRocket,(0,0))
redRocket.set_colorkey(c.trans)

orangeRocket = orangeUnder.copy()
orangeRocket.blit(buildRocket,(0,0))
orangeRocket.set_colorkey(c.trans)

pinkRocket = pinkUnder.copy()
pinkRocket.blit(buildRocket,(0,0))
pinkRocket.set_colorkey(c.trans)

purpleRocket = purpleUnder.copy()
purpleRocket.blit(buildRocket,(0,0))
purpleRocket.set_colorkey(c.trans)

dGreenRocket = dGreenUnder.copy()
dGreenRocket.blit(buildRocket,(0,0))
dGreenRocket.set_colorkey(c.trans)

dRedRocket = dRedUnder.copy()
dRedRocket.blit(buildRocket,(0,0))
dRedRocket.set_colorkey(c.trans)

hOrangeRocket = hOrangeUnder.copy()
hOrangeRocket.blit(buildRocket,(0,0))
hOrangeRocket.set_colorkey(c.trans)

#finished buildings
#XS overlays
clearXSD = transUnder.copy()
clearXSD.blit(buildXSD,(0,0))
clearXSD.set_colorkey(c.trans)

clearXSU = transUnder.copy()
clearXSU.blit(buildXSU,(0,0))
clearXSU.set_colorkey(c.trans)

clearXSR = transUnder.copy()
clearXSR.blit(buildXSR,(0,0))
clearXSR.set_colorkey(c.trans)

clearXSL = transUnder.copy()
clearXSL.blit(buildXSL,(0,0))
clearXSL.set_colorkey(c.trans)

whiteXSD = whiteUnder.copy()
whiteXSD.blit(buildXSD,(0,0))
whiteXSD.set_colorkey(c.trans)

whiteXSU = whiteUnder.copy()
whiteXSU.blit(buildXSU,(0,0))
whiteXSU.set_colorkey(c.trans)

whiteXSR = whiteUnder.copy()
whiteXSR.blit(buildXSR,(0,0))
whiteXSR.set_colorkey(c.trans)

whiteXSL = whiteUnder.copy()
whiteXSL.blit(buildXSL,(0,0))
whiteXSL.set_colorkey(c.trans)

greyXSD = greyUnder.copy()
greyXSD.blit(buildXSD,(0,0))
greyXSD.set_colorkey(c.trans)

greyXSU = greyUnder.copy()
greyXSU.blit(buildXSU,(0,0))
greyXSU.set_colorkey(c.trans)

greyXSR = greyUnder.copy()
greyXSR.blit(buildXSR,(0,0))
greyXSR.set_colorkey(c.trans)

greyXSL = greyUnder.copy()
greyXSL.blit(buildXSL,(0,0))
greyXSL.set_colorkey(c.trans)

greenXSD = greenUnder.copy()
greenXSD.blit(buildXSD,(0,0))
greenXSD.set_colorkey(c.trans)

greenXSU = greenUnder.copy()
greenXSU.blit(buildXSU,(0,0))
greenXSU.set_colorkey(c.trans)

greenXSR = greenUnder.copy()
greenXSR.blit(buildXSR,(0,0))
greenXSR.set_colorkey(c.trans)

greenXSL = greenUnder.copy()
greenXSL.blit(buildXSL,(0,0))
greenXSL.set_colorkey(c.trans)

aquaXSD = aquaUnder.copy()
aquaXSD.blit(buildXSD,(0,0))
aquaXSD.set_colorkey(c.trans)

aquaXSU = aquaUnder.copy()
aquaXSU.blit(buildXSU,(0,0))
aquaXSU.set_colorkey(c.trans)

aquaXSR = aquaUnder.copy()
aquaXSR.blit(buildXSR,(0,0))
aquaXSR.set_colorkey(c.trans)

aquaXSL = aquaUnder.copy()
aquaXSL.blit(buildXSL,(0,0))
aquaXSL.set_colorkey(c.trans)

yellowXSD = yellowUnder.copy()
yellowXSD.blit(buildXSD,(0,0))
yellowXSD.set_colorkey(c.trans)

yellowXSU = yellowUnder.copy()
yellowXSU.blit(buildXSU,(0,0))
yellowXSU.set_colorkey(c.trans)

yellowXSR = yellowUnder.copy()
yellowXSR.blit(buildXSR,(0,0))
yellowXSR.set_colorkey(c.trans)

yellowXSL = yellowUnder.copy()
yellowXSL.blit(buildXSL,(0,0))
yellowXSL.set_colorkey(c.trans)

redXSD = redUnder.copy()
redXSD.blit(buildXSD,(0,0))
redXSD.set_colorkey(c.trans)

redXSU = redUnder.copy()
redXSU.blit(buildXSU,(0,0))
redXSU.set_colorkey(c.trans)

redXSR = redUnder.copy()
redXSR.blit(buildXSR,(0,0))
redXSR.set_colorkey(c.trans)

redXSL = redUnder.copy()
redXSL.blit(buildXSL,(0,0))
redXSL.set_colorkey(c.trans)

orangeXSD = orangeUnder.copy()
orangeXSD.blit(buildXSD,(0,0))
orangeXSD.set_colorkey(c.trans)

orangeXSU = orangeUnder.copy()
orangeXSU.blit(buildXSU,(0,0))
orangeXSU.set_colorkey(c.trans)

orangeXSR = orangeUnder.copy()
orangeXSR.blit(buildXSR,(0,0))
orangeXSR.set_colorkey(c.trans)

orangeXSL = orangeUnder.copy()
orangeXSL.blit(buildXSL,(0,0))
orangeXSL.set_colorkey(c.trans)

blueXSD = blueUnder.copy()
blueXSD.blit(buildXSD,(0,0))
blueXSD.set_colorkey(c.trans)

blueXSU = blueUnder.copy()
blueXSU.blit(buildXSU,(0,0))
blueXSU.set_colorkey(c.trans)

blueXSR = blueUnder.copy()
blueXSR.blit(buildXSR,(0,0))
blueXSR.set_colorkey(c.trans)

blueXSL = blueUnder.copy()
blueXSL.blit(buildXSL,(0,0))
blueXSL.set_colorkey(c.trans)

purpleXSD = purpleUnder.copy()
purpleXSD.blit(buildXSD,(0,0))
purpleXSD.set_colorkey(c.trans)

purpleXSU = purpleUnder.copy()
purpleXSU.blit(buildXSU,(0,0))
purpleXSU.set_colorkey(c.trans)

purpleXSR = purpleUnder.copy()
purpleXSR.blit(buildXSR,(0,0))
purpleXSR.set_colorkey(c.trans)

purpleXSL = purpleUnder.copy()
purpleXSL.blit(buildXSL,(0,0))
purpleXSL.set_colorkey(c.trans)

pinkXSD = pinkUnder.copy()
pinkXSD.blit(buildXSD,(0,0))
pinkXSD.set_colorkey(c.trans)

pinkXSU = pinkUnder.copy()
pinkXSU.blit(buildXSU,(0,0))
pinkXSU.set_colorkey(c.trans)

pinkXSR = pinkUnder.copy()
pinkXSR.blit(buildXSR,(0,0))
pinkXSR.set_colorkey(c.trans)

pinkXSL = pinkUnder.copy()
pinkXSL.blit(buildXSL,(0,0))
pinkXSL.set_colorkey(c.trans)

#S overlays
clearSD = transUnder.copy()
clearSD.blit(buildSD,(0,0))
clearSD.set_colorkey(c.trans)

clearSU = transUnder.copy()
clearSU.blit(buildSU,(0,0))
clearSU.set_colorkey(c.trans)

clearSR = transUnder.copy()
clearSR.blit(buildSR,(0,0))
clearSR.set_colorkey(c.trans)

clearSL = transUnder.copy()
clearSL.blit(buildSL,(0,0))
clearSL.set_colorkey(c.trans)

whiteSD = whiteUnder.copy()
whiteSD.blit(buildSD,(0,0))
whiteSD.set_colorkey(c.trans)

whiteSU = whiteUnder.copy()
whiteSU.blit(buildSU,(0,0))
whiteSU.set_colorkey(c.trans)

whiteSR = whiteUnder.copy()
whiteSR.blit(buildSR,(0,0))
whiteSR.set_colorkey(c.trans)

whiteSL = whiteUnder.copy()
whiteSL.blit(buildSL,(0,0))
whiteSL.set_colorkey(c.trans)

greySD = greyUnder.copy()
greySD.blit(buildSD,(0,0))
greySD.set_colorkey(c.trans)

greySU = greyUnder.copy()
greySU.blit(buildSU,(0,0))
greySU.set_colorkey(c.trans)

greySR = greyUnder.copy()
greySR.blit(buildSR,(0,0))
greySR.set_colorkey(c.trans)

greySL = greyUnder.copy()
greySL.blit(buildSL,(0,0))
greySL.set_colorkey(c.trans)

greenSD = greenUnder.copy()
greenSD.blit(buildSD,(0,0))
greenSD.set_colorkey(c.trans)

greenSU = greenUnder.copy()
greenSU.blit(buildSU,(0,0))
greenSU.set_colorkey(c.trans)

greenSR = greenUnder.copy()
greenSR.blit(buildSR,(0,0))
greenSR.set_colorkey(c.trans)

greenSL = greenUnder.copy()
greenSL.blit(buildSL,(0,0))
greenSL.set_colorkey(c.trans)

aquaSD = aquaUnder.copy()
aquaSD.blit(buildSD,(0,0))
aquaSD.set_colorkey(c.trans)

aquaSU = aquaUnder.copy()
aquaSU.blit(buildSU,(0,0))
aquaSU.set_colorkey(c.trans)

aquaSR = aquaUnder.copy()
aquaSR.blit(buildSR,(0,0))
aquaSR.set_colorkey(c.trans)

aquaSL = aquaUnder.copy()
aquaSL.blit(buildSL,(0,0))
aquaSL.set_colorkey(c.trans)

yellowSD = yellowUnder.copy()
yellowSD.blit(buildSD,(0,0))
yellowSD.set_colorkey(c.trans)

yellowSU = yellowUnder.copy()
yellowSU.blit(buildSU,(0,0))
yellowSU.set_colorkey(c.trans)

yellowSR = yellowUnder.copy()
yellowSR.blit(buildSR,(0,0))
yellowSR.set_colorkey(c.trans)

yellowSL = yellowUnder.copy()
yellowSL.blit(buildSL,(0,0))
yellowSL.set_colorkey(c.trans)

redSD = redUnder.copy()
redSD.blit(buildSD,(0,0))
redSD.set_colorkey(c.trans)

redSU = redUnder.copy()
redSU.blit(buildSU,(0,0))
redSU.set_colorkey(c.trans)

redSR = redUnder.copy()
redSR.blit(buildSR,(0,0))
redSR.set_colorkey(c.trans)

redSL = redUnder.copy()
redSL.blit(buildSL,(0,0))
redSL.set_colorkey(c.trans)

orangeSD = orangeUnder.copy()
orangeSD.blit(buildSD,(0,0))
orangeSD.set_colorkey(c.trans)

orangeSU = orangeUnder.copy()
orangeSU.blit(buildSU,(0,0))
orangeSU.set_colorkey(c.trans)

orangeSR = orangeUnder.copy()
orangeSR.blit(buildSR,(0,0))
orangeSR.set_colorkey(c.trans)

orangeSL = orangeUnder.copy()
orangeSL.blit(buildSL,(0,0))
orangeSL.set_colorkey(c.trans)

blueSD = blueUnder.copy()
blueSD.blit(buildSD,(0,0))
blueSD.set_colorkey(c.trans)

blueSU = blueUnder.copy()
blueSU.blit(buildSU,(0,0))
blueSU.set_colorkey(c.trans)

blueSR = blueUnder.copy()
blueSR.blit(buildSR,(0,0))
blueSR.set_colorkey(c.trans)

blueSL = blueUnder.copy()
blueSL.blit(buildSL,(0,0))
blueSL.set_colorkey(c.trans)

purpleSD = purpleUnder.copy()
purpleSD.blit(buildSD,(0,0))
purpleSD.set_colorkey(c.trans)

purpleSU = purpleUnder.copy()
purpleSU.blit(buildSU,(0,0))
purpleSU.set_colorkey(c.trans)

purpleSR = purpleUnder.copy()
purpleSR.blit(buildSR,(0,0))
purpleSR.set_colorkey(c.trans)

purpleSL = purpleUnder.copy()
purpleSL.blit(buildSL,(0,0))
purpleSL.set_colorkey(c.trans)

pinkSD = pinkUnder.copy()
pinkSD.blit(buildSD,(0,0))
pinkSD.set_colorkey(c.trans)

pinkSU = pinkUnder.copy()
pinkSU.blit(buildSU,(0,0))
pinkSU.set_colorkey(c.trans)

pinkSR = pinkUnder.copy()
pinkSR.blit(buildSR,(0,0))
pinkSR.set_colorkey(c.trans)

pinkSL = pinkUnder.copy()
pinkSL.blit(buildSL,(0,0))
pinkSL.set_colorkey(c.trans)

#M overlays
clearMDR = transUnder.copy()
clearMDR.blit(buildMDR,(0,0))
clearMDR.set_colorkey(c.trans)

clearMUR = transUnder.copy()
clearMUR.blit(buildMUR,(0,0))
clearMUR.set_colorkey(c.trans)

clearMDL = transUnder.copy()
clearMDL.blit(buildMDL,(0,0))
clearMDL.set_colorkey(c.trans)

clearMUL = transUnder.copy()
clearMUL.blit(buildMUL,(0,0))
clearMUL.set_colorkey(c.trans)

whiteMDR = whiteUnder.copy()
whiteMDR.blit(buildMDR,(0,0))
whiteMDR.set_colorkey(c.trans)

whiteMUR = whiteUnder.copy()
whiteMUR.blit(buildMUR,(0,0))
whiteMUR.set_colorkey(c.trans)

whiteMDL = whiteUnder.copy()
whiteMDL.blit(buildMDL,(0,0))
whiteMDL.set_colorkey(c.trans)

whiteMUL = whiteUnder.copy()
whiteMUL.blit(buildMUL,(0,0))
whiteMUL.set_colorkey(c.trans)

greyMDR = greyUnder.copy()
greyMDR.blit(buildMDR,(0,0))
greyMDR.set_colorkey(c.trans)

greyMUR = greyUnder.copy()
greyMUR.blit(buildMUR,(0,0))
greyMUR.set_colorkey(c.trans)

greyMDL = greyUnder.copy()
greyMDL.blit(buildMDL,(0,0))
greyMDL.set_colorkey(c.trans)

greyMUL = greyUnder.copy()
greyMUL.blit(buildMUL,(0,0))
greyMUL.set_colorkey(c.trans)

greenMDR = greenUnder.copy()
greenMDR.blit(buildMDR,(0,0))
greenMDR.set_colorkey(c.trans)

greenMUR = greenUnder.copy()
greenMUR.blit(buildMUR,(0,0))
greenMUR.set_colorkey(c.trans)

greenMDL = greenUnder.copy()
greenMDL.blit(buildMDL,(0,0))
greenMDL.set_colorkey(c.trans)

greenMUL = greenUnder.copy()
greenMUL.blit(buildMUL,(0,0))
greenMUL.set_colorkey(c.trans)

aquaMDR = aquaUnder.copy()
aquaMDR.blit(buildMDR,(0,0))
aquaMDR.set_colorkey(c.trans)

aquaMUR = aquaUnder.copy()
aquaMUR.blit(buildMUR,(0,0))
aquaMUR.set_colorkey(c.trans)

aquaMDL = aquaUnder.copy()
aquaMDL.blit(buildMDL,(0,0))
aquaMDL.set_colorkey(c.trans)

aquaMUL = aquaUnder.copy()
aquaMUL.blit(buildMUL,(0,0))
aquaMUL.set_colorkey(c.trans)

yellowMDR = yellowUnder.copy()
yellowMDR.blit(buildMDR,(0,0))
yellowMDR.set_colorkey(c.trans)

yellowMUR = yellowUnder.copy()
yellowMUR.blit(buildMUR,(0,0))
yellowMUR.set_colorkey(c.trans)

yellowMDL = yellowUnder.copy()
yellowMDL.blit(buildMDL,(0,0))
yellowMDL.set_colorkey(c.trans)

yellowMUL = yellowUnder.copy()
yellowMUL.blit(buildMUL,(0,0))
yellowMUL.set_colorkey(c.trans)

redMDR = redUnder.copy()
redMDR.blit(buildMDR,(0,0))
redMDR.set_colorkey(c.trans)

redMUR = redUnder.copy()
redMUR.blit(buildMUR,(0,0))
redMUR.set_colorkey(c.trans)

redMDL = redUnder.copy()
redMDL.blit(buildMDL,(0,0))
redMDL.set_colorkey(c.trans)

redMUL = redUnder.copy()
redMUL.blit(buildMUL,(0,0))
redMUL.set_colorkey(c.trans)

orangeMDR = orangeUnder.copy()
orangeMDR.blit(buildMDR,(0,0))
orangeMDR.set_colorkey(c.trans)

orangeMUR = orangeUnder.copy()
orangeMUR.blit(buildMUR,(0,0))
orangeMUR.set_colorkey(c.trans)

orangeMDL = orangeUnder.copy()
orangeMDL.blit(buildMDL,(0,0))
orangeMDL.set_colorkey(c.trans)

orangeMUL = orangeUnder.copy()
orangeMUL.blit(buildMUL,(0,0))
orangeMUL.set_colorkey(c.trans)

blueMDR = blueUnder.copy()
blueMDR.blit(buildMDR,(0,0))
blueMDR.set_colorkey(c.trans)

blueMUR = blueUnder.copy()
blueMUR.blit(buildMUR,(0,0))
blueMUR.set_colorkey(c.trans)

blueMDL = blueUnder.copy()
blueMDL.blit(buildMDL,(0,0))
blueMDL.set_colorkey(c.trans)

blueMUL = blueUnder.copy()
blueMUL.blit(buildMUL,(0,0))
blueMUL.set_colorkey(c.trans)

purpleMDR = purpleUnder.copy()
purpleMDR.blit(buildMDR,(0,0))
purpleMDR.set_colorkey(c.trans)

purpleMUR = purpleUnder.copy()
purpleMUR.blit(buildMUR,(0,0))
purpleMUR.set_colorkey(c.trans)

purpleMDL = purpleUnder.copy()
purpleMDL.blit(buildMDL,(0,0))
purpleMDL.set_colorkey(c.trans)

purpleMUL = purpleUnder.copy()
purpleMUL.blit(buildMUL,(0,0))
purpleMUL.set_colorkey(c.trans)

pinkMDR = pinkUnder.copy()
pinkMDR.blit(buildMDR,(0,0))
pinkMDR.set_colorkey(c.trans)

pinkMUR = pinkUnder.copy()
pinkMUR.blit(buildMUR,(0,0))
pinkMUR.set_colorkey(c.trans)

pinkMDL = pinkUnder.copy()
pinkMDL.blit(buildMDL,(0,0))
pinkMDL.set_colorkey(c.trans)

pinkMUL = pinkUnder.copy()
pinkMUL.blit(buildMUL,(0,0))
pinkMUL.set_colorkey(c.trans)

#ML overlays
clearMLDR = transUnder.copy()
clearMLDR.blit(buildMLDR,(0,0))
clearMLDR.set_colorkey(c.trans)

clearMLUR = transUnder.copy()
clearMLUR.blit(buildMLUR,(0,0))
clearMLUR.set_colorkey(c.trans)

clearMLDL = transUnder.copy()
clearMLDL.blit(buildMLDL,(0,0))
clearMLDL.set_colorkey(c.trans)

clearMLUL = transUnder.copy()
clearMLUL.blit(buildMLUL,(0,0))
clearMLUL.set_colorkey(c.trans)

whiteMLDR = whiteUnder.copy()
whiteMLDR.blit(buildMLDR,(0,0))
whiteMLDR.set_colorkey(c.trans)

whiteMLUR = whiteUnder.copy()
whiteMLUR.blit(buildMLUR,(0,0))
whiteMLUR.set_colorkey(c.trans)

whiteMLDL = whiteUnder.copy()
whiteMLDL.blit(buildMLDL,(0,0))
whiteMLDL.set_colorkey(c.trans)

whiteMLUL = whiteUnder.copy()
whiteMLUL.blit(buildMLUL,(0,0))
whiteMLUL.set_colorkey(c.trans)

greyMLDR = greyUnder.copy()
greyMLDR.blit(buildMLDR,(0,0))
greyMLDR.set_colorkey(c.trans)

greyMLUR = greyUnder.copy()
greyMLUR.blit(buildMLUR,(0,0))
greyMLUR.set_colorkey(c.trans)

greyMLDL = greyUnder.copy()
greyMLDL.blit(buildMLDL,(0,0))
greyMLDL.set_colorkey(c.trans)

greyMLUL = greyUnder.copy()
greyMLUL.blit(buildMLUL,(0,0))
greyMLUL.set_colorkey(c.trans)

greenMLDR = greenUnder.copy()
greenMLDR.blit(buildMLDR,(0,0))
greenMLDR.set_colorkey(c.trans)

greenMLUR = greenUnder.copy()
greenMLUR.blit(buildMLUR,(0,0))
greenMLUR.set_colorkey(c.trans)

greenMLDL = greenUnder.copy()
greenMLDL.blit(buildMLDL,(0,0))
greenMLDL.set_colorkey(c.trans)

greenMLUL = greenUnder.copy()
greenMLUL.blit(buildMLUL,(0,0))
greenMLUL.set_colorkey(c.trans)

aquaMLDR = aquaUnder.copy()
aquaMLDR.blit(buildMLDR,(0,0))
aquaMLDR.set_colorkey(c.trans)

aquaMLUR = aquaUnder.copy()
aquaMLUR.blit(buildMLUR,(0,0))
aquaMLUR.set_colorkey(c.trans)

aquaMLDL = aquaUnder.copy()
aquaMLDL.blit(buildMLDL,(0,0))
aquaMLDL.set_colorkey(c.trans)

aquaMLUL = aquaUnder.copy()
aquaMLUL.blit(buildMLUL,(0,0))
aquaMLUL.set_colorkey(c.trans)

yellowMLDR = yellowUnder.copy()
yellowMLDR.blit(buildMLDR,(0,0))
yellowMLDR.set_colorkey(c.trans)

yellowMLUR = yellowUnder.copy()
yellowMLUR.blit(buildMLUR,(0,0))
yellowMLUR.set_colorkey(c.trans)

yellowMLDL = yellowUnder.copy()
yellowMLDL.blit(buildMLDL,(0,0))
yellowMLDL.set_colorkey(c.trans)

yellowMLUL = yellowUnder.copy()
yellowMLUL.blit(buildMLUL,(0,0))
yellowMLUL.set_colorkey(c.trans)

redMLDR = redUnder.copy()
redMLDR.blit(buildMLDR,(0,0))
redMLDR.set_colorkey(c.trans)

redMLUR = redUnder.copy()
redMLUR.blit(buildMLUR,(0,0))
redMLUR.set_colorkey(c.trans)

redMLDL = redUnder.copy()
redMLDL.blit(buildMLDL,(0,0))
redMLDL.set_colorkey(c.trans)

redMLUL = redUnder.copy()
redMLUL.blit(buildMLUL,(0,0))
redMLUL.set_colorkey(c.trans)

orangeMLDR = orangeUnder.copy()
orangeMLDR.blit(buildMLDR,(0,0))
orangeMLDR.set_colorkey(c.trans)

orangeMLUR = orangeUnder.copy()
orangeMLUR.blit(buildMLUR,(0,0))
orangeMLUR.set_colorkey(c.trans)

orangeMLDL = orangeUnder.copy()
orangeMLDL.blit(buildMLDL,(0,0))
orangeMLDL.set_colorkey(c.trans)

orangeMLUL = orangeUnder.copy()
orangeMLUL.blit(buildMLUL,(0,0))
orangeMLUL.set_colorkey(c.trans)

blueMLDR = blueUnder.copy()
blueMLDR.blit(buildMLDR,(0,0))
blueMLDR.set_colorkey(c.trans)

blueMLUR = blueUnder.copy()
blueMLUR.blit(buildMLUR,(0,0))
blueMLUR.set_colorkey(c.trans)

blueMLDL = blueUnder.copy()
blueMLDL.blit(buildMLDL,(0,0))
blueMLDL.set_colorkey(c.trans)

blueMLUL = blueUnder.copy()
blueMLUL.blit(buildMLUL,(0,0))
blueMLUL.set_colorkey(c.trans)

purpleMLDR = purpleUnder.copy()
purpleMLDR.blit(buildMLDR,(0,0))
purpleMLDR.set_colorkey(c.trans)

purpleMLUR = purpleUnder.copy()
purpleMLUR.blit(buildMLUR,(0,0))
purpleMLUR.set_colorkey(c.trans)

purpleMLDL = purpleUnder.copy()
purpleMLDL.blit(buildMLDL,(0,0))
purpleMLDL.set_colorkey(c.trans)

purpleMLUL = purpleUnder.copy()
purpleMLUL.blit(buildMLUL,(0,0))
purpleMLUL.set_colorkey(c.trans)

pinkMLDR = pinkUnder.copy()
pinkMLDR.blit(buildMLDR,(0,0))
pinkMLDR.set_colorkey(c.trans)

pinkMLUR = pinkUnder.copy()
pinkMLUR.blit(buildMLUR,(0,0))
pinkMLUR.set_colorkey(c.trans)

pinkMLDL = pinkUnder.copy()
pinkMLDL.blit(buildMLDL,(0,0))
pinkMLDL.set_colorkey(c.trans)

pinkMLUL = pinkUnder.copy()
pinkMLUL.blit(buildMLUL,(0,0))
pinkMLUL.set_colorkey(c.trans)

#L overlays
clearL = transUnder.copy()
clearL.blit(buildL,(0,0))
clearL.set_colorkey(c.trans)

whiteL = whiteUnder.copy()
whiteL.blit(buildL,(0,0))
whiteL.set_colorkey(c.trans)

greyL = greyUnder.copy()
greyL.blit(buildL,(0,0))
greyL.set_colorkey(c.trans)

greenL = greenUnder.copy()
greenL.blit(buildL,(0,0))
greenL.set_colorkey(c.trans)

aquaL = aquaUnder.copy()
aquaL.blit(buildL,(0,0))
aquaL.set_colorkey(c.trans)

yellowL = yellowUnder.copy()
yellowL.blit(buildL,(0,0))
yellowL.set_colorkey(c.trans)

redL = redUnder.copy()
redL.blit(buildL,(0,0))
redL.set_colorkey(c.trans)

orangeL = orangeUnder.copy()
orangeL.blit(buildL,(0,0))
orangeL.set_colorkey(c.trans)

blueL = blueUnder.copy()
blueL.blit(buildL,(0,0))
blueL.set_colorkey(c.trans)

purpleL = purpleUnder.copy()
purpleL.blit(buildL,(0,0))
purpleL.set_colorkey(c.trans)

pinkL = pinkUnder.copy()
pinkL.blit(buildL,(0,0))
pinkL.set_colorkey(c.trans)

#XL overXLays
clearXL = transUnder.copy()
clearXL.blit(buildXL,(0,0))
clearXL.set_colorkey(c.trans)

whiteXL = whiteUnder.copy()
whiteXL.blit(buildXL,(0,0))
whiteXL.set_colorkey(c.trans)

greyXL = greyUnder.copy()
greyXL.blit(buildXL,(0,0))
greyXL.set_colorkey(c.trans)

greenXL = greenUnder.copy()
greenXL.blit(buildXL,(0,0))
greenXL.set_colorkey(c.trans)

aquaXL = aquaUnder.copy()
aquaXL.blit(buildXL,(0,0))
aquaXL.set_colorkey(c.trans)

yellowXL = yellowUnder.copy()
yellowXL.blit(buildXL,(0,0))
yellowXL.set_colorkey(c.trans)

redXL = redUnder.copy()
redXL.blit(buildXL,(0,0))
redXL.set_colorkey(c.trans)

orangeXL = orangeUnder.copy()
orangeXL.blit(buildXL,(0,0))
orangeXL.set_colorkey(c.trans)

blueXL = blueUnder.copy()
blueXL.blit(buildXL,(0,0))
blueXL.set_colorkey(c.trans)

purpleXL = purpleUnder.copy()
purpleXL.blit(buildXL,(0,0))
purpleXL.set_colorkey(c.trans)

pinkXL = pinkUnder.copy()
pinkXL.blit(buildXL,(0,0))
pinkXL.set_colorkey(c.trans)


