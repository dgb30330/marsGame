import pygame
import color as c
import assets as a
import mapTileBuilding as o
import people as p

def getPauseScreen(screen,fadeFactor = 0):
    back = screen.copy()
    backFade = pygame.Surface((screen.get_width(),screen.get_height()))
    backFade.fill(c.black)
    backFade.set_alpha(255-fadeFactor)
    pauseText = getTextSurface("-PAUSED-", c.boldRed, 30)
    back.blit(pauseText,(int(back.get_width()/2)-int(pauseText.get_width()/2),10))
    if fadeFactor > 0:
        back.blit(backFade,(0,0))
    return back

def getFade(myBase,tileDetail,lightFade):
    #TODO might add timepad
    fadeFactor = 3
    if myBase.dustEvent>0:
        if myBase.dustEvent > myBase.dustEventDuration/2:
            myBase.dustAlpha += fadeFactor/500.0
            lightFade.set_alpha(int(myBase.dustAlpha))
        else:
            myBase.dustAlpha -= fadeFactor/500.0
            lightFade.set_alpha(int(myBase.dustAlpha))
    else:
        lightFade.set_alpha(5*fadeFactor)
    #lightFade.convert_alpha()
    return lightFade


def createBlankTiles(mapObject):
    TileSurface.grid = []
    xGrid = 1
    while xGrid <= mapObject.dimension:
        thisRow = []
        yGrid = 1
        while yGrid <= mapObject.dimension:
            #print("initializing surface draw")
            newTileSurface = TileSurface(xGrid,yGrid)
            thisRow.append(newTileSurface)
            yGrid +=1
        TileSurface.grid.append(thisRow) 
        xGrid += 1

class TileSurface:
    grid = [[]]
    @staticmethod
    def getTile(x,y):
        for row in TileSurface.grid:
            for tile in row:
                if tile.y == y and tile.x == x:
                    return tile

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.surface = a.tile.copy()
        self.surfaceS = a.tileSelected.copy()
        self.surfaceMO = a.tileMO.copy()
        self.animations = []
        self.buildingInfoObjects = []
        self.infoObject = None
        

def drawTileDetail(screen,tile,mouseLoc,sol):
    offset = 32
    gap = 5
    tileSurface = tile.getTileSurfaceObject()
    if len(tileSurface.buildingInfoObjects) == 0:
        for building in tile.tileBuildings:
            newInfoObj = InfoObject(building)
            tileSurface.buildingInfoObjects.append(newInfoObj)
    done = []
    buttonsShut = []
    buttonRectsShut = []
    buttonsPri = []
    buttonRectsPri = []
    for each in tileSurface.buildingInfoObjects:
        if each.object == tile.upBuilding:
            upLoc = (tile.upAnchor[0]-each.surface.get_width()+offset,tile.upAnchor[1]-offset-each.surface.get_height())
            if each.object.readoutAnimate and each.object.readout > 0 and sol > each.lastRefresh:
                numbers = each.object.getReadoutSurface(12)
                readoutA = Animation([numbers],(tile.upAnchor[0],\
                    tile.upAnchor[1]-offset/2),yVelocity = -1,yLimit = \
                        tile.upAnchor[1]-numbers.get_height()*8,fadeOut=True,alphaVelocity=-8)
                tile.addAnimation(readoutA)
            if each.alpha == 255:
                ulColor = each.object.color
                pygame.draw.line(screen,ulColor,(upLoc[0]+int(each.surface.get_width()/2),upLoc[1]+each.surface.get_height()),\
                    (upLoc[0]+int(each.surface.get_width()/2),upLoc[1]+each.surface.get_height()+12),1)
                pygame.draw.line(screen,ulColor,(upLoc[0]+int(each.surface.get_width()/2),upLoc[1]+each.surface.get_height()+12),\
                    (tile.upAnchor[0],upLoc[1]+each.surface.get_height()+12),1)
                pygame.draw.line(screen,ulColor,(tile.upAnchor[0],upLoc[1]+each.surface.get_height()+12),\
                    tile.upAnchor,1)
                if each.shutoffButton != None:
                    upSBLoc = (upLoc[0]-each.shutoffButton.buttonSurface.get_width()-gap,\
                        upLoc[1]+each.surface.get_height()-each.shutoffButton.buttonSurface.get_height())
                    upPLoc = (upSBLoc[0],upSBLoc[1]-gap-each.shutoffButton.buttonSurface.get_height())
                    sRect = each.shutoffButton.draw(screen,upSBLoc,mouseLoc)
                    pRect = each.priorityButton.draw(screen,upPLoc,mouseLoc)
                    buttonsShut.append(each.shutoffButton)
                    buttonRectsShut.append(sRect)
                    buttonsPri.append(each.priorityButton)
                    buttonRectsPri.append(pRect)
            each.draw(screen,upLoc,absoluteLoc=True,sol=sol)
            done.append(each)  
    for each in tileSurface.buildingInfoObjects:
        if each.object == tile.rightBuilding and (each not in done):
            rightLoc = (tile.rightAnchor[0]+offset,tile.rightAnchor[1]-each.surface.get_height()+offset)
            if each.object.readoutAnimate and each.object.readout > 0 and sol > each.lastRefresh:
                numbers = each.object.getReadoutSurface(12)
                readoutA = Animation([numbers],(tile.rightAnchor[0]-int(numbers.get_width()/2)+10,\
                    tile.rightAnchor[1]-offset/2),yVelocity = -1,yLimit = \
                        tile.rightAnchor[1]-numbers.get_height()*8,fadeOut=True,alphaVelocity=-7)
                tile.addAnimation(readoutA)
            if each.alpha == 255:
                ulColor = each.object.color
                pygame.draw.line(screen,ulColor,(rightLoc[0]+each.surface.get_width(),\
                    rightLoc[1]+int(each.surface.get_height()/2)),(rightLoc[0]+each.surface.get_width()+12,\
                    rightLoc[1]+int(each.surface.get_height()/2)),1)
                pygame.draw.line(screen,ulColor,(rightLoc[0]+each.surface.get_width()+12,rightLoc[1]\
                    +int(each.surface.get_height()/2)),(rightLoc[0]+each.surface.get_width()+12,tile.rightAnchor[1]),1)
                pygame.draw.line(screen,ulColor,(rightLoc[0]+each.surface.get_width()+12,tile.rightAnchor[1]),\
                    tile.rightAnchor,1)
                if each.shutoffButton != None:
                    rightSBLoc = (rightLoc[0]+each.surface.get_width()+gap,rightLoc[1]+\
                        each.surface.get_height()-each.shutoffButton.buttonSurface.get_height())
                    rightPLoc = (rightSBLoc[0],rightSBLoc[1]-gap-each.shutoffButton.buttonSurface.get_height())
                    sRect = each.shutoffButton.draw(screen,rightSBLoc,mouseLoc)
                    pRect = each.priorityButton.draw(screen,rightPLoc,mouseLoc)
                    buttonsShut.append(each.shutoffButton)
                    buttonRectsShut.append(sRect)
                    buttonsPri.append(each.priorityButton)
                    buttonRectsPri.append(pRect)
            each.draw(screen,rightLoc,absoluteLoc=True,sol=sol)
            done.append(each)
    for each in tileSurface.buildingInfoObjects:
        if each.object == tile.leftBuilding and (each not in done):
            leftLoc = (tile.leftAnchor[0]-offset-each.surface.get_width(),tile.leftAnchor[1]-offset)
            if each.object.readoutAnimate and each.object.readout > 0 and sol > each.lastRefresh:
                numbers = each.object.getReadoutSurface(12)
                readoutA = Animation([numbers],(tile.leftAnchor[0]-int(numbers.get_width()/2)-10,\
                    tile.leftAnchor[1]-offset/2),yVelocity = -1,yLimit = \
                        tile.leftAnchor[1]-numbers.get_height()*8,fadeOut=True,alphaVelocity=-7)
                tile.addAnimation(readoutA)
            if each.alpha == 255:
                ulColor = each.object.color
                pygame.draw.line(screen,ulColor,(leftLoc[0],leftLoc[1]+int(each.surface.get_height()/2)),\
                    (leftLoc[0]-12,leftLoc[1]+int(each.surface.get_height()/2)),1)
                pygame.draw.line(screen,ulColor,(leftLoc[0]-12,leftLoc[1]+int(each.surface.get_height()/2)),\
                    (leftLoc[0]-12,tile.leftAnchor[1]),1)
                pygame.draw.line(screen,ulColor,(leftLoc[0]-12,tile.leftAnchor[1]),tile.leftAnchor,1)
                if each.shutoffButton != None:
                    leftPLoc = (leftLoc[0]-gap-each.shutoffButton.buttonSurface.get_width(),leftLoc[1])
                    leftSBLoc = (leftPLoc[0],leftPLoc[1]+gap+each.shutoffButton.buttonSurface.get_height())
                    sRect = each.shutoffButton.draw(screen,leftSBLoc,mouseLoc)
                    pRect = each.priorityButton.draw(screen,leftPLoc,mouseLoc)
                    buttonsShut.append(each.shutoffButton)
                    buttonRectsShut.append(sRect)
                    buttonsPri.append(each.priorityButton)
                    buttonRectsPri.append(pRect)
            each.draw(screen,leftLoc,absoluteLoc=True,sol=sol)
            done.append(each)
    for each in tileSurface.buildingInfoObjects:
        if each.object == tile.downBuilding and (each not in done):
            downLoc = (tile.downAnchor[0]-offset,tile.downAnchor[1]+offset)
            if each.object.readoutAnimate and each.object.readout > 0 and sol > each.lastRefresh:
                numbers = each.object.getReadoutSurface(12)
                readoutA = Animation([numbers],(tile.downAnchor[0]-numbers.get_width(),\
                    tile.downAnchor[1]-offset/2),yVelocity = -1,yLimit = \
                        tile.downAnchor[1]-numbers.get_height()*8,fadeOut=True,alphaVelocity=-6)
                tile.addAnimation(readoutA)
            if each.alpha == 255:
                ulColor = each.object.color
                pygame.draw.line(screen,ulColor,(downLoc[0]+int(each.surface.get_width()/2),downLoc[1]+each.surface.get_height()),\
                    (downLoc[0]+int(each.surface.get_width()/2),downLoc[1]+each.surface.get_height()+12),1)
                pygame.draw.line(screen,ulColor,(downLoc[0]+int(each.surface.get_width()/2),downLoc[1]+each.surface.get_height()+12),\
                    (tile.downAnchor[0],downLoc[1]+each.surface.get_height()+12),1)
                pygame.draw.line(screen,ulColor,(tile.downAnchor[0],downLoc[1]+each.surface.get_height()+12),tile.downAnchor,1)
                if each.shutoffButton != None:
                    downPLoc = (downLoc[0]+gap+each.surface.get_width(),downLoc[1])
                    downSBLoc = (downPLoc[0],downPLoc[1]+gap+each.shutoffButton.buttonSurface.get_height())
                    sRect = each.shutoffButton.draw(screen,downSBLoc,mouseLoc)
                    pRect = each.priorityButton.draw(screen,downPLoc,mouseLoc)
                    buttonsShut.append(each.shutoffButton)
                    buttonRectsShut.append(sRect)
                    buttonsPri.append(each.priorityButton)
                    buttonRectsPri.append(pRect)
            each.draw(screen,downLoc,absoluteLoc=True,sol=sol)
            done.append(each)
    screen.blit(tile.getSurface(),tile.anchor)
    #button parse here
    for sButton in buttonsShut:
        if sButton.selected:
            if sButton.dataEmbed.shutoff:
                approve = choicePopUp(screen,mouseLoc,\
                    ["Are you sure you want to", "bring this "+sButton.dataEmbed.buildingName,"back into operation?"])
            else:
                approve = choicePopUp(screen,mouseLoc,\
                    ["Are you sure you want to", "shut down this "+sButton.dataEmbed.buildingName+"?"])
            if approve:
                sButton.dataEmbed.shutoffBuilding()
                sButton.toggleSelected()
                sButton.makeDead()
    for pButton in buttonsPri:
        if pButton.selected:
            if len(sButton.dataEmbed.jobs) > 0:
                approve = choicePopUp(screen,mouseLoc,\
                    ["Prioritizing future hires for "+pButton.dataEmbed.buildingName, \
                        "would cost {0:.2f}".format(pButton.dataEmbed.base.getAdminCost()) + " admin points.","Go ahead?"])
            else:
                approve = choicePopUp(screen,mouseLoc,\
                    ["Re-engineering this "+pButton.dataEmbed.buildingName, \
                        "would cost {0:.2f}".format(pButton.dataEmbed.base.getAdminCost()) + " admin points.","Go ahead?"])
            if approve:
                pButton.dataEmbed.prioritize()
                pButton.dataEmbed.base.makeAdminBuy()
                pButton.toggleSelected()

    buttonBundle = [buttonsShut,buttonRectsShut,buttonsPri,buttonRectsPri]
    return buttonBundle

class AdminPanel:
    def __init__(self,titleText,science = False):
        self.science = science
        if self.science:
            self.backPanel = getHorizontalBar(150,150)
        else:
            self.backPanel = getHorizontalBar(250,150)
        self.locked = True
        self.overlay = pygame.Surface((self.backPanel.get_width(),self.backPanel.get_height()))
        self.overlay.fill(c.grey)
        self.overlay.set_alpha(130)
        self.overlayButton = Button("UNLOCK")
        self.tag = titleText
        self.titleTag = getTextSurface(titleText,size=24)
        self.buttonRect = None
        self.loc = None
        self.gap = 5
        self.tSize = 15
        self.allButtons = []
        self.allRects = []
        self.clicked = False

    def checkCost(self,screen,base):
        if self.science:
            cost = base.eventCost*base.scienceCostFactor
            pts = base.sciencePointsBalance
            tag = "SCIENCE"
        else:
            cost = base.eventCost*base.adminCostFactor
            pts =base.adminPointsBalance 
            tag = "ADMIN"
        paid = False
        if pts > cost:
            paid = True
        else:
            messagePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()),self.loc[1]+2*self.gap),\
                ["Not enough "+tag+" points.","{0:.2f} needed.".format(cost)])
        return paid

    def makeAdminBuy(self,base):
        base.makeAdminBuy()

    def makeScienceBuy(self,base):
        base.makeScienceBuy()

    def checkClick(self,click):
        clicked = False
        if self.locked:
            if self.buttonRect.collidepoint(click):
                self.overlayButton.toggleSelected()
        else:
            index = 0
            for rect in self.allRects:
                if rect.collidepoint(click):
                    #print("click detected")
                    self.allButtons[index].toggleSelected()
                    clicked = True
                index += 1
        self.clicked = True
        return clicked
            
    def draw(self,screen,anchorLoc,mouseLoc,base):
        self.loc = anchorLoc
        screen.blit(self.backPanel,anchorLoc)
        if self.locked:
            screen.blit(self.overlay,anchorLoc)
            self.buttonRect = self.overlayButton.draw(screen,(anchorLoc[0] + int(self.backPanel.get_width()/2 - \
                self.overlayButton.buttonSurface.get_width()/2),anchorLoc[1]+50),mouseLoc)
        else:
            self.drawUnlocked(screen,anchorLoc,mouseLoc)
            self.controlSelections(screen,base)
        screen.blit(self.titleTag,(anchorLoc[0],anchorLoc[1]-self.titleTag.get_height()))

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        pass

    def controlSelections(self,screen,base):
        pass 

