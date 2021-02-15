import pygame

w = 800
h = 600
top = (0,0)
size = width, height = w, h
center = (w/2,h/2)
pygame.init()
screen = pygame.display.set_mode(size)#,pygame.FULLSCREEN )
title = "MARS GAME"
pygame.display.set_caption(title)
pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()

import mapTileBuilding as o
import assets as a
import draw as d
import space as s
import color as c
import people as p
import pickle

closeButton = d.Button("CLOSE",)
toggleButton = d.Button("TOGGLE",)

yBack = d.getHorizontalBar(screen.get_width(),40)
yBack.set_alpha(0)

productionChartPanel1 = d.ControlPanel(screen,(0,screen.get_height()-70),d.chartButtons1,\
        d.getHorizontalBar(screen.get_width(),80))
productionChartPanel2 = d.ControlPanel(screen,(0,screen.get_height()-44),d.chartButtons2,yBack)

consumptionChartPanel1 = d.ControlPanel(screen,(0,screen.get_height()-70),d.chartButtons3,\
        d.getHorizontalBar(screen.get_width(),80))
consumptionChartPanel2 = d.ControlPanel(screen,(0,screen.get_height()-44),d.chartButtons4,yBack)

adminPanels = [d.ManageBuilders("MANAGE BUILDERS"),d.PrioritizeIndustries("PRIORITIZE INDUSTRIES"),d.OptimizeJobs("OPTIMIZE JOBS"),\
    d.Holiday("DECLARE HOLIDAY"),d.Arts("THE ARTS"),d.Security("SECURITY"),\
        d.AdminPanel("OPEN PORT"),d.Economy("MARKET CONTROL"),d.AdminPanel("CHILDREN")]

sciencePanels = [d.SciencePanel("MEDICAL",True),d.SciencePanel("MARS",True),d.SciencePanel("ELECTRICAL",True),\
    d.SciencePanel("ORGANIC",True),d.MaterialPanel("MATERIALS",True),d.SciencePanel("NEURO",True),d.SciencePanel("CONSERVATION",True),\
        d.SciencePanel("GEOLOGY",True),d.SciencePanel("INDUSTRIAL",True),d.SciencePanel("EDUCATION",True),\
            d.SciencePanel("ROCKETRY",True),d.SciencePanel("INFO-TECH",True),d.SciencePanel("SCIENTIFIC",True)]

builderPlusButton = d.Button("BULDER +")
builderMinusButton = d.Button("BUILDER -")
explorerPlusButton = d.Button("EXPLORER +")
explorerMinusButton = d.Button("EXPLORER -")
artistPlusButton = d.Button("ARTIST +")
artistMinusButton = d.Button("ARTIST -")
securityPlusButton = d.Button("SECURITY +")
securityMinusButton = d.Button("SECURITY -")
fireButton = d.Button("FIRE")
managePeopleButtons = [builderPlusButton,builderMinusButton,explorerPlusButton,\
    explorerMinusButton,fireButton]

managePeoplePanel = d.ControlPanel(screen,(0,screen.get_height()-40),managePeopleButtons,\
        d.getHorizontalBar(screen.get_width(),40))

xPeoplePanel = d.ControlPanel(screen,(400,screen.get_height()-40),d.xButtons,yBack)
yPeoplePanel = d.ControlPanel(screen,(0,screen.get_height()-40),d.yButtons,\
    d.getHorizontalBar(screen.get_width(),40))


def saveGame(myBase):
    myBase.announcements.allAnimations = []
    for launch in space.launches:
       myBase.savedLaunchLists.append(launch.getSaveList())
    savedgame = open("savedgame", "wb")
    #TODO make save and load functions for myBaseObject NO SURFACES
    pickle.dump(myBase,savedgame)
    savedgame.close()
    d.messagePopUp(screen,(10,screen.get_height()-70),["Game saved successfully.",myBase.name+" sol:"+str(myBase.sol)])

def clearButtonSelections(buttonList):
    for button in buttonList:
        if button.selected:
            button.toggleSelected()

def genericButtonHandler(panel,click):
    index = 0
    action = False
    for rect in panel.buttonRects:
        if rect.collidepoint(click):
            if panel.buttonList[index].live:
                if panel.buttonList[index].selected:
                    action = True  
                    clearButtonSelections(panel.buttonList) 
                else:
                    action = True  
                    clearButtonSelections(panel.buttonList)
                    panel.buttonList[index].toggleSelected()
        index += 1
    return action

def multipleSelectionButtonHandler(panel,click):
    index = 0
    for rect in panel.buttonRects:
        if rect.collidepoint(click) and panel.buttonList[index].live:
            panel.buttonList[index].toggleSelected()
        index += 1

def introAnimation():
    blackBack = pygame.Surface((screen.get_width(),screen.get_height()))
    midX = int(screen.get_width()/2)
    midY = int(screen.get_height()/2)
    titleTag = "MARS GAME"
    active = True
    size = 1
    while active:
        screen.blit(blackBack,(0,0))
        nameSurface = d.getTextSurface(titleTag,c.boldRed,size)
        screen.blit(nameSurface,(midX-int(nameSurface.get_width()/2),midY-nameSurface.get_height()))
        size+=1
        pygame.display.flip()
        if nameSurface.get_width()>screen.get_width():
            active = False

