import pygame
import mapTileBuilding as o
import assets as a
import color as c
import draw as d



class Space:
    def __init__(self):
        self.launches = []
        self.launchRects = []
        self.earthRange = -50
        self.earthInc = -0.8
        self.marsRange = 0
        self.marsInc = 1.3
        self.durationFactor = 3.0
        self.duration = self.durationFactor * abs(self.marsRange-self.earthRange)

    def drawLaunches(self,canvas,leftBorder):
        launchY = 600 - 34
        self.resetLaunchRects()
        for launch in self.launches:
            if launch.landed:
                if launch.fadeAnimation == None:
                    launch.fade((leftBorder + 8, launchY))
                    launch.fadeAnimation.runAnimation()
                    launch.fadeAnimation.draw(canvas)
                    
                else:
                    launch.fadeAnimation.runAnimation()
                    launch.fadeAnimation.draw(canvas)
                    launchY += launch.fadeOffset
                    if launch.fadeOffset < 24:
                        launch.fadeOffset += 1
                    if launch.fadeAnimation.on == False:
                        self.launches.remove(launch)
            else:    
                launchRect = launch.draw(canvas,(leftBorder + 8, launchY))
                self.addLaunchRect(launchRect)
            launchY -= 24

    def checkLaunches(self):
        if len(self.launches) > 0:
            for launch in self.launches:
                if launch.arrived and launch.spaceport:
                    launch.spaceportSwitch = True
            return True
        else:
            return False

    def addLaunch(self, launch):
        self.launches.append(launch)
    
    def addLaunchRect(self,launchRect):
        self.launchRects.append(launchRect)
    
    def resetLaunchRects(self):
        self.launchRects = []

    def timePass(self):
        for launch in self.launches:
            launch.advanceLaunch()
        self.marsRange += self.marsInc
        if self.marsRange >= 230 or self.marsRange <= 0:
            self.marsInc *= -1
        self.earthRange += self.earthInc
        if self.earthRange >= -50 or self.earthRange <= -170:
            self.earthInc *= -1
        self.duration = int(self.durationFactor * abs(self.marsRange-self.earthRange))
        
        
    
    def getDurationText(self):
        text = d.getTextSurface("EARTH/MARS TRIP: " + str(self.duration) + "sol",size = 16)
        return text
            


class Launch:
    def __init__(self,base,duration,buildingCapsule,orbital=False,spaceport=False):
        self.launchSol = base.sol
        self.sols = 0
        self.duration = duration
        self.arrived = False
        self.landed = False
        self.progress = 0.0
        self.progressBar = 0 # out of 250
        self.clicked = False
        self.arrivedButtonAlpha = 255
        self.arrivedButtonIncrement = -5
        self.capsule = buildingCapsule
        self.unloadBuildingCapsule(buildingCapsule)
        self.arrivedButton = d.Button(self.payloadTag + " ARRIVED",300)
        self.fadeAnimation = None
        self.fadeOffset = 0
        self.orbital = orbital
        self.spaceport = spaceport
        self.spaceportSwitch = False

    def setLanded(self):
        self.landed = True

    def getSaveList(self):
        duration = self.duration
        tag = self.payloadTag
        orbital = self.orbital
        spaceport = self.spaceport
        solsElapsed = self.sols
        saveList = [duration,tag,orbital,spaceport,solsElapsed]
        return saveList

    def autoLander(self,builderObject,base):
        builderObject.setActiveBuildingFromLaunch(self)
        for building in base.transportList:
            if isinstance(building,o.SpacePort):
                tile = building.tile 
        if builderObject.launchObject != self:
            builderObject.launchObject = self ## WATCH LOGIC!!
        builderObject.createBuildingObject(base,tile,True)
        self.spaceportSwitch = False
        self.landed = True

    def fade(self,loc):
        self.fadeAnimation = d.Animation([self.arrivedButton.getSurface()],loc,fadeOut=True,alphaVelocity=-15)   

    def unloadBuildingCapsule(self,capsule):
        if isinstance(capsule[0],str):
            tag = capsule[0]
        else:
            tag = capsule[0][0]
        self.payloadTag = tag
        self.payloadSize = capsule[1]
        self.payloadPreview = capsule[3]

    def chooseLandingSite(self,builderObject):
        self.clicked = True
        if self.spaceport == False:
            self.arrivedButton = d.Button("CHOOSE LANDING SITE",300)
        self.arrivedButton.toggleSelected()
        self.arrivedButton.getSurface().set_alpha(255)
        builderObject.setActiveBuildingFromLaunch(self)

    def draw(self,screen,pos):
        if self.orbital:
            canvas = a.blankOrbitalLaunch.copy()
        else:
            canvas = a.blankLaunch.copy()
        startX = 25
        endX = 25 + self.progressBar
        pygame.draw.line(canvas,c.grey,(startX,11),(endX,11),2)
        if self.arrived:
            if self.clicked == False:
                buttonSurface = self.arrivedButton.getSurface()
                buttonSurface.set_alpha(self.arrivedButtonAlpha)
                canvas.blit(buttonSurface,(0,0))
                self.arrivedButtonAlpha += self.arrivedButtonIncrement
                if self.arrivedButtonAlpha == 255 or self.arrivedButtonAlpha == 100:
                    self.arrivedButtonIncrement *= -1
            else:
                buttonSurface = self.arrivedButton.getSurface()
                canvas.blit(buttonSurface,(0,0))
        launchRect = screen.blit(canvas,pos)
        return launchRect

    def advanceLaunch(self):
        if self.arrived == False:
            self.sols+=1
            self.progress = self.sols / self.duration
            self.progressBar = int(self.progress * 250)
            if self.sols >= self.duration:
                self.arrived = True
        
        