#costList = [g,r,c,m,f,e,p]
class MaterialPanel(AdminPanel):
    def __init__(self,titleText,science):
        super().__init__(titleText,science)
        self.key = titleText
        self.tag = titleText + " R&D"
        self.description = ["Direct research to","individual resources","to reduce amount",\
            "consumed in base","construction and","in industrial use."]
        self.titleTag = getTextSurface(self.tag,size=20,aa=True)
        self.backPanel = getHorizontalBar(150,150*3+8*4)
        self.overlay = pygame.Surface((self.backPanel.get_width(),self.backPanel.get_height()))
        self.overlay.fill(c.grey)
        self.overlay.set_alpha(130)
        self.regolithButton = Button("REGOLITH")
        self.rareButton = Button("RARE")
        self.concreteButton = Button("CONCRETE")
        self.metalButton = Button("METAL")
        self.fuelButton = Button("FUEL")
        self.electronicsButton = Button("ELECTRONICS")
        self.plasticsButton = Button("PLASTICS")
        self.organicsButton = Button("ORGANICS")
        self.waterButton = Button("WATER")
        self.allButtons = [self.regolithButton,self.rareButton,self.concreteButton,self.metalButton,\
            self.fuelButton,self.electronicsButton,self.plasticsButton,self.organicsButton,self.waterButton]
        self.allRects = []

    def update(self,baseObj):
        self.regolithButton.dataEmbed = baseObj.regolith
        self.rareButton.dataEmbed = baseObj.rare
        self.concreteButton.dataEmbed = baseObj.concrete
        self.metalButton.dataEmbed = baseObj.metal
        self.fuelButton.dataEmbed = baseObj.fuel
        self.electronicsButton.dataEmbed = baseObj.electronics
        self.plasticsButton.dataEmbed = baseObj.plastics
        self.organicsButton.dataEmbed = baseObj.organics
        self.waterButton.dataEmbed = baseObj.water

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        self.allRects = []
        yLoc = 2*self.gap + anchorLoc[1]
        for line in self.description:
            screen.blit(getTextSurface(line,size=17),(anchorLoc[0]+2*self.gap,yLoc))
            yLoc += getTextHeight(17)
        yLoc+=self.gap
        for button in self.allButtons:
            rect = button.draw(screen,(anchorLoc[0]+3*self.gap,yLoc),mouseLoc)
            yLoc += button.buttonSurface.get_height()+2
            discTag = getTextSurface("CURRENT COST: {0:.0f}%".format(button.dataEmbed.discount*100),\
                color=button.dataEmbed.color,size=15)
            screen.blit(discTag,(anchorLoc[0]+2*self.gap,yLoc))
            yLoc+= discTag.get_height() + self.gap
            self.allRects.append(rect)
        
 
    def drawProgressBar(self,screen,loc):
        limit = 1.0
        ratio = (self.currentBonus-1.0)/limit
        height = self.backPanel.get_height()-4*self.gap
        progressHeight = int(ratio*height)
        pygame.draw.line(screen,c.black,loc,(loc[0],loc[1]-height),self.gap*8)
        pygame.draw.line(screen,self.color,(loc[0],loc[1]-1),(loc[0],loc[1]-progressHeight+1),self.gap*8-2)

    def controlSelections(self,screen,base):
        for button in self.allButtons:
            if button.selected:
                paid = self.checkCost(screen,base)
                if paid:
                    approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                        -2*self.gap,self.loc[1]+10*self.gap),["Do "+button.dataEmbed.tag+" research?"])
                    if approval:
                        base.costChange = True
                        self.makeScienceBuy(base)
                        button.dataEmbed.discount *= 0.95
                        self.update(base)
                button.toggleSelected()

class SciencePanel(AdminPanel):
    def __init__(self,titleText,science):
        super().__init__(titleText,science)
        self.key = titleText
        self.tag = titleText + " R&D"
        self.description = []
        self.titleTag = getTextSurface(self.tag,size=20,aa=True)
        self.researchButton = Button("RESEARCH")
        self.allButtons = [self.researchButton]
        self.allRects = []
        self.maxBonus = 2.0
        self.currentBonus = 1.0
        self.color = None

    def update(self,baseObj):
        self.description = baseObj.bonuses.descriptionFromKey(self.key)
        self.currentBonus = baseObj.bonuses.bonusFromKey(self.key)
        self.color =  baseObj.bonuses.colorFromKey(self.key)

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        self.allRects = []
        researchRect = self.researchButton.draw(screen,(anchorLoc[0]+2*self.gap,anchorLoc[1]+2*self.gap),mouseLoc)
        yLoc = anchorLoc[1]+3*self.gap + self.researchButton.buttonSurface.get_height()
        for line in self.description:
            screen.blit(getTextSurface(line,size=17),(anchorLoc[0]+2*self.gap,yLoc))
            yLoc += getTextHeight(17)
        self.drawProgressBar(screen,(anchorLoc[0]+self.backPanel.get_width()-6*self.gap,\
            self.backPanel.get_height()+anchorLoc[1]-2*self.gap))
        self.allRects = [researchRect]
 
    def drawProgressBar(self,screen,loc):
        limit = 1.0
        ratio = (self.currentBonus-1.0)/limit
        height = self.backPanel.get_height()-4*self.gap
        progressHeight = int(ratio*height)
        pygame.draw.line(screen,c.black,loc,(loc[0],loc[1]-height),self.gap*8)
        pygame.draw.line(screen,self.color,(loc[0],loc[1]-1),(loc[0],loc[1]-progressHeight+1),self.gap*8-2)

    def controlSelections(self,screen,base):
        if self.researchButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Do "+self.key+" research?"])
                if approval:
                    self.makeScienceBuy(base)
                    base.bonuses.setByKey(self.key,0.05)
                    self.update(base)
                    if self.currentBonus >= 2.0:
                        self.researchButton.makeDead()
            self.researchButton.toggleSelected()

class ManageBuilders(AdminPanel):
    def __init__(self,titleText):
        super().__init__(titleText)
        description = ["Determines how much","of your builders' work","goes toward maintanance",\
            "while new buildings are","under construction."]
        self.backPanel = blitFromTextList(self.backPanel,description,(int(self.backPanel.get_width()/2)-2*self.gap,\
            4*self.gap),textSize = self.tSize,left= True)
        self.finalizeButton = Button("FINALIZE")
        self.finalizeRect = None
        self.plusButton = Button("PLUS")
        self.plusRect = None
        self.minusButton = Button("MINUS")
        self.minusRect = None
        self.allButtons = [self.finalizeButton,self.plusButton,self.minusButton]
        self.allRects = [self.finalizeRect,self.plusRect,self.minusRect]
        self.possibleRatios = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        self.readoutIndex = 0
        self.glowTag = GlowTag("{0:.0f}%".format(self.possibleRatios[self.readoutIndex]*100)\
            ,c.highlightOrange,c.panelGrey,24)


    def getReadSurface(self):
        readout = pygame.Surface((self.plusButton.buttonSurface.get_width(),\
            self.plusButton.buttonSurface.get_height()))
        readout.fill(c.highlightOrange)
        readout.blit(self.glowTag.get(),(int(readout.get_width()/2 - self.glowTag.get_width()/2),\
            int(readout.get_height()/2 - self.glowTag.get_height()/2)))  
        return readout      

    def updateGlowTag(self):
        self.glowTag = GlowTag("{0:.0f}%".format(self.possibleRatios[self.readoutIndex]*100)\
            ,c.highlightOrange,c.panelGrey,24)

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        self.allRects = []
        buttonY = anchorLoc[1]+4*self.gap
        self.plusRect = self.plusButton.draw(screen,(anchorLoc[0]+2*self.gap,buttonY),mouseLoc)
        buttonY += self.plusButton.buttonSurface.get_height() + 2*self.gap
        screen.blit(self.getReadSurface(),(anchorLoc[0]+2*self.gap,buttonY))
        buttonY += self.plusButton.buttonSurface.get_height() + 2*self.gap
        self.minusRect = self.minusButton.draw(screen,(anchorLoc[0]+2*self.gap,buttonY),mouseLoc)

        self.finalizeRect = self.finalizeButton.draw(screen,(anchorLoc[0]+\
            int(self.backPanel.get_width()/2)-2*self.gap,buttonY),mouseLoc)
        self.allRects = [self.finalizeRect,self.plusRect,self.minusRect]

    def controlSelections(self,screen,base):
        if self.plusButton.selected:
            if self.readoutIndex < 9:
                self.readoutIndex += 1
                self.updateGlowTag()
            self.plusButton.toggleSelected()
        if self.minusButton.selected:
            if self.readoutIndex > 0:
                self.readoutIndex -= 1
                self.updateGlowTag()
            self.minusButton.toggleSelected()
        if self.finalizeButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Change maintenance ratio",\
                        "to {0:.0f}% ?".format(self.possibleRatios[self.readoutIndex]*100)])
                if approval:
                    self.makeAdminBuy(base)
                    base.maintainRatio = self.possibleRatios[self.readoutIndex]
            self.finalizeButton.toggleSelected()

class Economy(AdminPanel):
    def __init__(self,titleText):
        super().__init__(titleText)
        description = ["Determine if allocation","of resources is by NEED","or by PRODUCTIVITY. Also",\
            "adjust excess production of","ELECTRONICS & PLASTICS."]
        self.backPanel = blitFromTextList(self.backPanel,description,(int(self.backPanel.get_width()/2)-3*self.gap,\
            4*self.gap),textSize = self.tSize,left= True)
        self.marketButton = Button("MARKET")
        self.marketButton.mouseOverInfo = True
        self.marketButton.makeMouseOver(["Allocated by PRODUCTIVITY"])
        self.marketRect = None
        self.socButton = Button("SOCIALIST")
        self.socButton.mouseOverInfo = True
        self.socButton.makeMouseOver(["Allocated evenly by NEED"])
        self.socRect = None
        self.plusButton = Button("PLUS")
        self.plusRect = None
        self.minusButton = Button("MINUS")
        self.minusRect = None
        self.allButtons = [self.marketButton,self.socButton,self.plusButton,self.minusButton]
        self.allRects = [self.marketRect,self.socRect,self.plusRect,self.minusRect]
        self.possibleRatios = [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75]
        self.readoutIndex = 0
        self.glowTag = GlowTag("{0:.0f}%".format(self.possibleRatios[self.readoutIndex]*100)\
            ,c.highlightOrange,c.panelGrey,24)


    def getReadSurface(self):
        readout = pygame.Surface((self.plusButton.buttonSurface.get_width(),\
            self.plusButton.buttonSurface.get_height()))
        readout.fill(c.highlightOrange)
        readout.blit(self.glowTag.get(),(int(readout.get_width()/2 - self.glowTag.get_width()/2),\
            int(readout.get_height()/2 - self.glowTag.get_height()/2)))  
        return readout      

    def updateGlowTag(self):
        self.glowTag = GlowTag("{0:.0f}%".format(self.possibleRatios[self.readoutIndex]*100)\
            ,c.highlightOrange,c.panelGrey,24)

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        self.allRects = []
        buttonY = anchorLoc[1]+4*self.gap
        self.plusRect = self.plusButton.draw(screen,(anchorLoc[0]+2*self.gap,buttonY),mouseLoc)
        buttonY += self.plusButton.buttonSurface.get_height() + 2*self.gap
        screen.blit(self.getReadSurface(),(anchorLoc[0]+2*self.gap,buttonY))
        buttonY += self.plusButton.buttonSurface.get_height() + 2*self.gap
        self.minusRect = self.minusButton.draw(screen,(anchorLoc[0]+2*self.gap,buttonY),mouseLoc)

        buttonY += 2*self.gap
        self.socRect = self.socButton.draw(screen,(anchorLoc[0]+\
            int(self.backPanel.get_width()/2)-3*self.gap,buttonY),mouseLoc)
        buttonY -= self.plusButton.buttonSurface.get_height() + self.gap   
        self.marketRect = self.marketButton.draw(screen,(anchorLoc[0]+\
            int(self.backPanel.get_width()/2)-3*self.gap,buttonY),mouseLoc)
        self.allRects = [self.marketRect,self.socRect,self.plusRect,self.minusRect]

    def controlSelections(self,screen,base):
        
        if self.plusButton.selected:
            if self.readoutIndex < 9:
                self.readoutIndex += 1 ##
                self.updateGlowTag()
            self.plusButton.toggleSelected()
        if self.minusButton.selected:
            if self.readoutIndex > 0:
                self.readoutIndex -= 1 ##
                self.updateGlowTag()
            self.minusButton.toggleSelected()
        if self.socButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Evenly distribute",\
                        "{0:.0f}%".format(self.possibleRatios[self.readoutIndex]*100)+\
                            " of ELECTRONICS","and PLASTICS production."])
                if approval:
                    self.makeAdminBuy(base)
                    base.consumerRatio = self.possibleRatios[self.readoutIndex]
                    base.market = False
            self.socButton.toggleSelected()
        if self.marketButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Allow open sale of",\
                        "{0:.0f}%".format(self.possibleRatios[self.readoutIndex]*100)+\
                            " of ELECTRONICS","and PLASTICS production."])
                if approval:
                    self.makeAdminBuy(base)
                    base.consumerRatio = self.possibleRatios[self.readoutIndex]
                    base.market = True
            self.marketButton.toggleSelected()