def getBaseName():
    blackBack = pygame.Surface((screen.get_width(),screen.get_height()))
    midX = int(screen.get_width()/2)
    midY = int(screen.get_height()/2)
    okayButton = d.Button("OKAY")
    okayButton.makeDead()
    namePrompt=d.getTextSurface("Enter a name for you new MARS BASE:")
    menuOn = True
    baseName = ""
    while menuOn:
        mouseLoc = pygame.mouse.get_pos()
        screen.blit(blackBack,(0,0))
        if okayButton.live == False and len(baseName)>0:
            okayButton.makeLive()
        if okayButton.live and len(baseName)==0:
            okayButton.makeDead()

        okayRect = okayButton.draw(screen,(midX-int(okayButton.buttonSurface.get_width()/2),midY+5),mouseLoc)
        nameSurface = d.getTextSurface("["+baseName+"]",size=36)
        screen.blit(namePrompt,(midX-int(namePrompt.get_width()/2),midY-namePrompt.get_height()-nameSurface.get_height()))
        screen.blit(nameSurface,(midX-int(nameSurface.get_width()/2),midY-nameSurface.get_height()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    baseName = baseName[:-1]
                elif event.key == pygame.K_RETURN:
                    confirmedBaseName = baseName
                    approve = d.choicePopUp(screen,(midX,midY),["Name your base",confirmedBaseName + "?"])
                    if approve:
                        menuOn = False
                else:
                    baseName += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if okayRect.collidepoint(click):
                    confirmedBaseName = baseName
                    approve = d.choicePopUp(screen,click,["Name your base",confirmedBaseName + "?"])
                    if approve:
                        menuOn = False
        if menuOn == False:
            screen.blit(blackBack,(0,0))
            loading = d.getTextSurface("LOADING",c.boldRed,24)
            screen.blit(loading,(midX-int(loading.get_width()/2),midY-loading.get_height()))
        pygame.display.flip()


    return confirmedBaseName

def setUpLaunches(builder):
    gap = 35
    maxPoints = 1000
    policyUnlocks = 2
    rocketSources = [a.whiteRocket,a.whiteRocket,a.whiteRocket,a.aquaRocket,a.blueRocket,\
        a.greenRocket,a.greyRocket,a.greyRocket,a.greyRocket,a.aquaRocket,a.hYellowRocket,\
            a.redRocket,a.purpleRocket,a.purpleRocket]
    blackBack = pygame.Surface((screen.get_width(),screen.get_height()))
    midX = int(screen.get_width()/2)
    midY = int(screen.get_height()/2)
    okayButton = d.Button("CONFIRM")
    okayButton.makeDead()
    prompt=d.getTextSurface("Select which ships to launch for your initial landing:")
    adminTag=d.getTextSurface("Available ADMINISTRATION balance on landing:")
    pointsTag = d.getTextSurface(str(maxPoints),c.pink)
    unlockTag=d.getTextSurface("POLICY UNLOCKS on landing:")
    unlockCountTag = d.getTextSurface(str(policyUnlocks),c.pink)
    menuOn = True
    bottomAnchor = screen.get_height() - 2*gap
    startCapsules = []
    rocketMatches = []
    removeButtons = []
    removeRects = []
    allButtons = builder.earthPanel1.buttonList + builder.earthPanel2.buttonList
    while menuOn:
        mouseLoc = pygame.mouse.get_pos()
        screen.blit(blackBack,(0,0))
        if okayButton.live == False and len(startCapsules)>2:
            okayButton.makeLive()
        if okayButton.live and len(startCapsules)<3:
            okayButton.makeDead()

        screen.blit(prompt,(gap,2*gap-prompt.get_height()))
        builder.earthPanel1.drawPanel(mouseLoc)
        builder.earthPanel2.drawPanel(mouseLoc)

        screen.blit(adminTag,(screen.get_width()-4*gap-adminTag.get_width(),int(screen.get_width()/4)+gap))
        screen.blit(pointsTag,(screen.get_width()-4*gap,int(screen.get_width()/4)+gap))
        screen.blit(unlockTag,(screen.get_width()-4*gap-unlockTag.get_width(),int(screen.get_width()/4)+gap+pointsTag.get_height()))
        screen.blit(unlockCountTag,(screen.get_width()-4*gap,int(screen.get_width()/4)+gap+pointsTag.get_height()))

        i = 0
        for button in allButtons:
            if button.selected:
                startCapsules.append(button.dataEmbed)
                newButton = d.Button("REMOVE")
                newButton.mouseOverInfo = True
                newButton.makeMouseOver(button.dataEmbed[0])
                removeButtons.append(newButton)
                rocketMatches.append(rocketSources[i])
                button.toggleSelected()
                maxPoints = 1000 - len(startCapsules)*100
                if len(startCapsules) < 6:
                    policyUnlocks = 2
                else:
                    if len(startCapsules) < 8:
                        policyUnlocks = 1
                    else:
                        policyUnlocks = 0
                unlockCountTag = d.getTextSurface(str(policyUnlocks),c.pink)
                pointsTag = d.getTextSurface(str(maxPoints),c.pink)
            i+=1

        if len(startCapsules)>=10:
            for button in allButtons:
                button.makeDead()

        okayRect = okayButton.draw(screen,(screen.get_width()-4*gap-okayButton.buttonSurface.get_width(),\
            int(screen.get_width()/4)+gap-okayButton.buttonSurface.get_height()-5),mouseLoc)
        
        i=0
        removeRects = []
        removeIndex = -1
        xLoc = gap
        for capsule in startCapsules:
            screen.blit(rocketMatches[i],(xLoc,bottomAnchor-rocketMatches[i].get_height()))
            removeRect = removeButtons[i].draw(screen,(xLoc,bottomAnchor),mouseLoc)
            removeRects.append(removeRect)
            if removeButtons[i].selected:
                removeIndex = i
                removeButtons[i].toggleSelected()
            xLoc+=gap/5 + rocketMatches[i].get_width()
            i+=1

        if removeIndex >= 0:
            startCapsules.remove(startCapsules[removeIndex])
            rocketMatches.remove(rocketMatches[removeIndex])
            removeButtons.remove(removeButtons[removeIndex])
            removeRects.remove(removeRects[removeIndex])
            maxPoints = 1000 - len(startCapsules)*100
            if len(startCapsules) < 6:
                    policyUnlocks = 2
            else:
                if len(startCapsules) < 8:
                    policyUnlocks = 1
                else:
                    policyUnlocks = 0
            unlockCountTag = d.getTextSurface(str(policyUnlocks),c.pink)
            pointsTag = d.getTextSurface(str(maxPoints),c.pink)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if okayRect.collidepoint(click):
                    confirmedBaseName = baseName
                    approve = d.choicePopUp(screen,click,["Commence Mars mission",\
                        "with " +str(len(startCapsules))+ " initial launches ?"])
                    if approve:
                        menuOn = False
                rI = 0
                for rect in removeRects:
                    if rect.collidepoint(click):
                        removeButtons[rI].toggleSelected()
                    rI+=1 

                genericButtonHandler(builder.earthPanel1,click)
                genericButtonHandler(builder.earthPanel2,click)

        if menuOn == False:
            screen.blit(blackBack,(0,0))
            loading = d.getTextSurface("LOADING",c.boldRed,24)
            screen.blit(loading,(midX-int(loading.get_width()/2),midY-loading.get_height()))
        pygame.display.flip()
    
    launchAnimate = True
    rocketLocY = []
    for capsule in startCapsules:
        rocketLocY.append(bottomAnchor-rocketMatches[0].get_height())

    while launchAnimate == True:
        screen.blit(blackBack,(0,0))
        i=0
        xLoc = gap
        for capsule in startCapsules:
            screen.blit(rocketMatches[i],(xLoc,rocketLocY[i]))
            if i == 0:
                rocketLocY[i] -= 1
            else:
                if rocketLocY[i] - rocketLocY[i-1] > 15:
                    rocketLocY[i] -= 1
            xLoc+=gap/5 + rocketMatches[i].get_width()
            i+=1
        if rocketLocY[-1]+rocketMatches[0].get_height()<0:
            launchAnimate = False
        pygame.display.flip()

    return startCapsules

def robotManager(pauseScreen):
    closeButton.selected = False
    gap = 8
    bar = d.getHorizontalBar(screen.get_width(),40)
    pauseScreen.blit(bar,(0,4))
    menuOn = True

    robotPanel = d.JobPanel(screen,[],c.white,"ROBOTS",myBase.robots,True)    
    buildButton = d.Button("BUILD ROBOT")
    buttonLoc = (int(screen.get_width()/4.0),int(screen.get_height()/3.0))

    robotPop = len(myBase.robots)

    buildOrders = 0
    for item in myBase.buildList:
        if isinstance(item,o.RobotDummy):
            buildOrders += 1

    robotCapacity = 0
    for building in myBase.industryList:
        if building.robots:
            for item in building.robotsList:
                if isinstance(item,o.RobotDummy):
                    buildOrders += 1
            robotCapacity += building.robotsStorage

    if (buildOrders+robotPop) >= robotCapacity:
        buildButton.makeDead()


    while menuOn:
        screen.blit(pauseScreen,top)
        mouseLoc = pygame.mouse.get_pos()

        buildRect = buildButton.draw(screen,buttonLoc,mouseLoc)

        robotPanel.draw(buttonLoc[1]+buildButton.buttonSurface.get_height()+gap,customX = buttonLoc[0])
        robotPanel.checkMouseOver(mouseLoc)

        closeRect = closeButton.draw(screen,(gap,gap),mouseLoc)

        if buildButton.selected:
            approve = d.choicePopUp(screen, mouseLoc,["Initiate ROBOT PROJECT?"]) #TODO add cost to choice
            if approve:
                buildSite = None
                for building in myBase.industryList:
                    if building.robots:
                        if len(building.robotsList) < building.robotsStorage:
                            buildSite = building
                newProject = o.RobotDummy(myBase.sol,myBase,buildSite.tile,buildSite.udlr,'S',buildSite)
                buildSite.robotsList.append(newProject)
                freeQueue = True
                for item in buildSite.robotsList:
                    if isinstance(item,o.RobotDummy) and item != newProject:
                        freeQueue = False
                if freeQueue:
                    newProject.startBuild()
                buildOrders += 1
            buildButton.toggleSelected()
            if (buildOrders+robotPop) >= robotCapacity:
                buildButton.makeDead()


        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(gap,gap),mouseLoc)
                    menuOn = False
                if buildRect.collidepoint(click):
                    buildButton.toggleSelected()
                    
        pygame.display.flip()

def scienceManager(pauseScreen):
    closeButton.selected = False
    gap = 8
    bar = d.getHorizontalBar(screen.get_width(),40)
    pauseScreen.blit(bar,(0,4))
    menuOn = True
    unlockBalanceTag = d.GlowTag("SCIENCE UNLOCKS AVAILABLE: " + str(myBase.scienceLevelBalance),size=24)
    scienceBalanceTag = d.GlowTag("SCIENCE BALANCE: {0:.1f}".format(myBase.sciencePointsBalance),size=15)
    scienceCostTag = d.GlowTag("SCIENCE COST: {0:.1f}".format(myBase.eventCost*myBase.scienceCostFactor),size=15)
    isClicked = False
    for panel in sciencePanels:
        panel.update(myBase)

    costButton = d.Button("PURE RESEARCH")
    if myBase.scienceLevelBalance < 1:
        costButton.makeDead()
    costTag = d.getTextSurface("Use a SCIENCE UNLOCK to decrease COSTS for SCIENCE events.")

    while menuOn:
        closeButton.selected = False
        screen.blit(pauseScreen,top)
        mouseLoc = pygame.mouse.get_pos()

        xLoc = gap
        yLoc = 68
        panelLoc = (xLoc,yLoc)
        index = 0
        for panel in sciencePanels:
            panel.draw(screen,panelLoc,mouseLoc,myBase)
            xLoc += panel.overlay.get_width() + gap
            if index !=3:
                if xLoc > 4*panel.overlay.get_width():
                    xLoc = gap
                    yLoc += sciencePanels[0].overlay.get_height()+2*gap
            panelLoc = (xLoc,yLoc)
            if panel.clicked:
                unlockBalanceTag = d.GlowTag("SCIENCE UNLOCKS AVAILABLE: " + str(myBase.scienceLevelBalance),size=24)
                scienceBalanceTag = d.GlowTag("SCIENCE BALANCE: {0:.1f}".format(myBase.sciencePointsBalance),size=15)
                scienceCostTag = d.GlowTag("SCIENCE COST: {0:.1f}".format(myBase.eventCost*myBase.scienceCostFactor),size=15)
                panel.clicked = False
            index+=1

        for panel in sciencePanels:
            if panel.overlayButton.selected:
                if panel.locked and myBase.scienceLevelBalance > 0:
                    approve = d.choicePopUp(screen,mouseLoc,["Unlock " + panel.tag + " panel?"])
                    if approve:
                        myBase.scienceLevelBalance -= 1
                        unlockBalanceTag = d.GlowTag("SCIENCE UNLOCKS AVAILABLE: " + str(myBase.scienceLevelBalance),size=24)
                        scienceBalanceTag = d.GlowTag("SCIENCE BALANCE: {0:.1f}".format(myBase.sciencePointsBalance),size=15)
                        scienceCostTag = d.GlowTag("SCIENCE COST: {0:.1f}".format(myBase.eventCost*myBase.scienceCostFactor),size=15)
                        panel.locked = False
                else:
                    d.messagePopUp(screen,mouseLoc,["Must level-up SCIENCE","to unlock research."])
                panel.overlayButton.toggleSelected()

        if myBase.scienceLevelBalance < 1:
            costButton.makeDead()
        panelLoc = (panelLoc[0],panelLoc[1]-10)
        costRect = costButton.draw(screen,panelLoc,mouseLoc)
        screen.blit(costTag,(panelLoc[0]+costButton.buttonSurface.get_width()+gap,panelLoc[1]+8))

        screen.blit(unlockBalanceTag.get(),(2*gap + closeButton.buttonSurface.get_width(),\
            gap + closeButton.buttonSurface.get_height()-unlockBalanceTag.get_height()))
        screen.blit(scienceBalanceTag.get(),(screen.get_width() - gap - scienceBalanceTag.get_width(),\
            gap + closeButton.buttonSurface.get_height()-scienceBalanceTag.get_height()))
        screen.blit(scienceCostTag.get(),(screen.get_width() - gap - scienceCostTag.get_width(),\
            gap + closeButton.buttonSurface.get_height()-scienceBalanceTag.get_height()\
                -scienceCostTag.get_height()))

        closeRect = closeButton.draw(screen,(gap,gap),mouseLoc)

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(gap,gap),mouseLoc)
                    menuOn = False
                if costRect.collidepoint(click):
                    costButton.toggleSelected()
                    costRect = costButton.draw(screen,panelLoc,mouseLoc)
                    approve = d.choicePopUp(screen,mouseLoc,["Conduct efficiency research?","Will lower event costs 25%"])
                    if approve:
                        myBase.scienceLevelBalance -= 1
                        myBase.eventCost*=0.75
                        unlockBalanceTag = d.GlowTag("SCIENCE UNLOCKS AVAILABLE: " + str(myBase.scienceLevelBalance),size=24)
                        scienceBalanceTag = d.GlowTag("SCIENCE BALANCE: {0:.1f}".format(myBase.sciencePointsBalance),size=15)
                        scienceCostTag = d.GlowTag("SCIENCE COST: {0:.1f}".format(myBase.eventCost*myBase.scienceCostFactor),size=15)
                for panel in sciencePanels:
                    isClicked = panel.checkClick(click)
                    
        pygame.display.flip()
    i = 0
    print(len(myBase.scienceUnlocked))
    print(myBase.scienceUnlocked)
    for panel in sciencePanels:
        print(i)
        print(panel.key)
        if panel.locked == False:
            myBase.scienceUnlocked[i] = True
        i += 1


def adminManager(pauseScreen):
    closeButton.selected = False
    gap = 12
    bar = d.getHorizontalBar(screen.get_width(),40)
    pauseScreen.blit(bar,(0,4))
    menuOn = True
    unlockBalanceTag = d.GlowTag("POLICY UNLOCKS AVAILABLE: " + str(myBase.adminLevelBalance),size=24)
    adminBalanceTag = d.GlowTag("ADMIN BALANCE: {0:.1f}".format(myBase.adminPointsBalance),size=15)
    adminCostTag = d.GlowTag("ADMIN COST: {0:.1f}".format(myBase.eventCost*myBase.adminCostFactor),size=15)
    isClicked = False

    costButton = d.Button("REORGANIZE")
    if myBase.adminLevelBalance < 1:
        costButton.makeDead()
    costTag = d.getTextSurface("Use a POLICY UNLOCK to decrease COSTS for ADMIN events.")

    while menuOn:
        screen.blit(pauseScreen,top)
        mouseLoc = pygame.mouse.get_pos()

        xLoc = gap
        yLoc = 68
        panelLoc = (xLoc,yLoc)
        for panel in adminPanels:
            panel.draw(screen,panelLoc,mouseLoc,myBase)
            xLoc += panel.overlay.get_width() + gap
            if xLoc > 3*panel.overlay.get_width():
                xLoc = gap
                yLoc += panel.overlay.get_height()+2*gap
            panelLoc = (xLoc,yLoc)
            if panel.clicked:
                unlockBalanceTag = d.GlowTag("POLICY UNLOCKS AVAILABLE: " + str(myBase.adminLevelBalance),size=24)
                adminBalanceTag = d.GlowTag("ADMIN BALANCE: {0:.1f}".format(myBase.adminPointsBalance),size=15)
                adminCostTag = d.GlowTag("ADMIN COST: {0:.1f}".format(myBase.eventCost*myBase.adminCostFactor),size=15)
                panel.clicked = False

        if myBase.adminLevelBalance < 1:
            costButton.makeDead() 
        panelLoc = (panelLoc[0],panelLoc[1]-20)
        costRect = costButton.draw(screen,panelLoc,mouseLoc)
        screen.blit(costTag,(panelLoc[0]+costButton.buttonSurface.get_width()+gap,panelLoc[1]+gap))

        screen.blit(unlockBalanceTag.get(),(2*gap + closeButton.buttonSurface.get_width(),\
            gap + closeButton.buttonSurface.get_height()-unlockBalanceTag.get_height()))
        screen.blit(adminBalanceTag.get(),(screen.get_width() - gap - adminBalanceTag.get_width(),\
            gap + closeButton.buttonSurface.get_height()-adminBalanceTag.get_height()))
        screen.blit(adminCostTag.get(),(screen.get_width() - gap - adminCostTag.get_width(),\
            gap + closeButton.buttonSurface.get_height()-adminBalanceTag.get_height()\
                -adminCostTag.get_height()))
        closeRect = closeButton.draw(screen,(gap,gap),mouseLoc)

        for panel in adminPanels:
            if panel.overlayButton.selected:
                if panel.locked and myBase.adminLevelBalance > 0:
                    approve = d.choicePopUp(screen,mouseLoc,["Unlock " + panel.tag + " policy panel?"])
                    if approve:
                        myBase.adminLevelBalance -= 1
                        unlockBalanceTag = d.GlowTag("POLICY UNLOCKS AVAILABLE: " + str(myBase.adminLevelBalance),size=24)
                        adminBalanceTag = d.GlowTag("ADMIN BALANCE: {0:.1f}".format(myBase.adminPointsBalance),size=15)
                        adminCostTag = d.GlowTag("ADMIN COST: {0:.1f}".format(myBase.eventCost*myBase.adminCostFactor),size=15)
                        panel.locked = False
                        if isinstance(panel,d.Arts):
                            myBase.arts = True
                        if isinstance(panel,d.Security):
                            myBase.security = True
                else:
                    d.messagePopUp(screen,mouseLoc,["Must level-up ADMIN","to unlock policy."])
                panel.overlayButton.toggleSelected()

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(gap,gap),mouseLoc)
                    menuOn = False
                if costRect.collidepoint(click):
                    costButton.toggleSelected()
                    costRect = costButton.draw(screen,panelLoc,mouseLoc)
                    approve = d.choicePopUp(screen,mouseLoc,["Reorganize administration?","Will lower event costs 25%"])
                    if approve:
                        myBase.adminLevelBalance -= 1
                        myBase.eventCost*=0.75
                        unlockBalanceTag = d.GlowTag("POLICY UNLOCKS AVAILABLE: " + str(myBase.adminLevelBalance),size=24)
                        adminBalanceTag = d.GlowTag("ADMIN BALANCE: {0:.1f}".format(myBase.adminPointsBalance),size=15)
                        adminCostTag = d.GlowTag("ADMIN COST: {0:.1f}".format(myBase.eventCost*myBase.adminCostFactor),size=15)
                for panel in adminPanels:
                    isClicked = panel.checkClick(click)
                    
        pygame.display.flip()
    index = 0
    for panel in adminPanels:
        if panel.locked == False:
            myBase.adminUnlocked[index] = True
        index += 1