class PrioritizeIndustries(AdminPanel):
    def __init__(self,titleText):
        super().__init__(titleText)
        self.constructionButton = Button("CONSTRUCTION")
        description = ["Choose which industries","receive highest priority", "in hiring."]
        self.backPanel = blitFromTextList(self.backPanel,description,(6*self.gap + \
            self.constructionButton.buttonSurface.get_width(),self.gap),\
            textSize = self.tSize,left= True)
        self.priorityList = []
        self.constructionRect = None
        self.priorityList.append([self.constructionButton,1.0,"CONSTRUCTION"])
        self.explorationButton = Button("EXPLORATION")
        self.explorationRect = None
        self.priorityList.append([self.explorationButton,1.0,"EXPLORATION"])
        self.powerButton = Button("POWER")
        self.powerRect = None
        self.priorityList.append([self.powerButton,1.0,"POWER"])
        self.lifeSupportButton = Button("LIFE SUPPORT")
        self.lifeSupportRect = None
        self.priorityList.append([self.lifeSupportButton,1.0,"LIFE SUPPORT"])
        self.recycleButton = Button("RECYCLE")
        self.recycleRect = None
        self.priorityList.append([self.recycleButton,1.0,"RECYCLE"])
        self.extractionButton = Button("EXTRACTION")
        self.extractionRect = None
        self.priorityList.append([self.extractionButton,1.0,"EXTRACTION"])
        self.industryButton = Button("INDUSTRY")
        self.industryRect = None
        self.priorityList.append([self.industryButton,1.0,"INDUSTRY"])
        self.scienceButton = Button("SCIENCE")
        self.scienceRect = None
        self.priorityList.append([self.scienceButton,1.0,"SCIENCE"])
        self.adminButton = Button("ADMINISTRATION")
        self.adminRect = None
        self.priorityList.append([self.adminButton,1.0,"ADMINISTRATION"])
        self.transportButton = Button("TRANSPORTATION")
        self.transportRect = None
        self.priorityList.append([self.transportButton,1.0,"TRANSPORTATION"])
        self.allButtons = [self.constructionButton,self.explorationButton,self.powerButton,\
            self.lifeSupportButton,self.recycleButton,self.extractionButton,self.industryButton,\
            self.scienceButton,self.adminButton,self.transportButton]
        self.allRects = []
        self.multiplier = 1.1 
        
    def reconfigureButtons(self):
        newPriority = []
        while len(self.priorityList) > 0:
            maxWt = self.priorityList[0][1]
            maxElement = self.priorityList[0]
            for element in self.priorityList:
                if element[1] > maxWt:
                    maxWt = element[1]
                    maxElement = element
            newPriority.append(maxElement)
            self.priorityList.remove(maxElement)
        self.priorityList = newPriority

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        self.allRects = []
        self.allButtons = []
        textHt = getTextHeight(15)
        buttonHt = self.powerButton.buttonSurface.get_height()
        xLoc = anchorLoc[0]+4*self.gap
        yLoc = anchorLoc[1]+self.backPanel.get_height()-self.gap-4*textHt-4*buttonHt
        yTop = yLoc + textHt + buttonHt
        count = 0
        for buttonBundle in self.priorityList:
            rect = buttonBundle[0].draw(screen,(xLoc,yLoc),mouseLoc)
            self.allRects.append(rect)
            self.allButtons.append(buttonBundle[0])
            yLoc += buttonHt
            screen.blit(getTextSurface("weight: {0:.2f}".format(buttonBundle[1]),\
                c.highlightOrange,15),(xLoc,yLoc))
            yLoc += textHt
            count+= 1
            if count == 4 or count == 7:
                yLoc = yTop
                xLoc += 2*self.gap + self.powerButton.buttonSurface.get_width()

    def findAndUpdate(self,thisButton):
        for buttonBundle in self.priorityList:
            if thisButton == buttonBundle[0]:
                buttonBundle[1] *= self.multiplier

    def controlSelections(self,screen,base):
        if self.powerButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize power?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.powerList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.powerButton)
                    self.multiplier *= 1.05
            self.powerButton.toggleSelected()
            self.reconfigureButtons()
        if self.lifeSupportButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize life support?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.lifeSupportList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.lifeSupportButton)
                    self.multiplier *= 1.05
            self.lifeSupportButton.toggleSelected()
            self.reconfigureButtons()
        if self.recycleButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize recycle?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.recycleList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.recycleButton)
                    self.multiplier *= 1.05
            self.recycleButton.toggleSelected()
            self.reconfigureButtons()
        if self.extractionButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize extraction?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.extractionList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.extractionButton)
                    self.multiplier *= 1.05
            self.extractionButton.toggleSelected()
            self.reconfigureButtons()
        if self.industryButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize industry?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.industryList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.industryButton)
                    self.multiplier *= 1.05
            self.industryButton.toggleSelected()
            self.reconfigureButtons()
        if self.scienceButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize science?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.labList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.scienceButton)
                    self.multiplier *= 1.05
            self.scienceButton.toggleSelected()
            self.reconfigureButtons()
        if self.adminButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize administration?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.adminList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.adminButton)
                    self.multiplier *= 1.05
            self.adminButton.toggleSelected()
            self.reconfigureButtons()
        if self.transportButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize transportation?"])
                if approval:
                    self.makeAdminBuy(base)
                    for building in base.transportList:
                        building.weight *= self.multiplier
                    self.findAndUpdate(self.transportButton)
                    self.multiplier *= 1.05
            self.transportButton.toggleSelected()
            self.reconfigureButtons()
        if self.constructionButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize construction?"])
                if approval:
                    self.makeAdminBuy(base)
                    for job in base.builders:
                        job.jobWeight *= self.multiplier
                    self.findAndUpdate(self.constructionButton)
                    self.multiplier *= 1.05
            self.constructionButton.toggleSelected()
            self.reconfigureButtons()
        if self.explorationButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Prioritize exploration?"])
                if approval:
                    self.makeAdminBuy(base)
                    for job in base.explorers:
                        job.jobWeight *= self.multiplier
                    self.findAndUpdate(self.explorationButton)
                    self.multiplier *= 1.05
            self.explorationButton.toggleSelected()
            self.reconfigureButtons()

class OptimizeJobs(AdminPanel):
    def __init__(self,titleText):
        super().__init__(titleText)
        description = ["Reassigns all jobs base","wide according to your","current industry and building",\
            "priorities, with the highest","priority jobs receiving the","most productive workers."]
        self.backPanel = blitFromTextList(self.backPanel,description,(self.gap,5*self.gap),\
            textSize = self.tSize,left= False)
        self.optimizeButton = Button("OPTIMIZE")
        self.optimizeRect = None
        self.allButtons = [self.optimizeButton]
        self.allRects = [self.optimizeRect]   

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        self.allRects = []
        self.optimizeRect = self.optimizeButton.draw(screen,(anchorLoc[0]+\
            int(self.backPanel.get_width()/2 - self.optimizeButton.buttonSurface.get_width()/2),\
            anchorLoc[1]+6*self.gap+int(self.backPanel.get_height()/2 - \
            self.optimizeButton.buttonSurface.get_height()/2)),mouseLoc)
        self.allRects = [self.optimizeRect] 

    def controlSelections(self,screen,base):
        if self.optimizeButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Optimize all jobs?"])
                if approval:
                    self.makeAdminBuy(base)
                    base.optimizeJobs()
            self.optimizeButton.toggleSelected()

class Holiday(AdminPanel):
    def __init__(self,titleText):
        super().__init__(titleText)
        description = ["Create a new 7 sol","holiday for your base to","celebrate, intensive PSYCH bonus",\
            "but work is generated at","quarter the rate as usual.","Starts next sol."]
        self.backPanel = blitFromTextList(self.backPanel,description,(self.gap,5*self.gap),\
            textSize = self.tSize,left= False)
        self.declareButton = Button("MAKE HOLIDAY")
        self.declareRect = None
        self.allButtons = [self.declareButton]
        self.allRects = [self.declareRect]   

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        self.allRects = []
        self.declareRect = self.declareButton.draw(screen,(anchorLoc[0]+\
            int(self.backPanel.get_width()/2 - self.declareButton.buttonSurface.get_width()/2),\
            anchorLoc[1]+6*self.gap+int(self.backPanel.get_height()/2 - \
            self.declareButton.buttonSurface.get_height()/2)),mouseLoc)
        self.allRects = [self.declareRect] 

    def controlSelections(self,screen,base):
        if self.declareButton.selected:
            paid = self.checkCost(screen,base)
            if paid:
                approval = choicePopUp(screen,(self.loc[0]+int(self.backPanel.get_width()/2)\
                    -2*self.gap,self.loc[1]+10*self.gap),["Declare sol:{0:.0f} the".format(base.solCycle+1),\
                        "start of a 5 sol holiday?"])
                if approval:
                    self.makeAdminBuy(base)
                    base.holidays.append(base.solCycle+1)
                    base.nameHoliday()
            self.declareButton.toggleSelected()

class Security(AdminPanel):
    def __init__(self,titleText):
        super().__init__(titleText)
        description = ["Unlocks ability to hire","your Astronauts to work as","SECURITY. Can force low-psych",\
            "astronauts to work. Hire","SECURITY on the MANAGE-JOBS","screen as needed."]
        self.backPanel = blitFromTextList(self.backPanel,description,(self.gap,5*self.gap),\
            textSize = self.tSize,left= False)

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        pass

    def controlSelections(self,screen,base):
        pass

class Arts(AdminPanel):
    def __init__(self,titleText):
        super().__init__(titleText)
        description = ["Unlocks ability to allow","your Astronauts to work as","ARTISTS. Increases base wide",\
            "PSYCH environment. Hire new","ARTISTS on the MANAGE-JOBS","screen as needed."]
        self.backPanel = blitFromTextList(self.backPanel,description,(self.gap,5*self.gap),\
            textSize = self.tSize,left= False)

    def drawUnlocked(self,screen,anchorLoc,mouseLoc):
        pass

    def controlSelections(self,screen,base):
        pass

def messagePopUp(screen,loc,textList,costObject = None):
    gap = 5
    textMaxWidth = 0
    for line in textList:
        w = getTextWidth(line,20)
        if w > textMaxWidth:
            textMaxWidth = w
    width = gap*3
    if (gap*2 + textMaxWidth) > width:
        width = gap*2 + textMaxWidth

    msg = getTextSurface("CLICK TO DISMISS",size=12)
    
    height = gap*2 + (len(textList)*getTextHeight(20)) + msg.get_height()+2
    if costObject != None:
        costHeight = len(costObject.tags)*getTextHeight(17)
        height += costHeight + gap
    popUp = getOutlinePanel(height,width)
    popUp = blitFromTextList(popUp,textList,(gap,gap))
    popUp.blit(msg,(int(popUp.get_width()/2-msg.get_width()/2),popUp.get_height()-2-msg.get_height()))
    if costObject != None:
        costObject.drawDeficit(popUp,(int(popUp.get_width()/2)-gap,popUp.get_height()\
            -2*gap-costHeight-msg.get_height()+2))
    back = getPauseScreen(screen)

    drawX = loc[0] + gap
    if loc[0] > screen.get_width()/2:
        drawX = loc[0]-int(popUp.get_width())

    drawY = gap*2
    if loc[1] > screen.get_height()/2:
        drawY = -1*(popUp.get_height()+gap)
    
    loc = (drawX,loc[1] + drawY)

    menuOn = True
    while menuOn:
        screen.blit(back,(0,0))
        msgRect = screen.blit(popUp,loc)

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if msgRect.collidepoint(click):
                    menuOn = False


        pygame.display.flip()


def choicePopUp(screen,loc,textList,costObject=None,yesText = "YES",noText = "NO"):
    gap = 5
    textMaxWidth = 0
    for line in textList:
        w = getTextWidth(line,20)
        if w > textMaxWidth:
            textMaxWidth = w

    yesButton = Button(yesText)
    noButton = Button(noText)
    width = gap*3 + yesButton.buttonSurface.get_width()*2
    if (gap*2 + textMaxWidth) > width:
        width = gap*2 + textMaxWidth

    height = gap*3 + (len(textList)*getTextHeight(20)) + yesButton.buttonSurface.get_height()
    bHeight = gap*2 + (len(textList)*getTextHeight(20))
    if costObject != None:
        costObject.makeDrawable()
        costHeight = len(costObject.tags)*getTextHeight(17)
        height += costHeight
        bHeight += costHeight
    popUp = getOutlinePanel(height,width)
    popUp = blitFromTextList(popUp,textList,(gap,gap))
    if costObject != None:
        costObject.draw(popUp,(int(popUp.get_width()/2)-gap,gap + (len(textList)*getTextHeight(20))))
    back = getPauseScreen(screen)

    drawX = loc[0] + gap
    if loc[0] > screen.get_width()/2:
        drawX = loc[0]-int(popUp.get_width())

    drawY = gap*2
    if loc[1] > screen.get_height()/2:
        drawY = -1*(popUp.get_height()+gap)
    
    loc = (drawX,loc[1] + drawY)
    
    newGap = int((width - (yesButton.buttonSurface.get_width()*2+gap))/2)

    confirmation = False
    menuOn = True
    while menuOn:
        screen.blit(back,(0,0))
        screen.blit(popUp,loc)

        mouseLoc = pygame.mouse.get_pos()

        yesRect = yesButton.draw(screen,(loc[0]+newGap,loc[1]+bHeight),mouseLoc)
        noRect = noButton.draw(screen,(loc[0]+newGap+gap+yesButton.buttonSurface.get_width(),loc[1]+bHeight),mouseLoc)
        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if yesRect.collidepoint(click):
                    confirmation = True
                    menuOn = False
                if noRect.collidepoint(click):
                    confirmation = False
                    menuOn = False

        pygame.display.flip()

    return confirmation

class Point:
    def __init__(self,xLoc,yLoc,surface = None,obj = None,line = False):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.xTrack = float(xLoc)
        self.yTrack = float(yLoc)
        self.xVelocity = 0
        self.yVelocity = 0
        self.surface = surface
        self.line = line
        self.nextX = xLoc
        self.nextY = yLoc
        self.object = obj
        self.infoObject = None
        self.mouseOver = False

    def createInfoObject(self):
        self.infoObject = InfoObject(self.object)
    
    def noMouseOver(self):
        self.mouseOver = False
        self.infoObject = None

class Graveyard:
    def __init__(self,screen,graveyard,line = False):
        self.canvas = screen
        self.gap = 30
        self.graveyard = graveyard
        self.rects = []
        panel = pygame.Surface((screen.get_width()-2*self.gap,screen.get_height()-3*self.gap))
        panel.fill(c.darken(c.grey,70))
        panel.set_alpha(200)
        self.backPanel = panel
        self.titleTag = getTextSurface("GRAVEYARD",size=24)
        if len(graveyard) > 0:
            totalAge = 0
            totalTimeOnMars = 0
            for person in graveyard:
                totalAge += person.age
                totalTimeOnMars += (person.diedSol - person.arrivedSol)
            avgAge = (totalAge/len(graveyard))/350.0
            avgTime = totalTimeOnMars/len(graveyard)
            self.ageTag = getTextSurface("LIFE EXPECTANCY: {0:.2f} EY".format(avgAge))
            self.timeTag = getTextSurface("AVERAGE TIME ON MARS: {0:.1f} SOL".format(avgTime))
        else:
            self.ageTag = getTextSurface("NO DEATHS SO FAR.")
            self.timeTag = getTextSurface("")

    def draw(self,mouseLoc):
        self.rects = []
        self.canvas.blit(self.backPanel,(self.gap,self.gap))
        self.canvas.blit(self.titleTag,(2*self.gap,2*self.gap))
        self.canvas.blit(self.ageTag,(2*self.gap,2*self.gap+self.titleTag.get_height()))
        self.canvas.blit(self.timeTag,(2*self.gap,2*self.gap+self.titleTag.get_height()+self.ageTag.get_height()))

        xLoc = 2*self.gap
        yLoc = 4* self.gap
        for person in self.graveyard:
            graveRect = self.canvas.blit(a.grave,(xLoc,yLoc))
            self.rects.append(graveRect)
            xLoc += a.grave.get_width()+(self.gap/2)
            if xLoc > self.canvas.get_width()-2*self.gap:
                xLoc = 2*self.gap
                yLoc += a.grave.get_height()+(self.gap/2)

        index = 0
        for each in self.rects:
            if each.collidepoint(mouseLoc):
                nameTag = getTextSurface(self.graveyard[index].name,c.darken(c.grey,70))
                yearsTag = getTextSurface(str(int(self.graveyard[index].diedYear-(self.graveyard[index].age/350.0)))+"-"+str(self.graveyard[index].diedYear),c.darken(c.grey,70))
                diedTag = getTextSurface(self.graveyard[index].diedString,c.darken(c.grey,70))
                moPanel = pygame.Surface((diedTag.get_width()+10,3*diedTag.get_height()+10))
                moPanel.fill(c.grey)
                moPanel.blit(nameTag,(int(moPanel.get_width()/2)-int(nameTag.get_width()/2),5))
                moPanel.blit(yearsTag,(int(moPanel.get_width()/2)-int(yearsTag.get_width()/2),5+nameTag.get_height()))
                moPanel.blit(diedTag,(int(moPanel.get_width()/2)-int(diedTag.get_width()/2),5+2*nameTag.get_height()))
                self.canvas.blit(moPanel,mouseLoc)
            index+=1
            



class Chart:
    def __init__(self,screen,workingObjects=[],line = False):
        self.transitionFrames = 30
        self.transitionCount = 0
        self.transition = False
        self.canvas = screen
        self.line = line
        self.gap = 30
        self.xMin = 0
        self.xMinScreen = self.gap*2
        self.xMinReadout = 0
        self.xMinReadoutVelocity = 0
        self.xMax = 0
        self.xMaxScreen = screen.get_width() - self.gap*2
        self.xMaxReadout = 0
        self.xMaxReadoutVelocity = 0
        self.xTag = ""

        #remember to flip y values!!
        self.yMin = 0
        self.yMinScreen = screen.get_height()-3*self.gap
        self.yMinReadout = 0
        self.yMinReadoutVelocity = 0
        self.yMax = 0
        self.yMaxScreen = self.gap*2
        self.yMaxReadout = 0
        self.yMaxReadoutVelocity = 0
        self.yTag = ""

        self.dataListList = [] # list of lists!
        self.dataListColors = []
        self.dataListRemoveTags = []
        self.points = []
        self.rects = [] #parallel to points
        self.animations = []
        panel = pygame.Surface((screen.get_width()-2*self.gap,screen.get_height()-3*self.gap))
        panel.fill(c.darken(c.grey,70))
        panel.set_alpha(200)
        pygame.draw.line(panel,c.grey,(self.gap,panel.get_height()-self.gap),\
            (panel.get_width()-self.gap,panel.get_height()-self.gap),2)
        pygame.draw.line(panel,c.grey,(self.gap,panel.get_height()-self.gap),\
            (self.gap,self.gap),2)
        self.backPanel = panel
    
    def valueFromKey(self,obj,key):
        if key == "Age":
            value = obj.age / 350.0
        if key == "Health":
            value = obj.health
        if key == "Skill":
            value = obj.skill
        if key == "Psych":
            value = obj.psych
        if key == "Prod":
            if obj.job != None:
                value = obj.job.productivity
            else:
                value = 0.0
        return value
        
    def setY(self,key):
        self.yTag = key
        self.transition = True
        if len(self.points) > 0:
            value = self.valueFromKey(self.points[0].object,key)
        if len(self.dataListList)>0:
            value = self.dataListList[0][0].object[1]
        yMax = value
        yMin = value
        if len(self.dataListList)>0:
            for eachList in self.dataListList:
                for pt in eachList:
                    value = pt.object[1]
                    if value > yMax:
                        yMax = value
                    if value < yMin:
                        yMin = value
        if len(self.points) > 0:
            for pt in self.points:
                value = self.valueFromKey(pt.object,key)
                if value > yMax:
                    yMax = value
                if value < yMin:
                    yMin = value
        self.yMin = yMin
        self.yMax = yMax
        self.yMinReadoutVelocity = (self.yMin - self.yMinReadout) / self.transitionFrames 
        self.yMaxReadoutVelocity = (self.yMax - self.yMaxReadout) / self.transitionFrames
        self.xMinReadoutVelocity = 0.0
        self.xMaxReadoutVelocity = 0.0 
        drawWidth = self.yMinScreen - self.yMaxScreen
        dataRange = self.yMax - self.yMin
        if len(self.points) > 0:
            for pt in self.points:
                value = self.valueFromKey(pt.object,key)
                if dataRange > 0:
                    ratio = (self.yMax - value) / dataRange
                else:
                    ratio = 0.0
                pt.nextY = self.yMaxScreen + int(drawWidth*ratio)
                pt.yVelocity = (pt.nextY - pt.yLoc) / 30.0
                pt.xVelocity = 0.0
        if len(self.dataListList) > 0:
            for eachList in self.dataListList:
                for pt in eachList:
                    value = pt.object[1]
                    if dataRange != 0:
                        ratio = (self.yMax - value) / dataRange
                    else: 
                        ratio = 0
                    pt.nextY = self.yMaxScreen + int(drawWidth*ratio)
                    pt.yVelocity = (pt.nextY - pt.yLoc) / 30.0


    def setX(self,key):
        self.xTag = key
        self.transition = True
        if len(self.points) > 0:
            value = self.valueFromKey(self.points[0].object,key)
        if len(self.dataListList)>0:
            value = self.dataListList[0][0].object[0]
        xMax = value
        xMin = value
        if len(self.dataListList)>0:
            for eachList in self.dataListList:
                for pt in eachList:
                    value = pt.object[0]
                    if value > xMax:
                        xMax = value
                    if value < xMin:
                        xMin = value
        if len(self.points) > 0:
            for pt in self.points:
                value = self.valueFromKey(pt.object,key)
                if value > xMax:
                    xMax = value
                if value < xMin:
                    xMin = value
        self.xMin = xMin
        self.xMax = xMax
        self.xMinReadoutVelocity = (self.xMin - self.xMinReadout) / self.transitionFrames 
        self.xMaxReadoutVelocity = (self.xMax - self.xMaxReadout) / self.transitionFrames
        if len(self.points) > 0:
            self.yMinReadoutVelocity = 0.0
            self.yMaxReadoutVelocity = 0.0 
        drawWidth = self.xMaxScreen - self.xMinScreen
        dataRange = self.xMax - self.xMin
        if len(self.points) > 0:
            for pt in self.points:
                value = self.valueFromKey(pt.object,key)
                if dataRange > 0:
                    ratio = (value - self.xMin) / dataRange
                else:
                    ratio = 0.0
                pt.nextX = self.xMinScreen + int(drawWidth*ratio)
                pt.xVelocity = (pt.nextX - pt.xLoc) / 30.0
                pt.yVelocity = 0.0
        if len(self.dataListList) > 0:
            for eachList in self.dataListList:
                for pt in eachList:
                    value = pt.object[0]
                    if dataRange != 0:
                        ratio = (value - self.xMin) / dataRange
                    else: 
                        ratio = 0
                    pt.nextX = self.xMinScreen + int(drawWidth*ratio)
                    pt.xVelocity = (pt.nextX - pt.xLoc) / 30.0

            
    def runTransition(self):
        self.transitionCount += 1
        if self.transitionCount == self.transitionFrames:
            self.transition = False
            self.transitionCount = 0
        # fix, runs both always
        self.xMinReadout += self.xMinReadoutVelocity
        self.xMaxReadout += self.xMaxReadoutVelocity
        self.yMinReadout += self.yMinReadoutVelocity
        self.yMaxReadout += self.yMaxReadoutVelocity
        if len(self.points) > 0:
            for pt in self.points:
                pt.xTrack += pt.xVelocity
                pt.xLoc = int(pt.xTrack)
                if self.transition == False:
                    pt.xLoc = pt.nextX
                    pt.xTrack = float(pt.nextX)
                pt.yTrack += pt.yVelocity
                pt.yLoc = int(pt.yTrack)
                if self.transition == False:
                    pt.yLoc = pt.nextY
                    pt.yTrack = float(pt.nextY)
        if len(self.dataListList) > 0:
            for eachList in self.dataListList:
                for pt in eachList:
                    pt.xTrack += pt.xVelocity
                    pt.xLoc = int(pt.xTrack)
                    if self.transition == False:
                        pt.xLoc = pt.nextX
                        pt.xTrack = float(pt.nextX)
                    pt.yTrack += pt.yVelocity
                    pt.yLoc = int(pt.yTrack)
                    if self.transition == False:
                        pt.yLoc = pt.nextY
                        pt.yTrack = float(pt.nextY)

    def peopleToPoints(self,popList):
        for x in popList:
            #ADD different surfaces here
            if x.age < p.People.workingAge:
                newPoint = Point(self.xMinScreen,self.yMinScreen,a.nautKid,x)
            else:
                if x.sane:
                    newPoint = Point(self.xMinScreen,self.yMinScreen,a.naut,x)
                else:
                    newPoint = Point(self.xMinScreen,self.yMinScreen,a.nautBad,x)
            self.points.append(newPoint)

    def productionListToPoints(self,fullProdList,color):
        circ = pygame.Surface((10,10))
        circ.fill(c.trans)
        circ.set_colorkey(c.trans)
        pygame.draw.circle(circ,color,(5,5),5)
        newDataList = []
        week = 0
        self.dataListRemoveTags.append(fullProdList[0])
        if len(fullProdList) >= 50:
            prodList = fullProdList[-50:]
        else:
            prodList = fullProdList[1:]
        for pt in prodList:
            newPoint = Point(self.xMinScreen,self.yMinScreen,circ,(week,pt),line=True)
            newDataList.append(newPoint)
            week+=1
        self.dataListList.append(newDataList)
        self.dataListColors.append(color)

    def findAndRemove(self,tag):
        i = 0
        for eachTag in self.dataListRemoveTags:
            if eachTag == tag:
                self.dataListRemoveTags.remove(eachTag)
                self.dataListList.remove(self.dataListList[i])
                self.dataListColors.remove(self.dataListColors[i])
                break
            i += 1
            
    def runAnimations(self,screen):
        for an in self.animations:
            an.runAnimation()
            an.draw(screen)
            if an.on == False:
                self.animations.remove(an)

    def draw(self,mouseLoc):
        if self.transition:
            self.runTransition()
        self.canvas.blit(self.backPanel,(self.gap,self.gap))
        yTag = getTextSurface(self.yTag,c.grey,17)
        yTag = pygame.transform.rotate(yTag,90)
        self.canvas.blit(yTag,(2*self.gap-yTag.get_width(),\
            int(self.gap+self.backPanel.get_height()/2-yTag.get_height()/2)))
        yMaxTag = getTextSurface("{0:.2f}".format(self.yMaxReadout),c.grey,15)
        self.canvas.blit(yMaxTag,(2*self.gap-yMaxTag.get_width(),2*self.gap))
        yMinTag = getTextSurface("{0:.2f}".format(self.yMinReadout),c.grey,15)
        self.canvas.blit(yMinTag,(2*self.gap-yMinTag.get_width(),\
            self.backPanel.get_height()-yMinTag.get_height()))
        xMaxTag = getTextSurface("{0:.3f}".format(self.xMaxReadout),c.grey,17)
        self.canvas.blit(xMaxTag,(self.backPanel.get_width()-xMaxTag.get_width(),\
            self.backPanel.get_height()+3))
        xMinTag = getTextSurface("{0:.3f}".format(self.xMinReadout),c.grey,17)
        self.canvas.blit(xMinTag,(self.gap*2,self.backPanel.get_height()+3))
        xTag = getTextSurface(self.xTag,c.grey,17)
        self.canvas.blit(xTag,(int(self.canvas.get_width()/2-xTag.get_width()/2),\
            self.backPanel.get_height()+3))
        if self.line == False:
            if len(self.points) > 0:
                self.rects = []
                for pt in self.points:
                    rect = self.canvas.blit(pt.surface,(pt.xLoc-int(pt.surface.get_width()/2),\
                        pt.yLoc - int(pt.surface.get_height()/2)))
                    self.rects.append(rect)
            i = 0
            self.runAnimations(self.canvas)
            for rect in self.rects:
                if rect.collidepoint(mouseLoc): 
                    if self.points[i].mouseOver == False:
                        self.points[i].mouseOver = True
                        self.points[i].createInfoObject()
                    else:
                        self.points[i].infoObject.draw(self.canvas,mouseLoc)
                else:
                    if self.points[i].infoObject != None:
                        fade = self.points[i].infoObject.draw(self.canvas,mouseLoc,True)
                        self.animations.append(fade)
                        self.points[i].noMouseOver()
                i+=1
        else:
            if len(self.dataListList) > 0:
                listIndex = 0
                for eachList in self.dataListList:
                    if listIndex == 0:
                        pass
                    else:
                        lastLoc = None
                        listColor = self.dataListColors[listIndex]
                        for pt in eachList:
                            ptLoc = (pt.xLoc,pt.yLoc)
                            self.canvas.blit(pt.surface,(ptLoc[0]-int(pt.surface.get_width()/2),\
                                ptLoc[1] - int(pt.surface.get_height()/2)))
                            if lastLoc != None:
                                pygame.draw.line(self.canvas,listColor,lastLoc,ptLoc,2)
                            lastLoc = ptLoc
                    listIndex+=1




def drawProductionChart(canvas,anchorLoc,resourceList,numPoints):
    color = c.darken(c.grey,50)
    width = canvas.get_width() - (2 * anchorLoc[0])
    height = canvas.get_height() - (anchorLoc[1]) - 50
    leftX = anchorLoc[0]
    topY = anchorLoc[1]
    bottomY = anchorLoc[1] + height
    #draw base line
    pygame.draw.line(canvas,color,(leftX-2,bottomY),(leftX+width,bottomY),4)
    pygame.draw.line(canvas,color,(leftX,bottomY),(leftX,topY),4)

    maxProd = 0
    for resource in resourceList:
        print(resource.weeklyProductionReports)
        for report in resource.weeklyProductionReports:
            if report > maxProd:
                maxProd = report
    print(maxProd)
    
    if maxProd == 0:
        noneTag = getTextSurface("NO DATA",c.boldRed,40)
        canvas.blit(noneTag,(leftX+5,bottomY-5-noneTag.get_height()))
    else:
        ratio = (0.7*height)/maxProd
        print(ratio)
        for resource in resourceList:
            xIncrement = int(width / numPoints)
            if len(resource.weeklyProductionReports) > numPoints:
                len(resource.weeklyProductionReports)
                originPoint = (leftX,bottomY - int(resource.weeklyProductionReports[len(resource.weeklyProductionReports) - numPoints]*ratio))
                index = len(resource.weeklyProductionReports) - (numPoints - 1)
                while index < len(resource.weeklyProductionReports):
                    newPoint = (originPoint[0] + xIncrement,bottomY - int(resource.weeklyProductionReports[index]*ratio))
                    pygame.draw.line(canvas,resource.color,originPoint,newPoint,2)
                    originPoint = newPoint
                    index+=1
            else:
                originPoint = (leftX,bottomY)
                for point in resource.weeklyProductionReports:
                    newPoint = (originPoint[0] + xIncrement,bottomY - int(point*ratio))
                    pygame.draw.line(canvas,resource.color,originPoint,newPoint,2)
                    originPoint = newPoint