def peopleCharts(pauseScreen):
    closeButton.selected = False
    peopleChart = d.Chart(screen)
    peopleChart.peopleToPoints(myBase.population)
    for bt in xPeoplePanel.buttonList:
        if bt.selected:
            peopleChart.setX(bt.dataEmbed)
    for bt in yPeoplePanel.buttonList:
        if bt.selected:
            peopleChart.setY(bt.dataEmbed)

    menuOn = True
    while menuOn:
        screen.blit(pauseScreen,top)
        mouseLoc = pygame.mouse.get_pos()

        peopleChart.draw(mouseLoc)

        closeRect = closeButton.draw(screen,(5,5),mouseLoc)

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(35,35),mouseLoc)
                    menuOn = False
                if peopleChart.transition == False:
                    xAction = genericButtonHandler(xPeoplePanel,click)
                    yAction = genericButtonHandler(yPeoplePanel,click)
                    if xAction:
                        i = 0
                        for bt in xPeoplePanel.buttonList:
                            if bt.selected:
                                peopleChart.setX(bt.dataEmbed)
                                for btY in yPeoplePanel.buttonList:
                                    btY.makeLive()
                                yPeoplePanel.buttonList[i].makeDead()
                            i +=1
                    if yAction:
                        i = 0
                        for bt in yPeoplePanel.buttonList:
                            if bt.selected:
                                peopleChart.setY(bt.dataEmbed)
                                for btX in xPeoplePanel.buttonList:
                                    btX.makeLive()
                                xPeoplePanel.buttonList[i].makeDead()
                            i += 1

        yPeoplePanel.drawPanel(mouseLoc)
        xPeoplePanel.drawPanel(mouseLoc)
        

        pygame.display.flip()

def productionCharts(pauseScreen):
    closeButton.selected = False
    toggleLoc = (screen.get_width()-toggleButton.buttonSurface.get_width()\
            -10,screen.get_height()-62)
    productionTag = d.getTextSurface("PRODUCTION")
    consumptionTag = d.getTextSurface("CONSUMPTION")
    productionChart = d.Chart(screen,line=True)
    productionChart.productionListToPoints(myBase.weekControl,c.black)
    allButtons = productionChartPanel1.buttonList + productionChartPanel2.buttonList\
        + consumptionChartPanel1.buttonList + consumptionChartPanel2.buttonList
    allStates = []
    for button in allButtons:
        if button.selected:
            if button.dataEmbed[-1] == 'C':
                searchTag = button.dataEmbed[0:-1]
                resource = myBase.parseResourceFromCapsule([searchTag])
                productionChart.productionListToPoints(resource.weeklyConsumptionReports,c.darken(resource.color,40))
            else:
                resource = myBase.parseResourceFromCapsule([button.dataEmbed])
                productionChart.productionListToPoints(resource.weeklyProductionReports,resource.color)
            allStates.append(True)
        else:
            allStates.append(False)
    productionChart.setY("Production Units")
    productionChart.setX("Weeks")
    menuOn = True
    while menuOn:
        screen.blit(pauseScreen,top)

        mouseLoc = pygame.mouse.get_pos()

        productionChart.draw(mouseLoc)

        closeRect = closeButton.draw(screen,(5,5),mouseLoc)

        i = 0
        for button in allButtons:
            if allStates[i]:
                if button.selected == False:
                    resource = myBase.parseResourceFromCapsule([button.dataEmbed])
                    productionChart.findAndRemove(button.dataEmbed)
                    productionChart.setY("Production Tons")
                    productionChart.setX("Weeks")
                    allStates[i] = False
            else:
                if button.selected:
                    if button.dataEmbed[-1] == 'C':
                        searchTag = button.dataEmbed[0:-1]
                        resource = myBase.parseResourceFromCapsule([searchTag])
                        productionChart.productionListToPoints(resource.weeklyConsumptionReports,c.darken(resource.color,40))
                    else:
                        resource = myBase.parseResourceFromCapsule([button.dataEmbed])
                        productionChart.productionListToPoints(resource.weeklyProductionReports,resource.color)
                    productionChart.setY("Production Tons") 
                    productionChart.setX("Weeks")
                    allStates[i] = True
            i+=1

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if productionChart.transition == False:
                    if toggleButton.selected:
                        multipleSelectionButtonHandler(consumptionChartPanel1,click)
                        multipleSelectionButtonHandler(consumptionChartPanel2,click)
                    else:
                        multipleSelectionButtonHandler(productionChartPanel1,click)
                        multipleSelectionButtonHandler(productionChartPanel2,click)
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(5,5),mouseLoc)
                    menuOn = False
                if toggleRect.collidepoint(click):
                    toggleButton.toggleSelected()

        
        if toggleButton.selected:
            consumptionChartPanel1.drawPanel(mouseLoc)
            consumptionChartPanel2.drawPanel(mouseLoc)
            screen.blit(consumptionTag,(screen.get_width()-consumptionTag.get_width()\
            -10,screen.get_height()-62+toggleButton.buttonSurface.get_height()+5))
        else:
            productionChartPanel1.drawPanel(mouseLoc)
            productionChartPanel2.drawPanel(mouseLoc)
            screen.blit(productionTag,(screen.get_width()-productionTag.get_width()\
            -10,screen.get_height()-62+toggleButton.buttonSurface.get_height()+5))

        toggleRect = toggleButton.draw(screen,toggleLoc,mouseLoc)

        pygame.display.flip()