#spaceManagePanel
class SpaceManager:
    def __init__(self,screen,base,space):
        self.base = base
        self.space = space
        self.screen = screen
        self.rocketCost = o.Cost(self.base,o.rCost)
        self.savedEarthLaunches = self.base.availableEarthLaunches
        self.launchTag = GlowTag("AVAILABLE LAUCHES: "+str(self.base.availableEarthLaunches))
        self.savedLaunchCost = self.base.launchCost*self.base.earthCostFactor
        self.costTag = GlowTag("LAUNCH COST: {0:.2f}".format(self.base.launchCost*self.base.earthCostFactor),size=17)
        self.savedScienceNum = self.base.sciencePointsBalance
        self.scienceNum = GlowTag("{0:.1f}".format(self.base.sciencePointsBalance),c.white,c.purple,17)
        self.savedAdminNum = self.base.adminPointsBalance
        self.adminNum = GlowTag("{0:.1f}".format(self.base.adminPointsBalance),c.white,c.pink,17)
        self.savedExportNum = self.base.exportPoints
        self.exportNum = GlowTag("{0:.1f}".format(self.base.exportPoints),c.white,c.darken(c.grey,-40),17)
        self.rocketTag = GlowTag("AVAILABLE ROCKETS: "+str(self.base.availableOutbound))
        self.savedRocketsCount = self.base.availableOutbound
        queuedNumber = 0
        for pad in self.base.launchPads:
            queuedNumber += len(pad.queue)
        self.savedQueuedNumber = queuedNumber
        self.queuedTag = GlowTag("QUEUED ROCKETS: "+str(self.savedQueuedNumber))
        self.launchButton = Button("GET LAUNCH")
        self.launchRect = None
        self.rocketButton = Button("GET ROCKET") 
        self.rocketRect = None
        if self.rocketCost.check() == False:
            self.rocketButton.makeDead()

        self.panel = self.getPanel()

    def checkClick(self,click):
        if self.rocketRect.collidepoint(click):
            self.rocketButton.toggleSelected()
        if self.launchRect.collidepoint(click):
            self.launchButton.toggleSelected()

    def action(self,click):
        if self.rocketButton.selected:
            self.rocketButton.toggleSelected()
            approve = choicePopUp(self.screen,click,["Ready a rocket for","export payload?"],self.rocketCost)
            if approve:
                self.rocketCost.makeBuy()
                self.base.availableOutbound += 1
        if self.launchButton.selected:
            self.launchButton.toggleSelected()
            need = self.base.launchCost*self.base.earthCostFactor
            if self.base.exportPoints >= need:
                approve = choicePopUp(self.screen,click,["Authorize resupply mission","for your base?"])
                if approve:
                    self.base.addEarthLaunch()
            else:
                need -= self.base.exportPoints
                if (self.base.adminPointsBalance > need and self.base.sciencePointsBalance > need):
                    approve = choicePopUp(self.screen,click,["Convert admin or science","points for launch?"],None,"ADMIN","SCIENCE")
                    if approve:
                        self.base.addEarthLaunch("Admin")
                    else:
                        self.base.addEarthLaunch("Science")
                elif self.base.adminPointsBalance > need:
                    approve = choicePopUp(self.screen,click,["Convert admin","points for launch?"])
                    if approve:
                        self.base.addEarthLaunch("Admin")
                elif self.base.sciencePointsBalance > need:
                    approve = choicePopUp(self.screen,click,["Convert science","points for launch?"])
                    if approve:
                        self.base.addEarthLaunch("Science")
        # updates button status
        if self.rocketCost.check() == False:
            self.rocketButton.makeDead()
        if (self.base.adminPointsBalance + self.base.exportPoints < self.base.launchCost*self.base.earthCostFactor and\
        self.base.sciencePointsBalance + self.base.exportPoints < self.base.launchCost*self.base.earthCostFactor):
            self.launchButton.makeDead()

    def getPanel(self):
        color = c.highlightOrange
        panel = getHorizontalBar(200,580)
        gap = 10
        yLoc = gap
        yLoc+=self.launchTag.get_height()+self.costTag.get_height()

        panel.blit(self.space.getDurationText(),(gap*2,yLoc))
        yLoc+=self.space.getDurationText().get_height()

        exportTag  = getTextSurface("export credit:",color,17)
        panel.blit(exportTag,(int(panel.get_width()/2)-exportTag.get_width(),yLoc))

        yLoc+=exportTag.get_height()

        scienceTag = getTextSurface("science pts:",color,17)
        panel.blit(scienceTag,(int(panel.get_width()/2)-scienceTag.get_width(),yLoc))

        yLoc+=scienceTag.get_height()
        
        adminTag  = getTextSurface("admin pts:",color,17)
        panel.blit(adminTag,(int(panel.get_width()/2)-adminTag.get_width(),yLoc))

        yLoc+=24 + gap*2

        transportTag  = getTextSurface("SPACE INFRASTRUCTURE:",color)
        panel.blit(transportTag,(gap,yLoc))
        yLoc+=transportTag.get_height()
        if len(self.base.transportList) == 0:
            transportNone  = getTextSurface("none",color,17)
            panel.blit(transportNone,(2*gap,yLoc))
        else:
            for b in self.base.transportList:
                transportNone  = getTextSurface(b.buildingName,b.color,17)
                panel.blit(transportNone,(2*gap,yLoc))
                yLoc+=transportNone.get_height()

        yLoc = panel.get_height()-gap-self.queuedTag.get_height()-3*getTextHeight(17)
        self.rocketCost.draw(panel,(3*gap+self.rocketButton.buttonSurface.get_width()-int(gap/2),yLoc))
        return panel
    
    def draw(self,mouseLoc):
        self.screen.blit(self.panel,(self.screen.get_width()-10-self.panel.get_width(),10))
        xA = self.screen.get_width()-10-self.panel.get_width()
        yA = 10
        gap = 10
        if self.savedEarthLaunches != self.base.availableEarthLaunches:
            self.launchTag = GlowTag("AVAILABLE LAUCHES: "+str(self.base.availableEarthLaunches))
            self.savedEarthLaunches = self.base.availableEarthLaunches
        yLoc = yA + gap
        self.screen.blit(self.launchTag.get(),(xA+gap,yLoc))
        yLoc+=self.launchTag.get_height()
        if self.savedLaunchCost != self.base.launchCost*self.base.earthCostFactor:
            self.costTag = GlowTag("LAUNCH COST: {0:.2f}".format(self.base.launchCost*self.base.earthCostFactor),size=17)
            self.savedLaunchCost = self.base.launchCost*self.base.earthCostFactor
        self.screen.blit(self.costTag.get(),(xA+gap*2,yLoc))
        yLoc+=self.costTag.get_height()+self.space.getDurationText().get_height()

        if self.savedExportNum != self.base.exportPoints:
            self.exportNum = GlowTag("{0:.1f}".format(self.base.exportPoints),c.white,c.grey,17)
            self.savedExportNum = self.base.exportPoints
        self.screen.blit(self.exportNum.get(),(xA + int(self.panel.get_width()/2),yLoc))
        yLoc+=self.exportNum.get_height()

        if self.savedScienceNum != self.base.sciencePointsBalance:
            self.scienceNum = GlowTag("{0:.1f}".format(self.base.sciencePointsBalance),c.white,c.purple,17)
            self.savedScienceNum = self.base.sciencePointsBalance
        self.screen.blit(self.scienceNum.get(),(xA + int(self.panel.get_width()/2),yLoc))
        yLoc+=self.scienceNum.get_height()

        if self.savedAdminNum != self.base.adminPointsBalance:
            self.adminNum = GlowTag("{0:.1f}".format(self.base.adminPointsBalance),c.white,c.pink,17)
            self.savedAdminNum = self.base.adminPointsBalance
        self.screen.blit(self.adminNum.get(),(xA + int(self.panel.get_width()/2),yLoc))
        yLoc+=self.adminNum.get_height()

        self.launchRect = self.launchButton.draw(self.screen,(xA + 5*gap,yLoc),mouseLoc)

        #draw  buy Button / switch from bottum
        queuedNumber = 0
        yLoc = yA + self.panel.get_height() - gap - self.queuedTag.get_height()
        for pad in self.base.launchPads:
            queuedNumber += len(pad.queue)
        if queuedNumber != self.savedQueuedNumber:
            self.savedQueuedNumber = queuedNumber
            self.queuedTag = GlowTag("QUEUED ROCKETS: "+str(self.savedQueuedNumber))
        self.screen.blit(self.queuedTag.get(),(xA+gap,yLoc))
        yLoc -= self.rocketTag.get_height()+3*getTextHeight(17)

        if self.savedRocketsCount != self.base.availableOutbound:
            self.rocketTag = GlowTag("AVAILABLE ROCKETS: "+str(self.base.availableOutbound))
            self.savedRocketsCount = self.base.availableOutbound
        self.screen.blit(self.rocketTag.get(),(xA+gap,yLoc))
        yLoc += self.rocketTag.get_height() + int(gap/2)
        self.rocketRect = self.rocketButton.draw(self.screen,(xA+2*gap,yLoc),mouseLoc)

        


def gauges(base):
    color = c.highlightOrange
    badColor = c.boldRed
    ptsWidth = 0
    statWidth = 0
    mWidth = 0
    reWidth= 0
    gap = 5

    maintainTag = getTextSurface("maint:",color,17)
    if base.maintainBalance >= 1.0:
        maintainNum = getTextSurface("{0:.1f}%".format(base.maintainBalance*100),c.white,17)
    else:
        maintainNum = getTextSurface("{0:.1f}%".format(base.maintainBalance*100),badColor,17)
    mWidth += maintainTag.get_width() + maintainNum.get_width() + gap

    buildingTag = getTextSurface("bld:",color,17)
    if base.buildingCondition >= 1.0:
        buildingNum = getTextSurface("{0:.1f}%".format(base.buildingCondition*100),c.white,17)
    else:
        buildingNum = getTextSurface("{0:.1f}%".format(base.buildingCondition*100),badColor,17)
    mWidth += buildingTag.get_width() + buildingNum.get_width() + gap

    housedTag = getTextSurface("housed:",color,17)
    if base.populationCount == 0:
        housedNum = getTextSurface("0%",badColor,17)
    elif base.habitatUnits/base.populationCount > 0.9999:
        housedNum = getTextSurface("100%",c.white,17)
    else:
        housedNum = getTextSurface("{0:.0f}%".format(100*(base.habitatUnits/base.populationCount)),badColor,17)
    mWidth += housedTag.get_width() + housedNum.get_width() + gap

    scienceTag = getTextSurface("sci({0:.0f}):".format(base.scienceLevel),color,17)
    scienceNum = getTextSurface("{0:.1f}".format(base.sciencePointsBalance) + \
        " ({0:.0f}/".format(base.sciencePoints)+"{0:.0f})".format(base.scienceLevelUp),c.purple,17)
    ptsWidth += scienceTag.get_width() +scienceNum.get_width()+ gap
    
    adminTag  = getTextSurface("adm({0:.0f}):".format(base.adminLevel),color,17)
    adminNum = getTextSurface("{0:.1f}".format(base.adminPointsBalance) + \
        " ({0:.0f}/".format(base.adminPoints)+"{0:.0f})".format(base.adminLevelUp),c.pink,17)
    ptsWidth += adminTag.get_width() + adminNum.get_width() + gap

    healthTag = getTextSurface("health:",color,17)
    healthNum = getTextSurface("{0:.1f}%".format(base.healthBalance*35000),c.green,17)
    statWidth += healthTag.get_width() + healthNum.get_width() + gap

    skillTag = getTextSurface("skill:",color,17)
    skillNum = getTextSurface("{0:.1f}%".format(base.skillBalance*35000),c.red,17)
    statWidth += skillTag.get_width() + skillNum.get_width() + gap

    psychTag = getTextSurface("psych:",color,17)
    psychNum = getTextSurface("{0:.1f}%".format(base.psychBalance*35000),c.aqua,17)
    statWidth += psychTag.get_width() + psychNum.get_width() + gap


    airTag = getTextSurface("airRe:",color,17)
    airNum = getTextSurface("{0:.1f}%".format(base.air.recyclePercent*100),base.air.color,17)
    reWidth += airTag.get_width() + airNum.get_width() + gap

    waterTag = getTextSurface("h2oRe:",color,17)
    waterNum = getTextSurface("{0:.1f}%".format(base.water.recyclePercent*100),base.water.color,17)
    reWidth += waterTag.get_width() + waterNum.get_width() + gap
    
    foodTag = getTextSurface("foodRe:",color,17)
    foodNum = getTextSurface("{0:.1f}%".format(base.food.recyclePercent*100),base.food.color,17)
    reWidth += foodTag.get_width() + foodNum.get_width() + gap

    widths = [ptsWidth,statWidth,reWidth,mWidth]
    maxWidth = 0
    for w in widths:
        if w > maxWidth:
            maxWidth = w

    panel = pygame.Surface((maxWidth,maintainTag.get_height()*4))
    panel.fill(c.trans)
    
    pygame.draw.line(panel,color,(panel.get_width()-mWidth,panel.get_height()-1),(panel.get_width()-5,panel.get_height()-1),1)

    xLoc = maxWidth - ptsWidth
    yLoc = 0
    
    panel.blit(scienceTag,(xLoc,yLoc))
    xLoc += scienceTag.get_width() 
    panel.blit(scienceNum,(xLoc,yLoc))
    xLoc += scienceNum.get_width() + gap
    panel.blit(adminTag,(xLoc,yLoc))
    xLoc += adminTag.get_width() 
    panel.blit(adminNum,(xLoc,yLoc))
    xLoc += adminNum.get_width() + gap

    xLoc = maxWidth - statWidth
    yLoc += adminTag.get_height()

    panel.blit(healthTag,(xLoc,yLoc))
    xLoc += healthTag.get_width() 
    panel.blit(healthNum,(xLoc,yLoc))
    xLoc += healthNum.get_width() + gap
    panel.blit(skillTag,(xLoc,yLoc))
    xLoc += skillTag.get_width() 
    panel.blit(skillNum,(xLoc,yLoc))
    xLoc += skillNum.get_width() + gap
    panel.blit(psychTag,(xLoc,yLoc))
    xLoc += psychTag.get_width() 
    panel.blit(psychNum,(xLoc,yLoc))
    xLoc += psychNum.get_width() + gap

    xLoc = maxWidth - reWidth
    yLoc += adminTag.get_height()

    panel.blit(airTag,(xLoc,yLoc))
    xLoc += airTag.get_width() 
    panel.blit(airNum,(xLoc,yLoc))
    xLoc += airNum.get_width() + gap
    panel.blit(waterTag,(xLoc,yLoc))
    xLoc += waterTag.get_width() 
    panel.blit(waterNum,(xLoc,yLoc))
    xLoc += waterNum.get_width() + gap
    panel.blit(foodTag,(xLoc,yLoc))
    xLoc += foodTag.get_width() 
    panel.blit(foodNum,(xLoc,yLoc))
    xLoc += foodNum.get_width() + gap

    xLoc = maxWidth - mWidth
    yLoc += adminTag.get_height()

    panel.blit(maintainTag,(xLoc,yLoc))
    xLoc += maintainTag.get_width()
    panel.blit(maintainNum,(xLoc,yLoc))
    xLoc += maintainNum.get_width() + gap
    panel.blit(buildingTag,(xLoc,yLoc))
    xLoc += buildingTag.get_width()
    panel.blit(buildingNum,(xLoc,yLoc))
    xLoc += buildingNum.get_width() + gap
    panel.blit(housedTag,(xLoc,yLoc))
    xLoc += housedTag.get_width()
    panel.blit(housedNum,(xLoc,yLoc))



    panel.set_colorkey(c.trans)
    return panel

def resourceValues(base):
    width = 400
    panel = pygame.Surface((width,3*getTextHeight(17)))
    panel.fill(c.trans)
    title = getTextSurface("CURRENT EXPORT CREDITS PER TON:",size=17)
    panel.blit(title,(0,0))
    yLoc = title.get_height()
    xLoc = 0
    for resource in base.allResources:
        if resource.tag != "POWER":
            tag = getTextSurface(resource.shortTag+":{0:.2f}ec".format(resource.value),resource.color,17)
            if xLoc + tag.get_width() > width:
                xLoc = 0
                yLoc += tag.get_height()
            panel.blit(tag,(xLoc,yLoc))
            xLoc += tag.get_width() + 3   
    panel.set_colorkey(c.trans)
    return panel

class HomeCharts:
    foodChart = None
    airChart = None
    waterChart = None
    powerChart = None
    resourceSurface = None
    gaugesSurface = None

    @staticmethod
    def draw(screen):
        if HomeCharts.gaugesSurface != None:
            screen.blit(HomeCharts.gaugesSurface,(screen.get_width()-HomeCharts.gaugesSurface.get_width(),60))
            gaugesHeight = HomeCharts.gaugesSurface.get_height()
        else:
            gaugesHeight = 0
        if HomeCharts.resourceSurface != None:
            screen.blit(HomeCharts.resourceSurface,(screen.get_width()-HomeCharts.resourceSurface.get_width()-5,60+gaugesHeight))
        if HomeCharts.foodChart != None:
            gap = 5
            chartWidth = HomeCharts.powerChart.get_width()
            chartHeight = HomeCharts.powerChart.get_height()
            
            screen.blit(HomeCharts.powerChart,(screen.get_width()-chartWidth-gap,screen.get_height()-chartHeight-gap))
            screen.blit(HomeCharts.airChart,(screen.get_width()-2*chartWidth-2*gap,screen.get_height()-chartHeight-gap))
            screen.blit(HomeCharts.waterChart,(screen.get_width()-3*chartWidth-3*gap,screen.get_height()-chartHeight-gap))
            screen.blit(HomeCharts.foodChart,(screen.get_width()-4*chartWidth-4*gap,screen.get_height()-chartHeight-gap))