def vitalsCharts(pauseScreen):
    closeButton.selected = False
    keyTag = d.getTextSurface("KEY: ")
    healthTag = d.getTextSurface("HEALTH ",c.green)
    skillTag = d.getTextSurface("SKILL ",c.red)
    psychTag = d.getTextSurface("PSYCH ",c.aqua)
    workTag = d.getTextSurface("WORK ",c.white)
    popGrowthTag = d.getTextSurface("POPULATION",c.yellow)
    keyLoc = (50,screen.get_height()-75)

    vitalsChart = d.Chart(screen,line=True)
    vitalsChart.productionListToPoints(myBase.weekControl,c.black)
    vitalsChart.setY("Percentage")
    vitalsChart.setX("Weeks")

    popFeed = []
    index = 0
    maxPop = 1
    for pop in myBase.populationTracker:
        if index > 0:
            if pop > maxPop:
                maxPop = pop
        index+=1
    index = 0
    for pop in myBase.populationTracker:
        if index > 0:
            popFeed.append(100.0*(pop/maxPop))
        else:
            popFeed.append(pop)
        index+=1

    vitalsChart.productionListToPoints(popFeed,c.yellow)

    vitalsChart.productionListToPoints(myBase.productivityTracker,c.white)
    vitalsChart.productionListToPoints(myBase.healthTracker,c.green)
    vitalsChart.productionListToPoints(myBase.skillTracker,c.red)
    vitalsChart.productionListToPoints(myBase.psychTracker,c.aqua)
    
    vitalsChart.setY("Percentage")
    vitalsChart.setX("Weeks")

    menuOn = True
    while menuOn:
        screen.blit(pauseScreen,top)

        mouseLoc = pygame.mouse.get_pos()

        vitalsChart.draw(mouseLoc)

        screen.blit(keyTag,keyLoc)
        keyLoc = (keyLoc[0]+keyTag.get_width(),keyLoc[1])
        screen.blit(healthTag,keyLoc)
        keyLoc = (keyLoc[0]+healthTag.get_width(),keyLoc[1])
        screen.blit(skillTag,keyLoc)
        keyLoc = (keyLoc[0]+skillTag.get_width(),keyLoc[1])
        screen.blit(psychTag,keyLoc)
        keyLoc = (keyLoc[0]+psychTag.get_width(),keyLoc[1])
        screen.blit(workTag,keyLoc)
        keyLoc = (keyLoc[0]+workTag.get_width(),keyLoc[1])
        screen.blit(popGrowthTag,keyLoc)
        keyLoc = (50,screen.get_height()-70)

        closeRect = closeButton.draw(screen,(5,5),mouseLoc)

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(5,5),mouseLoc)
                    menuOn = False

        pygame.display.flip()

def graveyardView(pauseScreen):
    graveyard = d.Graveyard(screen,myBase.graveyard)

    menuOn = True
    while menuOn:
        screen.blit(pauseScreen,top)
        
        mouseLoc = pygame.mouse.get_pos()

        graveyard.draw(mouseLoc)

        closeRect = closeButton.draw(screen,(5,5),mouseLoc)

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(5,5),mouseLoc)
                    menuOn = False

        pygame.display.flip()

def spaceManager(pauseScreen,baseObject,builder,spaceObject):
    closeButton.selected = False
    gap = 35
    panelHt = 55

    earthLaunchTag = d.getTextSurface("AVAILABLE EARTH LAUNCHES:")
    orbitalTag = d.getTextSurface("AVAILABLE ORBITAL LANDERS:")
    orbitalTag = d.getTextSurface("AVAILABLE SPACEPORT ARRIVALS:")
    rocketTag = d.getTextSurface("AVAILABLE EXPORT PAYLOADS:")
    
    allRocketButtons = builder.rocketPanel1.buttonList+builder.rocketPanel2.buttonList
    
    allOrbitalButtons = builder.orbitalPanel1.buttonList + builder.orbitalPanel2.buttonList
    if myBase.availableEarthLaunches < 1 or myBase.earthLaunches == False or myBase.orbitalResupply == False:
        for button in allOrbitalButtons:
            button.makeDead()

    if myBase.availableEarthLaunches < 1 or myBase.earthLaunches == False:
        for b in builder.earthPanel1.buttonList:
            b.makeDead()
        for b in builder.earthPanel2.buttonList:
            b.makeDead()
    else:
        for b in builder.earthPanel1.buttonList:
            b.makeLive()
        for b in builder.earthPanel2.buttonList:
            b.makeLive()
    if myBase.outbound == False:
        for b in builder.rocketPanel1.buttonList:
            b.makeDead()
        for b in builder.rocketPanel2.buttonList:
            b.makeDead()
    else:
        for b in builder.rocketPanel1.buttonList:
            b.makeLive()
        for b in builder.rocketPanel2.buttonList:
            b.makeLive()
    for button in allRocketButtons:
        if myBase.parseResourceFromCapsule(button.dataEmbed).quantity <=0:
            button.makeDead()
    resourceValues = d.resourceValues(myBase)
    spaceManager = d.SpaceManager(screen,myBase,spaceObject)

    orbitalDuration = 8
    menuOn = True
    click = (0,0)
    while menuOn:
        mouseLoc = pygame.mouse.get_pos()
        screen.blit(pauseScreen,top)
        
        closeRect = closeButton.draw(screen,(35,35),mouseLoc)
        screen.blit(earthLaunchTag,(gap,gap+panelHt-earthLaunchTag.get_height()))
        builder.earthPanel1.drawPanel(mouseLoc)
        builder.earthPanel2.drawPanel(mouseLoc)

        screen.blit(orbitalTag,(gap,gap+panelHt*4-orbitalTag.get_height()))
        builder.orbitalPanel1.drawPanel(mouseLoc)
        builder.orbitalPanel2.drawPanel(mouseLoc)

        screen.blit(rocketTag,(gap,screen.get_height()-2*panelHt-gap-rocketTag.get_height()))
        screen.blit(resourceValues,(gap,screen.get_height()-2*panelHt-gap-rocketTag.get_height()-resourceValues.get_height()))
        builder.rocketPanel1.drawPanel(mouseLoc)
        builder.rocketPanel2.drawPanel(mouseLoc)

        spaceManager.draw(mouseLoc)
        spaceManager.action(mouseLoc)

        allLanderButtons = builder.earthPanel1.buttonList+builder.earthPanel2.buttonList+\
            builder.orbitalPanel1.buttonList+builder.orbitalPanel2.buttonList
        for button in allLanderButtons:
            if myBase.availableEarthLaunches > 0 and button.live == False and myBase.earthLaunches:
                if button in allOrbitalButtons:
                    if myBase.orbitalResupply:
                        button.makeLive()
                else:
                    button.makeLive()
            if button.selected:
                if button in allOrbitalButtons:
                    duration = orbitalDuration

                    launchString = "from space-station?"
                    orbital = True
                    if button in builder.orbitalPanel2.buttonList:
                        spaceport = True
                    else:
                        spaceport = False
                else:
                    duration = spaceObject.duration
                    launchString = "from earth?"
                    orbital = False
                    spaceport = False
                if isinstance(button.dataEmbed[0],str):
                    podName = button.dataEmbed[0]
                else:
                    podName = button.dataEmbed[0][0]
                approved = d.choicePopUp(screen,click,["Launch " + podName,launchString])
                if approved:
                    spaceObject.addLaunch(s.Launch(myBase,duration,button.dataEmbed,orbital,spaceport))
                    myBase.availableEarthLaunches -= 1
                    if orbital:
                        orbitalDuration += 4
                button.toggleSelected()
                if myBase.availableEarthLaunches < 1:
                    for b in allLanderButtons:
                        b.makeDead()
        allRocketButtons = builder.rocketPanel1.buttonList+builder.rocketPanel2.buttonList
        for button in allRocketButtons:
            if button.selected:
                approved = d.choicePopUp(screen,click,["Launch " + button.dataEmbed[0] + " PAYLOAD"," into outer space?"])
                if approved:
                    thisPad = myBase.launchPads[0]
                    minQueue = len(myBase.launchPads[0].queue)
                    for pad in myBase.launchPads:
                        if len(pad.queue) < minQueue:
                            thisPad = pad
                            minQueue = len(pad.queue)
                    button.dataEmbed[5] = myBase.parseResourceFromCapsule(button.dataEmbed)
                    thisPad.queue.append(button.dataEmbed)
                button.toggleSelected()

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(35,35),mouseLoc)
                    menuOn = False
                spaceManager.checkClick(click)
                genericButtonHandler(builder.earthPanel1,click)
                genericButtonHandler(builder.earthPanel2,click)
                genericButtonHandler(builder.rocketPanel1,click)
                genericButtonHandler(builder.rocketPanel2,click)
                genericButtonHandler(builder.orbitalPanel1,click)
                genericButtonHandler(builder.orbitalPanel2,click)
        
        pygame.display.flip()