def resourceChart(base,storageUse,storageCapacity,usage):
    width = 80
    panel = pygame.Surface((width,300))
    panel.fill(c.trans)
    panel.set_colorkey(c.trans)
    yLoc = 2
    rTag = getTextSurface("RESOURCES",c.highlightOrange,12)
    sTag = getTextSurface("STORAGE",c.highlightOrange,12)
    xLoc = width - sTag.get_width()
    panel.blit(sTag,(xLoc,yLoc))
    yLoc += sTag.get_height()
    if usage > storageCapacity:
        thisColor = c.red
    else:
        thisColor = c.grey
    sTag2 = getTextSurface("{0:.1f}".format(usage) + "/{0:.1f}".format(storageCapacity),thisColor,17)
    xLoc = width - sTag2.get_width()
    panel.blit(sTag2,(xLoc,yLoc))
    yLoc += sTag2.get_height()
    sTag3 = getTextSurface("{0:.1f}%".format(storageUse*100),thisColor,17)
    xLoc = width - sTag3.get_width()
    panel.blit(sTag3,(xLoc,yLoc))
    yLoc += sTag3.get_height() + 3
    
    xLoc = width - rTag.get_width()
    panel.blit(rTag,(xLoc,yLoc))
    yLoc+= rTag.get_height()
    for resource in base.allResources:
        if resource.selfStorage == False:
            if resource.quantity > 0:
                thisColor = resource.color
            else:
                thisColor = c.darken(c.grey,50)
            tag = getTextSurface(resource.shortTag+":{0:.2f}".format(resource.quantity),thisColor,17)
            xLoc = width - tag.get_width()
            if resource.deficit > 0:
                block = pygame.Surface((tag.get_width(),tag.get_height()))
                block.fill(c.red)
                if 5*resource.deficit < 255:
                    block.set_alpha(5*resource.deficit)
                else:
                    block.set_alpha(255)
                    resource.deficit = 50
                resource.deficit -=1
                panel.blit(block,(xLoc,yLoc))
            panel.blit(tag,(xLoc,yLoc))
            yLoc+=tag.get_height()
            if resource.production > 0 or resource.baseConsumption+resource.industryConsumption > 0:
                thisColor = resource.color
            else:
                thisColor = c.darken(c.grey,50)
            tag2 = getTextSurface("(+{0:.2f}".format(resource.production) + " -{0:.2f})"\
                .format(resource.baseConsumption+resource.industryConsumption),thisColor,13)
            xLoc = width - tag2.get_width()
            panel.blit(tag2,(xLoc,yLoc))
            yLoc += tag2.get_height()
    


            
    
    return panel

def needChart(resource,air = False,airVolume = 0, power = False, powerFactor = 0):
    #dailyProd,dailyUse,stored,storeCap
    panel = pygame.Surface((60,140))
    panel.fill(c.trans)
    activity = True
    color = resource.color
    tag = resource.tag
    totalConsumption = resource.baseConsumption + resource.industryConsumption
    if resource.storageCapacity != 0:
        ratio = resource.quantity/resource.storageCapacity
    else:
        ratio = 0
    auxColor = c.highlightOrange
    if totalConsumption > 0 or resource.production > 0:
        if totalConsumption > resource.production:
            auxColor = c.boldRed
            prodRatio = resource.production/totalConsumption
            pygame.draw.line(panel,color,(28,105),(28,105-int(105*prodRatio)),2) #prod
            pygame.draw.line(panel,color,(32,105),(32,0),2) #use
            if resource.industryConsumption > 0:
                indRatio = resource.industryConsumption/totalConsumption
                pygame.draw.line(panel,c.darken(color,75),(32,0),(32,int(105*indRatio)),2) #ind use diff
            if air:
                solSupply = (resource.quantity - airVolume) / (totalConsumption-resource.production)
            else:
                solSupply = resource.quantity/(totalConsumption-resource.production)
            infoLabel = getTextSurface("{0:.1f} SOL LEFT".format(solSupply),auxColor,13)
        else:
            prodRatio = totalConsumption/resource.production
            pygame.draw.line(panel,color,(28,105),(28,0),2) #prod
            pygame.draw.line(panel,color,(32,105),(32,105-int(105*prodRatio)),2) #use
            if resource.industryConsumption > 0:
                indRatio = resource.industryConsumption/totalConsumption
                ht = 105-(105-int(105*prodRatio))
                pygame.draw.line(panel,c.darken(color,75),(32,105-int(105*prodRatio)),(32,105-int(105*prodRatio)-(int(ht*indRatio))),2) #ind use diff
            if ratio < 0.999:
                infoLabel = getTextSurface("{0:.1f} SURPLUS".format(resource.production-totalConsumption),auxColor,13)
            else:
                infoLabel = getTextSurface("{0:.1f} WASTE".format(resource.production-totalConsumption),auxColor,13)
    else:
        activity = False
        infoLabel = getTextSurface("NO ACTIVITY",auxColor,13)

    if air or power:
        if air and (airVolume > 0):
            pressure = (resource.quantity/airVolume)*100
            if pressure > 100:
                pressureLabel = getTextSurface("+100%",color)
            elif pressure > 90:
                pressureLabel = getTextSurface("{0:.1f}%".format(pressure),c.highlightOrange)
            else:
                pressureLabel = getTextSurface("{0:.1f}%".format(pressure),c.boldRed)
            panel.blit(pressureLabel,(60-pressureLabel.get_width(),74))
        if power:
            if powerFactor > 0.99:
                powerLabel = getTextSurface("+100%",color)
            elif powerFactor > 0.8:
                powerLabel = getTextSurface("{0:.1f}%".format(100*powerFactor),c.highlightOrange)
            else:
                powerLabel = getTextSurface("{0:.1f}%".format(100*powerFactor),c.boldRed)
            panel.blit(powerLabel,(60-powerLabel.get_width(),74))

    prodLabel = getTextSurface("+{0:.1f}".format(resource.production),color,16)
    useLabel = getTextSurface("-{0:.1f}".format(totalConsumption),color,16)

    if air == False:
        storedText = str(int(resource.quantity))
        capacityText = str(int(resource.storageCapacity))
    else:
        storedText = str(int(resource.quantity - airVolume))
        capacityText = str(int(resource.storageCapacity - airVolume))
    if ratio > 0.15:
        capacityLabel = getTextSurface(storedText + "/" + capacityText,color)
    else:
        capacityLabel = getTextSurface(storedText + "/" + capacityText,auxColor)

    label = getTextSurface(tag,color)

    bar = pygame.Surface((60,4))
    bar.fill(c.grey)
    if ratio > 0:
        fillBar = pygame.Surface((int(60*ratio),4))
    else:
        fillBar = pygame.Surface((1,4))
    fillBar.fill(color)
    bar.blit(fillBar,(0,0))

    panel.blit(capacityLabel,(30-int(capacityLabel.get_width()/2),140-capacityLabel.get_height()))
    panel.blit(label,(30-int(label.get_width()/2),140-capacityLabel.get_height()-label.get_height()))
    panel.blit(bar,(0,140-capacityLabel.get_height()-label.get_height()-bar.get_height()))
    panel.blit(infoLabel,(60-infoLabel.get_width(),140-capacityLabel.get_height()-label.get_height()-bar.get_height()-infoLabel.get_height()))
    if activity:
        panel.blit(prodLabel,(0,140-capacityLabel.get_height()-label.get_height()-bar.get_height()-infoLabel.get_height()-prodLabel.get_height()))
        panel.blit(useLabel,(60-useLabel.get_width(),140-capacityLabel.get_height()-label.get_height()-bar.get_height()-infoLabel.get_height()-useLabel.get_height()))

    panel.set_colorkey(c.trans)
    return panel

def mainPanel(base):
    panel = getHorizontalBar(800,60)
    baseName = getTextSurface(base.name)
    panel.blit(baseName,(panel.get_width() - 5 - baseName.get_width() ,int(panel.get_height() / 20)))
    timeLabel = getTextSurface(str(base.hour) + ":00 sol:" + str(base.solCycle) + " MY:" + str(base.marsYear)+ " EY:" + str(base.earthYear))
    panel.blit(timeLabel,(panel.get_width() - 5 - timeLabel.get_width() ,int(panel.get_height() / 20)+baseName.get_height()))
    popLabel = getTextSurface("population:" + str(base.populationCount))
    panel.blit(popLabel,(panel.get_width() - 5 - popLabel.get_width() ,int(panel.get_height() / 20)+baseName.get_height()+timeLabel.get_height()))
    return panel

def getHorizontalBar(w,h,color = c.panelGrey):
    width = w
    height = h
    panel = pygame.Surface((width, height))
    panel.fill(color)
    stripe = pygame.Surface((width,1))
    stripe.fill(c.highlightOrange)
    panel.blit(stripe,(0,1))
    panel.blit(stripe,(0,height-2))
    return panel

class GlowTag:
    def __init__(self,text,startColor=c.highlightYellow,endColor=c.highlightOrange,size = 20,frames = 20):
        self.text = text
        self.size = size
        self.color = startColor
        self.rTracker = float(startColor[0])
        self.gTracker = float(startColor[1])
        self.bTracker = float(startColor[2])
        self.rTarget = endColor[0]
        self.gTarget = endColor[1]
        self.bTarget = endColor[2]
        self.rVelocity = (self.rTarget-self.rTracker)/float(frames)
        self.gVelocity = (self.gTarget-self.gTracker)/float(frames)
        self.bVelocity = (self.bTarget-self.bTracker)/float(frames)
        self.surface = getTextSurface(self.text,self.color,self.size)
        self.done = False

    def get_height(self):
        return self.surface.get_height()

    def get_width(self):
        return self.surface.get_width()

    def updateColor(self):
        r = int(self.rTracker)
        if r > 255:
            r = 255
        if r < 0:
            r = 0
        g = int(self.gTracker)
        if g > 255:
            g = 255
        if g < 0:
            g = 0
        b = int(self.bTracker)
        if b > 255:
            b = 255
        if b < 0:
            b = 0
        self.color = (r,g,b)

    def adjustAspect(self,tracker,target,velocity):
        if velocity <= 0:
            if tracker > target:
                tracker += velocity
            else:
                tracker = target
        else:
            if tracker < target:
                tracker += velocity
            else:
                tracker = target
        return tracker

    def get(self):
        if self.done == False:
            toReturn = self.surface.copy()
            if self.bTracker == self.bTarget and self.gTracker == self.gTarget and self.rTracker == self.rTarget:
                self.done = True
            if self.rTracker != self.rTarget:
                self.rTracker = self.adjustAspect(self.rTracker,self.rTarget,self.rVelocity)
            if self.gTracker != self.gTarget:
                self.gTracker = self.adjustAspect(self.gTracker,self.gTarget,self.gVelocity)
            if self.bTracker != self.bTarget:
                self.bTracker = self.adjustAspect(self.bTracker,self.bTarget,self.bVelocity)
            self.updateColor()
            self.surface = getTextSurface(self.text,self.color,self.size)
            return toReturn
        else:
            return self.surface


def getTextSurface(text, color = c.highlightOrange, size = 20,aa = True):
    font = pygame.font.SysFont('arialblack.ttf',size)
    textSurface = font.render(text,aa,color)
    return textSurface

def getTextHeight(thisSize):
    test = getTextSurface("TIyi",size=thisSize)
    return test.get_height()

def getTextWidth(text,thisSize):
    test = getTextSurface(text,size=thisSize)
    return test.get_width()


class Button:
    def __init__(self, buttonText, width = 64, height = 24, theme = "main", \
        fit = False, img = None,info = False,dataEmbed = None,live = True):
        self.selected = False
        self.dataEmbed = dataEmbed
        self.live = live
        # adjust (make main else)
        if(theme=="main"):
            mainColor = c.subRedDark 
            textColor = c.highlightOrange 
            moColor = c.subRed
            selectColor = c.highlightYellow
        textSurface = getTextSurface(buttonText)
        textSurfaceSelected = getTextSurface(buttonText,selectColor)
        if img != None:
            width = img.get_width()
            height = img.get_height()
        if fit:
            if width < textSurface.get_width():
                width = textSurface.get_width()
        else:
            resize = 19
            while textSurface.get_width() > (width - 6):
                textSurface = getTextSurface(buttonText,size = resize)
                textSurfaceSelected = getTextSurface(buttonText, selectColor, size = resize)
                resize -= 1
            
        plate = pygame.Surface((width,height))
        button = plate.copy()
        button.fill(mainColor)
        buttonMO = plate.copy()
        buttonMO.fill(moColor)
        plateBorder = pygame.Surface((width-2,height-2))
        plateBorder.fill(textColor)
        plateInner = pygame.Surface((width-4,height-4))
        plateInner.fill(mainColor)
        plateInnerMO = plateInner.copy()
        plateInnerMO.fill(moColor)
        button.blit(plateBorder,(1,1))
        button.blit(plateInner,(2,2))
        buttonMO.blit(plateBorder,(1,1))
        buttonMO.blit(plateInnerMO,(2,2))
        if img != None:
            button.blit(img,(0,-1))
            buttonMO.blit(img,(0,-1))

        buttonS = button.copy()
        buttonSMO = buttonMO.copy()

        textLoc = (int(button.get_width()/2-textSurface.get_width()/2),1+int(button.get_height()/2-textSurface.get_height()/2))
        button.blit(textSurface,textLoc)
        buttonMO.blit(textSurface,textLoc)

        buttonS.blit(textSurfaceSelected,textLoc)
        buttonSMO.blit(textSurfaceSelected,textLoc)

        buttonDeadOver = pygame.Surface((button.get_width(),button.get_height()))
        buttonDead = button.copy()
        buttonDeadOver.fill(c.grey)
        buttonDeadOver.set_alpha(130)
        buttonDead.blit(buttonDeadOver,(0,0))

        self.buttonSurface = button
        self.buttonSurfaceMO = buttonMO
        self.buttonSurfaceSelected = buttonS
        self.buttonSurfaceSelectedMO = buttonSMO
        self.buttonSurfaceDead = buttonDead
        self.mouseOverInfo = info
        self.infoTextList = []
        self.mouseOverSurface = None
        self.mouseOverLoc = (0,0)
        self.mouseOverAlpha = 0
        self.protectedMO = False
    
    def makeBuildingMouseOver(self,capsule,costObject):
        gap = 3
        lineSurfaces = []
        costObject.makeDrawable()
        costHeight = len(costObject.tags)*getTextHeight(17)
        height = 3*gap + costHeight
        width = 2*gap
        for line in capsule[6]:
            lineS = getTextSurface(line,size=17)
            if lineS.get_width()+2*gap > width:
                width = lineS.get_width()+2*gap
            height += lineS.get_height()
            lineSurfaces.append(lineS)            
        popUp = getOutlinePanel(height,width,c.darken(c.grey,50))
        popUp = blitFromSurfaceList(popUp,lineSurfaces,(gap,gap),left=True)
        costObject.draw(popUp,(2*gap,height-gap-costHeight))
        """
        if costObject.check():
            costIndicator = getTextSurface("ok",c.green,24)
        else:
            costIndicator = getTextSurface("X",c.red,24)
        popUp.blit(costIndicator,(popUp.get_width()-gap-costIndicator.get_width(),\
            popUp.get_height()-gap-costIndicator.get_height()))
        """
        self.mouseOverSurface = popUp

    def makeMouseOver(self,textList):
        gap = 3
        lineSurfaces = []
        height = 2*gap
        width = 2*gap
        for line in textList:
            lineS = getTextSurface(line,size=17)
            if lineS.get_width()+2*gap > width:
                width = lineS.get_width()+2*gap
            height += lineS.get_height()
            lineSurfaces.append(lineS)            
        popUp = getOutlinePanel(height,width,c.darken(c.grey,50))
        popUp = blitFromSurfaceList(popUp,lineSurfaces,(gap,gap),left=True)
        self.mouseOverSurface = popUp
        
    def makeLive(self):
        self.live = True

    def makeDead(self,protected = False):
        self.live = False
        if protected:
            self.protectedMO = protected
        
    def setInfoTextList(self,textList):
        self.infoTextList = textList
    
    def toggleSelected(self):
        if self.live:
            if self.selected:
                self.selected = False
            else:
                self.selected = True

    def getSurface(self):
        return self.buttonSurface

    def getMouseOver(self):
        return self.buttonSurfaceMO

    def getSelected(self):
        return self.buttonSurfaceSelected
    
    def getSelectedMO(self):
        return self.buttonSurfaceSelectedMO

    def draw(self,canvas,loc,mouseLoc):
        if self.live:
            if self.selected:
                selfRect = canvas.blit(self.getSelected(),loc)
                if selfRect.collidepoint(mouseLoc):
                    selfRect = canvas.blit(self.getSelectedMO(),loc)
            else:
                selfRect = canvas.blit(self.getSurface(),loc)
                if selfRect.collidepoint(mouseLoc):
                    selfRect = canvas.blit(self.getMouseOver(),loc)
            if self.mouseOverInfo:
                if loc[0] < 40:
                    self.mouseOverLoc = (loc[0]+5+self.buttonSurface.get_width(),mouseLoc[1]-int(self.mouseOverSurface.get_height()/2))
                elif loc[1] < 50:
                    self.mouseOverLoc = (mouseLoc[0]-int(self.mouseOverSurface.get_width()/2),loc[1]+5+self.buttonSurface.get_height())
                else:
                    self.mouseOverLoc = (mouseLoc[0]-int(self.mouseOverSurface.get_width()/2),loc[1]-5-self.mouseOverSurface.get_height())
        else:
            selfRect = canvas.blit(self.buttonSurfaceDead,loc)
        if self.mouseOverInfo:
            if loc[0] < 40:
                self.mouseOverLoc = (loc[0]+5+self.buttonSurface.get_width(),mouseLoc[1]-int(self.mouseOverSurface.get_height()/2))
            elif loc[1] < 50:
                self.mouseOverLoc = (mouseLoc[0]-int(self.mouseOverSurface.get_width()/2),loc[1]+5+self.buttonSurface.get_height())
            else:
                self.mouseOverLoc = (mouseLoc[0]-int(self.mouseOverSurface.get_width()/2),loc[1]-5-self.mouseOverSurface.get_height())
        if self.live or self.protectedMO:
            if self.mouseOverInfo and selfRect.collidepoint(mouseLoc):
                if self.mouseOverAlpha < 255:
                    self.mouseOverAlpha +=15
                    self.mouseOverSurface.set_alpha(self.mouseOverAlpha)
                self.mouseTracker = mouseLoc
                canvas.blit(self.mouseOverSurface,self.mouseOverLoc)
            else:
                if self.mouseOverAlpha > 0:
                    self.mouseOverAlpha -=15
                    self.mouseOverSurface.set_alpha(self.mouseOverAlpha)
                    canvas.blit(self.mouseOverSurface,(self.mouseOverLoc))
        return selfRect