def managePeople(pauseScreen,baseObject):
    closeButton.selected = False
    ## TODO build building basaed lists per industry
    unemployedPanels = d.getUnemployedPanels(baseObject.population,baseObject.robots)
    unemployedPanels[1].set_alpha(150)
    managePeoplePanelLocal = managePeoplePanel

    redraw = False
    if baseObject.arts or baseObject.security:
        managePeopleButtons = [builderPlusButton,builderMinusButton,explorerPlusButton,\
        explorerMinusButton]
        if baseObject.arts:
            managePeopleButtons += [artistPlusButton,artistMinusButton]
        if baseObject.security:
            managePeopleButtons += [securityPlusButton,securityMinusButton]
        managePeopleButtons.append(fireButton)
        redraw = True


    if redraw:
        managePeoplePanelLocal = d.ControlPanel(screen,(0,screen.get_height()-40),managePeopleButtons,\
            d.getHorizontalBar(screen.get_width(),40))

    builderPanel = d.JobPanel(screen,[],c.white,"CONSTRUCTION",baseObject.builders)
    explorerPanel = d.JobPanel(screen,[],c.surfaceRed,"EXPLORATION",baseObject.explorers)
    lifeSupportPanel = d.JobPanel(screen,baseObject.lifeSupportList,c.green,"LIFE-SUPPORT")
    extractionPanel = d.JobPanel(screen,baseObject.extractionList,c.red,"EXTRACTION")
    powerPanel = d.JobPanel(screen,baseObject.powerList,c.yellow,"POWER")
    industryPanel = d.JobPanel(screen,baseObject.industryList,c.orange,"INDUSTRY")
    labPanel = d.JobPanel(screen,baseObject.labList,c.purple,"SCIENCE")
    recyclePanel = d.JobPanel(screen,baseObject.recycleList,c.aqua,"RECYCLE")
    adminPanel = d.JobPanel(screen,baseObject.adminList,c.pink,"ADMINISTRATION")
    transportPanel = d.JobPanel(screen,baseObject.transportList,c.blue,"TRANSPORT")
    artsPanel = d.JobPanel(screen,[],c.highlightOrange,"THE ARTS",baseObject.artists)
    securityPanel = d.JobPanel(screen,[],c.boldRed,"SECURITY",baseObject.guards)
    allJobPanels = [builderPanel,explorerPanel,lifeSupportPanel,extractionPanel,powerPanel,\
        industryPanel,labPanel,recyclePanel,adminPanel,transportPanel]

    fireFromJob = False
    fireTag = d.getTextSurface("CLICK WORKER TO FIRE")

    menuOn = True
    gap = 10 
    
    while menuOn:
        mouseLoc = pygame.mouse.get_pos()
        screen.blit(pauseScreen,top)

        closeRect = closeButton.draw(screen,(20,35),mouseLoc)

        builderPanel.draw(2*gap+unemployedPanels[0].get_height(),True)
        builderPanel.checkMouseOver(mouseLoc)
        explorerPanel.draw(2*gap+unemployedPanels[0].get_height(),False)
        explorerPanel.checkMouseOver(mouseLoc)
        lifeSupportPanel.draw(3*gap+unemployedPanels[0].get_height()+builderPanel.panelHeight,True)
        lifeSupportPanel.checkMouseOver(mouseLoc)
        recyclePanel.draw(4*gap+unemployedPanels[0].get_height()+builderPanel.panelHeight\
            +lifeSupportPanel.panelHeight,True)
        recyclePanel.checkMouseOver(mouseLoc)
        transportPanel.draw(5*gap+unemployedPanels[0].get_height()+builderPanel.panelHeight\
            +lifeSupportPanel.panelHeight+recyclePanel.panelHeight,True)
        transportPanel.checkMouseOver(mouseLoc)
        adminPanel.draw(6*gap+unemployedPanels[0].get_height()+builderPanel.panelHeight\
            +lifeSupportPanel.panelHeight+recyclePanel.panelHeight+transportPanel.panelHeight,True)
        adminPanel.checkMouseOver(mouseLoc)
        powerPanel.draw(3*gap+unemployedPanels[0].get_height()+explorerPanel.panelHeight,False)
        powerPanel.checkMouseOver(mouseLoc)
        extractionPanel.draw(4*gap+unemployedPanels[0].get_height()+explorerPanel.panelHeight\
            +powerPanel.panelHeight,False)
        extractionPanel.checkMouseOver(mouseLoc)
        industryPanel.draw(5*gap+unemployedPanels[0].get_height()+explorerPanel.panelHeight\
            +powerPanel.panelHeight+extractionPanel.panelHeight,False)
        industryPanel.checkMouseOver(mouseLoc)
        labPanel.draw(6*gap+unemployedPanels[0].get_height()+explorerPanel.panelHeight\
            +powerPanel.panelHeight+extractionPanel.panelHeight+industryPanel.panelHeight,False)
        labPanel.checkMouseOver(mouseLoc)
        if baseObject.arts:
            artsPanel.draw(7*gap+unemployedPanels[0].get_height()+explorerPanel.panelHeight\
                +powerPanel.panelHeight+extractionPanel.panelHeight+industryPanel.panelHeight+\
                    labPanel.panelHeight,False)
            artsPanel.checkMouseOver(mouseLoc)
        if baseObject.security:
            securityPanel.draw(7*gap+unemployedPanels[0].get_height()+builderPanel.panelHeight\
                +lifeSupportPanel.panelHeight+recyclePanel.panelHeight+transportPanel.panelHeight\
                    +adminPanel.panelHeight,True)
            securityPanel.checkMouseOver(mouseLoc)

        screen.blit(unemployedPanels[1],(screen.get_width()-unemployedPanels[1].get_width()-gap,gap))
        unemployedRect = screen.blit(unemployedPanels[0],(screen.get_width()-unemployedPanels[0].get_width()-gap,gap))
        if unemployedRect.collidepoint(mouseLoc):
            screen.blit(unemployedPanels[2],(mouseLoc[0]-unemployedPanels[2].get_width()-2,mouseLoc[1]))

        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuOn = False
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if closeRect.collidepoint(click):
                    closeButton.toggleSelected()
                    closeButton.draw(screen,(20,35),mouseLoc)
                    menuOn = False
                genericButtonHandler(managePeoplePanelLocal,click)
                if fireButton.selected:
                    for panel in allJobPanels:
                        person = panel.getPersonObject(click)
                        if person != None:
                            approve = d.choicePopUp(screen,click,["Fire "+person.name + " from their","job as "+person.job.tag + "?"])
                            if approve:
                                person.job.fire()
                                if person.robot == False:
                                    person.psych -= 0.05
                                fireButton.toggleSelected()
                                unemployedPanels = d.getUnemployedPanels(baseObject.population,baseObject.robots)

        managePeoplePanelLocal.drawPanel(mouseLoc)

        if builderPlusButton.selected:
            baseObject.addBuilderJob()
            builderPanel = d.JobPanel(screen,[],c.white,"CONSTRUCTION",baseObject.builders)
            builderPlusButton.toggleSelected()
        if builderMinusButton.selected:
            baseObject.removeBuilderJob()
            builderPanel = d.JobPanel(screen,[],c.white,"CONSTRUCTION",baseObject.builders)
            builderMinusButton.toggleSelected()
            unemployedPanels = d.getUnemployedPanels(baseObject.population,baseObject.robots)
        if explorerPlusButton.selected:
            baseObject.addExplorerJob()
            explorerPanel = d.JobPanel(screen,[],c.surfaceRed,"EXPLORERS",baseObject.explorers)
            explorerPlusButton.toggleSelected()
        if explorerMinusButton.selected:
            baseObject.removeExplorerJob()
            explorerPanel = d.JobPanel(screen,[],c.surfaceRed,"EXPLORERS",baseObject.explorers)
            explorerMinusButton.toggleSelected()
            unemployedPanels = d.getUnemployedPanels(baseObject.population,baseObject.robots)
        if artistPlusButton.selected:
            baseObject.addArtistJob()
            artsPanel = d.JobPanel(screen,[],c.highlightOrange,"THE ARTS",baseObject.artists)
            artistPlusButton.toggleSelected()
        if artistMinusButton.selected:
            baseObject.removeArtistJob()
            artsPanel = d.JobPanel(screen,[],c.highlightOrange,"THE ARTS",baseObject.artists)
            artistMinusButton.toggleSelected()
            unemployedPanels = d.getUnemployedPanels(baseObject.population,baseObject.robots)
        if securityPlusButton.selected:
            baseObject.addGuardJob()
            securityPanel = d.JobPanel(screen,[],c.boldRed,"SECURITY",baseObject.guards)
            securityPlusButton.toggleSelected()
        if securityMinusButton.selected:
            baseObject.removeGuardJob()
            securityPanel = d.JobPanel(screen,[],c.boldRed,"SECURITY",baseObject.guards)
            securityMinusButton.toggleSelected()
            unemployedPanels = d.getUnemployedPanels(baseObject.population,baseObject.robots)
        if fireButton.selected:
            screen.blit(fireTag,(int(pauseScreen.get_width()/2-fireTag.get_width()/2),50))

        pygame.display.flip()