def getUnemployedPanels(population,robots):
    unemployedList = []
    backColor = c.black
    textColor = c.white
    for person in population:
        if person.job == None:
            unemployedList.append(person)
    for r in robots:
        if r.job == None:
            unemployedList.append(r)
    aWidth = a.naut.get_width()
    aHeight = a.naut.get_height()
    unLabel = getTextSurface("UNEMPLOYED",textColor,15)
    subLabel1 = getTextSurface("CHILDREN",textColor,12)
    subLabel2 = getTextSurface("ADULTS",textColor,12)
    gap = 3
    width = aWidth*len(unemployedList) + 3*gap
    if unLabel.get_width() + 2*gap > width:
        width = unLabel.get_width() + 2*gap
    if subLabel1.get_width() + subLabel2.get_width() + gap *3 > width and len(unemployedList)>0:
        width = subLabel1.get_width() + subLabel2.get_width() + gap *3

    height = aHeight + unLabel.get_height() + subLabel1.get_height() + 2*gap
    # FORK and return two panels, one to fade??
    fadePanel = getOutlinePanel(height,width,backColor,textColor)
    panel = pygame.Surface((width,height))
    panel.fill(c.trans)
    panel.set_colorkey(c.trans)
    panel.blit(unLabel,(gap,gap))
    if len(unemployedList)>0:
        panel.blit(subLabel1,(gap,panel.get_height()-gap-subLabel1.get_height()))
        panel.blit(subLabel2,(panel.get_width()-gap-subLabel2.get_width(),\
            panel.get_height()-gap-subLabel2.get_height()))
    xAnchor = gap
    yAnchor = gap + unLabel.get_height()
    toWriteSurfacesMO = []
    toWriteSurfacesMO.append(getTextSurface("CHILDREN:",backColor,15))
    for person in unemployedList:
        if person.age < p.People.workingAge and person.robot == False:
            panel.blit(a.nautKid,(xAnchor,yAnchor))
            xAnchor+=aWidth
            toWriteSurfacesMO.append(getTextSurface(" "+person.name,backColor,12))
    xAnchor = panel.get_width() - gap - aWidth
    toWriteSurfacesMO.append(getTextSurface("ADULTS:",backColor,15))
    for person in unemployedList:
        if person.age >= p.People.workingAge or person.robot:
            if person.robot:
                if person.functional:
                    panel.blit(a.bot,(xAnchor,yAnchor))
                else:
                    panel.blit(a.botBad,(xAnchor,yAnchor))
            else:
                if person.sane:
                    panel.blit(a.naut,(xAnchor,yAnchor))
                else:
                    panel.blit(a.nautBad,(xAnchor,yAnchor))
            xAnchor-=aWidth
            toWriteSurfacesMO.append(getTextSurface(" "+person.name,backColor,12))
    h = gap*2
    w = gap*2
    m = 0
    for line in toWriteSurfacesMO:
        h += line.get_height()
        if line.get_width() > m:
            m = line.get_width()
    w += m
    mouseOver = pygame.Surface((w,h))
    mouseOver.fill(textColor)
    mouseOver = blitFromSurfaceList(mouseOver,toWriteSurfacesMO,(gap,gap),True)

    unemployedPanels = [panel,fadePanel,mouseOver]
    return unemployedPanels

class JobPanel:
    def __init__(self,screen,buildingList,color,jobsTag,nonBuildingJobList = [],robot = False):
        aWidth = a.naut.get_width()
        aHeight = a.naut.get_height()
        self.robot = robot
        self.canvas = screen
        self.backColor = color
        darkenFactor = 70
        self.textColor = c.darken(color,darkenFactor)
        self.gap = 10
        self.maxWidth = int(self.canvas.get_width()/2) - 2*self.gap
        self.tag = getTextSurface(jobsTag,self.textColor,15)
        self.jobList = [] #contains person, so name and prod
        self.buildingNameList = [] 
        if self.robot == False:
            for building in buildingList:
                for job in building.jobs:
                    self.jobList.append(job)
                    self.buildingNameList.append(building.buildingName)
            for job in nonBuildingJobList:
                self.jobList.append(job)
                self.buildingNameList.append("BASE")
        else:
            for robot in nonBuildingJobList:
                self.jobList.append(robot)
        if len(self.jobList) > 0:
            self.jobRows = 1
        else:
            self.jobRows = 0
        self.panelWidth = 2*self.gap + aWidth * len(self.jobList)
        self.perRow = len(self.jobList)
        while self.panelWidth > self.maxWidth:
            self.jobRows += 1
            if len(self.jobList) % self.jobRows != 0:
                self.panelWidth = 2*self.gap + aWidth * (int(len(self.jobList)/self.jobRows)+1)
                self.perRow = (int(len(self.jobList)/self.jobRows)+1)
            else:
                self.panelWidth = 2*self.gap + aWidth * int(len(self.jobList)/self.jobRows)
                self.perRow = int(len(self.jobList)/self.jobRows)
        if self.panelWidth < 2*self.gap + self.tag.get_width():
            self.panelWidth = 2*self.gap + self.tag.get_width()
        self.panelHeight = 2*self.gap + aHeight*self.jobRows + self.tag.get_height()
        self.backPanel = getOutlinePanel(self.panelHeight,self.panelWidth,self.backColor,self.textColor)
        self.backPanel.blit(self.tag,(self.gap,int(self.gap/2)))
        self.backPanel.set_alpha(150)
        self.rectList = []
        # must be parrallel for mouseover, fire, must be drawn each time.

    def draw(self,yLoc,left = True,customX = 0):
        aWidth = a.naut.get_width()
        aHeight = a.naut.get_height()
        self.rectList = []
        if customX == 0:
            if left:
                startLoc = (self.gap,yLoc)
            else:
                startLoc = (self.canvas.get_width()-self.gap-self.panelWidth,yLoc)
        else:
            startLoc = (customX,yLoc)
        self.canvas.blit(self.backPanel,startLoc)
        count = 0
        xLoc = startLoc[0] + self.gap
        yLoc = startLoc[1]+self.gap+self.tag.get_height()
        if self.robot:
            for robot in self.jobList:
                if robot.functional:
                    jobRect = self.canvas.blit(a.bot,(xLoc,yLoc))
                else:
                    jobRect = self.canvas.blit(a.botBad,(xLoc,yLoc))
                # TODO fork for non-functional
                self.rectList.append(jobRect)
                xLoc += aWidth
                count+=1
                if count == self.perRow:
                    count = 0
                    yLoc += aHeight
                    xLoc = startLoc[0] + self.gap
        else:
            for job in self.jobList:
                if job.person != None:
                    if job.person.robot:
                        if job.person.functional:
                            jobRect = self.canvas.blit(a.bot,(xLoc,yLoc))
                        else:
                            jobRect = self.canvas.blit(a.botBad,(xLoc,yLoc))
                    else:
                        if job.person.sane:
                            jobRect = self.canvas.blit(a.naut,(xLoc,yLoc))
                        else:
                            jobRect = self.canvas.blit(a.nautBad,(xLoc,yLoc))
                else:
                    jobRect = self.canvas.blit(a.nautShadow,(xLoc,yLoc))
                self.rectList.append(jobRect)
                xLoc += aWidth
                count+=1
                if count == self.perRow:
                    count = 0
                    yLoc += aHeight
                    xLoc = startLoc[0] + self.gap

    def getPersonObject(self,click):
        person = None
        index = 0
        for rect in self.rectList:
            if rect.collidepoint(click):
                if self.jobList[index].person != None:
                    person = self.jobList[index].person
            index += 1
        return person

    def checkMouseOver(self,mouseLoc):
        index = 0
        for rect in self.rectList:
            if rect.collidepoint(mouseLoc):
                toWriteSurfacesMO = []
                if self.robot:
                    toWriteSurfacesMO.append(getTextSurface(self.jobList[index].name,self.backColor,15))
                    if self.jobList[index].job == None:
                        toWriteSurfacesMO.append(getTextSurface("IDLE",self.backColor,15))
                    else:
                        toWriteSurfacesMO.append(getTextSurface(self.jobList[index].job.tag,self.backColor,15))
                        toWriteSurfacesMO.append(getTextSurface("{0:.3f}".format(self.jobList[index].job.productivity),self.backColor,15))
                    toWriteSurfacesMO.append(getTextSurface("COND: {0:.0f}%".format(100.0*(self.jobList[index].health/1.5)),self.backColor,15))
                else:
                    toWriteSurfacesMO.append(getTextSurface(self.jobList[index].tag,self.backColor,15))
                    if self.jobList[index].person == None:
                        toWriteSurfacesMO.append(getTextSurface("EMPTY",c.boldRed,12))
                        if self.jobList[index].building != None:
                            toWriteSurfacesMO.append(getTextSurface(self.jobList[index].building.buildingName,self.backColor,15))
                            if self.jobList[index].building.shutoff:
                                toWriteSurfacesMO.append(getTextSurface("OFFLINE",c.boldRed,12))
                    else: 
                        if self.jobList[index].person.job.building != None:
                            toWriteSurfacesMO.append(getTextSurface(self.jobList[index].person.job.building.buildingName,self.backColor,15))
                        toWriteSurfacesMO.append(getTextSurface(self.jobList[index].person.name,self.backColor,15))
                        toWriteSurfacesMO.append(getTextSurface("{0:.3f}".format(self.jobList[index].productivity),self.backColor,15))
                h = self.gap*2
                w = self.gap*2
                m = 0
                for line in toWriteSurfacesMO:
                    h += line.get_height()
                    if line.get_width() > m:
                        m = line.get_width()
                w += m
                mouseOver = pygame.Surface((w,h))
                mouseOver.fill(self.textColor)
                mouseOver = blitFromSurfaceList(mouseOver,toWriteSurfacesMO,(self.gap,self.gap))
                if mouseLoc[0] < int(self.canvas.get_width()/2):
                    xLoc = mouseLoc[0] + self.gap
                else:
                    xLoc = mouseLoc[0]-int(mouseOver.get_width()) - self.gap
                self.canvas.blit(mouseOver,(xLoc,mouseLoc[1]-3-mouseOver.get_height()))
            index += 1




        


## MAKE OBJECT ##
#def getJobPanel(mainLabel,pList = [],industryBuildingList,unemployed=False):
    #subdivide
    #make labels
    #get size
    #get panel
    #place dudes
    #label?


def getOutlinePanel(height,width,color = c.panelGrey,borderColor = c.highlightOrange):
    panel = pygame.Surface((width,height))
    panel.fill(color)
    pygame.draw.line(panel,borderColor,(1,1),(1,height-2),1)
    pygame.draw.line(panel,borderColor,(1,1),(width-2,1),1)
    pygame.draw.line(panel,borderColor,(width-2,1),(width-2,height-2),1)
    pygame.draw.line(panel,borderColor,(width-2,height-2),(1,height-2),1)
    return panel

def blitFromSurfaceList(canvas,surfaceList,startLoc,left=False):
    yLoc = startLoc[1]
    for surface in surfaceList:
        if left:
            xLoc = startLoc[0]
        else:
            xLoc = int(canvas.get_width()/2) - int(surface.get_width()/2)
        canvas.blit(surface,(xLoc,yLoc))
        yLoc += surface.get_height()
    return canvas

def blitFromTextList(canvas,textList,startLoc,textColor = c.highlightOrange,textSize = 20,left=False):
    blitList = []
    for text in textList:
        textSurface = getTextSurface(text,textColor,textSize)
        blitList.append(textSurface)
    yLoc = startLoc[1]
    for line in blitList:
        if left:
            xLoc = startLoc[0]
        else:
            xLoc = int(canvas.get_width()/2) - int(line.get_width()/2)
        canvas.blit(line,(xLoc,yLoc))
        yLoc += line.get_height()
    return canvas