def mainLoop(thisMap):
    blackBack = pygame.Surface((screen.get_width(),screen.get_height()))
    midX = int(screen.get_width()/2)
    midY = int(screen.get_height()/2)
    screen.blit(blackBack,(0,0))
    loading = d.getTextSurface("LOADING",c.boldRed,24)
    screen.blit(loading,(midX-int(loading.get_width()/2),midY-loading.get_height()))
    pygame.display.flip()
    for row in thisMap.grid:
        for tile in row:
            tile.redrawSurfaces()

    screen.blit(blackBack,(0,0))
    loading = d.getTextSurface("LOADING",c.boldRed,24)
    screen.blit(loading,(midX-int(loading.get_width()/2),midY-loading.get_height()))
    pygame.display.flip()
    

    saveTag = d.getTextSurface("SAVE",size = 15)
    #button set up
    buildButton = d.Button("BUILD")
    manageButton = d.Button("MANAGE")
    inquireButton = d.Button("INQUIRE")
    earthButton = d.Button("SPACE")
    controlButtons = [buildButton,manageButton,inquireButton,earthButton]

    globalCancelButton = d.Button("CANCEL") # can add to any panel, will be checked)

    mainPanel = d.ControlPanel(screen,(0,0),controlButtons,d.mainPanel(myBase))

    controlAnchor = (0,mainPanel.height)

    builder = o.Builder(screen,controlAnchor,myBase)

    if myBase.new:
        capsulesToLaunch = setUpLaunches(builder)
        trip = space.duration - 15
        adjust = trip - 5
        for capsule in capsulesToLaunch:
            space.addLaunch(s.Launch(myBase,trip,capsule))
            trip+=o.randomGap()
        tripCount = adjust
        myBase.adminPointsBalance += 1000 - len(capsulesToLaunch)*100
        if len(capsulesToLaunch) < 6:
            myBase.adminLevelBalance += 2
        else:
            if len(capsulesToLaunch) < 8:
                myBase.adminLevelBalance += 1
        while tripCount > 0 :
            space.timePass()
            tripCount -= 1

        #for launch in space.launches:
        #   launch.sols+=adjust
        myBase.new = False

    emptyPanel = d.ControlPanel(screen,controlAnchor,[])

    jobsButton = d.Button("JOBS")
    robotsButton = d.Button("ROBOTS")
    policyButton = d.Button("POLICIES")
    scienceButton = d.Button("RESEARCH")
    manageButtonList = [jobsButton,robotsButton,policyButton,scienceButton]

    managePanel = d.ControlPanel(screen,controlAnchor,manageButtonList)


    tileInfoButton = d.Button("TILE INFO")
    peopleInqButton = d.Button("PEOPLE")
    vitalsButton = d.Button("VITALS")
    productionButton = d.Button("PRODUCTION")
    graveyardButton = d.Button("GRAVEYARD")
    inquireButtonList = [tileInfoButton,productionButton,peopleInqButton,vitalsButton,graveyardButton]

    inquirePanel = d.ControlPanel(screen,controlAnchor,inquireButtonList)

    activePanel = emptyPanel

    background = pygame.transform.scale(a.background,(w,h))

    tileDetail = False
    blackout = a.blackout.copy()
    blackout.set_alpha(130)
    tileDetailToDraw = None

    lightFade = a.blackout.copy()
    lightFade.fill(c.darken(c.boldRed,75))

    gameOver = False
    TIMEPAD = 1
    timePad = TIMEPAD
    bAlpha = 255
    while gameOver == False:
        clock.tick(60)
        #data work
        timePad -= 1
        if timePad == 0:
            myBase.timePass()
            mainPanel.updateImg(d.mainPanel(myBase))
            timePad = TIMEPAD
            if myBase.hour == 0:
                newDay = True
                space.timePass()
            else:
                newDay = False
        #gets mouse position for mouseovers
        mouseLoc = pygame.mouse.get_pos()

        screen.blit(background,top)

        toDrawOver = []
        tileAnchor = thisMap.getStartDraw(center)
        for row in thisMap.grid:
            drawTileTuple = tileAnchor
            if tileDetail or myBase.dustEvent>0:
                fade = d.getFade(myBase,tileDetail,lightFade)
                screen.blit(fade,(0,0))
            for tile in row:
                tile.setClickAnchor(drawTileTuple)
                #print("mo " + str(tile.mouseOver) + " sel: " + str(tile.selected) + " " +str(builder.activeBuilding))
                if tile.checkClick(mouseLoc) and tileDetail == False:
                    tile.yesMouseOver()
                    if tile.mouseCount == 0:
                        tile.createInfoObject()
                else:
                    if tile.getTileSurfaceObject().infoObject != None and tile.exploreAnnounce == False:
                        infoFade = tile.getTileSurfaceObject().infoObject.draw(screen,tile.getTileSurfaceObject().infoObject.lastDraw,True,True)
                        tile.addAnimation(infoFade)
                    tile.noMouseOver()
                screen.blit(tile.getSurface(),drawTileTuple)
                tile.progressHandler(screen)
                if len(tile.getTileSurfaceObject().animations) > 0:
                    if tileDetail == False:
                        tile.runAnimations(screen)
                    else:
                        toDrawOver.append(tile)
                if (tile.mouseOver or tile.exploreAnnounce) and tile.getTileSurfaceObject().infoObject != None:
                    toDrawOver.append(tile)
                if tile.mouseOver and builder.activeBuilding != None:
                    builder.drawPreview(tile,screen,drawTileTuple)
                drawTileTuple = (drawTileTuple[0]+int(thisMap.tileWidth/2),drawTileTuple[1]+int(thisMap.tileWidth/4))
            tileAnchor = (tileAnchor[0]-int(thisMap.tileWidth/2), tileAnchor[1]+int(thisMap.tileWidth/4))
        if tileDetail:
            screen.blit(blackout,(0,0))
            tileDetailButtons = d.drawTileDetail(screen,tileDetailToDraw,mouseLoc,myBase.sol)  
            if len(tileDetailToDraw.getTileSurfaceObject().animations) > 0:
                tileDetailToDraw.runAnimations(screen) 
        if len(toDrawOver) > 0 and tileDetail == False:
            for tile in toDrawOver:
                if len(tile.getTileSurfaceObject().animations) > 0:
                    tile.runAnimations(screen)
                if tile.getTileSurfaceObject().infoObject != None:
                    if tile.exploreAnnounce:
                        tile.getTileSurfaceObject().infoObject.draw(screen,(tile.anchor[0],tile.anchor[1]+30\
                            -tile.getTileSurfaceObject().infoObject.surface.get_height()),absoluteLoc=True)
                        if tile.getTileSurfaceObject().infoObject.delay == 0:
                            tile.exploreAnnounce = False
                    else:
                        tile.getTileSurfaceObject().infoObject.draw(screen,mouseLoc)


        if bAlpha>0:
            bAlpha-=1
            blackBack.set_alpha(bAlpha)
            screen.blit(blackBack,(0,0))
        #draw panels

        mainPanel.drawPanel(mouseLoc)
        myBase.announcements.run(screen)
        myBase.drawCharts(screen)
        screen.blit(space.getDurationText(),(activePanel.width + 8,h - 10))
        if space.checkLaunches:
            space.drawLaunches(screen,activePanel.width)
            for launch in space.launches:
                if launch.spaceportSwitch:
                    launch.autoLander(builder,myBase)
        activePanel.drawPanel(mouseLoc)

        if manageButton.selected:
            builder.reset()
            activePanel = managePanel
            if jobsButton.selected:
                managePeople(d.getPauseScreen(screen,100),myBase)
                jobsButton.toggleSelected()
            if robotsButton.selected:
                robotManager(d.getPauseScreen(screen,100))
                robotsButton.toggleSelected()
            if policyButton.selected:
                adminManager(d.getPauseScreen(screen,100))
                policyButton.toggleSelected()
            if scienceButton.selected:
                scienceManager(d.getPauseScreen(screen,100))
                if myBase.costChange:
                    builder.refreshButtons(screen,controlAnchor)
                    myBase.costChange = False
                scienceButton.toggleSelected()

        if buildButton.selected:
            activePanel = builder.getPanel()

        if inquireButton.selected:
            builder.reset()
            activePanel = inquirePanel
            if productionButton.selected:
                productionCharts(d.getPauseScreen(screen))
                productionButton.toggleSelected()
            if peopleInqButton.selected:
                peopleCharts(d.getPauseScreen(screen))
                peopleInqButton.toggleSelected()
            if vitalsButton.selected:
                vitalsCharts(d.getPauseScreen(screen))
                vitalsButton.toggleSelected()
            if graveyardButton.selected:
                graveyardView(d.getPauseScreen(screen))
                graveyardButton.toggleSelected()

        if earthButton.selected:
            builder.reset()
            activePanel = emptyPanel
            spaceManager(d.getPauseScreen(screen,100),myBase,builder,space)
            earthButton.toggleSelected()

        if globalCancelButton.selected:
            activePanel = emptyPanel
            globalCancelButton.toggleSelected()
            builder.reset()

        saveRect = screen.blit(saveTag,(5,screen.get_height()-saveTag.get_height()))

        pygame.display.flip()
        
        #EVENT HANDLE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
                pygame.display.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                mainPanelIndex = 0
                if saveRect.collidepoint(click):
                    approve = d.choicePopUp(screen,click,["Save current base?"])
                    if approve:
                        saveGame(myBase)
                if tileDetail:
                    buttonClick = False
                    index = 0
                    for shutoffRect in tileDetailButtons[1]:
                        if shutoffRect.collidepoint(click):
                            buttonClick = True
                            tileDetailButtons[0][index].toggleSelected()
                        index+=1
                    index = 0
                    for priorityRect in tileDetailButtons[3]:
                        if priorityRect.collidepoint(click):
                            buttonClick = True
                            tileDetailButtons[2][index].toggleSelected()
                        index+=1
                    if buttonClick == False:
                        tileDetail = False
                        tileDetailToDraw.buildingInfoObjects = []
                        break
                for buttonRect in mainPanel.buttonRects:
                    if buttonRect.collidepoint(click):
                        tileInfoButton.selected = False
                        clearButtonSelections(mainPanel.buttonList)
                        mainPanel.buttonList[mainPanelIndex].toggleSelected()
                    mainPanelIndex += 1
                activePanelIndex = 0
                for buttonRect in activePanel.buttonRects:
                    if buttonRect.collidepoint(click):
                        clearButtonSelections(activePanel.buttonList)
                        activePanel.buttonList[activePanelIndex].toggleSelected()
                    activePanelIndex += 1
                #Launch overlay controls
                if space.checkLaunches():
                    launchIndex = 0
                    for launchRect in space.launchRects:
                        if launchRect.collidepoint(click) and space.launches[launchIndex].arrived:
                            tileInfoButton.selected = False
                            space.launches[launchIndex].chooseLandingSite(builder)
                            clearButtonSelections(mainPanel.buttonList)
                            activePanel = d.ControlPanel(screen,controlAnchor,[globalCancelButton])
                        launchIndex += 1
                for row in thisMap.grid:
                    for tile in row:
                        if tile.checkClick(click) and tileDetail == False:
                            if tile.selected:
                                if builder.activeBuilding != None:
                                    if builder.tileOpen: 
                                        if builder.activeCost.check():
                                            if builder.landing:
                                                approve = True
                                            else:
                                                approve = d.choicePopUp(screen,click,\
                                                    ["Construct " + builder.activeBuilding + " here?"],builder.activeCost)
                                            if approve:
                                                tileInfoButton.selected = False                
                                                builder.createBuildingObject(myBase,tile)
                                                builder.resetPanel(activePanel)
                                                builder.resetPanel(mainPanel)
                                                activePanel = emptyPanel
                                                myBase.updateExploreGrid(tile)
                                        else:
                                            d.messagePopUp(screen,click,["Need additional resources:"],builder.activeCost)
                                            myBase.gauges = d.gauges(myBase)
                                    else:
                                        pass #TODO build NO animation OPen and cost seperate
                                if tileInfoButton.selected and tileDetail == False:
                                    tileSurface = tile.getTileSurfaceObject()
                                    for each in tileSurface.buildingInfoObjects:
                                        if each.shutoffButton != None:
                                            each.updateButtons()
                                    tileDetail = True
                                    tileDetailToDraw = tile
                            tile.setSelected()
                            #print("x:" + str(tile.x) + " y:" + str(tile.y))


#MAIN
#LOAD GAME DON'T BUILD SPACE OR MAP
#LOAD GAME CREATES BLANK TILE SURFACES FROM MAP GRID THEN REDRAWS

introAnimation()
newGame = d.choicePopUp(screen,(315,250),["Start a new base or","continue game?"],\
    yesText="NEW GAME", noText="CONTINUE")

#NEW GAME
if newGame:
    baseName = getBaseName()
    newMap = o.Map(12)
    d.createBlankTiles(newMap)
    myBase = o.Base(baseName,newMap)
    """
    newRobot = p.People(robot=True)
    newRobot2 = p.People(robot=True)
    myBase.robotDummyResource.quantity+=2
    myBase.robots.append(newRobot)
    myBase.robots.append(newRobot2)
    """
    space = s.Space() #TODO Seed with sol to control trip distance
    """
    space.addLaunch(s.Launch(myBase,10,o.landerHabitatCapsule))
    space.addLaunch(s.Launch(myBase,8,o.supplyLanderCapsule))
    space.addLaunch(s.Launch(myBase,6,o.recycleLanderCapsule))
    space.addLaunch(s.Launch(myBase,4,o.powerLanderCapsule))
    space.addLaunch(s.Launch(myBase,4,o.minerBotLanderCapsule))
    space.addLaunch(s.Launch(myBase,4,o.probeLanderCapsule))
    space.addLaunch(s.Launch(myBase,4,o.builderLanderCapsule))
    space.addLaunch(s.Launch(myBase,4,o.luxuryCargoCapsule))
    #space.addLaunch(s.Launch(myBase,4,o.shuttleCapsule))
    """
    ##testing junk
    """
    myBase.metal.quantity = 100.0
    myBase.plastics.quantity = 100.0
    myBase.electronics.quantity = 100.0
    myBase.concrete.quantity = 100.0
    myBase.regolith.quantity = 100.0
    myBase.fuel.quantity = 100.0
    myBase.rare.quantity = 100.0
    """
else:
    blackBack = pygame.Surface((screen.get_width(),screen.get_height()))
    midX = int(screen.get_width()/2)
    midY = int(screen.get_height()/2)
    screen.blit(blackBack,(0,0))
    loading = d.getTextSurface("LOADING",c.boldRed,24)
    screen.blit(loading,(midX-int(loading.get_width()/2),midY-loading.get_height()))
    pygame.display.flip()
    loadfile = open("savedgame", "rb")
    myBase = pickle.load(loadfile)
    loadfile.close()
    d.createBlankTiles(myBase.map)
    myBase.redrawAllTiles()
    index = 0
    for status in myBase.adminUnlocked:
        if status:
            adminPanels[index].locked = False
        index += 1
    index = 0
    for status in myBase.scienceUnlocked:
        if status:
            sciencePanels[index].locked = False
        index += 1
    myBase.announcements.addAnnouncement("SAVED GAME: " + myBase.name + " sol:" + \
        str(myBase.sol) + " successfully loaded.")
    space = s.Space()
    for launchList in myBase.savedLaunchLists:
        capsule = o.getLanderCapsule(launchList[1])
        recoveredLaunch = s.Launch(myBase,launchList[0],capsule,launchList[2],launchList[3])
        recoveredLaunch.sols = launchList[4]
        space.addLaunch(recoveredLaunch)
    myBase.savedLaunchLists = []

mainLoop(myBase.map)