class InfoObject:
    def __init__(self,thisObject,delay = 0):
        self.object = thisObject
        self.createSurface(thisObject)
        self.alpha = 15
        self.lastRefresh = 0 #use sol to track
        self.delay = delay
        self.lastDraw = (0,0)
        #TODO only make buttons if valid (all but habitat & storage?)
        if isinstance(thisObject,o.Building) and isinstance(thisObject,o.StorageBuilding) == False:
            if thisObject.shutoff:
                self.shutoffButton = Button("RESTART",dataEmbed=self.object)
            else:
                self.shutoffButton = Button("SHUT DOWN",dataEmbed=self.object)
            if len(thisObject.jobs) > 0:
                self.priorityButton = Button("PRIORITIZE",dataEmbed=self.object)
            else:
                self.priorityButton = Button("REENGINEER",dataEmbed=self.object)
        else:
            self.shutoffButton = None
            self.priorityButton = None

    def updateButtons(self):
        if self.object.shutoff:
            self.shutoffButton = Button("RESTART",dataEmbed=self.object)
        else:
            self.shutoffButton = Button("SHUT DOWN",dataEmbed=self.object)

    def createSurface(self,thisObject):
        gap = 2
        size = 17
        color = c.panelGrey
        toWrite = []
        textColor = c.highlightOrange
        borderColor = c.highlightOrange
        if isinstance(thisObject,o.Building):
            nameLine = getTextSurface(thisObject.buildingName,thisObject.color,size+3)
            toWrite.append(nameLine)
            if thisObject.shutoff:
                locLine = getTextSurface("OFFLINE",textColor,size)
                toWrite.append(locLine)
            elif thisObject.finished == False:
                if thisObject.lander:
                    locLine = getTextSurface("INBOUND",textColor,size)
                else:
                    locLine = getTextSurface("UNDER CONSTRUCTION",textColor,size)
                toWrite.append(locLine)
            else:
                locLine = getTextSurface("maint:{0:.3f}".format(thisObject.maintain),textColor,size)
                toWrite.append(locLine)
                pLine = getTextSurface("power:{0:.3f}".format(thisObject.base.powerFactor),textColor,size)
                toWrite.append(pLine)
                if len(thisObject.jobs)>0:
                    for job in thisObject.jobs:
                        jobLine = getTextSurface(job.tag+":",thisObject.color,size)
                        toWrite.append(jobLine)
                        if job.person != None:
                            jobNameLine = getTextSurface(" "+job.person.name,textColor,size-2)
                        else:
                            jobNameLine = getTextSurface(" UNFILLED",textColor,size-2)
                        toWrite.append(jobNameLine)
                if isinstance(thisObject,o.HabitatBuilding):
                    oLine = getTextSurface("psych:{0:.0f}%".format(thisObject.base.powerFactor * thisObject.bonus*thisObject.maintain*thisObject.psychEffect*100),textColor,size)
                    toWrite.append(oLine)
                    rLine = getTextSurface("RESIDENTS:",thisObject.color,size)
                    toWrite.append(rLine)
                    if len(thisObject.residents) > 0:
                        if len(thisObject.residents) <= 10:
                            for person in thisObject.residents:
                                nameLine = getTextSurface(" "+person.name,textColor,size-3)
                                toWrite.append(nameLine)
                        elif len(thisObject.residents) <= 20:
                            col = 0
                            for person in thisObject.residents:
                                if col == 0:
                                    nameText = " "+person.name
                                    col+=1
                                else:
                                    nameText += " / "+person.name
                                    nameLine = getTextSurface(nameText,textColor,size-3)
                                    toWrite.append(nameLine)
                                    col = 0
                        else:
                            col = 0
                            for person in thisObject.residents:
                                if col == 0:
                                    nameText = " "+person.name
                                    col+=1
                                else:
                                    nameText += " / "+person.name
                                    if col ==1:
                                        col+=1
                                    else:
                                        nameLine = getTextSurface(nameText,textColor,size-3)
                                        toWrite.append(nameLine)
                                        col = 0
                    else:
                        nLine = getTextSurface(" UNOCCUPIED",textColor,size-2)
                        toWrite.append(nLine)
                ## TODO consider other special readouts / BUILD readout main
                if isinstance(thisObject,o.IndustryBuilding) and thisObject.robots == False:
                    if thisObject.industry.supplied == False:
                        nLine = getTextSurface("UNSUPPLIED!",textColor,size)
                        toWrite.append(nLine)
                if thisObject.readout > 0:
                    if isinstance(thisObject,o.ExtractionBuilding) or isinstance(thisObject,o.RecycleBuilding)\
                         or isinstance(thisObject,o.LifeSupportBuilding):
                        oLine = getTextSurface(thisObject.readoutTag + ":",textColor,size)
                        toWrite.append(oLine)
                        o2Line = thisObject.getReadoutSurface(size)
                        toWrite.append(o2Line)
                    else:
                        oLine = getTextSurface(thisObject.readoutTag + ":{0:.3f}".format(thisObject.readout),textColor,size)
                        toWrite.append(oLine)

        if isinstance(thisObject,p.People):
            nameLine = getTextSurface(thisObject.name,textColor,size+3)
            toWrite.append(nameLine)
            #age
            ageEY = thisObject.age / 350
            locLine = getTextSurface("age: {0:.1f}".format(ageEY),textColor,size)
            toWrite.append(locLine)
            #job (denote child)
            if thisObject.age > p.People.workingAge:
                if thisObject.job != None:
                    jobLine = getTextSurface("job: " + thisObject.job.tag,textColor,size)
                    toWrite.append(jobLine)
                    if thisObject.job.building != None:
                        jobBLine = getTextSurface("  @" + thisObject.job.building.buildingName,\
                            thisObject.job.building.color,size)
                        toWrite.append(jobBLine)
                    prodLine = getTextSurface("productivity: {0:.2f}".format(thisObject.job.productivity),textColor,size-3)
                    toWrite.append(prodLine)
                else:
                    jobLine = getTextSurface("UNEMPLOYED",textColor,size)
                    toWrite.append(jobLine)
            else:
                jobLine = getTextSurface("CHILD",textColor,size)
                toWrite.append(jobLine)
            healthLine = getTextSurface("health:{0:.3f}".format(thisObject.health),c.green,size)
            toWrite.append(healthLine)
            skillLine = getTextSurface("skill:{0:.3f}".format(thisObject.skill),c.red,size)
            toWrite.append(skillLine)
            psychLine = getTextSurface("psych:{0:.3f}".format(thisObject.psych),c.aqua,size)
            toWrite.append(psychLine)
            if thisObject.native:
                nLine = getTextSurface("NATIVE",textColor,size)
                toWrite.append(nLine)

        if isinstance(thisObject,o.Tile):
            locLine = getTextSurface("x:"+str(thisObject.x)+" y:"+str(thisObject.y),textColor,size)
            toWrite.append(locLine)
            if len(thisObject.tileBuildings) > 0:
                for b in thisObject.tileBuildings:
                    bTag = getTextSurface(b.buildingName,textColor,size)
                    toWrite.append(bTag)

            if thisObject.explored == False:
                exploreTag = getTextSurface("UNEXPLORED",textColor,size)
                toWrite.append(exploreTag)
                if thisObject.exploreProgress > 0:
                    exploreProgress = getTextSurface("{0:.1f}/100".format(thisObject.exploreProgress),textColor,size)
                    toWrite.append(exploreProgress)

            else:
                exploreTag = getTextSurface("RESOURCES:",textColor,size)
                toWrite.append(exploreTag)
                regolithTag = getTextSurface("reg:{0:.2f}".format(thisObject.regolith),c.boldRed,size)
                toWrite.append(regolithTag)
                oreTag = getTextSurface("ore:{0:.2f}".format(thisObject.ore),c.red,size)
                toWrite.append(oreTag)
                if thisObject.water > 0:
                    waterTag = getTextSurface("ice:{0:.2f}".format(thisObject.water),c.blue,size)
                    toWrite.append(waterTag)
                if thisObject.rare > 0:
                    rareTag = getTextSurface("r:{0:.2f}".format(thisObject.rare),c.pink,size)
                    toWrite.append(rareTag)

        maxWidth = 0
        height = 2*gap
        for line in toWrite:
            height += line.get_height()
            if line.get_width() > maxWidth:
                maxWidth = line.get_width()
        width = maxWidth + 4*gap
        panel = getOutlinePanel(height,width,color,borderColor)
        panel = blitFromSurfaceList(panel,toWrite,(gap*2,gap),True)
        
        self.surface = panel


    def draw(self,canvas,loc,final = False,absoluteLoc = False,sol=-1):
        if self.delay > 0:
            self.delay -= 1
        if sol > self.lastRefresh:
            self.lastRefresh = sol
            self.createSurface(self.object)
        if self.alpha < 255:
            self.alpha += 15
            self.surface.set_alpha(self.alpha)
        if absoluteLoc:
            canvas.blit(self.surface,(loc))
            self.lastDraw = loc
        else:
            xLoc = loc[0] - int(self.surface.get_width()/3)
            if xLoc+self.surface.get_width() > canvas.get_width():
                xLoc = loc[0] - int(self.surface.get_width())
            yLoc = loc[1]-self.surface.get_height()-12
            if yLoc < 0:
                yLoc = loc[1]+12
            canvas.blit(self.surface,(xLoc,yLoc))
            self.lastDraw = (xLoc,yLoc)
        if final:
            animation = Animation([self.surface],(self.lastDraw),fadeOut = True,alphaVelocity=-30)
            return animation
        else:
            return None

class ControlPanel:
    def __init__(self,canvas,anchorLoc,buttonList,backImg = None):
        self.canvas = canvas
        self.anchor = anchorLoc
        if backImg == None:
            self.width = 80
            self.height = 540
            self.backPanel = pygame.Surface((self.width, self.height))
            self.backPanel.fill(c.grey)
            self.backPanel.set_alpha(100)
        else:
            self.backPanel = backImg
            self.width = backImg.get_width()
            self.height = backImg.get_height()
        if self.height > self.width:
            self.vert = True
        else:
            self.vert = False
        self.buttonList = buttonList
        self.gap = 8
        self.buttonRects = []

    def updateImg(self,newImg):
        #must be same size
        self.backPanel = newImg

    def drawPanel(self,mouseLoc):
        self.canvas.blit(self.backPanel,self.anchor)
        self.buttonRects = []
        buttonX = self.anchor[0] + self.gap
        buttonY = self.anchor[1] + self.gap
        for button in self.buttonList:
            rect = button.draw(self.canvas,(buttonX,buttonY),mouseLoc)
            self.buttonRects.append(rect)
            if self.vert:
                buttonY += rect.height + self.gap
            else:
                buttonX += rect.width + self.gap

class Announcements:
    announcements = []
    def __init__(self):
        self.allAnimations = []
        self.anchorLoc = (82,62)
        self.textGap = 15

    def addAnnouncement(self,announceText):
        textSurface = getTextSurface(announceText,c.highlightYellow)
        textPlate = pygame.Surface((textSurface.get_width(),self.textGap))
        textPlate.fill(c.trans)
        textPlate.blit(textSurface,(0,0))
        textPlate.set_colorkey(c.trans)
        if len(self.allAnimations) > 0:
            y = self.allAnimations[len(self.allAnimations) -1].loc[1]+self.textGap
        else:
            y = self.anchorLoc[1]
        loc = (self.anchorLoc[0],y)
        animationObject = Animation([textPlate],loc,fadeOut=True)
        self.allAnimations.append(animationObject)

    def run(self,canvas):
        toRemove = []
        yAnchor = self.anchorLoc[1]
        for a in self.allAnimations:
            a.runAnimation()
            a.draw(canvas)
            if a.loc[1] > yAnchor:
                a.loc = (a.loc[0],a.loc[1]-1)
            if a.on == False:
                toRemove.append(a)
            yAnchor += self.textGap
        if len(toRemove)>0:
            for each in toRemove:
                self.allAnimations.remove(each)

# class owner constructs and calls draw function
class Animation:
    def __init__(self,surfaceSequence,startLoc,\
        xLimit = 800,yLimit = 600, xVelocity = 0, yVelocity = 0,fadeOut = False,\
            alphaVelocity = -1,triggerObject = None):
        self.surfaceSequence = surfaceSequence
        self.frame = 0
        self.frameLimit = len(surfaceSequence) - 1
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.loc = startLoc
        self.xLimit = xLimit
        self.yLimit = yLimit
        self.startAlpha = 255
        if fadeOut:
            self.alphaVelocity = alphaVelocity
        else:
            self.alphaVelocity = 0
        self.on = True
        self.triggerObject = triggerObject

    def draw(self,canvas):
        if isinstance(self.surfaceSequence[self.frame],GlowTag):
            canvas.blit(self.surfaceSequence[self.frame].get(),self.loc)
        else:
            canvas.blit(self.surfaceSequence[self.frame],self.loc)

    def runAnimation(self):
        if self.frame + 1 <= self.frameLimit:
            self.frame += 1
        else:
            self.frame = 0
        self.loc = (self.loc[0]+self.xVelocity,self.loc[1]+self.yVelocity)
        if self.xVelocity != 0:
            if self.xVelocity > 0 and (self.loc[0] > self.xLimit):
                self.on = False
            if self.xVelocity < 0 and (self.loc[0] < self.xLimit):
                self.on = False
        if self.yVelocity != 0:
            if self.yVelocity > 0 and (self.loc[1] > self.yLimit):
                self.on = False
            if self.yVelocity < 0 and (self.loc[1] < self.yLimit):
                self.on = False
        if self.alphaVelocity != 0:
            self.startAlpha += self.alphaVelocity
            for img in self.surfaceSequence:
                img.set_alpha(self.startAlpha)
            if self.startAlpha <= 0:
                self.on = False
        
#build production panels out here, selectiosn saved between calls
airButton = Button("AIR")
airButton.dataEmbed = "AIR"
waterButton = Button("WATER")
waterButton.dataEmbed = "WATER"
foodButton = Button("FOOD")
foodButton.dataEmbed = "FOOD"
organicsButton = Button("ORGANICS")
organicsButton.dataEmbed = "ORGANICS"
regolithButton = Button("REGOLITH")
regolithButton.dataEmbed = "REGOLITH"
oreButton = Button("ORE")
oreButton.dataEmbed = "ORE"
rareButton = Button("RARE")
rareButton.dataEmbed = "RARE"
chartButtons1 = [foodButton,waterButton,airButton,organicsButton,regolithButton,oreButton,rareButton]

powerButton = Button("POWER")
powerButton.dataEmbed = "POWER"
powerButton.selected = True
concreteButton = Button("CONCRETE")
concreteButton.dataEmbed = "CONCRETE"
metalButton = Button("METAL")
metalButton.dataEmbed = "METAL"
fuelButton = Button("FUEL")
fuelButton.dataEmbed = "FUEL"
medsButton = Button("MEDS")
medsButton.dataEmbed = "MEDS"
electronicsButton = Button("ELECTRONICS")
electronicsButton.dataEmbed = "ELECTRONICS"
plasticsButton = Button("PLASTICS")
plasticsButton.dataEmbed = "PLASTICS"
chartButtons2 = [powerButton,concreteButton,metalButton,fuelButton,medsButton,electronicsButton,plasticsButton]

airCButton = Button("AIR")
airCButton.dataEmbed = "AIRC"
waterCButton = Button("WATER")
waterCButton.dataEmbed = "WATERC"
foodCButton = Button("FOOD")
foodCButton.dataEmbed = "FOODC"
organicsCButton = Button("ORGANICS")
organicsCButton.dataEmbed = "ORGANICSC"
regolithCButton = Button("REGOLITH")
regolithCButton.dataEmbed = "REGOLITHC"
oreCButton = Button("ORE")
oreCButton.dataEmbed = "OREC"
rareCButton = Button("RARE")
rareCButton.dataEmbed = "RAREC"
chartButtons3 = [foodCButton,waterCButton,airCButton,organicsCButton,regolithCButton,oreCButton,rareCButton]

powerCButton = Button("POWER")
powerCButton.dataEmbed = "POWERC"
powerCButton.selected = True
concreteCButton = Button("CONCRETE")
concreteCButton.dataEmbed = "CONCRETEC"
metalCButton = Button("METAL")
metalCButton.dataEmbed = "METALC"
fuelCButton = Button("FUEL")
fuelCButton.dataEmbed = "FUELC"
medsCButton = Button("MEDS")
medsCButton.dataEmbed = "MEDSC"
electronicsCButton = Button("ELECTRONICS")
electronicsCButton.dataEmbed = "ELECTRONICSC"
plasticsCButton = Button("PLASTICS")
plasticsCButton.dataEmbed = "PLASTICSC"
chartButtons4 = [powerCButton,concreteCButton,metalCButton,fuelCButton,medsCButton,electronicsCButton,plasticsCButton]

ageButton = Button("AGE")
ageButton.dataEmbed = "Age"
healthButton = Button("HEALTH")
healthButton.dataEmbed = "Health"
skillButton = Button("SKILL")
skillButton.dataEmbed = "Skill"
psychButton = Button("PSYCH")
psychButton.dataEmbed = "Psych"
prodButton = Button("WORK")
prodButton.dataEmbed = "Prod"

ageButton2 = Button("AGE")
ageButton2.dataEmbed = "Age"
healthButton2 = Button("HEALTH")
healthButton2.dataEmbed = "Health"
skillButton2 = Button("SKILL")
skillButton2.dataEmbed = "Skill"
psychButton2 = Button("PSYCH")
psychButton2.dataEmbed = "Psych"
prodButton2 = Button("WORK")
prodButton2.dataEmbed = "Prod"

xButtons = [ageButton,healthButton,skillButton,psychButton,prodButton]
yButtons = [ageButton2,healthButton2,skillButton2,psychButton2,prodButton2]

