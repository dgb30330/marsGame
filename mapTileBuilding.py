import pygame
import assets as a
import draw as d
import people as p
import color as c
import industry as i
import random

def randomGap():
    number = random.randrange(3,7)
    return number

powerBuildings = ["EARTH REACTOR","PREFAB SOLAR","BATTERY COMPLEX","SOLAR PANEL","SIMPLE REACTOR","SOLAR CLUSTER","FUSION REACTOR","SOLAR FARM","SUPER REACTOR"]
recycleBuildings = ["COMPOSTER","H2O TREATMENT","AIR FILTRATION","BIOCYCLER","WASTEWATER PLANT","AIR RECYCLER","RECYCLE HUB","RECYCLE POD"]
waterExtractionBuildings = ["MINER BOT","VAPORIZER","ICE DRILL","VAPOR FARM","ICE PIT","ICE MINE","ICE FACILITY","FULL DIG"]
regolithExtractionBuildings = ["MINER BOT","REGOLITH PIT","REGOLITH MINE","REGOLITH FIELD","SURFACE SCRAPE","SMALL MINE","FULL DIG"]
oreExtractionBuildings = ["MINER BOT","ORE PIT","ORE MINE","ORE EXCAVATION","SURFACE SCRAPE","SMALL MINE","FULL DIG"]
rareExtractionBuildings = ["MINER BOT","RARE SITE","RARE MINE","HI-TECH MINE","SMALL MINE","FULL DIG"]
extractionBuildings = waterExtractionBuildings+oreExtractionBuildings+rareExtractionBuildings+rareExtractionBuildings
concreteBuildings = ["CONCRETE MIXER","CONCRETE WORKSHOP","CONCRETE PLANT","CONCRETE FACTORY"]
metalBuildings = ["AUTO SMELTER","METALSMITH","STEEL MILL","METAL FACTORY"] 
fuelBuildings = ["ELECTROLYSER","FUEL WORKSHOP","FUEL PLANT","REFINERY"] 
medsBuildings = ["MEDICAL LAB","MEDS FACILITY","MEDS FACTORY"]  
plasticsBuildings = ["POLYMER POD","PLASTICS PLANT","PLASTICS FACTORY"]
electronicsBuildings = ["ELECTRONICS SHOP","CIRCUIT PLANT","E-MANUFACTURER"] 
waterBuildings = ["REG OVEN","ROCK COOKER","MARS EVAPORATOR","REGOLITH STEAMER"]
industryBuildings = concreteBuildings+metalBuildings+fuelBuildings+medsBuildings+plasticsBuildings+\
    electronicsBuildings+waterBuildings
adminOutputBuildings = ["COMM. RELAY","OFFICE POD","MAIN OFFICE","NERVE CENTER","HQ","AI NODE"] 
psychPenaltyBuildings = ["LAUNCH PAD","SPACEPORT"]
psychPenaltyBuildings += extractionBuildings
organicsBuildings = ["GARDEN","MEGA GARDEN","TERRARIUM","GREENHOUSE","FARM DOME"]
airBuildings = ["AIR MOD","MEGA GARDEN","GREENHOUSE","TERRARIUM","FARM DOME"]
medicalBuildings = ["FIELD LAB","LABORATORY","SCIENCE COMPLEX","MED DEPOT","MED BOT","FIELD HOSPITAL","HOSPITAL"]
scienceBuildings = ["PROBE","FIELD LAB","LABORATORY","SCIENCE COMPLEX","FIELD HOSPITAL","HOSPITAL"]
educationBuildings = ["COMM. RELAY","TRAINING TERM.","SCHOOL POD","SPACE COLLEGE","NERVE CENTER","HQ","AI NODE"]


holidayPossibleNames = ["Martian Christmas","Founder's Day","Regolith Festival","Astronaut Memorial"]
artJobTags = ["PAINTER","SCULPTER","FILM-MAKER","MUSICIAN","SINGER","VIDEOGRAPHER","PHOTOGRAPHER",\
    "ILLUSTRATOR","COMEDIAN","NOVELIST","WRITER"]

INCREASE_CONST = 1.1
LEVEL_UP_CONST = 1.25

class Base:
    def __init__(self, name,thisMap):
        self.new = True
        self.name = name
        self.populationCount = 0
        self.population = [] 
        self.populationTracker = ["POPULATION"]
        self.healthTracker = ["HEALTH"]
        self.skillTracker = ["SKILL"]
        self.psychTracker = ["PSYCH"]
        self.productivityTracker = ["PRODUCTIVITY"]
        self.graveyard = [] # TODO build life expectancy method
        self.environment = p.Environment()
        self.announcements = d.Announcements() #contains allAnnouncements list, move to Class?
        self.exploreGrid = [] #Tile objects
        self.exploreGridInitialized = False
        self.map = thisMap 
        for row in thisMap.grid:
            for tile in row:
                self.exploreGrid.append(tile)
        # time
        self.sol = 1
        self.solCycle = 1
        self.earthYear = 2033
        self.marsYear = 0
        self.hour = 0
        self.maxHour = 24
        self.maxSol = 668
        
        self.holidayPriorityNames = []
        self.holidays = [] #solCycleStrts
        self.holidayNames = []
        self.isHoliday = False
        self.holidayCount = 0
        #mars
        self.sun = 1.0
        self.dustEvent = 0
        self.dustEventDuration = 0
        self.dustAlpha = 0

        self.savedLaunchLists = []
        # NEEDS
        self.FOOD_MIN_CONST = 0.016
        self.FOOD_MAX_CONST = 0.025
        self.food = i.Resource("FOOD","fd",c.green,True,25.0)
        self.AIR_CONST = 0.005
        self.air = i.Resource("AIR","a",c.aqua,True,100.0)
        self.totalVolume = 0 #air needs must have air > volume and use
        self.WATER_MIN_CONST = 0.25
        self.WATER_MAX_CONST = 0.33
        self.water = i.Resource("WATER","h2o",c.blue,True,50.0)
        self.organics = i.Resource("ORGANICS","org",c.darkGreen,False,15.0)
        self.power = i.Resource("POWER","pwr",c.yellow,True,0.0)
        self.ore = i.Resource("ORE","ore",c.red,False,1.0)
        self.regolith = i.Resource("REGOLITH","reg",c.surfaceRed,False,0.25)
        self.rare = i.Resource("RARE","r",c.pink,False,5.0)
        #industrial resources
        self.concrete = i.Resource("CONCRETE","crt",c.white,False,10.0)
        self.metal = i.Resource("METAL","mtl",c.grey,False,20.0)
        self.fuel = i.Resource("FUEL","f",c.orange,False,20.0)
        self.electronics = i.Resource("ELECTRONICS","elc",c.highlightYellow,False,50.0)
        self.meds = i.Resource("MEDS","med",c.purple,False,50.0)
        self.plastics = i.Resource("PLASTICS","plc",c.highlightOrange,False,30.0)
        self.robotDummyResource = i.Resource("ROBOTS","rbt",c.white,False,1000.0)
        self.globalDiscount = 1.0 #add to Cost mechanics TODO

        self.bonuses = i.Bonuses()

        self.powerFactor = 1.0
     
        self.artists = []
        self.artBonus = 1.0
        self.arts = False

        self.guards = []
        self.guardBonus = 1.0
        self.security = False
        self.securityRatio = 0
        
        #industries
        self.builders = []
        self.robots = []
        self.builderBonus = 1.0
        # TODO use bonus
        self.addBuilderJob()
        self.maintainRatio = 0.0
        self.maintainBalance = 0.0
        self.buildingCondition = 0.0
        self.explorers = []
        self.exploreBonus = 1.0
        self.addExplorerJob()

        self.generalStorageUse = 0.0
        self.generalStorageCapacity = 0.0
        self.generalStorageFull = True
        #each instatiated here, controled via myBase.industry.method()
        self.buildList = []
        self.habitatList = []
        self.habitatUnits = 0

        self.lifeSupportList = []
        self.farmingIndustry = i.Industry("FARMING",self.announcements,True,[self.organics,self.water],[0.7,0.3],self.food)
        self.airIndustry = i.Industry("AIR",self.announcements,True,[self.power],[0.01],self.air)
        self.organicsIndustry = i.Industry("ORGANICS",self.announcements,True,[self.water],[0.75],self.organics)

        self.recycleList = []
        self.recycle = i.Industry("RECYCLE",self.announcements)
        self.weekControl = ["control"]

        self.adminList = []
        self.adminPoints = 0.0
        self.adminPointsBalance = 0 #1000.0
        self.adminLevelUp = 100.0
        self.adminLevel = 0
        self.adminLevelBalance = 0
        self.adminCostFactor = 1.00
        #TODO control other admin bonuses
        self.adminUnlocked = [False,False,False,False,False,False,False,False,False]
        self.scienceUnlocked = [False,False,False,False,False,False,False,False,False,False,False,False,False]
        self.costChange = False

        self.eventCost = 50.0
        ## for ALL science / admin buys ##

        self.labList = []
        self.sciencePointsBalance = 0 #1000.0
        self.sciencePoints = 0.0
        self.scienceLevelUp = 100.0
        self.scienceLevel = 0
        self.scienceLevelBalance = 2
        self.scienceCostFactor = 1.00
        self.educationBonus = 0.0
        self.educationPoints = 0
        self.medFill = 0.0 #ratio of needed meds 0.0 to 1.0
        self.medicalFactor = 0.1

        self.launchCost = 50.0 
        self.transportList = []
        self.earthLaunches = False
        self.orbitalResupply = False
        self.earthCostFactor = 1.00
        self.availableEarthLaunches = 0
        self.outbound = False
        self.availableOutbound = 1
        self.launchPads = []
        self.exportPoints = 0.0

        self.healthBalance = 0.0
        self.skillBalance = 0.0
        self.psychBalance = 0.0

        self.consumerRatio = 0.0
        self.market = True

        self.powerList = []
        self.powerIndustry = i.Industry("POWER",self.announcements)
        self.powerFuelIndustry = i.Industry("POWER",self.announcements,True,[self.fuel],[0.04],self.power)
        
        self.extractionList = []
        self.extractionIndustry = i.Industry("EXTRACTION",self.announcements)

        self.industryList = []
        self.concreteIndustry = i.Industry("CONCRETE",self.announcements,True,\
            [self.regolith,self.water],[0.75,0.25],self.concrete)
        self.metalIndustry = i.Industry("METAL",self.announcements,True,\
            [self.ore],[2.5],self.metal)
        self.fuelIndustry = i.Industry("FUEL",self.announcements,True,\
            [self.water,self.air],[0.75,0.05],self.fuel)
        self.medsIndustry = i.Industry("MEDS",self.announcements,True,\
            [self.organics,self.rare],[2.0,0.5],self.meds)
        self.electronicsIndustry = i.Industry("ELECTRONICS",self.announcements,True,\
            [self.metal,self.rare],[0.6,0.4],self.electronics)
        self.plasticsIndustry = i.Industry("PLASTICS",self.announcements,True,\
            [self.fuel,self.organics],[0.7,0.3],self.plastics)
        self.waterFromRegolithIndustry = i.Industry("MARS-WATER",self.announcements,True,\
            [self.regolith],[12.0],self.water)
        
        self.allResources = [self.air,self.water,self.food,self.organics,self.power,\
            self.regolith,self.ore,self.rare,self.concrete,self.metal,self.fuel,self.meds,\
                self.electronics,self.plastics]
        self.allBuildings = [] #Buildings contain surfaces

    def redrawAllTiles(self):
        for row in self.map.grid:
            for tile in row:
                tile.redrawSurfaces()

    def updateGauges(self):
        d.HomeCharts.gaugesSurface = d.gauges(self)

    def updateResourceChart(self):
        totalGeneralUsage = self.spoilage()
        d.HomeCharts.resourceSurface = d.resourceChart(self,self.generalStorageUse,self.generalStorageCapacity,totalGeneralUsage)

    def getTile(self,x,y):
        for row in self.map.grid:
            for tile in row:
                if tile.y == y and tile.x == x:
                    return tile
    
    def rehouse(self):
        #remove all residents
        bestHabs = []
        allHabs = self.habitatList.copy()
        for hab in allHabs:
            for resident in hab.residents:
                resident.housed = False
            hab.residents = []
        while len(allHabs) > 0:
            maxHab = allHabs[0]
            maxV = maxHab.psychEffect
            for hab in allHabs:
                if hab.psychEffect > maxV:
                    maxHab = hab
                    maxV = hab.psychEffect
            bestHabs.append(maxHab)
            allHabs.remove(maxHab)
        
        peoplePriority = []
        if self.market:
            peoplePriority = self.getMostProductive()
        else:
            peoplePriority = self.getLowestPsych()
        for hab in bestHabs:
            if hab.shutoff == False:
                hab.fillFromList(peoplePriority)
            #print(hab.getReport())
    
    def checkAdminCost(self):
        available = False
        if self.adminPointsBalance > self.eventCost*self.adminCostFactor:
            available = True
        return available

    def getAdminCost(self):
        return self.eventCost*self.adminCostFactor

    def makeAdminBuy(self):
        self.adminPointsBalance -= self.eventCost*self.adminCostFactor
        self.eventCost *= INCREASE_CONST

    def makeScienceBuy(self):
        self.sciencePointsBalance -= self.eventCost*self.scienceCostFactor
        self.eventCost *= INCREASE_CONST

    def getLowestPsych(self):
        lowestPsych = []
        allPeople = self.population.copy()
        while len(allPeople) > 0:
            minP = allPeople[0]
            minV = minP.psych
            for person in allPeople:
                psy = person.psych
                if psy < minV:
                    minP = person
                    minV = psy
            #print(minP.name + str(minV))
            lowestPsych.append(minP)
            allPeople.remove(minP)
        return lowestPsych

    def getMostProductive(self):
        mostProductive = []
        allPeople = self.population.copy()
        while len(allPeople) > 0:
            maxP = allPeople[0]
            if allPeople[0].job !=None:
                maxV = allPeople[0].job.productivity
            else:
                maxV = 0.0
            for person in allPeople:
                if person.job !=None:
                    prod = person.job.productivity
                else:
                    prod = 0.0
                if prod > maxV:
                    maxP = person
                    maxV = prod
            #print(maxP.name + str(maxV))
            mostProductive.append(maxP)
            allPeople.remove(maxP)
        return mostProductive


    def runHabitatList(self):
        #run psych adjust here
        DEMAND_CUT = 10.0
        SOC_DEMAND = 0.3
        demand = 0
        consumePlasticsRatio = 1.0
        consumeElecRatio = 1.0
        prePsych = postPsych = 0
        for person in self.population:
            prePsych += person.psych
            if self.consumerRatio > 0:
                if self.market:
                    if person.job == None:
                        pass
                    else:
                        if person.job.productivity > 1.0:
                            demand += person.job.productivity - 1.0
                        else:
                            pass
                else:
                    demand += SOC_DEMAND
        if self.consumerRatio > 0:
            if demand/(2*DEMAND_CUT) > (self.consumerRatio*self.plastics.quantity):
                # if not enough re
                if demand/(2*DEMAND_CUT) > 0:
                    consumePlasticsRatio = (self.consumerRatio*self.plastics.quantity)/(demand/(2*DEMAND_CUT))
                else:
                    consumePlasticsRatio = 0.0
                self.plastics.baseConsumption += self.consumerRatio*self.plastics.quantity
                self.plastics.quantity -= self.consumerRatio*self.plastics.quantity
            else:
                # if plenty re
                self.plastics.baseConsumption += demand/(2*DEMAND_CUT)
                self.plastics.quantity -= demand/(2*DEMAND_CUT)
            if demand/(2*DEMAND_CUT) > (self.consumerRatio*self.electronics.quantity):
                # if not enough re
                if demand/(2*DEMAND_CUT) > 0:
                    consumeElecRatio = (self.consumerRatio*self.electronics.quantity)/(demand/(2*DEMAND_CUT))
                else:
                    consumeElecRatio = 0.0
                self.electronics.baseConsumption += self.consumerRatio*self.electronics.quantity
                self.electronics.quantity -= self.consumerRatio*self.electronics.quantity
            else:
                # if plenty re
                self.electronics.baseConsumption += demand/(2*DEMAND_CUT)
                self.electronics.quantity -= demand/(2*DEMAND_CUT)
        self.environment.calcPsychBackground(self.populationCount,prePsych)
        globalPsychAdjust = (self.environment.psychBackground - 1)/350.0
        for b in self.habitatList:
            for person in b.residents:
                factor = b.psychEffect * b.maintain * b.bonus * self.powerFactor
                person.psych += (factor - 1.0)/350.0
        for person in self.population:
            if globalPsychAdjust > 0:
                person.psych += globalPsychAdjust * self.bonuses.psychBonus
            else:
                person.psych += globalPsychAdjust * (1/self.bonuses.psychBonus)
            if person.housed == False:
                person.psych -= p.People.YEARLY_10TH*2
            if person.job == None:
                person.psych -= p.People.YEARLY_20TH*person.skill
            if self.isHoliday:
                person.psych += 0.015 * (1/person.psych)
            if self.consumerRatio > 0:
                if self.market:
                    if person.job == None:
                        pass
                    else:
                        if person.job.productivity > 1.0:
                            person.psych += (((person.job.productivity - 1.0)/(2*DEMAND_CUT))*consumeElecRatio)/350
                            person.psych += (((person.job.productivity - 1.0)/(2*DEMAND_CUT))*consumePlasticsRatio)/350
                        else:
                            person.psych -= p.People.YEARLY_100TH
                else:
                    person.psych += ((SOC_DEMAND/(2*DEMAND_CUT))*consumeElecRatio)/350
                    person.psych += ((SOC_DEMAND/(2*DEMAND_CUT))*consumePlasticsRatio)/350
            postPsych += person.psych
            if person.psych < 0.5 and person.sane:
                msg = person.insane(self.securityRatio)
                self.announcements.addAnnouncement("sol:" + str(self.sol) + " "+msg)
            if person.sane ==False and person.psych >= 0.5:
                person.sane = True
                self.announcements.addAnnouncement("sol:" + str(self.sol) + " " + person.name + \
                    " resolved PSYCH CRISIS.")
        if self.populationCount > 0:
            prePsych /= self.populationCount
            postPsych /= self.populationCount
            self.psychBalance = postPsych-prePsych
        else:
            self.psychBalance = 0.0

    def runRecycleList(self):
        airD = airToUse = self.air.baseConsumption
        waterD = waterToUse = self.water.baseConsumption
        foodD = foodToUse = self.food.baseConsumption

        airN = 0
        waterN = 0
        foodN = 0
        for building in self.recycleList:
            if building.shutoff == False:
                if building.automated:
                    work = 1.0
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                efficiency = building.actualEfficiency + (building.maxEfficiency-building.actualEfficiency) *(1.0-(work*self.bonuses.recycleBonus*building.maintain))
                building.multiReadout[0] = 0.0
                if building.airCapacity > 0 and airToUse > 0:
                    airRe = self.recycle.run(building.airCapacity,efficiency,self.powerFactor,airToUse)
                    airToUse -= building.airCapacity
                    #print(airRe)
                    self.air.quantity += airRe
                    self.air.production += airRe
                    building.multiReadout[0] = airRe
                    airN += airRe
                building.multiReadout[1] = 0.0
                if building.waterCapacity > 0 and waterToUse > 0:
                    waterRe = self.recycle.run(building.waterCapacity,efficiency,self.powerFactor,waterToUse)
                    waterToUse -= building.waterCapacity
                    self.water.quantity += waterRe
                    self.water.production += waterRe
                    building.multiReadout[1] = waterRe
                    waterN += waterRe
                building.multiReadout[2] = 0.0
                if building.foodCapacity > 0 and foodToUse > 0:
                    organicsRe = self.recycle.run(building.foodCapacity,efficiency,self.powerFactor,foodToUse)
                    foodToUse -= building.foodCapacity
                    #TODO check dry storage
                    self.organics.quantity += organicsRe
                    self.organics.production += organicsRe
                    building.multiReadout[2] = organicsRe
                    foodN += organicsRe
        if airD != 0:
            self.air.recyclePercent = airN/airD
        else:
            self.air.recyclePercent = 0.0
        if waterD != 0:
            self.water.recyclePercent = waterN/waterD
        else:
            self.water.recyclePercent = 0.0
        if foodD != 0:
            self.food.recyclePercent = foodN/foodD
        else:
            self.food.recyclePercent = 0.0

    
    def runLifeSupportList(self):
        startState = self.farmingIndustry.supplied
        for building in self.lifeSupportList:
            if building.shutoff == False:
                if len(building.jobs) == 0:
                    work = 1.0 # this test automation
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                work*=self.bonuses.lifeSupportBonus
                productivity = building.maintain * work * building.bonus
                building.multiReadout[0] = self.farmingIndustry.run(building.foodOutput,productivity,self.powerFactor)
                if building.organicsOutput > 0:
                    building.multiReadout[2] = self.organicsIndustry.run(building.organicsOutput,productivity,self.powerFactor)
                if building.airOutput > 0:
                    building.multiReadout[1] = self.airIndustry.run(building.airOutput,productivity,self.powerFactor)
        self.industryAnnouncer(self.farmingIndustry,startState)
        
    def industryAnnouncer(self,industry,startState):
        if industry.supplied != startState:
            if industry.supplied == False:
                industry.announcements.addAnnouncement(industry.tag + " low on " + industry.lowResource)
            else:
                industry.announcements.addAnnouncement(industry.tag + " resumed full production!")
        

    def runAdminList(self):
        edWork = 0
        for building in self.adminList:
            if building.shutoff == False:
                if len(building.jobs) < 1:
                    work = 1.0 
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                productivity = building.maintain * work * building.output *building.bonus * self.bonuses.adminBonus
                ###print("maintain:" + str(building.maintain) + " work:" + str(work) + "out:" + str(building.output))
                building.readout = productivity
                self.adminPoints += productivity
                self.adminPointsBalance += productivity
                ###print(self.adminPoints)
                if self.adminPoints > self.adminLevelUp:
                    self.doAdminLevelUp()
                if building.educationFactor > 0:
                    edWork += work * building.educationFactor
        if self.populationCount > 0:
            self.educationBonus = (edWork*5.0)/self.populationCount
        else:
            self.educationBonus = 0.0

       

    def runLabList(self):
        medWork = 0.0
        for building in self.labList:
            if building.shutoff == False:
                if len(building.jobs) == 0:
                    work = 1.0 
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                productivity = building.maintain * work * building.output *building.bonus * self.bonuses.scienceBonus
                building.readout = productivity
                self.sciencePoints += productivity
                self.sciencePointsBalance +=productivity
                #print(self.sciencePoints)
                if self.sciencePoints > self.scienceLevelUp:
                    self.doScienceLevelUp()
                if building.medicalFactor > 0.0:
                    medWork += work*building.medicalFactor
        if self.populationCount>0:
            self.medicalFactor = ((medWork*50.0)/self.populationCount)+0.1
            if self.medicalFactor > 2.0:
                self.medicalFactor = 2.0
            medNeed = self.populationCount *0.01
            if medNeed < self.meds.quantity:
                self.medFill = 1.0
                self.meds.quantity -= medNeed
                self.meds.baseConsumption += medNeed
            else:
                self.medFill = (self.meds.quantity/medNeed)/2.0 + 0.50
                self.meds.baseConsumption += self.meds.quantity
                self.meds.quantity = 0.0
        else:
            self.medFill = 0.50
            self.medicalFactor = 0.1





    def doAdminLevelUp(self):
        self.adminLevel += 1
        self.adminLevelBalance += 1
        self.adminPoints -= self.adminLevelUp
        self.adminLevelUp *= LEVEL_UP_CONST
        self.builderBonus *= INCREASE_CONST
        self.announcements.addAnnouncement("Administrative level-up! Level:" + str(self.adminLevel))

    def doScienceLevelUp(self):
        self.scienceLevel += 1
        self.scienceLevelBalance += 1
        self.sciencePoints -= self.scienceLevelUp
        self.scienceLevelUp *= LEVEL_UP_CONST
        self.exploreBonus *= INCREASE_CONST
        self.announcements.addAnnouncement("Science level-up! Level:" + str(self.scienceLevel))
        self.educationPoints += 1
    
    def runIndustryList(self):
        concreteStartState = self.concreteIndustry.supplied
        metalStartState = self.metalIndustry.supplied
        fuelStartState = self.fuelIndustry.supplied
        medsStartState = self.medsIndustry.supplied
        electronicsStartState = self.electronicsIndustry.supplied
        plasticsStartState = self.plasticsIndustry.supplied
        waterFromRegolithStartState = self.waterFromRegolithIndustry.supplied
        for building in self.industryList:
            if building.shutoff == False and building.robots == False:
                #robots run in buildMaintain
                if building.automated:
                    work = 1.0 
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                productivity = building.maintain * work * building.bonus * self.bonuses.industryBonus
                building.readout = building.industry.run(building.efficiency,productivity,self.powerFactor) 
        self.industryAnnouncer(self.concreteIndustry,concreteStartState)   
        self.industryAnnouncer(self.metalIndustry,metalStartState)    
        self.industryAnnouncer(self.fuelIndustry,fuelStartState)
        self.industryAnnouncer(self.medsIndustry,medsStartState)
        self.industryAnnouncer(self.electronicsIndustry,electronicsStartState)
        self.industryAnnouncer(self.plasticsIndustry,plasticsStartState)
        self.industryAnnouncer(self.waterFromRegolithIndustry,waterFromRegolithStartState)
    
    def runExtractionList(self):
        for building in self.extractionList:
            if building.shutoff == False:
                if len(building.jobs) == 0:
                    work = 1.0 # this test automation
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                productivity = building.maintain *work *building.bonus *self.bonuses.extractionBonus
                multiRead = False
                building.multiReadout = []
                if building.water:
                    waterProd = self.extractionIndustry.run(building.waterOutput,productivity,self.powerFactor)
                    self.water.quantity += waterProd
                    self.water.production += waterProd
                    building.readout = waterProd
                    multiRead = True
                    building.multiReadout.append(waterProd)
                if building.regolith:
                    regolithProd = self.extractionIndustry.run(building.regolithOutput,productivity,self.powerFactor)
                    self.regolith.quantity += regolithProd
                    self.regolith.production += regolithProd
                    if multiRead:
                        building.readout = 666
                        building.multiReadout.append(regolithProd)
                    else:
                        building.readout = regolithProd
                        multiRead = True
                        building.multiReadout.append(regolithProd)
                if building.ore:
                    oreProd = self.extractionIndustry.run(building.oreOutput,productivity,self.powerFactor)
                    self.ore.quantity += oreProd
                    self.ore.production += oreProd
                    if multiRead:
                        building.multiReadout.append(oreProd)
                        if building.readout != 666:
                            building.readout = 667
                    else:
                        building.readout = oreProd
                if building.rare:
                    rareProd = self.extractionIndustry.run(building.rareOutput,productivity,self.powerFactor)
                    self.rare.quantity += rareProd
                    self.rare.production += rareProd
                    if multiRead:
                        building.multiReadout.append(rareProd)
                    else:
                        building.readout = rareProd


    def runTransportList(self):
        totalDiscount = 0.0
        for building in self.transportList:
            if building.shutoff == False:
                if len(building.jobs) < 1:
                    work = 1.0
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                if isinstance(building,CommsCenter):
                    self.environment.addPsychEffect(work/3.0,0.0,1) # WATCH - PSYCH BONUS FOR SPACE COMS
                totalDiscount += (building.earthCostEffect * building.maintain * work * self.bonuses.transportBonus)
                if isinstance(building,LaunchPad):
                    if len(building.queue) > 0 and building.full == False:
                        building.createLaunch(building.queue[0])
                        building.queue.remove(building.queue[0])
        self.earthCostFactor = 1.0 - totalDiscount

    def getEarthCost(self):
        return self.eventCost * self.earthCostFactor
    
    def addEarthLaunch(self,pointsToConvert="None"):
        if self.exportPoints > self.launchCost*self.earthCostFactor:
            self.exportPoints -= self.launchCost*self.earthCostFactor
        else:
            need = self.launchCost*self.earthCostFactor
            need -= self.exportPoints
            self.exportPoints = 0.0
            if pointsToConvert != "None":
                if pointsToConvert == "Science":
                    self.sciencePointsBalance -= need
                if pointsToConvert == "Admin":
                    self.adminPointsBalance -= need
        self.availableEarthLaunches += 1
        self.launchCost *= INCREASE_CONST

    def parseResourceFromCapsule(self,capsule):
        if capsule[0] == "CONCRETE":
            return self.concrete
        if capsule[0] == "METAL":
            return self.metal
        if capsule[0] == "FOOD":
            return self.food
        if capsule[0] == "AIR":
            return self.air
        if capsule[0] == "WATER":
            return self.water
        if capsule[0] == "ELECTRONICS":
            return self.electronics
        if capsule[0] == "ORE":
            return self.ore
        if capsule[0] == "FUEL":
            return self.fuel
        if capsule[0] == "MEDS":
            return self.meds
        if capsule[0] == "RARE":
            return self.rare
        if capsule[0] == "REGOLITH":
            return self.regolith
        if capsule[0] == "ORGANICS":
            return self.organics
        if capsule[0] == "PLASTICS":
            return self.plastics
        if capsule[0] == "POWER":
            return self.power
        if capsule[0] == "ROBOTS":
            return self.robotDummyResource

    def runPowerList(self):
        # power deducted in buildMaintain()
        for building in self.powerList:
            if building.shutoff == False:
                if building.automated:
                    work = 1.0
                else:
                    work = 0
                    for job in building.jobs:
                        work += job.productivity
                    work /= len(building.jobs)
                    if self.isHoliday:
                        work/=4.0
                work *= self.bonuses.powerBonus
                if building.nuclear:
                    powerAdd = self.powerIndustry.run(building.powerOutput,work*building.maintain*building.bonus,1.0)
                    building.readout = powerAdd
                else:
                    if building.solar:
                        powerAdd = self.powerIndustry.run(building.powerOutput,work*building.maintain*building.bonus,self.sun)
                        building.readout = powerAdd
                    else:
                        powerAdd = 0
                        readout = self.powerFuelIndustry.run(building.powerOutput,work*building.maintain*building.bonus,1.0)
                        building.readout = readout
                self.power.quantity += powerAdd
                self.power.production += powerAdd
                
    
    def optimizeJobs(self):
        allJobs = self.getAllJobsList(True)
        for job in allJobs:
            job.fire()
        self.fillJobs(allJobs)

    def getAllJobsList(self,optimize = False):
        allJobs = self.builders + self.explorers +self.artists +self.guards #TODO add all non-building jobs
        for building in self.allBuildings:
            if len(building.jobs) > 0 and building.shutoff == False:
                for job in building.jobs:
                    allJobs.append(job)
        if optimize and len(allJobs) > 0:
            for job in allJobs:
                job.updateImportance()
            sortedJobs = []
            while len(allJobs) > 0:
                maxJob = allJobs[0]
                maxImport = allJobs[0].importance
                print(maxJob.tag)
                print(len(allJobs))
                for job in allJobs:
                    print(job.tag)
                    if job.importance > maxImport:
                        maxJob = job
                        maxImport = job.importance
                print("max: "+maxJob.tag)
                print(len(allJobs))
                sortedJobs.append(maxJob)
                allJobs.remove(maxJob)
                print(len(allJobs))
            allJobs = sortedJobs

        #TODO check building shutoff, recalc importance, sort jobs
        return allJobs

    def fillJobs(self,allJobs):
        unemployed = []
        for p in self.population:
            if p.job == None and p.age > 6200 and (p.sane or self.securityRatio>1.0):
                unemployed.append(p)
        for r in self.robots:
            if r.job == None and r.functional:
                unemployed.append(r)
        if len(unemployed) > 0:
            if len(allJobs) > 0:
                for job in allJobs:
                    if job.person == None:
                        bestCandidate = unemployed[0]
                        for p in unemployed:
                            if job.jobTest(p) > job.jobTest(bestCandidate):
                                bestCandidate = p
                        job.hire(bestCandidate)
                        unemployed.remove(bestCandidate)
                        
                        self.announcements.addAnnouncement(bestCandidate.name + " hired as " + job.tag + \
                            " : prod:{0:.2f}".format(job.productivity))
                    if len(unemployed) == 0:
                        break
    
    def nameHoliday(self):
        if len(self.holidayPriorityNames) > 0:
            # TODO seed holiday priority name logic
            name = self.holidayPriorityNames[random.randrange(0,len(self.holidayPriorityNames))]
            self.holidayPriorityNames.remove(name)
        else:
            name = holidayPossibleNames[random.randrange(0,len(holidayPossibleNames))]
            holidayPossibleNames.remove(name)
        self.holidayNames.append(name)

    def timePass(self):
        self.hour += 1
        # reset daily reads
        if self.hour == 1:
            self.refreshNeedCharts()
            self.resetDailyResourceReadings()
        # people sorter
        if self.hour == 4:
            self.runHabitatList()
        if self.hour == 5:
            self.explore()
        if self.hour == 6:
            self.fillJobs(self.getAllJobsList())
        if self.hour == 7:
            self.runArts()
            self.runSecurity()
        if self.hour == 8:
            self.peopleNeeds() #people needs
            self.assignJobs()
        # recycle
        if self.hour == 8:
            self.runTransportList()
        if self.hour == 9:
            self.runRecycleList()
        # work
        if self.hour == 10:
            self.runLifeSupportList()
        if self.hour == 11:
            self.runExtractionList()
        if self.hour == 12:
            self.runIndustryList()
        if self.hour == 13:
            self.runLabList()
        if self.hour == 14:
            self.runAdminList()
        if self.hour == 15:
            self.runPowerList()
        if self.hour == 16:
            self.buildMaintain()
        if self.hour == 20:
            self.updateGauges()
        if self.hour == 21:
            pass
            #self.resourceChart = d.resourceChart(self,self.generalStorageUse,self.generalStorageCapacity)
        if self.hour == 22:
            self.updateSun()
        if self.hour == 23:
            self.updateResourceChart()
        if self.hour > self.maxHour:
            self.solCycle += 1
            if self.isHoliday:
                self.holidayCount+=1
                if self.holidayCount == 7:
                    self.isHoliday = False
                    self.announcements.addAnnouncement("Holiday ended.")
            index = 0
            for holidayStart in self.holidays:
                if self.solCycle == holidayStart:
                    self.isHoliday = True
                    self.announcements.addAnnouncement("sol:" + str(self.sol) + " "+self.holidayNames[index]+" begins today.")
                    self.holidayCount = 0
                index += 1
            self.sol += 1
            if self.dustEvent > 0:
                self.dustEvent -= 1
                if self.dustEvent == 0:
                    self.announcements.addAnnouncement("Dust storm ended.")
            if self.sol % 7 == 0:
                self.updateResourceWeekly()
                self.updateVitalsTracker()
            if self.sol % 30 == 0:
                self.rehouse()
            if self.sol % (365 - 15) == 0:
                self.earthYear +=1
            self.hour = 0
            if self.solCycle > self.maxSol:
                self.marsYear += 1
                self.solCycle = 0
        
    def updateSun(self):
        dustFactor = 1.0
        if self.dustEvent > 0:
            dustFactor = random.uniform(0.2,0.4)
        sunMax = 0.8 + (0.0012 * abs(self.solCycle - 334))
        sunMin = 0.6 + (0.0012 * abs(self.solCycle - 334))
        self.sun = random.uniform(sunMin,sunMax) * dustFactor
        if 0 == random.randrange(0,668): 
            self.dustEvent += random.randrange(6,55)
            self.dustEventDuration = self.dustEvent
            self.announcements.addAnnouncement("sol:" + str(self.sol) + " A dust storm has began.")
            self.environment.addPsychEffect(-0.15*self.populationCount,(-0.15*self.populationCount)/self.dustEvent,self.dustEvent)
        #print(self.sun)

    def updateVitalsTracker(self):
        count = 0
        health = 0
        skill = 0
        psych = 0
        productivity = 0
        for person in self.population:
            count += 1
            health += person.health
            skill += person.skill
            psych += person.psych
            if person.job != None:
                productivity += person.job.productivity
        self.populationTracker.append(count)
        if count > 0:
            self.healthTracker.append(100.0*(health/count))
            self.skillTracker.append(100.0*(skill/count))
            self.psychTracker.append(100.0*(psych/count))
            self.productivityTracker.append(100.0*(productivity/count))
        else:
            self.healthTracker.append(0)
            self.skillTracker.append(0)
            self.psychTracker.append(0)
            self.productivityTracker.append(0)
        
    def spoilage(self):
        #non self storage resurces need checked at production
        total = 0
        for resource in self.allResources:
            resource.value *= 1.0 + (0.01 / 350)
            if resource.quantity < 0:
                resource.quantity = 0.0
                print(resource.tag + " went negative.")
            if resource.selfStorage:
                fullStatus = resource.full
                if resource.quantity >= resource.storageCapacity:
                    resource.quantity = resource.storageCapacity
                    resource.full = True
                    if fullStatus == False and resource.tag != "POWER":
                        self.announcements.addAnnouncement(resource.tag+" storage maxed out!")
                        self.environment.addPsychEffect(1.0,0.1,7)
                else:
                    resource.full = False
            else:
                total += resource.quantity
        if self.generalStorageCapacity > 0:
            if total > self.generalStorageCapacity:
                if self.generalStorageFull == False:
                    self.announcements.addAnnouncement("sol:" + str(self.sol) + " Storage has reached capacity.")
                    self.generalStorageFull = True
                self.generalStorageUse = 1.0
                adjust = total/self.generalStorageCapacity
                for resource in self.allResources:
                    if resource.selfStorage == False:
                        if resource.storageFreeze < 0:
                            resource.quantity/=adjust
                            resource.storageFreeze = resource.quantity
                        else:
                            if resource.quantity > resource.storageFreeze:
                                resource.quantity = resource.storageFreeze
                        #TODO track waste here?
            else:
                if self.generalStorageFull:
                    for resource in self.allResources:
                        if resource.selfStorage == False:
                            resource.storageFreeze = -1.0
                self.generalStorageFull = False
                self.generalStorageUse = total/self.generalStorageCapacity
        else:

            self.generalStorageUse = 0.0
        return total

                
    def getEducationFactor(self):
        weightedPoints = 0
        weight = self.educationBonus
        count = 1
        while count <= self.educationPoints:
            weightedPoints += weight
            if count > self.populationCount:
                weight *= ((self.populationCount-1)/self.populationCount)
            count += 1
        if self.populationCount > 0:
            factor = (weightedPoints/self.populationCount)*p.People.YEARLY_100TH
        else:
            factor = 0.0
        return factor
        
    
    def peopleNeeds(self):
        foodPortionList = self.basicRation(self.food.quantity,self.FOOD_MIN_CONST,self.FOOD_MAX_CONST) #provides basic ration
        # excessPortion = 
        waterRationList = self.basicRation(self.water.quantity,self.WATER_MIN_CONST,self.WATER_MAX_CONST)
        airPressure = self.air.quantity / (self.totalVolume + 0.001)
        #reset daily trackers - move to own function?
        self.food.baseConsumption = 0
        self.water.baseConsumption = 0
        self.air.baseConsumption = 0
        preHealth = postHealth = 0
        preSkill = postSkill = 0
        for person in self.population:
            preHealth += person.health
            preSkill += person.skill
            self.water.quantity -= waterRationList[person.needCatagory]
            self.water.baseConsumption += waterRationList[person.needCatagory]
            if waterRationList[person.needCatagory] < self.WATER_MIN_CONST:
                person.health -= self.WATER_MIN_CONST - waterRationList[person.needCatagory]
            self.food.quantity -= foodPortionList[person.needCatagory] # food deducted
            self.food.baseConsumption += foodPortionList[person.needCatagory]
            if foodPortionList[person.needCatagory] < self.FOOD_MIN_CONST:
                person.health -= self.FOOD_MIN_CONST - foodPortionList[person.needCatagory] # health deduct under 
            self.air.quantity -= self.AIR_CONST
            self.air.baseConsumption += self.AIR_CONST
            if airPressure < 1:
                person.health -= (1-airPressure) * 0.5
            edFactor = self.getEducationFactor()
            if person.age < p.People.workingAge:
                person.skill += ((p.People.YOUTH_ONE/2.0) * self.bonuses.skillBonus)+(edFactor/2.0)
            else:
                person.skill += edFactor * self.bonuses.skillBonus
            if person.job != None: ## daily update to productivity at job
                person.job.updateProductivity()
                #TODO job psych skill and health effects
            if self.populationCount>0:
                healthBonus = self.bonuses.healthBonus * (((self.medFill*self.populationCount)/self.populationCount)*self.medicalFactor)
            else:
                healthBonus = 0.1
            birth = person.ageSol(healthBonus) # lastly age person / returns slight birth chance
            if birth:
                self.addBirth(person.lastName)
            if person.alive == False:
                self.deadPerson(person)
            postHealth += person.health
            postSkill += person.skill
        if self.populationCount > 0:
            preHealth /= self.populationCount
            preSkill /= self.populationCount
            postHealth /= self.populationCount
            postSkill /= self.populationCount
            self.healthBalance = postHealth-preHealth
            self.skillBalance = postSkill-preSkill
        else:
            self.healthBalance = 0.0
            self.skillBalance = 0.0


    def assignJobs(self):
        pass

    def resetResource(self,resource):
        resource.weeklyConsumption += (resource.baseConsumption + resource.industryConsumption)
        resource.baseConsumption = 0
        resource.industryConsumption = 0
        resource.weeklyProduction += resource.production 
        resource.production = 0


    def updateResourceWeekly(self):
        self.weekControl.append(1)
        for resource in self.allResources:
            resource.weeklyProductionReports.append(resource.weeklyProduction)
            resource.weeklyProduction = 0
            resource.weeklyConsumptionReports.append(resource.weeklyConsumption)
            resource.weeklyConsumption = 0



    def resetDailyResourceReadings(self):
        for resource in self.allResources:
            self.resetResource(resource)

    def basicRation(self,available,minCONST,maxCONST):
        minRation = minCONST * self.populationCount
        maxRation = maxCONST * self.populationCount
        if available < minRation:
            #equal ration
            if self.populationCount > 0:
                portion = available / self.populationCount
            else:
                portion = 0
        else:
            portion = minCONST
            #buildExcess TODO
        return [portion] # return list based on people.needCatagory index TODO

    def addPeople(self,toAdd):
        self.announcements.addAnnouncement("sol:" + str(self.sol) + " "+ str(toAdd) + " new arrivals.")
        self.environment.addPsychEffect(toAdd,toAdd/30.0,30)
        while toAdd > 0:
            newPerson = p.People(sol=self.sol)
            self.population.append(newPerson)
            toAdd -= 1
        self.populationCount = len(self.population)

    def addBirth(self,babyLastName):
        newPerson = p.People(native=True,lastName=babyLastName)
        self.population.append(newPerson)
        self.populationCount = len(self.population)
        self.announcements.addAnnouncement("sol:" + str(self.sol) + " " + newPerson.name + " born!")
        psychPts = (0.5*self.populationCount)/((self.populationCount-1.0)/self.populationCount)
        self.environment.addPsychEffect(psychPts,psychPts/200,200)

    def deadPerson(self,personObject):
        self.environment.addPsychEffect(-18/(personObject.age/350),(-18/(personObject.age/350))/30,30)
        personObject.diedString = "Died: MY:"+str(self.marsYear)+"-"+str(self.solCycle)+" Age:{0:.0f}".format(personObject.age/350.0)
        personObject.diedSol = self.sol
        personObject.diedYear = self.earthYear
        if personObject.job != None:
            personObject.job.person = None
            personObject.job.productivity = 0
            personObject.job = None
        self.population.remove(personObject)
        self.populationCount = len(self.population)
        self.graveyard.append(personObject)
        self.announcements.addAnnouncement("sol:" + str(self.sol) + " " + personObject.name + " has died.")
        #TODO add body to organics
        
    def refreshNeedCharts(self):
        d.HomeCharts.foodChart = d.needChart(self.food)
        d.HomeCharts.airChart = d.needChart(self.air,True,self.totalVolume)
        d.HomeCharts.waterChart = d.needChart(self.water)
        d.HomeCharts.powerChart = d.needChart(self.power,power=True,powerFactor = self.powerFactor)

    def drawCharts(self,screen):
        d.HomeCharts.draw(screen)
    
    def getProductionData(self,resourcePanel): # TODO ALWAYS ADD NEW RESOURCES!!
        #rPanel button index 0 food 1 water 2 air 3 organics
        parrallelResources = [self.food,self.water,self.air,self.organics]
        returnResources = []
        index = 0
        for button in resourcePanel.buttonList:
            if button.selected:
                returnResources.append(parrallelResources[index])
            index+=1
        return returnResources

    def runSecurity(self):
        securityWork = 0.0
        if self.security:
            for guard in self.guards:
                securityWork += guard.productivity
        if self.populationCount-len(self.guards) > 0:
            self.securityRatio = (securityWork*7.0)/(self.populationCount-len(self.guards))
        else:
            self.securityRatio = 0.0 

    def runArts(self):
        if self.arts:
            for artist in self.artists:
                self.environment.addPsychEffect(artist.productivity,0.0,1)

    def addGuardJob(self):
        guard = i.Job("SECURITY GUARD",0.6,0.2,0.2,None)
        self.guards.append(guard)
        if self.environment.psychPoints > 1:
            self.environment.psychPoints -= 1
    
    def removeGuardJob(self):
        if len(self.guards) > 0:
            removeIndex = len(self.guards)-1
            if self.guards[removeIndex].person != None:
                self.guards[removeIndex].fire()
            self.guards.remove(self.guards[removeIndex])
            self.environment.psychPoints += 1

    def addArtistJob(self):
        artJobTag = artJobTags[random.randrange(0,len(artJobTags))]
        artist = i.Job(artJobTag,0.0,0.2,0.8,None,1.5)
        self.artists.append(artist)
    
    def removeArtistJob(self):
        if len(self.artists) > 0:
            removeIndex = len(self.artists)-1
            if self.artists[removeIndex].person != None:
                self.artists[removeIndex].fire()
            self.artists.remove(self.artists[removeIndex])

    def addBuilderJob(self):
        builder = i.Job("BUILDER",0.5,0.3,0.2)
        self.builders.append(builder)

    def removeBuilderJob(self):
        if len(self.builders) > 0:
            removeIndex = len(self.builders)-1
            if self.builders[removeIndex].person != None:
                self.builders[removeIndex].fire()
            self.builders.remove(self.builders[removeIndex])

    def addExplorerJob(self):
        explorer = i.Job("EXPLORER",0.3,0.4,0.3)
        self.explorers.append(explorer)
    
    def removeExplorerJob(self):
        if len(self.explorers) > 0:
            removeIndex = len(self.explorers)-1
            if self.explorers[removeIndex].person != None:
                self.explorers[removeIndex].fire()
            self.explorers.remove(self.explorers[removeIndex])

    def buildMaintain(self):
        availableBuildPoints = 0
        for b in self.builders:
            availableBuildPoints += b.productivity*self.builderBonus*self.bonuses.surfaceBonus
        buildingsQueued = len(self.buildList)
        if buildingsQueued > 0:
            maintainPoints = availableBuildPoints * self.maintainRatio
            availableBuildPoints = (availableBuildPoints - maintainPoints) / float(buildingsQueued)
        else:
            maintainPoints = availableBuildPoints
            availableBuildPoints = 0.0
        for buildingUnderConstruction in self.buildList:
            buildingUnderConstruction.buildProgress += availableBuildPoints
            if buildingUnderConstruction.buildProgress > buildingUnderConstruction.buildCost:
                buildingUnderConstruction.finishBuild()
        neededMaintain = 0.0
        for building in self.allBuildings:
            if building.shutoff == False:
                neededMaintain += building.maintainCost
        for robot in self.robots:
            neededMaintain += robot.health/30.0
        if neededMaintain > 0:
            self.maintainBalance = maintainPoints/neededMaintain
        else:
            self.maintainBalance = 0.0
        totalPowerNeed = 0.0
        buildingCurrentTotal = 0.0
        buildingMaxTotal = 0.0
        for robot in self.robots:
            totalPowerNeed += robot.health
            robot.health -= ((1.0-self.maintainBalance)*(robot.health/30.0))
            if robot.health > 1.875:
                robot.health = 1.875
            if robot.health < 0:
                robot.health = 0.0
        for building in self.allBuildings:
            #maintanence v degredation. 1:7?
            if building.shutoff == False:
                totalPowerNeed += building.powerUsage
                building.maintain -= ((1.0-self.maintainBalance)*building.maintainCost)
                if building.maintain > building.maintainMax:
                    building.maintain = building.maintainMax
                if building.maintain < 0:
                    building.maintain = 0.0
                if building.maintain < building.maintainMax * 0.70:
                    pass
                    #self.announcements.addAnnouncement(building.buildingName + " is falling into disrerair.")
                buildingCurrentTotal += building.maintain
                buildingMaxTotal += building.maintainMax
        if buildingMaxTotal > 0:
            self.buildingCondition = buildingCurrentTotal/buildingMaxTotal
        else:
            self.buildingCondition = 0.0
        if totalPowerNeed <= self.power.quantity:
            self.powerFactor = 1.0
            self.power.quantity -= totalPowerNeed
            self.power.baseConsumption = totalPowerNeed
            if self.power.quantity < 0:
                self.power.quantity = 0.0
        else:
            self.powerFactor = self.power.quantity/totalPowerNeed
            self.power.baseConsumption = totalPowerNeed
            self.power.quantity = 0.0
        for robot in self.robots:
            if robot.functional:
                if robot.health < 0.5:
                    robot.functional = False
                    self.announcements.addAnnouncement(robot.name + " is broke-down. Can do no work.")
            else:
                if robot.health > 0.5:
                    robot.functional = True
                    self.announcements.addAnnouncement(robot.name + " is functioning normally again.")
            if robot.job != None:
                robot.job.updateProductivity(self.powerFactor)
        

    def explore(self):
        explorePoints = 0
        for e in self.explorers:
            explorePoints += e.productivity*self.exploreBonus*self.bonuses.surfaceBonus
        if len(self.exploreGrid) > 0:
            self.exploreGrid[0].exploreProgress += explorePoints
            self.sciencePoints += (explorePoints / 5.0)
            self.sciencePointsBalance += (explorePoints / 5.0)
            if self.exploreGrid[0].exploreProgress > 100:
                self.revealTile(self.exploreGrid[0])
        else:
            self.sciencePoints += explorePoints
            self.sciencePointsBalance += explorePoints
        if self.sciencePoints > self.scienceLevelUp:
            self.doScienceLevelUp()

    def revealTile(self,tileObject):
        self.announcements.addAnnouncement("Tile x:" + str(tileObject.x) + " y:"\
                     + str(tileObject.y) + " surveyed")
        tileObject.explored = True
        tileObject.exploreProgress = 101
        tileObject.exploreAnnounce = True
        tileObject.createInfoObject(True)
        self.exploreGrid.remove(tileObject)

    def updateExploreGrid(self,tileObject):
        #print("Run grid update")
        if tileObject.explored == False:
            self.exploreGrid.remove(tileObject)
            self.exploreGrid.insert(0,tileObject)
            if self.exploreGridInitialized == False:
                    self.initializeExploreGrid()
            toFront = []
            for tile in self.exploreGrid:
                if tile.exploreProgress > 0:
                    toFront.append(tile)
            for tile in toFront:
                self.exploreGrid.remove(tile)
                self.exploreGrid.insert(0,tile)
            
    def initializeExploreGrid(self):
        centerX = self.exploreGrid[0].x
        centerY = self.exploreGrid[0].y
        newGrid = [self.exploreGrid[0]]
        self.exploreGrid.remove(self.exploreGrid[0])
        diff = 1
        toRemove = []
        while len(self.exploreGrid) > 0:
            for tile in self.exploreGrid:
                diffX = abs(centerX-tile.x)
                diffY = abs(centerY-tile.y)
                thisDiff = diffX + diffY
                if thisDiff == diff:
                    newGrid.append(tile)
                    toRemove.append(tile)
            diff += 1
            for tile in toRemove:
                self.exploreGrid.remove(tile)
            toRemove = []
        self.exploreGrid = newGrid
        self.exploreGridInitialized = True

    def appendBuildList(self,habitatBuildingObject):
        self.buildList.append(habitatBuildingObject)

    def appendHabitatList(self,habitatBuildingObject):
        self.habitatList.append(habitatBuildingObject)

    def appendRecycleList(self,recycleBuildingObject):
        self.recycleList.append(recycleBuildingObject)

    def appendPowerList(self,powerBuildingObject):
        self.powerList.append(powerBuildingObject)

    def appendLifeSupportList(self,lifeSupportBuildingObject):
        self.lifeSupportList.append(lifeSupportBuildingObject)

    def appendExtractionList(self,extractionBuildingObject):
        self.extractionList.append(extractionBuildingObject)
    
    def appendIndustryList(self,industryBuildingObject):
        self.industryList.append(industryBuildingObject)

    def appendLabList(self,labBuildingObject):
        self.labList.append(labBuildingObject)
    
    def appendAdminList(self,adminBuildingObject):
        self.adminList.append(adminBuildingObject)
    
    def appendTransportList(self,transportBuildingObject):
        self.transportList.append(transportBuildingObject)

#costList = [g,r,c,m,f,e,p] / [0,0,0,0,0,0,0]
class Cost:
    def __init__(self,baseObject,costList):
        self.drawable = False
        self.base = baseObject
        self.regolith = float(costList[0])*baseObject.regolith.discount
        self.rare = float(costList[1])*baseObject.rare.discount
        self.concrete = float(costList[2])*baseObject.concrete.discount
        self.metal = float(costList[3])*baseObject.metal.discount
        self.fuel = float(costList[4])*baseObject.fuel.discount
        self.electronics = float(costList[5])*baseObject.electronics.discount
        self.plastics = float(costList[6])*baseObject.plastics.discount
        self.allCosts = [self.regolith, self.rare, self.concrete, self.metal, self.fuel, \
            self.electronics, self.plastics]
        self.allResources = [self.base.regolith, self.base.rare, self.base.concrete, self.base.metal,\
            self.base.fuel, self.base.electronics, self.base.plastics]
        self.tags = [] # Glow tag objects
        

    def makeDrawable(self):
        self.tags = []
        index = 0
        self.drawable = True
        for cost in self.allCosts:
            if cost > 0:
                self.tags.append(self.generateGlowTag(index))
            index+=1

    def draw(self,screen,loc):
        if self.drawable == False:
            self.makeDrawable()
            
        xLoc = loc[0]
        yLoc = loc[1]
        for tag in self.tags:
            screen.blit(tag.get(),(xLoc,yLoc))
            yLoc += tag.get_height()

    def drawDeficit(self,screen,loc):
        xLoc = loc[0]
        yLoc = loc[1]
        index = 0
        for cost in self.allCosts:
            if cost > self.allResources[index].quantity:
                tag = d.getTextSurface("-{0:.2f}".format(cost-self.allResources[index].quantity)+\
                    " "+self.allResources[index].shortTag,c.red,17)
                self.allResources[index].deficit = 10
                screen.blit(tag,(xLoc,yLoc))
                yLoc += tag.get_height()
            index += 1

    def makeGlow(self):
        self.tags = []
        index = 0
        for cost in self.allCosts:
            if cost > 0:
                self.tags.append(self.generateGlowTag(index,True))
            index+=1

    def generateGlowTag(self,costIndex,glow = False):
        if glow:
            startColor = c.glowYellow
        else: 
            startColor = self.allResources[costIndex].color
        thisGlowTag = d.GlowTag("-{0:.2f}".format(self.allCosts[costIndex])+" "+self.allResources[costIndex].shortTag,\
            startColor,self.allResources[costIndex].color,17,40)
        return thisGlowTag

    def check(self):
        okay = True
        index = 0
        for cost in self.allCosts:
            if cost > self.allResources[index].quantity:
                okay = False
            index += 1
        return okay

    def makeBuy(self):
        index = 0
        for cost in self.allCosts:
            self.allResources[index].quantity -= cost
            self.allResources[index].baseConsumption += cost
            if cost > 0:
                self.allResources[index].deficit += 10 + int(cost/2)
            index += 1

        
        
class Builder:
    def __init__(self,screen,anchorLoc,baseObject):
        self.base = baseObject
        self.noCost = Cost(self.base,[0,0,0,0,0,0,0])
        nextButtonA = d.Button("NEXT")
        habitatButton = d.Button("HABITATS",img = a.whiteL)
        storageButton = d.Button("STORAGE",img = a.greyL)
        lifeSuportButton = d.Button("LIFE SUPPORT",img = a.greenL)
        recycleButton = d.Button("RECYCLE",img = a.aquaL)
        transportationButton = d.Button("TRANSPORT",img = a.blueL)
        
        powerButton = d.Button("POWER",img = a.yellowXSD)
        extractionButton = d.Button("EXTRACTION",img = a.redXSD)
        industryButton = d.Button("INDUSTRY",img = a.orangeXSD)
        labButton = d.Button("LAB",img = a.purpleXSD)
        adminButton = d.Button("ADMIN",img = a.pinkXSD)
        nextButtonB = d.Button("NEXT")

        regolithButton = d.Button("REGOLITH")
        oreButton = d.Button("ORE")
        waterButton = d.Button("WATER")
        rareButton = d.Button("RARE")
        backExtractionButton = d.Button("BACK")
        extractionButtonList = [regolithButton,oreButton,waterButton,rareButton,backExtractionButton]

        concreteButton = d.Button("CONCRETE")
        metalButton = d.Button("METAL")
        fuelButton = d.Button("FUEL")
        medsButton = d.Button("MEDS")
        electronicsButton = d.Button("ELECTRONICS")
        plasticsButton = d.Button("PLASTICS")
        waterIndButton = d.Button("WATER")
        backIndustryButton = d.Button("BACK")
        robotsButton = d.Button("ROBOTS")
        industryButtonList = [concreteButton,metalButton,fuelButton,medsButton,\
            electronicsButton,plasticsButton,waterIndButton,robotsButton,backIndustryButton]
        
        panelAList = [habitatButton,storageButton,lifeSuportButton,\
            recycleButton,transportationButton,nextButtonA]
        panelBList = [powerButton,extractionButton,industryButton,\
            labButton,adminButton,nextButtonB]
        
        self.anchorLoc = anchorLoc
        self.panelA = d.ControlPanel(screen,anchorLoc,panelAList)
        self.panelB = d.ControlPanel(screen,anchorLoc,panelBList)

        self.habitatCapsules = [marsHomeCapsule,basicHabitatCapsule,crewQuartersCapsule,\
            bunksCapsule,dormitoryCapsule,apartmentBlockCapsule,domeHabCapsule,\
                townhouseCapsule,luxuryApartmentCapsule]
        self.lifeSupportCapsules = [airModCapsule, farmPodCapsule, meatLabCapsule, greenHouseCapsule,\
            farmDomeCapsule, foodFactoryCapsule, gardenCapsule, megaGardenCapsule, terrariumCapsule]
        self.waterExtractionCapsules = [vaporizerCapsule,iceDrillCapsule,vaporFarmCapsule,\
            icePitCapsule,iceMineCapsule,iceFacilityCapsule]
        self.regolithExtractionCapsules = [regolithPitCapsule, smallMineCapsule, regolithMineCapsule,\
            regolithOreMineCapsule, regolithExcavationCapsule, fullDigCapsule]
        self.oreExtractionCapsules = [orePitCapsule, smallMineCapsule, oreMineCapsule,\
            regolithOreMineCapsule, oreExcavationCapsule, fullDigCapsule]
        self.rareExtractionCapsules = [rareSiteCapsule, smallMineCapsule, rareMineCapsule, \
            hiTechMineCapsule, fullDigCapsule]
        self.concreteIndCapsules = [concreteMixerCapsule,concreteWorkshopCapsule,\
            concretePlantCapsule,concreteFactoryCapsule ]
        self.metalIndCapsules = [autoSmelterCapsule,metalsmithCapsule,steelMillCapsule,metalFactoryCapsule]
        self.fuelIndCapsules = [electrolyserCapsule,fuelWorkshopCapsule,fuelPlantCapsule,refineryCapsule ]
        self.medsIndCapsules = [medicalLabCapsule,medsFacilityCapsule,medsFactoryCapsule]
        self.electronicsIndCapsules = [electronicsWorkshopCapsule,circuitPlantCapsule,eManufacturerCapsule]
        self.plasticsIndCapsules = [polymerPodCapsule,plasticsPlantCapsule,plasticsFactoryCapsule]
        self.waterIndCapsules = [regOvenCapsule,rockCookerCapsule,marsEvaporatorCapsule,regolithSteamerCapsule]
        self.powerCapsules = [batteryComplexCapsule, generatorCapsule, solarPanelCapsule, simpleReactorCapsule,\
            solarClusterCapsule,fusionReactorCapsule,solarFarmCapsule,superReactorCapsule]
        self.storageCapsules = [storeShedCapsule,airTanksCapsule,reservoirCapsule,pantryCapsule,\
            vitalsCapsule,hangarCapsule,warehouseCapsule,depotCapsule,storageTunnelsCapsule]
        self.transportCapsules = [earthAntennaCapsule, commsCenterCapsule, controlTowerCapsule,\
            launchPadCapsule, spacePortCapsule]
        self.labCapsules = [surveyPostCapsule,fieldLabCapsule,laboratoryCapsule,scienceComplexCapsule,\
            medBotCapsule,fieldHospitalCapsule,hospitalCapsule]
        self.adminCapsules = [officePodCapsule,mainOfficeCapsule,nerveCenterCapsule,\
            hqCapsule,aiNodeCapsule,trainingTerminalCapsule,schoolPodCapsule,spaceCollegeCapsule]
        self.recycleCapsules = [composterCapsule,h2oTreatmentCapsule,airFiltrationCapsule,\
            biocyclerCapsule,wastewaterPlantCapsule,airRecyclerCapsule,recycleHubCapsule]
        self.robotsIndCapsules = [roboPodCapsule,robotWorkshopCapsule,robotFactoryCapsule]
        
        self.habitatPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.habitatCapsules))
        self.storagePanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.storageCapsules))
        self.lifeSupportPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.lifeSupportCapsules))
        self.recyclePanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.recycleCapsules))
        self.transportPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.transportCapsules))

        self.industryPanel = d.ControlPanel(screen,anchorLoc,industryButtonList)
        self.concreteIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.concreteIndCapsules))
        self.metalIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.metalIndCapsules))
        self.fuelIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.fuelIndCapsules))
        self.medsIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.medsIndCapsules))
        self.electronicsIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.electronicsIndCapsules))
        self.plasticsIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.plasticsIndCapsules))
        self.waterIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.waterIndCapsules))
        self.robotsIndPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.robotsIndCapsules))

        self.extractionPanel = d.ControlPanel(screen,anchorLoc,extractionButtonList)
        self.waterExtractionPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.waterExtractionCapsules))
        self.regolithExtractionPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.regolithExtractionCapsules))
        self.oreExtractionPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.oreExtractionCapsules))
        self.rareExtractionPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.rareExtractionCapsules))

        self.adminPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.adminCapsules))
        self.labPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.labCapsules))
        self.powerPanel = d.ControlPanel(screen,anchorLoc,self.buttonsFromCapsules(self.powerCapsules))

        ## SPACE BUTTONS LIVE HERE ##

        earthButtons1 = self.buttonsFromCapsules([smallCrewLanderCapsule,landerHabitatCapsule,\
            marsTranspoCapsule,airLanderCapsule,waterLanderCapsule,foodLanderCapsule,luxuryCargoCapsule])
            
        earthButtons2 = self.buttonsFromCapsules([supplyLanderCapsule,builderLanderCapsule,\
            recycleLanderCapsule,powerLanderCapsule,minerBotLanderCapsule,probeLanderCapsule,medDepotCapsule])

        orbitalButtons1 = self.buttonsFromCapsules([crewDropCapsule,prefabSolarCapsule,\
            commandRelayLanderCapsule,concreteDropCapsule,metalDropCapsule])
            
        orbitalButtons2 = self.buttonsFromCapsules([shuttleCapsule,medsDropCapsule,\
            electronicsDropCapsule,plasticsDropCapsule,orbitalAirCapsule,orbitalWaterCapsule,orbitalFoodCapsule])

        rocketButtons1 = self.buttonsFromCapsules([aquaRocketCapsule,blueRocketCapsule,\
            greenRocketCapsule,dGreenRocketCapsule,dRedRocketCapsule,redRocketCapsule,pinkRocketCapsule])

        rocketButtons2 = self.buttonsFromCapsules([whiteRocketCapsule,greyRocketCapsule,\
            orangeRocketCapsule,purpleRocketCapsule,hYellowRocketCapsule,hOrangeRocketCapsule,robotRocketCapsule])
        earthButtons1.remove(earthButtons1[len(earthButtons1)-1])
        earthButtons2.remove(earthButtons2[len(earthButtons2)-1])
        rocketButtons1.remove(rocketButtons1[len(rocketButtons1)-1])
        rocketButtons2.remove(rocketButtons2[len(rocketButtons2)-1])
        orbitalButtons1.remove(orbitalButtons1[len(orbitalButtons1)-1])
        orbitalButtons2.remove(orbitalButtons2[len(orbitalButtons2)-1])

        clearBack = d.getHorizontalBar(screen.get_width(),80)
        clearBack.set_alpha(0)
        gap = 35
        panelHt = 55
        self.earthPanel1 = d.ControlPanel(screen,(gap,gap+panelHt),earthButtons1,clearBack)
        self.earthPanel2 = d.ControlPanel(screen,(gap,gap+2*panelHt),earthButtons2,clearBack)
        self.rocketPanel1 = d.ControlPanel(screen,(gap,screen.get_height()-2*panelHt-gap),rocketButtons1,clearBack)
        self.rocketPanel2 = d.ControlPanel(screen,(gap,screen.get_height()-panelHt-gap),rocketButtons2,clearBack)
        self.orbitalPanel1 = d.ControlPanel(screen,(gap,gap+4*panelHt),orbitalButtons1,clearBack)
        self.orbitalPanel2 = d.ControlPanel(screen,(gap,gap+5*panelHt),orbitalButtons2,clearBack)


        self.subPanel = False
        self.panelToggle = True #True for A, False for B
        self.activeBuilding = None
        self.activeCost = None
        self.buildingSize = ""
        self.buildingPreviewU = None
        self.buildingPreviewD = None
        self.buildingPreviewR = None
        self.buildingPreviewL = None
        self.tileOpen = False
        self.landing = False
        self.launchObject = None
        self.bonusTag = ""
        self.adjacencyBonus = 1.0

    def refreshButtons(self,screen,anchorLoc):
        # This is slow, COST obj updates, need to update mouseovers
        self.updateMouseOverFromList(self.habitatPanel.buttonList)
        self.updateMouseOverFromList(self.storagePanel.buttonList)
        self.updateMouseOverFromList(self.lifeSupportPanel.buttonList) 
        self.updateMouseOverFromList(self.recyclePanel.buttonList)        
        self.updateMouseOverFromList(self.transportPanel.buttonList)
        self.updateMouseOverFromList(self.concreteIndPanel.buttonList)
        self.updateMouseOverFromList(self.metalIndPanel.buttonList)
        self.updateMouseOverFromList(self.fuelIndPanel.buttonList)
        self.updateMouseOverFromList(self.medsIndPanel.buttonList)
        self.updateMouseOverFromList(self.electronicsIndPanel.buttonList)
        self.updateMouseOverFromList(self.plasticsIndPanel.buttonList)
        self.updateMouseOverFromList(self.waterIndPanel.buttonList)
        self.updateMouseOverFromList(self.robotsIndPanel.buttonList)

        self.updateMouseOverFromList(self.waterExtractionPanel.buttonList)
        self.updateMouseOverFromList(self.regolithExtractionPanel.buttonList)
        self.updateMouseOverFromList(self.oreExtractionPanel.buttonList)
        self.updateMouseOverFromList(self.rareExtractionPanel.buttonList)

        self.updateMouseOverFromList(self.adminPanel.buttonList)
        self.updateMouseOverFromList(self.labPanel.buttonList)
        self.updateMouseOverFromList(self.powerPanel.buttonList)


    def reset(self):
        self.subPanel = False
        self.panelToggle = True
        self.tileOpen = False
        self.landing = False
        self.activeBuilding = None
        self.bonusTag = ""
        self.adjacencyBonus = 1.0
        self.activeCost = None
        self.resetPanel(self.panelA)
        self.resetPanel(self.panelB)
        self.resetPanel(self.extractionPanel)
        self.resetPanel(self.industryPanel)

    def resetPanel(self,panel):
        for button in panel.buttonList:
            if button.selected:
                button.toggleSelected()
        self.activeBuilding = None
        self.bonusTag = ""
        self.adjacencyBonus = 1.0
        self.activeCost = None

    def checkSubBackButton(self,panel): 
        if panel.buttonList[len(panel.buttonList)-1].selected:
            self.reset()
            self.resetPanel(panel)
            self.needUDLR = False

    def checkSelections(self):
        if self.panelToggle:
            index = 0
            for button in self.panelA.buttonList:
                if button.selected:
                    if index != 5:
                        self.subPanel = True
                    else:
                        self.panelToggle = False
                        button.toggleSelected()
                index += 1
        else:
            index = 0
            for button in self.panelB.buttonList:
                if button.selected:
                    if index != 5:
                        self.subPanel = True
                    else:
                        self.panelToggle = True
                        button.toggleSelected()
                index += 1

    def getPanel(self):
        returnPanel = None
        if self.subPanel:
            returnPanel = self.getSubPanel()
            self.checkSubBackButton(returnPanel)
            self.setActiveBuilding(returnPanel)
        else:
            self.checkSelections()
            if self.panelToggle:
                returnPanel = self.panelA
            else:
                returnPanel = self.panelB
        #slows down game too much
        for button in returnPanel.buttonList:
            if button.dataEmbed != None:
                if len(button.dataEmbed) > 7:
                    cost = Cost(self.base,button.dataEmbed[7])
                else:
                    cost = self.noCost
                if cost.check():
                    button.makeLive()
                else:
                    button.makeDead(protected=True)
        return returnPanel

    def getSubPanel(self):
        returnPanel = None
        if self.panelToggle:
            if self.panelA.buttonList[0].selected: # habitat
                returnPanel = self.habitatPanel
            if self.panelA.buttonList[1].selected: # storage
                returnPanel = self.storagePanel
            if self.panelA.buttonList[2].selected: #life support
                returnPanel = self.lifeSupportPanel
            if self.panelA.buttonList[3].selected:
                returnPanel = self.recyclePanel
            if self.panelA.buttonList[4].selected:
                returnPanel = self.transportPanel
        else:
            if self.panelB.buttonList[0].selected: #power
                returnPanel = self.powerPanel
            if self.panelB.buttonList[1].selected: #extraction
                if self.extractionPanel.buttonList[0].selected:
                    returnPanel = self.regolithExtractionPanel
                elif self.extractionPanel.buttonList[1].selected:
                    returnPanel = self.oreExtractionPanel
                elif self.extractionPanel.buttonList[2].selected:
                    returnPanel = self.waterExtractionPanel
                elif self.extractionPanel.buttonList[3].selected:
                    returnPanel = self.rareExtractionPanel
                else:
                    returnPanel = self.extractionPanel
            if self.panelB.buttonList[2].selected: #industry
                if self.industryPanel.buttonList[0].selected:
                    returnPanel = self.concreteIndPanel
                elif self.industryPanel.buttonList[1].selected:
                    returnPanel = self.metalIndPanel
                elif self.industryPanel.buttonList[2].selected:
                    returnPanel = self.fuelIndPanel
                elif self.industryPanel.buttonList[3].selected:
                    returnPanel = self.medsIndPanel
                elif self.industryPanel.buttonList[4].selected:
                    returnPanel = self.electronicsIndPanel
                elif self.industryPanel.buttonList[5].selected:
                    returnPanel = self.plasticsIndPanel
                elif self.industryPanel.buttonList[6].selected:
                    returnPanel = self.waterIndPanel
                elif self.industryPanel.buttonList[7].selected:
                    returnPanel = self.robotsIndPanel
                else:
                    returnPanel = self.industryPanel
            if self.panelB.buttonList[3].selected: #lab
                returnPanel = self.labPanel
            if self.panelB.buttonList[4].selected: #admin
                returnPanel = self.adminPanel
        return returnPanel


    def getBonusReadout(self,connectedBuildings):
        readout = None
        if self.bonusTag == "STORAGE":
            initialized = False
            for building in connectedBuildings:
                if isinstance(building,StorageBuilding):
                    if initialized == False:
                        initialized = True
                        self.adjacencyBonus = 1.0 + ((building.generalStorage/400.0))
                    else:
                        self.adjacencyBonus += ((building.generalStorage/400.0))
            if initialized:
                readout = d.getTextSurface("{0:.1f}%".format(100*self.adjacencyBonus)+" G.S.",size=13)
        if self.bonusTag == "POW":
            eff = 1.0
            initialized = False
            for building in connectedBuildings:
                if isinstance(building,LabBuilding):
                    if building.output > 0.0:
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.output/10.0)
                        else:
                            eff += (building.output/10.0)
            if initialized:
                readout = d.getTextSurface("{0:.1f}%".format(100*eff),size=13) 
        if self.bonusTag == "MED":
            eff = 1.0
            initialized = False
            for building in connectedBuildings:
                if isinstance(building,IndustryBuilding) and building.buildingName in medsBuildings:
                    if initialized == False:
                        initialized = True
                        eff = 1.0 + (building.efficiency/10.0)
                    else:
                        eff += (building.efficiency/10.0)
            if initialized:
                readout = d.getTextSurface("{0:.1f}%".format(100*eff),size=13) 
        if self.bonusTag == "EDU":
            eff = 1.0
            initialized = False
            for building in connectedBuildings:
                if isinstance(building,LabBuilding):
                    if building.output > 0.0:
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.output/10.0)
                        else:
                            eff += (building.output/10.0)
            if initialized:
                readout = d.getTextSurface("{0:.1f}%".format(100*eff),size=13) 
        if self.bonusTag == "LS":
            eff = 1.0
            initialized = False
            for building in connectedBuildings:
                if isinstance(building,RecycleBuilding):
                    if initialized == False:
                        initialized = True
                        eff = 1.0 + (building.actualEfficiency-0.75)
                    else:
                        eff += (building.actualEfficiency-0.75)
                if isinstance(building,LabBuilding):
                    if building.output > 0.0:
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.output/10.0)
                        else:
                            eff += (building.output/10.0)
            if initialized:
                readout = d.getTextSurface("{0:.1f}%".format(100*eff),size=13) 
        if self.bonusTag == "EX":
            initialized = False
            power = False
            eff = 1.0
            for building in connectedBuildings:
                if isinstance(building,PowerBuilding):
                    power = True
                if isinstance(building,AdminBuilding):
                    if building.output > 1.0:
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.output/20.0)
                        else:
                            eff += (building.output/20.0) 
            if initialized or power:
                if power:
                    indTag = " +E"
                else:
                    indTag = ""
                readout = d.getTextSurface("{0:.1f}%".format(100*eff)+indTag,size=13)    
        if self.bonusTag == "HAB":
            initialized = False
            eff = 1.0
            for building in connectedBuildings:
                if isinstance(building,LifeSupportBuilding):
                    if initialized == False:
                        if building.organicsOutput > 0:
                            initialized = True
                            eff = 1.0 + ((building.organicsOutput/4.0))
                    else:
                        if building.organicsOutput > 0:
                            eff += ((building.organicsOutput/4.0))
                if isinstance(building,LabBuilding):
                    if building.medicalFactor > 0.0:
                        if initialized == False:
                            eff = 1.0 + (building.medicalFactor/15.0)
                        else:
                            eff += (building.medicalFactor/15.0)
                if isinstance(building,AdminBuilding):
                    if building.educationFactor > 0.0:
                        if initialized == False:
                            eff = 1.0 + (building.educationFactor/15.0)
                        else:
                            eff += (building.educationFactor/15.0)
                if isinstance(building,LaunchPad) or isinstance(building,SpacePort) or isinstance(building,ExtractionBuilding):
                    if initialized == False:
                        initialized = True
                        eff = 0.9
                    else:
                        eff -= 0.1
            if initialized:
                readout = d.getTextSurface("{0:.1f}%".format(100*eff)+" PSYCH",size=13)
        if self.bonusTag != "" and self.bonusTag[0] == 'I':
            initialized = False
            power = False
            eff = 1.0
            for building in connectedBuildings:
                if isinstance(building,PowerBuilding):
                    power = True
                if isinstance(building,ExtractionBuilding):
                    if building.water == True and (self.bonusTag[-1] == 'C' or self.bonusTag[-1] == 'F'):
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.extractionEfficiency/10.0)
                        else:
                            eff += (building.extractionEfficiency/10.0)
                    if building.regolith == True and (self.bonusTag[-1] == 'C' or self.bonusTag[-1] == 'W'):
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.extractionEfficiency/10.0)
                        else:
                            eff += (building.extractionEfficiency/10.0)
                    if building.ore == True and self.bonusTag[-1] == 'M':
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.extractionEfficiency/10.0)
                        else:
                            eff += (building.extractionEfficiency/10.0)
                    if building.rare ==True and (self.bonusTag[-1] == 'D' or self.bonusTag[-1] == 'E'):
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.extractionEfficiency/10.0)
                        else:
                            eff += (building.extractionEfficiency/10.0)
                if isinstance(building,IndustryBuilding):
                    if building.buildingName in metalBuildings and self.bonusTag[-1] == 'E':
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.efficiency/10.0)
                        else:
                            eff += (building.efficiency/10.0)
                    if building.buildingName in fuelBuildings and self.bonusTag[-1] == 'P':
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.efficiency/10.0)
                        else:
                            eff += (building.efficiency/10.0)
                    if building.buildingName in waterBuildings and self.bonusTag[-1] == 'C':
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.efficiency/10.0)
                        else:
                            eff += (building.efficiency/10.0)
                if isinstance(building,LifeSupportBuilding):
                    if building.organicsOutput > 0.0 and self.bonusTag[-1] == 'D':
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.organicsOutput/3.0)
                        else:
                            eff += (building.organicsOutput/3.0)
                    if building.airOutput > 0.0 and self.bonusTag[-1] == 'F':
                        if initialized == False:
                            initialized = True
                            eff = 1.0 + (building.airOutput*2.0)
                        else:
                            eff += (building.airOutput*2.0)
            if initialized or power:
                if power:
                    indTag = " PROD +E"
                else:
                    indTag = " PROD"
                readout = d.getTextSurface("{0:.1f}%".format(100*eff)+indTag,size=13)    
        return readout

    def drawPreview(self,tile,screen,loc):
        preview = a.blank
        if self.buildingSize == 'L':
            possiblePreview = self.buildingPreviewU
            bonusLoc = tile.clickAnchor
            quad = "all"
            connectedBuildings = tile.checkConnected()
        else:
            if tile.mouseUp:
                possiblePreview = self.buildingPreviewU
                bonusLoc = tile.upAnchor
                if self.buildingSize == "M":
                    quad = "ur"
                else:
                    quad = "u"
            if tile.mouseDown:
                possiblePreview = self.buildingPreviewD
                bonusLoc = tile.downAnchor
                if self.buildingSize == "M":
                    quad = "dl"
                else:
                    quad = "d"
            if tile.mouseRight:
                possiblePreview = self.buildingPreviewR
                bonusLoc = tile.rightAnchor
                if self.buildingSize == "M":
                    quad = "rd"
                else:
                    quad = "r"
            if tile.mouseLeft:
                possiblePreview = self.buildingPreviewL
                bonusLoc = tile.leftAnchor
                if self.buildingSize == "M":
                    quad = "lu"
                else:
                    quad = "l"
            if self.landing:
                connectedBuildings = tile.checkConnected(quad)
                quad = "all"
            else:
                connectedBuildings = tile.checkConnected(quad)
        connection = False
        if len(connectedBuildings) > 0 or self.landing:
            connection = True
        if tile.checkOpen(quad) and connection:
            preview = possiblePreview
            self.tileOpen = True
        else:
            tile.drawNo(screen,quad)
            self.tileOpen = False
        if self.tileOpen:
            bonusReadout = self.getBonusReadout(connectedBuildings)
        else:
            bonusReadout = None
        screen.blit(preview,loc)
        if bonusReadout != None:
            screen.blit(bonusReadout,(bonusLoc[0]-int(bonusReadout.get_width()/2),(bonusLoc[1]-2*bonusReadout.get_height())))
        for building in connectedBuildings:
            bonusSurface = building.checkBonusPreview(self.activeBuilding)
            if bonusSurface != None:
                if building.bonusAnimation == False:
                    building.bonusAnimation = True
                    if building.udlr == 'u':
                        fadeLoc = building.tile.upAnchor
                    elif building.udlr == 'd':
                        fadeLoc = building.tile.downAnchor
                    elif building.udlr == 'l':
                        fadeLoc = building.tile.leftAnchor
                    else:
                        fadeLoc = building.tile.rightAnchor
                    newAnimation = d.Animation([bonusSurface],(fadeLoc[0]-int(bonusSurface.get_width()/2),\
                        fadeLoc[1]-2*bonusSurface.get_height()),fadeOut=True,alphaVelocity=-10,triggerObject = building)
                    building.tile.addAnimation(newAnimation)


    def fadePreview(self,surface):
        surfaceNew = surface.copy()
        surfaceNew.set_alpha(150)
        return surfaceNew

    def buttonsFromCapsules(self,capsuleList):
        buttonList = []
        for capsule in capsuleList:
            if isinstance(capsule[0],str):
                tag = capsule[0]
            else:
                tag = capsule[0][0]
            newButton = d.Button(tag,img = capsule[4])
            if len(capsule)>6:
                newButton.mouseOverInfo = True
                newButton.makeMouseOver(capsule[6])
                if len(capsule)>7:
                    newCost = Cost(self.base,capsule[7])
                    newButton.makeBuildingMouseOver(capsule,newCost)
            newButton.dataEmbed = capsule    
            buttonList.append(newButton)
        backButton = d.Button("BACK")
        buttonList.append(backButton)
        return buttonList

    def updateMouseOverFromList(self,buttonList):
        for button in buttonList:
            if button.dataEmbed != None:
                if len(button.dataEmbed)>7:
                    newCost = Cost(self.base,button.dataEmbed[7])
                    button.makeBuildingMouseOver(button.dataEmbed,newCost)

    def unpackBuilding(self,capsule):
        if isinstance(capsule[0],str):
            self.activeBuilding = capsule[0]
        else:
            self.activeBuilding = capsule[0][0]
            self.bonusTag = capsule[0][1]
        if len(capsule) > 7:
            self.activeCost = Cost(self.base,capsule[7])
        else:
            self.activeCost = self.noCost
        self.buildingSize = capsule[1]
        self.buildingPreviewU = self.fadePreview(capsule[2])
        self.buildingPreviewD = self.fadePreview(capsule[3])
        self.buildingPreviewR = self.fadePreview(capsule[4])
        self.buildingPreviewL = self.fadePreview(capsule[5])

    def setActiveBuildingFromLaunch(self,launchObject):
        self.unpackBuilding(launchObject.capsule)
        self.landing = True
        self.launchObject = launchObject

    def setActiveBuilding(self,panel):
        # can be further streamlined
        if panel == self.habitatPanel:
            #capsuleList = habitatCapsules - just need to turn off next button
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.habitatCapsules[0])
            elif panel.buttonList[1].selected:
                self.unpackBuilding(self.habitatCapsules[1])
            elif panel.buttonList[2].selected:
                self.unpackBuilding(self.habitatCapsules[2])
            elif panel.buttonList[3].selected:
                self.unpackBuilding(self.habitatCapsules[3])
            elif panel.buttonList[4].selected:
                self.unpackBuilding(self.habitatCapsules[4])
            elif panel.buttonList[5].selected:
                self.unpackBuilding(self.habitatCapsules[5])
            elif panel.buttonList[6].selected:
                self.unpackBuilding(self.habitatCapsules[6])
            elif panel.buttonList[7].selected:
                self.unpackBuilding(self.habitatCapsules[7])
            elif panel.buttonList[8].selected:
                self.unpackBuilding(self.habitatCapsules[8])
            else:
                self.activeBuilding = None
                self.bonusTag = ""
                self.activeCost = None
        if panel == self.storagePanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.storageCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.storageCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.storageCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.storageCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.storageCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.storageCapsules[5])
            if panel.buttonList[6].selected:
                self.unpackBuilding(self.storageCapsules[6])
            if panel.buttonList[7].selected:
                self.unpackBuilding(self.storageCapsules[7])
            if panel.buttonList[8].selected:
                self.unpackBuilding(self.storageCapsules[8])
        if panel == self.lifeSupportPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.lifeSupportCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.lifeSupportCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.lifeSupportCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.lifeSupportCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.lifeSupportCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.lifeSupportCapsules[5])
            if panel.buttonList[6].selected:
                self.unpackBuilding(self.lifeSupportCapsules[6])
            if panel.buttonList[7].selected:
                self.unpackBuilding(self.lifeSupportCapsules[7])
            if panel.buttonList[8].selected:
                self.unpackBuilding(self.lifeSupportCapsules[8])
        if panel == self.recyclePanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.recycleCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.recycleCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.recycleCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.recycleCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.recycleCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.recycleCapsules[5])
            if panel.buttonList[6].selected:
                self.unpackBuilding(self.recycleCapsules[6])
        if panel == self.powerPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.powerCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.powerCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.powerCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.powerCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.powerCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.powerCapsules[5])
            if panel.buttonList[6].selected:
                self.unpackBuilding(self.powerCapsules[6])
            if panel.buttonList[7].selected:
                self.unpackBuilding(self.powerCapsules[7])
        if panel == self.waterExtractionPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.waterExtractionCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.waterExtractionCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.waterExtractionCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.waterExtractionCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.waterExtractionCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.waterExtractionCapsules[5])
        if panel == self.regolithExtractionPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.regolithExtractionCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.regolithExtractionCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.regolithExtractionCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.regolithExtractionCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.regolithExtractionCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.regolithExtractionCapsules[5])
        if panel == self.oreExtractionPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.oreExtractionCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.oreExtractionCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.oreExtractionCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.oreExtractionCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.oreExtractionCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.oreExtractionCapsules[5])
        if panel == self.rareExtractionPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.rareExtractionCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.rareExtractionCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.rareExtractionCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.rareExtractionCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.rareExtractionCapsules[4])
        if panel == self.concreteIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.concreteIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.concreteIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.concreteIndCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.concreteIndCapsules[3])
        if panel == self.metalIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.metalIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.metalIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.metalIndCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.metalIndCapsules[3])
        if panel == self.fuelIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.fuelIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.fuelIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.fuelIndCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.fuelIndCapsules[3])
        if panel == self.medsIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.medsIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.medsIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.medsIndCapsules[2])
        if panel == self.electronicsIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.electronicsIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.electronicsIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.electronicsIndCapsules[2])
        if panel == self.plasticsIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.plasticsIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.plasticsIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.plasticsIndCapsules[2])
        if panel == self.waterIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.waterIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.waterIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.waterIndCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.waterIndCapsules[3])
        if panel == self.robotsIndPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.robotsIndCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.robotsIndCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.robotsIndCapsules[2])
        if panel == self.labPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.labCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.labCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.labCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.labCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.labCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.labCapsules[5])
            if panel.buttonList[6].selected:
                self.unpackBuilding(self.labCapsules[6])
        if panel == self.adminPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.adminCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.adminCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.adminCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.adminCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.adminCapsules[4])
            if panel.buttonList[5].selected:
                self.unpackBuilding(self.adminCapsules[5])
            if panel.buttonList[6].selected:
                self.unpackBuilding(self.adminCapsules[6])
            if panel.buttonList[7].selected:
                self.unpackBuilding(self.adminCapsules[7])
        if panel == self.transportPanel:
            if panel.buttonList[0].selected:
                self.unpackBuilding(self.transportCapsules[0])
            if panel.buttonList[1].selected:
                self.unpackBuilding(self.transportCapsules[1])
            if panel.buttonList[2].selected:
                self.unpackBuilding(self.transportCapsules[2])
            if panel.buttonList[3].selected:
                self.unpackBuilding(self.transportCapsules[3])
            if panel.buttonList[4].selected:
                self.unpackBuilding(self.transportCapsules[4])




    def createBuildingObject(self,base,tile,spaceport = False):
        #if self.landing - start animation - init DOES NOT add to build list - add tile animation?
        print("create:"+str(self.adjacencyBonus))
        self.activeCost.makeGlow()
        yLoc = tile.anchor[1]
        for tag in self.activeCost.tags:
            newAnimation = d.Animation([tag],\
                (tile.anchor[0],yLoc),xVelocity=2,yVelocity=-1,yLimit=0,)
            tile.addAnimation(newAnimation)
            yLoc+=tag.get_height()
        if self.buildingSize == "L":
            udlr = 'u'
        elif spaceport:
            udlr = 'r'
        else:
            if tile.mouseUp:
                udlr = 'u'
            if tile.mouseDown:
                udlr = 'd'
            if tile.mouseRight:
                udlr = 'r'
            if tile.mouseLeft:
                udlr = 'l'
        if self.activeCost != None:
            self.activeCost.makeBuy()
        if self.activeBuilding == "BASIC HAB":
            buildingObject = BasicHabitat(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MARS HOME":
            buildingObject = MarsHome(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "CREW QUARTERS":
            buildingObject = CrewQuarters(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "BUNKS":
            buildingObject = Bunks(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "DORMITORY":
            buildingObject = Dormitory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "APT. BLOCK":
            buildingObject = ApartmentBlock(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "DOME HAB":
            buildingObject = DomeHab(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "TOWNHOUSE":
            buildingObject = Townhouse(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "LUXURY APT.":
            buildingObject = LuxuryApartment(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SHED":
            buildingObject = StoreShed(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "AIR TANKS":
            buildingObject = AirTanks(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "RESERVOIR":
            buildingObject = Reservoir(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "PANTRY":
            buildingObject = Pantry(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "VITALS":
            buildingObject = Vitals(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "HANGAR":
            buildingObject = Hangar(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "WAREHOUSE":
            buildingObject = Warehouse(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "DEPOT":
            buildingObject = Depot(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "STORAGE TUNNELS":
            buildingObject = StorageTunnels(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "AIR MOD":
            buildingObject = AirMod(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "GARDEN":
            buildingObject = Garden(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MEGA GARDEN":
            buildingObject = MegaGarden(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "TERRARIUM":
            buildingObject = Terrarium(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FARM POD":
            buildingObject = FarmPod(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MEAT LAB":
            buildingObject = MeatLab(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "GREENHOUSE":
            buildingObject = GreenHouse(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FARM DOME":
            buildingObject = FarmDome(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FOOD FACTORY":
            buildingObject = FoodFactory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "VAPORIZER":
            buildingObject = Vaporizer(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ICE DRILL":
            buildingObject = IceDrill(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "VAPOR FARM":
            buildingObject = VaporFarm(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ICE PIT":
            buildingObject = IcePit(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ICE MINE":
            buildingObject = IceMine(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ICE FACILITY":
            buildingObject = IceFacility(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "REGOLITH PIT":
            buildingObject = RegolithPit(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ORE PIT":
            buildingObject = OrePit(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "RARE SITE":
            buildingObject = RareSite(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "REGOLITH MINE":
            buildingObject = RegolithMine(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ORE MINE":
            buildingObject = OreMine(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "RARE MINE":
            buildingObject = RareMine(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SURFACE SCRAPE":
            buildingObject = RegolithOreMine(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "REGOLITH FIELD":
            buildingObject = RegolithExcavation(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ORE EXCAVATION":
            buildingObject = OreExcavation(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "HI-TECH MINE":
            buildingObject = HiTechMine(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SMALL MINE":
            buildingObject = SmallMine(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FULL DIG":
            buildingObject = FullDig(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "BATTERY COMPLEX":
            buildingObject = BatteryComplex(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SOLAR PANEL":
            buildingObject = SolarPanel(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "GENERATOR":
            buildingObject = Generator(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SIMPLE REACTOR":
            buildingObject = SimpleReactor(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SOLAR CLUSTER":
            buildingObject = SolarCluster(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FUSION REACTOR":
            buildingObject = FusionReactor(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SOLAR FARM":
            buildingObject = SolarFarm(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SUPER REACTOR":
            buildingObject = SuperReactor(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "CONCRETE MIXER":
            buildingObject = ConcreteMixer(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "CONCRETE WORKSHOP":
            buildingObject = ConcreteWorkshop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "CONCRETE PLANT":
            buildingObject = ConcretePlant(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "CONCRETE FACTORY":
            buildingObject = ConcreteFactory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "AUTO SMELTER":
            buildingObject = AutoSmelter(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "METALSMITH":
            buildingObject = Metalsmith(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "STEEL MILL":
            buildingObject = SteelMill(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "METAL FACTORY":
            buildingObject = MetalFactory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ELECTROLYSER":
            buildingObject = Electrolyser(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FUEL WORKSHOP":
            buildingObject = FuelWorkshop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FUEL PLANT":
            buildingObject = FuelPlant(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "REFINERY":
            buildingObject = Refinery(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MEDICAL LAB":
            buildingObject = MedicalLab(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MEDS FACILITY":
            buildingObject = MedsFacility(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MEDS FACTORY":
            buildingObject = MedsFactory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ELECTRONICS SHOP":
            buildingObject = ElectronicsWorkshop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "CIRCUIT PLANT":
            buildingObject = CircuitPlant(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "E-MANUFACTURER":
            buildingObject = EManufacturer(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "POLYMER POD":
            buildingObject = PolymerPod(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "PLASTICS PLANT":
            buildingObject = PlasticsPlant(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "PLASTICS FACTORY":
            buildingObject = PlasticsFactory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "REG OVEN":
            buildingObject = RegOven(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ROCK COOKER":
            buildingObject = RockCooker(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MARS EVAPORATOR":
            buildingObject = MarsEvaporator(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "REGOLITH STEAMER":
            buildingObject = RegolithSteamer(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ROBO-POD":
            buildingObject = RoboPod(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ROBOT WORKSHOP":
            buildingObject = RobotWorkshop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "ROBOT FACTORY":
            buildingObject = RobotFactory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SURVEY POST":
            buildingObject = SurveyPost(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FIELD LAB":
            buildingObject = FieldLab(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "LABORATORY":
            buildingObject = Laboratory(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SCIENCE COMPLEX":
            buildingObject = ScienceComplex(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MED BOT":
            buildingObject = MedBot(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "FIELD HOSPITAL":
            buildingObject = FieldHospital(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "HOSPITAL":
            buildingObject = Hospital(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "OFFICE POD":
            buildingObject = OfficePod(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "MAIN OFFICE":
            buildingObject = MainOffice(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "NERVE CENTER":
            buildingObject = NerveCenter(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "HQ":
            buildingObject = HQ(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "AI NODE":
            buildingObject = AINode(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "TRAINING TERM.":
            buildingObject = TrainingTerminal(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SCHOOL POD":
            buildingObject = SchoolPod(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SPACE COLLEGE":
            buildingObject = SpaceCollege(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "COMPOSTER":
            buildingObject = Composter(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "H2O TREATMENT":
            buildingObject = H2oTreatment(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "AIR FILTRATION":
            buildingObject = AirFiltration(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "BIOCYCLER":
            buildingObject = Biocycler(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "WASTEWATER PLANT":
            buildingObject = WastewaterPlant(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "AIR RECYCLER":
            buildingObject = AirRecycler(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "RECYCLE HUB":
            buildingObject = RecycleHub(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "EARTH ANTENNA":
            buildingObject = EarthAntenna(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "CONTROL TOWER":
            buildingObject = ControlTower(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "COMMS CENTER":
            buildingObject = CommsCenter(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "LAUNCH PAD":
            buildingObject = LaunchPad(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "SPACEPORT":
            buildingObject = SpacePort(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
        if self.activeBuilding == "LANDER HAB":
            buildingObject = LanderHabitat(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "SMALL CREW":
            buildingObject = SmallCrewLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "SHUTTLE":
            buildingObject = Shuttle(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "CREW DROP":
            buildingObject = CrewDrop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "MARS TRANSPO.":
            buildingObject = MarsTranspo(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "SUPPLY POD":
            buildingObject = SupplyLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "BUILDER POD":
            buildingObject = BuilderLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "RECYCLE POD":
            buildingObject = RecycleLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "EARTH REACTOR":
            buildingObject = PowerLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "PREFAB SOLAR":
            buildingObject = PrefabSolar(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "MINER BOT":
            buildingObject = MinerBotLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "PROBE":
            buildingObject = ProbeLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "LUX. CARGO":
            buildingObject = LuxuryCargo(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "MED DEPOT":
            buildingObject = MedDepot(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "COMM. RELAY":
            buildingObject = CommandRelay(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "AIR DROP":
            buildingObject = AirLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "WATER DROP":
            buildingObject = WaterLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "FOOD DROP":
            buildingObject = FoodLander(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "ORBITAL AIR":
            buildingObject = OrbitalAir(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "ORBITAL WATER":
            buildingObject = OrbitalWater(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "ORBITAL FOOD":
            buildingObject = OrbitalFood(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "CONCRETE DROP":
            buildingObject = ConcreteDrop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "METAL DROP":
            buildingObject = MetalDrop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "ELECT. DROP":
            buildingObject = ElectronicsDrop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "PLASTICS DROP":
            buildingObject = PlasticsDrop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        if self.activeBuilding == "MEDS DROP":
            buildingObject = MedsDrop(base.sol,base,tile,udlr,self.buildingSize,self.adjacencyBonus)
            self.launchObject.setLanded()
            self.launchObject = None
        self.reset()


class Map:
    def __init__(self,dimension):
        self.tileWidth = 64
        self.tileHeight = 64
        self.clickOffset = 33
        self.dimension = dimension #integer value of map h and w
        #creates grid of Tile objects
        self.grid = []
        xGrid = 1
        while xGrid <= dimension:
            thisRow = []
            yGrid = 1
            while yGrid <= dimension:
                newTile = Tile(xGrid,yGrid,self)
                thisRow.append(newTile)
                yGrid +=1
            self.grid.append(thisRow) 
            xGrid += 1
        self.width = self.tileWidth * dimension
        self.height = self.tileHeight * dimension 

    def getStartDraw(self,center):
        x = center[0] - int(self.tileHeight/2)
        y = center[1] - int(self.height / 4)
        return (x,y)
        
class Tile:
    def __init__(self,x,y,tMap):
        self.map = tMap
        self.x = x
        self.y = y
        self.selected = False
        self.exploreAnnounce = False
        self.mouseOver = False
        self.mouseUp = False
        self.mouseDown = False
        self.mouseRight = False
        self.mouseLeft = False
        self.upBuilding = None
        self.downBuilding = None
        self.rightBuilding = None
        self.leftBuilding = None
        self.anchor = (0,0)
        self.clickAnchor = (0,0) # Tuple assigned each draw loop - center of tile
        # center of each quadrant
        self.upAnchor = (0,0)
        self.downAnchor = (0,0)
        self.rightAnchor = (0,0)
        self.leftAnchor = (0,0)
        self.upOpen = True
        self.downOpen = True
        self.rightOpen = True
        self.leftOpen = True
        self.debrisKey = [0,0,0,0]
        self.tileBuildings = []
        #info needs
        self.exploreProgress = 0 # out of 100
        self.explored = False
        self.setTerrain()
        self.setResource()
        self.mouseCount = 32   

    def getTileSurfaceObject(self):
        return d.TileSurface.grid[self.x-1][self.y-1]   
                    
    def setTerrain(self):
        upRand = random.randrange(0,20)
        downRand = random.randrange(0,20)
        rightRand = random.randrange(0,20)
        leftRand = random.randrange(0,20)
        if upRand == 1:
            self.upOpen = False
            self.debrisKey[0] = random.randrange(1,5)
        if downRand == 1:
            self.downOpen = False
            self.debrisKey[1] = random.randrange(1,5)
        if rightRand == 1:
            self.rightOpen = False
            self.debrisKey[2] = random.randrange(1,5)
        if leftRand == 1:
            self.leftOpen = False
            self.debrisKey[3] = random.randrange(1,5)


    def setResource(self):
        factor = 1.0
        quads = [self.upOpen,self.downOpen,self.rightOpen,self.leftOpen]
        for quad in quads:
            if quad == False:
                factor*=1.2
        self.regolith = random.uniform(3.0*factor,6.0*factor)
        self.ore = random.uniform(0.0,3.0*factor)
        self.water = random.uniform(-1.0/factor,2.0*factor)
        if self.water < 0:
            self.water = 0
        #rare method creates normal distribution around rareAnchor!
        rareAnchor = 0.5
        rareRange = random.uniform(-3.0/factor,3.0*factor)
        if rareRange > rareAnchor:
            self.rare = random.uniform(rareAnchor,rareRange)
        else:
            self.rare = random.uniform(rareRange,rareAnchor)
        if self.rare < 0:
            self.rare = 0

    def createInfoObject(self,delayed = False):
        tileSurface = d.TileSurface.grid[self.x-1][self.y-1]
        if delayed:
            tileSurface.infoObject = d.InfoObject(self,35)
        else: 
            tileSurface.infoObject = d.InfoObject(self)

    def checkConnected(self,quad = "all"):
        connectedBuildings = []
        if quad == "all":
            for row in self.map.grid:
                for tile in row:
                    if tile.y == self.y - 1 and tile.x == self.x:
                        if tile.rightBuilding != None:
                            connectedBuildings.append(tile.rightBuilding)
                        if tile.downBuilding != None:
                            if (tile.downBuilding != tile.rightBuilding):
                                connectedBuildings.append(tile.downBuilding)
                    if tile.y == self.y + 1 and tile.x == self.x:
                        if tile.leftBuilding != None:
                            connectedBuildings.append(tile.leftBuilding)
                        if tile.upBuilding != None:
                            if (tile.upBuilding != tile.leftBuilding):
                                connectedBuildings.append(tile.upBuilding)
                    if tile.x == self.x - 1 and tile.y == self.y:
                        if tile.leftBuilding != None:
                            connectedBuildings.append(tile.leftBuilding)
                        if tile.downBuilding != None:
                            if (tile.downBuilding != tile.leftBuilding):
                                connectedBuildings.append(tile.downBuilding)
                    if tile.x == self.x + 1 and tile.y == self.y:
                        if tile.rightBuilding != None:
                            connectedBuildings.append(tile.rightBuilding)
                        if tile.upBuilding != None:
                            if (tile.upBuilding != tile.rightBuilding):
                                connectedBuildings.append(tile.upBuilding)
        if quad == "u" or quad == "ur" or quad == "lu":
            if self.rightBuilding!=None and self.rightBuilding!=self.upBuilding:
                connectedBuildings.append(self.rightBuilding)
            if self.leftBuilding != None and self.leftBuilding!=self.upBuilding:
                connectedBuildings.append(self.leftBuilding)
            for row in self.map.grid:
                for tile in row:
                    if tile.y == self.y - 1 and tile.x == self.x:
                        if tile.rightBuilding != None:
                            connectedBuildings.append(tile.rightBuilding)
                    if tile.x == self.x - 1  and tile.y == self.y:
                        if tile.leftBuilding != None:
                            connectedBuildings.append(tile.leftBuilding) 
        if quad == "d" or quad == "dl" or quad == "rd":
            if self.rightBuilding!=None and self.rightBuilding!=self.downBuilding:
                connectedBuildings.append(self.rightBuilding)
            if self.leftBuilding != None and self.leftBuilding!=self.downBuilding:
                connectedBuildings.append(self.leftBuilding)
            for row in self.map.grid:
                for tile in row:
                    if tile.y == self.y + 1 and tile.x == self.x:
                        if tile.leftBuilding != None:
                            connectedBuildings.append(tile.leftBuilding) 
                    if tile.x == self.x + 1  and tile.y == self.y:
                        if tile.rightBuilding != None:
                            connectedBuildings.append(tile.rightBuilding) 
        if quad == "r" or quad == "ur" or quad == "rd":
            if self.upBuilding!=None and self.upBuilding!=self.rightBuilding:
                connectedBuildings.append(self.upBuilding)
            if self.downBuilding != None and self.downBuilding!=self.rightBuilding:
                connectedBuildings.append(self.downBuilding)
            for row in self.map.grid:
                for tile in row:
                    if tile.y == self.y + 1 and tile.x == self.x:
                        if tile.upBuilding != None:
                            if tile.upBuilding not in connectedBuildings:
                                connectedBuildings.append(tile.upBuilding)
                    if tile.x == self.x - 1  and tile.y == self.y:
                        if tile.downBuilding != None:
                            if tile.downBuilding not in connectedBuildings:
                                connectedBuildings.append(tile.downBuilding)
        if quad == "l" or quad == "dl" or quad == "lu":
            if self.upBuilding!=None and self.upBuilding!=self.leftBuilding:
                connectedBuildings.append(self.upBuilding)
            if self.downBuilding != None and self.downBuilding!=self.leftBuilding:
                connectedBuildings.append(self.downBuilding)
            for row in self.map.grid:
                for tile in row:
                    if tile.y == self.y - 1 and tile.x == self.x:
                        if tile.downBuilding != None:
                            if tile.downBuilding not in connectedBuildings:
                                connectedBuildings.append(tile.downBuilding)
                    if tile.x == self.x + 1  and tile.y == self.y:
                        if tile.upBuilding != None:
                            if tile.upBuilding not in connectedBuildings:
                                connectedBuildings.append(tile.upBuilding)
        return connectedBuildings
    
    def checkOpen(self, quad = "all"):
        openTile = False
        if quad == "all":
            if self.upOpen and self.downOpen and self.leftOpen and self.rightOpen:
                openTile = True
        if quad == "u":
            if self.upOpen:
                openTile = True
        if quad == "d":
            if self.downOpen:
                openTile = True
        if quad == "r":
            if self.rightOpen:
                openTile = True
        if quad == "l":
            if self.leftOpen:
                openTile = True
        if quad == "ur":
            if self.upOpen and self.rightOpen:
                openTile = True
        if quad == "dl":
            if self.downOpen and self.leftOpen:
                openTile = True
        if quad == "rd":
            if self.downOpen and self.rightOpen:
                openTile = True
        if quad == "lu":
            if self.upOpen and self.leftOpen:
                openTile = True
        return openTile

    def drawNo(self,screen,quad = "all"):
        if quad == "all":
            loc = (self.clickAnchor[0]-16,self.clickAnchor[1]-8)
        if quad == "u" or quad == "ur":
            loc = (self.upAnchor[0]-16,self.upAnchor[1]-8)
        if quad == "d" or quad == "dl":
            loc = (self.downAnchor[0]-16,self.downAnchor[1]-8)
        if quad == "r" or quad == "rd":
            loc = (self.rightAnchor[0]-16,self.rightAnchor[1]-8)
        if quad == "l" or quad == "lu":
            loc = (self.leftAnchor[0]-16,self.leftAnchor[1]-8)
        screen.blit(a.noTile,loc)

    def progressHandler(self,screen):
        if len(self.tileBuildings) > 0 or self.exploreProgress > 0:
            if self.exploreProgress > 0 and self.exploreProgress < 100:
                self.drawProgressBar(screen, self.exploreProgress, 100, c.purple)
            for building in self.tileBuildings:
                if building.finished == False and building.lander == False:
                    if isinstance(building,RobotDummy):
                        if (building not in building.base.buildList) and (building.buildLoc.shutoff == False):
                            building.base.buildList.append(building)
                        if isinstance(self.downBuilding,IndustryBuilding) and self.downBuilding.robots:
                            quad = "d"
                        elif isinstance(self.rightBuilding,IndustryBuilding) and self.rightBuilding.robots:
                            quad = "r"
                        elif isinstance(self.leftBuilding,IndustryBuilding) and self.leftBuilding.robots:
                            quad = "l"
                        elif isinstance(self.upBuilding,IndustryBuilding) and self.upBuilding.robots:
                            quad = "u"
                        else:
                            quad = "d"
                        #print("RP found " + quad)
                    else:
                        if self.downBuilding == building:
                            quad = "d"
                        elif self.rightBuilding == building:
                            quad = "r"
                        elif self.leftBuilding == building:
                            quad = "l"
                        elif self.upBuilding == building:
                            quad = "u"
                        else:
                            quad = "d"
                    self.drawProgressBar(screen, building.buildProgress,building.buildCost, c.white,quad)
            

    def drawProgressBar(self,screen,progress,limit,color,quad = "all"):
        if limit > 0:
            ratio = progress/limit
        else:
            ratio = 0.0
        height = 50
        progressHeight = int(ratio*height)
        if quad == "all":
            loc = (self.clickAnchor[0]-31,self.clickAnchor[1]-6)
        if quad == "u" or quad == "ur":
            loc = (self.upAnchor[0]-14,self.upAnchor[1]-4)
        if quad == "d" or quad == "dl":
            loc = (self.downAnchor[0]-12,self.downAnchor[1]-4)
        if quad == "r" or quad == "rd":
            loc = (self.rightAnchor[0]-12,self.rightAnchor[1]-4)
        if quad == "l" or quad == "lu":
            loc = (self.leftAnchor[0]-10,self.leftAnchor[1]-4)
        pygame.draw.line(screen,c.black,loc,(loc[0],loc[1]-height-2),5)
        pygame.draw.line(screen,color,(loc[0],loc[1]-1),(loc[0],loc[1]-progressHeight-1),3)
        

    def runAnimations(self,screen):
        tileSurface = d.TileSurface.grid[self.x-1][self.y-1]
        for a in tileSurface.animations:
            a.runAnimation()
            a.draw(screen)
            if a.on == False:
                if a.triggerObject != None:
                    if a.triggerObject.bonusAnimation:
                        a.triggerObject.bonusAnimation = False
                    else:
                        if a.triggerObject.lander or (a.triggerObject.lander and a.triggerObject.launch):
                            a.triggerObject.finishBuild()
                        if a.triggerObject.launch and a.triggerObject.lander==False:
                            a.triggerObject.export()
                            a.triggerObject.pad.full = False
                tileSurface.animations.remove(a)

    def addAnimation(self,animationObject):
        tileSurface = d.TileSurface.grid[self.x-1][self.y-1]
        tileSurface.animations.insert(0,animationObject)

    def addBuilding(self,buildingObject):
        if buildingObject.lander and buildingObject.launch:
            print("animation found")
            landingAnimation = d.Animation([buildingObject.getSurface()],\
                (self.anchor[0]+600,self.anchor[1]-600),xLimit = self.anchor[0],yLimit=self.anchor[1],\
                    xVelocity = -2,yVelocity=2,triggerObject=buildingObject)
            self.addAnimation(landingAnimation)
        elif buildingObject.lander:
            landingAnimation = d.Animation([buildingObject.getSurface()],\
                (self.anchor[0],self.anchor[1]-600),yLimit=self.anchor[1],\
                    yVelocity=2,triggerObject=buildingObject)
            self.addAnimation(landingAnimation)
        if buildingObject.launch == False or buildingObject.lander == False:
            if buildingObject.drawSize == 'L':
                self.upOpen = False
                self.downOpen = False
                self.rightOpen = False
                self.leftOpen = False
            if buildingObject.udlr == "u":
                if buildingObject.drawSize == 'M':
                    self.upOpen = False
                    self.rightOpen = False
                else:
                    self.upOpen = False
            if buildingObject.udlr == "d":
                if buildingObject.drawSize == 'M':
                    self.downOpen = False
                    self.leftOpen = False
                else:
                    self.downOpen = False
            if buildingObject.udlr == "r":
                if buildingObject.drawSize == 'M':
                    self.rightOpen = False
                    self.downOpen = False
                else:
                    self.rightOpen = False
            if buildingObject.udlr == "l":
                if buildingObject.drawSize == 'M':
                    self.leftOpen = False
                    self.upOpen = False
                else:
                    self.leftOpen = False
            self.tileBuildings.append(buildingObject)
            if buildingObject.launch == False:
                if buildingObject.drawSize == 'L':
                    self.upBuilding = buildingObject
                    self.downBuilding = buildingObject
                    self.rightBuilding = buildingObject
                    self.leftBuilding = buildingObject
                if buildingObject.udlr == "u":
                    if buildingObject.drawSize == 'M':
                        self.upBuilding = buildingObject
                        self.rightBuilding = buildingObject
                    else:
                        self.upBuilding = buildingObject
                if buildingObject.udlr == "d":
                    if buildingObject.drawSize == 'M':
                        self.downBuilding = buildingObject
                        self.leftBuilding = buildingObject
                    else:
                        self.downBuilding = buildingObject
                if buildingObject.udlr == "r":
                    if buildingObject.drawSize == 'M':
                        self.rightBuilding = buildingObject
                        self.downBuilding = buildingObject
                    else:
                        self.rightBuilding = buildingObject
                if buildingObject.udlr == "l":
                    if buildingObject.drawSize == 'M':
                        self.leftBuilding = buildingObject
                        self.upBuilding = buildingObject
                    else:
                        self.leftBuilding = buildingObject
        self.redrawSurfaces()

    def redrawSurfaces(self):
        tileSurface = d.TileSurface.grid[self.x-1][self.y-1]
        tileSurface.surface = a.tile.copy()
        tileSurface.surfaceS = a.tileSelected.copy()
        tileSurface.surfaceMO = a.tileMO.copy()
        debrisLocs = [self.translateLoc("u"),self.translateLoc("d"),self.translateLoc("r"),self.translateLoc("l")]
        debrisSurfaces = [a.debris1,a.debris2,a.debris3,a.crater]
        i = 0
        for key in self.debrisKey:
            if key != 0:
                tileSurface.surface.blit(debrisSurfaces[i],debrisLocs[i])
                tileSurface.surfaceS.blit(debrisSurfaces[i],debrisLocs[i])
                tileSurface.surfaceMO.blit(debrisSurfaces[i],debrisLocs[i])
            i+=1

        for building in self.tileBuildings:
            if building.udlr == "u" and building.launch == False:
                if building.finished:
                    printSurface = building.getSurface()
                else:
                    printSurface = building.getSurfaceConstruction()
                tileSurface.surface.blit(printSurface,(0,0))
                tileSurface.surfaceS.blit(printSurface,(0,0))
                tileSurface.surfaceMO.blit(printSurface,(0,0))
        for building in self.tileBuildings:
            if building.udlr == "l":
                if building.finished:
                    printSurface = building.getSurface()
                else:
                    printSurface = building.getSurfaceConstruction()
                tileSurface.surface.blit(printSurface,(0,0))
                tileSurface.surfaceS.blit(printSurface,(0,0))
                tileSurface.surfaceMO.blit(printSurface,(0,0))
        for building in self.tileBuildings:
            if building.udlr == "r":
                if building.finished:
                    printSurface = building.getSurface()
                else:
                    printSurface = building.getSurfaceConstruction()
                tileSurface.surface.blit(printSurface,(0,0))
                tileSurface.surfaceS.blit(printSurface,(0,0))
                tileSurface.surfaceMO.blit(printSurface,(0,0))
        for building in self.tileBuildings:
            if building.udlr == "d":
                if building.finished:
                    printSurface = building.getSurface()
                else:
                    printSurface = building.getSurfaceConstruction()
                tileSurface.surface.blit(printSurface,(0,0))
                tileSurface.surfaceS.blit(printSurface,(0,0))
                tileSurface.surfaceMO.blit(printSurface,(0,0))
        for building in self.tileBuildings:
            if building.launch:
                printSurface = building.getSurfaceConstruction()
                tileSurface.surface.blit(printSurface,(0,0))
                tileSurface.surfaceS.blit(printSurface,(0,0))
                tileSurface.surfaceMO.blit(printSurface,(0,0))

    def getSurface(self):
        tileSurface = d.TileSurface.grid[self.x-1][self.y-1]
        if not self.selected:
            if not self.mouseOver:
                surface = tileSurface.surface
            else:
                surface = tileSurface.surfaceMO
        else:
            surface = tileSurface.surfaceS
        return surface

    def yesMouseOver(self):
        self.mouseOver = True
        if self.exploreAnnounce == False:
            self.mouseCount -= 1
    
    def noMouseOver(self):
        tileSurface = d.TileSurface.grid[self.x-1][self.y-1]
        self.mouseOver = False
        if self.exploreAnnounce == False:
            tileSurface.infoObject = None
        self.mouseCount = 32

    def unselect(self):
        self.selected = False

    def setSelected(self):
        for row in self.map.grid:
            for tile in row:
                tile.unselect()
        self.selected = True

    def translateLoc(self,key):
        start = (0,0)
        middle = (start[0] + self.map.tileWidth/2, start[1] + self.map.clickOffset)
        rightMid = (middle[0]+int(self.map.tileWidth/4),middle[1])
        leftMid = (middle[0]-int(self.map.tileWidth/4),middle[1])
        upMid = (middle[0],middle[1]-int(self.map.tileWidth/8))
        downMid = (middle[0],middle[1]+int(self.map.tileWidth/8))
        if key == "u" or key == "ur":
            loc = (upMid[0]-16,upMid[1]-8)
        if key == "d" or key == "dl":
            loc = (downMid[0]-16,downMid[1]-8)
        if key == "r" or key == "rd":
            loc = (rightMid[0]-16,rightMid[1]-8)
        if key == "l" or key == "lu":
            loc = (leftMid[0]-16,leftMid[1]-8)
        return loc
    
    def setClickAnchor(self,anchorTuple):
        self.anchor = anchorTuple
        self.clickAnchor = (anchorTuple[0] + self.map.tileWidth/2, anchorTuple[1] + self.map.clickOffset)
        self.rightAnchor = (self.clickAnchor[0]+int(self.map.tileWidth/4),self.clickAnchor[1])
        self.leftAnchor = (self.clickAnchor[0]-int(self.map.tileWidth/4),self.clickAnchor[1])
        self.upAnchor = (self.clickAnchor[0],self.clickAnchor[1]-int(self.map.tileWidth/8))
        self.downAnchor = (self.clickAnchor[0],self.clickAnchor[1]+int(self.map.tileWidth/8))

    def resetMouseQuad(self):
        self.mouseUp = False
        self.mouseDown = False
        self.mouseRight = False
        self.mouseLeft = False

    def checkMouseQuad(self,clickTuple):
        self.resetMouseQuad()
        if clickTuple[0] >= self.rightAnchor[0] - self.map.tileWidth/4 and clickTuple[0] <= self.rightAnchor[0] + self.map.tileWidth/4:
            yAllowed = int((self.map.tileWidth/4 - abs(clickTuple[0]-self.rightAnchor[0]))/2)
            if clickTuple[1] >= self.rightAnchor[1] - yAllowed and clickTuple[1] <= self.rightAnchor[1] + yAllowed:
                self.mouseRight = True
        if clickTuple[0] >= self.leftAnchor[0] - self.map.tileWidth/4 and clickTuple[0] <= self.leftAnchor[0] + self.map.tileWidth/4:
            yAllowed = int((self.map.tileWidth/4 - abs(clickTuple[0]-self.leftAnchor[0]))/2)
            if clickTuple[1] >= self.leftAnchor[1] - yAllowed and clickTuple[1] <= self.leftAnchor[1] + yAllowed:
                self.mouseLeft = True
        if clickTuple[0] >= self.upAnchor[0] - self.map.tileWidth/4 and clickTuple[0] <= self.upAnchor[0] + self.map.tileWidth/4:
            yAllowed = int((self.map.tileWidth/4 - abs(clickTuple[0]-self.upAnchor[0]))/2)
            if clickTuple[1] >= self.upAnchor[1] - yAllowed and clickTuple[1] <= self.upAnchor[1] + yAllowed:
                self.mouseUp = True
        if clickTuple[0] >= self.downAnchor[0] - self.map.tileWidth/4 and clickTuple[0] <= self.downAnchor[0] + self.map.tileWidth/4:
            yAllowed = int((self.map.tileWidth/4 - abs(clickTuple[0]-self.downAnchor[0]))/2)
            if clickTuple[1] >= self.downAnchor[1] - yAllowed and clickTuple[1] <= self.downAnchor[1] + yAllowed:
                self.mouseDown = True

    def checkClick(self,clickTuple):
        clicked = False
        if clickTuple[0] >= self.clickAnchor[0] - self.map.tileWidth/2 and clickTuple[0] <= self.clickAnchor[0] + self.map.tileWidth/2:
            yAllowed = int((self.map.tileWidth/2 - abs(clickTuple[0]-self.clickAnchor[0]))/2)
            if clickTuple[1] >= self.clickAnchor[1] - yAllowed and clickTuple[1] <= self.clickAnchor[1] + yAllowed:
                clicked = True
                #print("clicked " + str(self.x) + " " + str(self.y))
        if clicked:
            self.checkMouseQuad(clickTuple)
        else:
            self.resetMouseQuad()
        return clicked

blankMsg = []
noCost = [0,0,0,0,0,0,0]

class Building:
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        print(adjacencyBonus)
        self.buildSol = sol
        self.base = baseObject
        self.tile = tileObject
        self.drawSize = size
        self.udlr = udlr
        self.lander = False #change in init for earth based landers
        self.launch = False
        self.finished = False
        self.jobs = []
        self.buildBonus = adjacencyBonus
        self.bonusAnimation = False
        print("bb="+str(self.buildBonus))

        #self.size = "" # hard code string in cap
        self.buildCost = 0.0 # in total work days
        self.buildProgress = 0.0
        self.powerUsage = 0 # 
        self.maintainMax = 1.0
        self.maintainCost = 0.015
        self.maintain = 1.0
        self.volume = 0
        self.bonus = 1.0
        self.buildingName = ""
        self.drawSize = ''
        self.weight = 1.0
        self.shutoff = False
        self.readout = -1.0 #update with daily output
        self.readoutTag = ""
        self.readoutAnimate = False
        self.color = None

    def getSurface(self):
        pass

    def getSurfaceConstruction(self):
        pass

    def checkBonusPreview(self,buildingName):
        return None
    
    def runBonus(self,callingBuilding):
        pass

    def installBonuses(self):
        if self.drawSize == 'L':
            quad = "all"
        else:
            if self.udlr == 'u':
                if self.drawSize == "M":
                    quad = "ur"
                else:
                    quad = "u"
            if self.udlr == 'd':
                if self.drawSize == "M":
                    quad = "dl"
                else:
                    quad = "d"
            if self.udlr == 'r':
                if self.drawSize == "M":
                    quad = "rd"
                else:
                    quad = "r"
            if self.udlr == 'l':
                if self.drawSize == "M":
                    quad = "lu"
                else:
                    quad = "l"
        connectedBuildings = self.tile.checkConnected(quad)
        for building in connectedBuildings:
            self.runBonus(building)
        for building in connectedBuildings:
            building.runBonus(self)

    def getReadoutSurface(self,size):
        if self.shutoff:
            readoutSurface = d.getTextSurface("*",self.color,size,False)
        else:
            readoutSurface = d.getTextSurface("+{0:.2f}".format(self.readout),self.color,size,False)
        return readoutSurface

    def specialFinish(self):
        pass # can add special functions in specific building subclass TODO

    def generalFinish(self):
        self.finished = True
        self.base.totalVolume += self.volume
        self.base.air.storageCapacity += self.volume
        if self.lander == False:
            self.base.buildList.remove(self)
        if self.launch == False:
            self.base.allBuildings.append(self)
        self.tile.redrawSurfaces()
        self.specialFinish()
        self.installBonuses()
        self.announceCompletion()

    def shutoffBuilding(self):
        if self.shutoff:
            self.shutoff = False
            self.restartSpecial()
        else:
            self.shutoff = True
            self.maintain = 0.0
            self.readout = 0.0
            for job in self.jobs:
                job.fire()
            print("SHUTOFF")
            self.shutoffSpecial()
            self.base.announcements.addAnnouncement(self.buildingName + " shut down.")

    def shutoffSpecial(self):
        pass

    def restartSpecial(self):
        pass

    def prioritize(self):
        if len(self.jobs) > 0:
            self.weight *= 1.2
        else:
            self.bonus *= 0.30 + ((self.base.scienceLevel+3.0)/(self.base.scienceLevel+4.0))
            self.base.announcements.addAnnouncement("Productivity improved at " +self.buildingName)

    def announceCompletion(self):
        if self.lander and self.launch:
            self.base.announcements.addAnnouncement("sol:" + str(self.base.sol) + \
                " " + self.buildingName + " arrived at Spaceport.")
        elif self.lander:
            self.base.announcements.addAnnouncement("sol:" + str(self.base.sol) + \
                " " + self.buildingName + " touched down.")
        elif self.launch:
            if isinstance(self,RobotRocket):
                self.base.announcements.addAnnouncement("sol:" + str(self.base.sol) + \
                    " " + self.buildingName + " of {0:.0f} robots launched!".format(len(self.robots)))
            else:
                self.base.announcements.addAnnouncement("sol:" + str(self.base.sol) + \
                    " " + self.buildingName + " of {0:.1f} tons launched!".format(self.payloadQuantity))
        else:
            self.base.announcements.addAnnouncement("sol:" + str(self.base.sol) + \
                " Construction completed on " + self.buildingName + ".")

        #children get special run method.

roboMsg = ["Initiate build for",\
        "a new ROBOT. Can work",\
        "any job at your base."]
roboCost = [0,20,0,20,0,20,20]
robotDummyCapsule = ["ROBOT PROJECT","S",a.blankTile,a.blankTile,a.blankTile,a.blankTile,roboMsg,roboCost]
class RobotDummy(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size, robotBuilding):
        super().__init__(sol, baseObject, tileObject,udlr, size,1.0)
        self.color = c.blue
        self.buildLoc = robotBuilding
        #self.base.appendBuildList(self)
        self.buildCost = 100 * (1.0/robotBuilding.efficiency)
        self.maintainCost = 0
        self.volume = 0
        self.buildingName = "ROBOT PROJECT "
        self.drawSize = 'S'
        self.inProgress = False
        #finally
    
    def startBuild(self):
        print("Robot build start")
        self.base.appendBuildList(self)
        self.tile.tileBuildings.append(self)
        self.inProgress = True

    def getSurface(self):
        return a.blankTile

    def getSurfaceConstruction(self):
        return a.blankTile

    def specialFinish(self):
        newRobot = p.People(robot=True,sol=self.base.sol)
        newRobot.skill *= ((self.base.scienceLevel+3.0)/(self.base.scienceLevel+4.0))
        # TODO any robot psych?
        self.buildLoc.robotsList.remove(self)
        self.buildLoc.robotsList.append(newRobot)
        self.base.robots.append(newRobot)
        self.base.robotDummyResource.quantity += 1
        nextFound = False
        for item in self.buildLoc.robotsList:
            if nextFound == False:
                if isinstance(item,RobotDummy):
                    if item.inProgress == False:
                        item.startBuild()
                        nextFound = True
    
    def finishBuild(self):
        self.tile.tileBuildings.remove(self)
        self.generalFinish()

class Rocket(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size, capsule,padObject,payloadResource):
        super().__init__(sol, baseObject, tileObject,udlr, size,1.0)
        self.launch = True
        self.color = c.blue
        self.pad = padObject
        self.base.appendBuildList(self)
        self.buildCost = 25.0 * (1.0/self.base.bonuses.transportBonus)
        self.maintainCost = 0
        self.volume = 0
        self.buildingName = capsule[0] + " PAYLOAD"
        self.payload = payloadResource
        if payloadResource.tag == "AIR":
            airpad = self.base.totalVolume
        else:
            airpad = 0
        if payloadResource.tag == "ROBOTS":
            self.robotGet()
        else:
            if payloadResource.quantity -airpad > 50.0:
                self.payloadQuantity = 50.0
                payloadResource.quantity -= 50.0
            else:
                self.payloadQuantity = payloadResource.quantity - airpad
                payloadResource.quantity = airpad

        self.drawSize = 'L'
        #finally
        self.tile.addBuilding(self)

    def robotGet(self):
        pass
    
    def getSurface(self):
        under = pygame.Surface((64,47))
        under.fill(self.payload.color)
        under.blit(a.buildRocket,(0,0))
        under.set_colorkey(c.trans)
        return under

    def getSurfaceConstruction(self):
        under = pygame.Surface((64,47))
        under.fill(self.payload.color)
        under.blit(a.buildRocket,(0,0))
        under.set_colorkey(c.trans)
        return under

    def export(self):
        points = self.payload.value * self.payloadQuantity
        self.payload.value *= 1.0 - ((self.payloadQuantity/50.0)*0.1)
        self.base.exportPoints += points
        self.base.announcements.addAnnouncement("sol:" + str(self.base.sol) + " {0:.2f}".format(self.payloadQuantity)+\
            " tons of " + self.payload.tag + " deliverd to orbit.")
        self.base.announcements.addAnnouncement("+{0:.2f}".format(points)+ " export credits gained.")
        self.base.environment.addPsychEffect(3.0,0.25,7)
    
    def finishBuild(self):
        launchAnimation = d.Animation([self.getSurface()],\
                (self.tile.anchor),yLimit=self.tile.anchor[1]-600,\
                    yVelocity=-2,triggerObject=self)
        self.tile.addAnimation(launchAnimation)
        self.tile.tileBuildings.remove(self)
        self.generalFinish()

class RobotRocket(Rocket):
    def __init__(self, sol, baseObject, tileObject,udlr, size, capsule,padObject,payloadResource):
        self.robots = []
        super().__init__(sol, baseObject, tileObject,udlr, size, capsule,padObject,payloadResource)

    def export(self):
        points = self.payload.value * len(self.robots)
        self.payload.value *= 1.0 - ((len(self.robots)/3.0)*0.1)
        self.base.exportPoints += points
        self.base.announcements.addAnnouncement("sol:" + str(self.base.sol) + " {0:.0f}".format(len(self.robots))+\
            " robots exported to orbit.")
        self.base.announcements.addAnnouncement("+{0:.2f}".format(points)+ " export credits gained.")
        self.base.environment.addPsychEffect(3.0,0.25,7)

    def robotGet(self):
        toRemove = []
        if len(self.base.robots) <= 3:
            for robot in self.base.robots:         
                toRemove.append(robot)
        else:
            toCheck = []
            prodList = []
            for robot in self.base.robots:
                if robot.job != None:
                    toCheck.append(robot)
            for robot in toCheck:
                prodList.append(robot.job.productivity)
            prodList.sort()
            employCheck = False
            while len(toRemove) < 3:
                if employCheck == False:
                    employCheck = True
                    for robot in self.base.robots:
                        if robot.job == None:
                            toRemove.append(robot)
                else:
                    for robot in toCheck:
                        if robot.job.productivity == prodList[0]:
                            toRemove.append(robot)
                            prodList.remove(prodList[0])
        if len(toRemove) > 3:
            toRemove = [toRemove[0],toRemove[1],toRemove[2]]
        for robot in toRemove:
            self.robots.append(robot)
            if robot.job != None:
                robot.job.fire()
            for building in self.base.industryList:
                if building.robots:
                    if robot in building.robotsList:
                        building.robotsList.remove(robot)
            self.base.robots.remove(robot)
            self.base.robotDummyResource.quantity -= 1

class AdminBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.pink
        self.output = 0.0
        self.educationFactor = 0.0
        self.readoutTag = "admin pts"
        self.readoutAnimate = True

    def checkBonusPreview(self,buildingName):
        returnSurface  = None
        if buildingName in scienceBuildings:
            returnSurface = d.getTextSurface("+EDUCATION",c.purple,13)
        return returnSurface
    
    def runBonus(self,callingBuilding):
        if self.educationFactor > 0.0:
            outputAdjust = 1.0
            if isinstance(callingBuilding,LabBuilding):
                if callingBuilding.output > 0.0:
                    outputAdjust += (callingBuilding.output/10.0)
            self.educationFactor *= outputAdjust
            if outputAdjust > 1.0:
                self.base.announcements.addAnnouncement(self.buildingName + \
                    "'s education rate up {0:.1f}%.".format(100.0*(outputAdjust-1.0)) + \
                        " Nearby SCIENCE facility.")

    def finishBuild(self):
        self.generalFinish()
        self.base.appendAdminList(self)

class LabBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.purple
        self.output = 0.0
        self.exploreIncrease = 1.1
        self.readoutTag = "science pts"
        self.readoutAnimate = True
        self.medicalFactor = 0.0

    def checkBonusPreview(self,buildingName):
        returnSurface  = None
        if buildingName in medsBuildings:
            returnSurface = d.getTextSurface("+MEDICAL",c.orange,13)
        return returnSurface
    
    def runBonus(self,callingBuilding):
        if self.medicalFactor > 0.0:
            outputAdjust = 1.0
            if isinstance(callingBuilding,IndustryBuilding) and callingBuilding.buildingName in medsBuildings:
                outputAdjust += (callingBuilding.efficiency/10.0)
            self.medicalFactor *= outputAdjust
            if outputAdjust > 1.0:
                self.base.announcements.addAnnouncement(self.buildingName + \
                    "'s medical rating {0:.1f}%.".format(100.0*(outputAdjust-1.0)) + \
                        " MEDS produced nearby.")

    def finishBuild(self):
        self.generalFinish()
        self.base.appendLabList(self)
        self.base.exploreBonus *= self.exploreIncrease

class TransportBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.blue
        self.earthCostEffect = 0.0
        self.launch = False
            
    def finishBuild(self):
        self.generalFinish()
        self.base.appendTransportList(self)

class IndustryBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.orange
        self.efficiency = 0.0
        self.industry = None
        self.automated = False
        self.robots = False
        self.robotsStorage = 0
        self.robotsList = []
        self.readoutAnimate = True
    
    def getReadoutSurface(self,size):
        rColor = self.industry.output.color
        readoutSurface = d.getTextSurface("+{0:.2f}".format(self.readout),rColor,size,False)
        return readoutSurface

    def finishBuild(self):
        self.generalFinish()
        self.base.appendIndustryList(self)
        self.base.environment.addPsychEffect(self.efficiency,self.efficiency/7,7)

    def checkBonusPreview(self,buildingName):
        returnSurface  = None
        if buildingName in powerBuildings:
            returnSurface = d.getTextSurface("-E. USE",c.yellow,13)
        if buildingName in extractionBuildings:
            match = False
            if buildingName in waterExtractionBuildings and (self.buildingName in concreteBuildings or self.buildingName in fuelBuildings):
                match = True
            if buildingName in oreExtractionBuildings and self.buildingName in metalBuildings:
                match = True
            if buildingName in regolithExtractionBuildings and (self.buildingName in concreteBuildings or self.buildingName in waterBuildings):
                match = True
            if buildingName in rareExtractionBuildings and (self.buildingName in electronicsBuildings or self.buildingName in medsBuildings):
                match = True
            if match:
                returnSurface = d.getTextSurface("+CAPACITY",c.red,13)
        if buildingName in industryBuildings:
            match = False
            if buildingName in metalBuildings and self.buildingName in electronicsBuildings:
                match = True
            if buildingName in fuelBuildings and self.buildingName in plasticsBuildings:
                match = True
            if buildingName in waterBuildings and self.buildingName in concreteBuildings:
                match = True
            if match:
                returnSurface = d.getTextSurface("+CAPACITY",c.highlightOrange,13)   
        if buildingName in organicsBuildings or buildingName in airBuildings:
            match = False
            if buildingName in organicsBuildings and self.buildingName in medsBuildings:
                match = True
            if buildingName in airBuildings and self.buildingName in fuelBuildings:
                match = True
            if match:
                returnSurface = d.getTextSurface("+CAPACITY",c.green,13)  
        return returnSurface
    
    def runBonus(self,callingBuilding):
        if isinstance(callingBuilding,PowerBuilding):
            rate = 1.0 - (callingBuilding.powerOutput / 300.0) - (callingBuilding.powerStorage / 1000.0)
            self.powerUsage *= rate
            self.base.announcements.addAnnouncement(self.buildingName + \
                " now uses {0:.1f}% ".format(100.0 - (rate*100.0)) + "less ENERGY. Near Power source.")
        if isinstance(callingBuilding,ExtractionBuilding):
            match = False
            if callingBuilding.water == True and (self.buildingName in concreteBuildings or self.buildingName in fuelBuildings):
                match = True
            if callingBuilding.regolith == True and (self.buildingName in concreteBuildings or self.buildingName in waterBuildings):
                match = True
            if callingBuilding.ore == True and self.buildingName in metalBuildings:
                match = True
            if callingBuilding.rare ==True and (self.buildingName in electronicsBuildings or self.buildingName in medsBuildings):
                match = True
            if match:
                rate = 1.0 + (callingBuilding.extractionEfficiency/10.0)
                self.efficiency *= rate
                self.base.announcements.addAnnouncement(self.buildingName + \
                    " capacity at {0:.1f}%.".format(100.0*rate)+" Near RESOURCE extraction.") 
        if isinstance(callingBuilding,IndustryBuilding):
            match = False
            if callingBuilding.buildingName in metalBuildings and self.buildingName in electronicsBuildings:
                match = True
            if callingBuilding.buildingName in fuelBuildings and self.buildingName in plasticsBuildings:
                match = True
            if callingBuilding.buildingName in waterBuildings and self.buildingName in concreteBuildings:
                match = True
            if match:
                rate = 1.0 + (callingBuilding.efficiency/10.0)
                self.efficiency *= rate
                self.base.announcements.addAnnouncement(self.buildingName + \
                    " capacity at {0:.1f}%.".format(100.0*rate)+" Near feed production.")   
        if isinstance(callingBuilding,LifeSupportBuilding):
            match = False
            if callingBuilding.organicsOutput > 0.0 and self.buildingName in medsBuildings:
                match = True
                rate = 1.0 + (callingBuilding.organicsOutput/3.0)
            if callingBuilding.airOutput > 0.0 and self.buildingName in fuelBuildings:
                match = True
                rate = 1.0 + (callingBuilding.airOutput*2.0)
            if match:
                self.efficiency *= rate
                self.base.announcements.addAnnouncement(self.buildingName + \
                    " capacity at {0:.1f}%.".format(100.0*rate)+" Near feed production.")     

    def shutoffSpecial(self):
        if self.robots:
            toRemove = []
            for cons in self.base.buildList:
                if isinstance(cons,RobotDummy):
                    if cons.buildLoc == self:
                        toRemove.append(cons)
            for each in toRemove:
                self.base.buildList.remove(each)


class ExtractionBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.water = False
        self.regolith = False
        self.ore = False
        self.rare = False
        self.atmospheric = False
        self.color = c.red
        self.waterOutput = 0.0
        self.regolithOutput = 0.0
        self.oreOutput = 0.0
        self.rareOutput = 0.0
        self.extractionEfficiency = 0.0
        self.readoutAnimate = True
        self.multiReadout = [0,0,0,0]

    def shutoffSpecial(self):
        self.readout = 0
        self.multiReadout = [0,0,0,0]

    def checkBonusPreview(self,buildingName):
        returnSurface  = None
        if buildingName in powerBuildings:
            returnSurface = d.getTextSurface("-E. USE",c.yellow,13)
        if buildingName in adminOutputBuildings:
            returnSurface = d.getTextSurface("+OUTPUT",c.pink,13)
    
    def runBonus(self,callingBuilding):
        if isinstance(callingBuilding,PowerBuilding):
            rate = 1.0 - (callingBuilding.powerOutput / 300.0) - (callingBuilding.powerStorage / 1000.0)
            self.powerUsage *= rate
            self.base.announcements.addAnnouncement(self.buildingName + \
                " now uses {0:.1f}% ".format(100.0 - (rate*100.0)) + \
                    "less ENERGY due to " + callingBuilding.buildingName + " proximity.")  
        if isinstance(callingBuilding,AdminBuilding):
            if callingBuilding.output > 0.0:
                rate = 1.0 + (callingBuilding.output/20.0)
                self.base.announcements.addAnnouncement(self.buildingName + \
                    " extraction up {0:.1f}%".format((rate*100.0)-100.0) + ". ADMIN bonus.") 
    
    def getReadoutSurface(self,size):
        size = size - 1
        if self.water and self.regolith and self.ore and self.rare:
            readoutSurface1 = d.getTextSurface("+{0:.2f}".format(self.multiReadout[0]),c.blue,size,False)
            readoutSurface2 = d.getTextSurface("+{0:.2f}".format(self.multiReadout[1]),c.boldRed,size,False)
            readoutSurface3 = d.getTextSurface("+{0:.2f}".format(self.multiReadout[2]),c.red,size,False)
            readoutSurface4 = d.getTextSurface("+{0:.2f}".format(self.multiReadout[3]),c.pink,size,False)
            readoutSurface = pygame.Surface((readoutSurface2.get_width(),readoutSurface2.get_height()*4))
            readoutSurface.fill(c.trans)
            readoutSurface.set_colorkey(c.trans)
            yLoc = 0
            if self.multiReadout[0] > 0:
                readoutSurface.blit(readoutSurface1,(0,yLoc))
                yLoc += readoutSurface1.get_height()
            if self.multiReadout[1] > 0:
                readoutSurface.blit(readoutSurface2,(0,yLoc))
                yLoc += readoutSurface1.get_height()
            if self.multiReadout[2] > 0:
                readoutSurface.blit(readoutSurface3,(0,yLoc))
                yLoc += readoutSurface1.get_height()
            if self.multiReadout[3] > 0:
                readoutSurface.blit(readoutSurface4,(0,yLoc))
        elif self.regolith and self.ore:
            readoutSurface1 = d.getTextSurface("+{0:.2f}".format(self.multiReadout[0]),c.boldRed,size,False)
            readoutSurface2 = d.getTextSurface("+{0:.2f}".format(self.multiReadout[1]),c.red,size,False)
            if len(self.multiReadout) > 2:
                readoutSurface3 = d.getTextSurface("+{0:.2f}".format(self.multiReadout[2]),c.pink,size,False)
            readoutSurface = pygame.Surface((readoutSurface2.get_width(),readoutSurface2.get_height()*3))
            readoutSurface.fill(c.trans)
            readoutSurface.set_colorkey(c.trans)
            yLoc = 0
            if self.multiReadout[0] > 0:
                readoutSurface.blit(readoutSurface1,(0,yLoc))
                yLoc += readoutSurface1.get_height()
            if self.multiReadout[1] > 0:
                readoutSurface.blit(readoutSurface2,(0,yLoc))
                yLoc += readoutSurface1.get_height()
            if len(self.multiReadout) > 2 and self.multiReadout[2] > 0:
                readoutSurface.blit(readoutSurface3,(0,yLoc))
        else:
            if self.regolith:
                rColor = c.boldRed
            if self.ore:
                rColor = c.red
            if self.rare:
                rColor = c.pink
            if self.water:
                rColor = c.blue 
            readoutSurface = d.getTextSurface("+{0:.2f}".format(self.readout),rColor,size+1,False)
        return readoutSurface

    def getReadoutTag(self):
        pre = ""
        if self.water:
            self.readoutTag += pre+"water"
            pre = "/"
        if self.regolith:
            self.readoutTag += pre+"regolith"
            pre = "/"
        if self.ore:
            self.readoutTag += pre+"ore"
            pre = "/"
        if self.rare:
            self.readoutTag += pre+"rare"

    def finishBuild(self):
        self.generalFinish()
        self.base.appendExtractionList(self)

    def calculateOutput(self):
        if self.water:
            if self.atmospheric:
                self.waterOutput = self.extractionEfficiency * 0.75
            else:
                self.waterOutput = self.extractionEfficiency * self.tile.water
        if self.regolith:
            self.regolithOutput = self.extractionEfficiency * self.tile.regolith
        if self.ore:
            self.oreOutput = self.extractionEfficiency * self.tile.ore
        if self.rare:
            self.rareOutput = self.extractionEfficiency * self.tile.rare
        self.getReadoutTag()
        

class LifeSupportBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.green
        self.foodOutput = 0
        self.airOutput = 0
        self.organicsOutput = 0
        self.readoutAnimate = True
        self.multiReadout = [0,0,0] #fao
        self.readout = 1

    def shutoffSpecial(self):
        self.multiReadout = [0,0,0]

    def checkBonusPreview(self,buildingName):
        returnSurface  = None
        if buildingName in recycleBuildings or buildingName in scienceBuildings:
            returnSurface = d.getTextSurface("+OUTPUT",c.aqua,13)
        return returnSurface
    
    def runBonus(self,callingBuilding):
        outputAdjust = 1.0
        recycle = False
        sci = False
        if isinstance(callingBuilding,RecycleBuilding):
            outputAdjust += (callingBuilding.actualEfficiency-0.75)
            recycle = True
        if isinstance(callingBuilding,LabBuilding):
            outputAdjust += (callingBuilding.output/10.0)
            sci = True
        if sci and recycle:
            msgString  = " Access to RECYCLING and nearby research."
        else:
            if sci:
                msgString  = " Nearby research facilities."
            if recycle:
                msgString  = " Access to RECYCLING."
        self.foodOutput *= outputAdjust
        self.airOutput *= outputAdjust
        self.organicsOutput *= outputAdjust
        if outputAdjust > 1.0:
            self.base.announcements.addAnnouncement(self.buildingName + \
                "'s output up {0:.1f}%.".format(100*(outputAdjust-1.0))+msgString)

    def getReadoutSurface(self,size):
        readoutSurfaceF = d.getTextSurface("+{0:.2f}".format(self.multiReadout[0]),c.green,size,False)
        readoutSurfaceA = d.getTextSurface("+{0:.3f}".format(self.multiReadout[1]),c.aqua,size,False)
        readoutSurfaceO = d.getTextSurface("+{0:.2f}".format(self.multiReadout[2]),c.darkGreen,size,False)
        toAdd = []
        if self.foodOutput > 0 and self.multiReadout[0] > 0:
            toAdd.append(readoutSurfaceF)
        if self.airOutput > 0 and self.multiReadout[1] > 0:
            toAdd.append(readoutSurfaceA)
        if self.organicsOutput > 0 and self.multiReadout[2] > 0:
            toAdd.append(readoutSurfaceO)
        maxW = 1
        maxH = 1
        for surf in toAdd:
            if surf.get_width() > maxW:
                maxW = surf.get_width()
            if surf.get_height() > maxH:
                maxH = surf.get_height()
        readoutSurface = pygame.Surface((maxW,maxH*len(toAdd)))
        readoutSurface.fill(c.trans)
        readoutSurface.set_colorkey(c.trans)
        yLoc = 0
        for surf in toAdd:
            readoutSurface.blit(surf,(0,yLoc))
            yLoc += surf.get_height()
        return readoutSurface

    def getReadoutTag(self):
        pre = ""
        if self.foodOutput > 0:
            self.readoutTag += pre+"food"
            pre = "/"
        if self.airOutput > 0:
            self.readoutTag += pre+"air"
            pre = "/"
        if self.organicsOutput > 0:
            self.readoutTag += pre+"organics"
            pre = "/"

    def finishBuild(self):
        self.base.appendLifeSupportList(self)
        self.generalFinish()
        self.getReadoutTag()
        # TODO build environment bonus

class HabitatBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.white
        self.housingUnits = 0
        self.passengers = 0
        self.residents = []
        self.psychEffect = 1.0 #

    def checkBonusPreview(self,buildingName):
        returnSurface  = None
        if buildingName in psychPenaltyBuildings:
            returnSurface = d.getTextSurface("-PSYCH",c.red,13)
        if buildingName in organicsBuildings or buildingName in educationBuildings or buildingName in medicalBuildings:
            returnSurface = d.getTextSurface("+PSYCH",c.aqua,13)
        return returnSurface
    
    def runBonus(self,callingBuilding):
        psychAdjust = 1.0
        describeTag = ""
        if isinstance(callingBuilding,LifeSupportBuilding):
            psychAdjust += (callingBuilding.organicsOutput/4.0)
            describeTag += " Greenspace Bonus."
        if isinstance(callingBuilding,LabBuilding):
            if callingBuilding.medicalFactor > 0.0:
                psychAdjust += (callingBuilding.medicalFactor/15.0)
                describeTag += " Medical Access."
        if isinstance(callingBuilding,AdminBuilding):
            if callingBuilding.educationFactor > 0.0:
                psychAdjust += (callingBuilding.educationFactor/15.0)
                describeTag += " Educational Access."
        if isinstance(callingBuilding,LaunchPad) or isinstance(callingBuilding,SpacePort) or isinstance(callingBuilding,ExtractionBuilding):
            psychAdjust -= 0.10
            describeTag += " Loud neighbors."
        self.psychEffect *= psychAdjust
        if psychAdjust > 1.0:
            self.base.announcements.addAnnouncement(self.buildingName + \
                "'s environment improved {0:.1f}%.".format((100.0*psychAdjust)-100.0)+describeTag)
        if psychAdjust < 1.0:
            self.base.announcements.addAnnouncement(self.buildingName + \
                "'s environment degraded {0:.1f}%.".format(100.0-(100.0*psychAdjust))+describeTag)
        

    def getReport(self):
        residents = ""
        for each in self.residents:
            residents += each.name + " "
        return self.buildingName + " res: " + residents

    def restartSpecial(self):
        self.base.habitatUnits += self.housingUnits

    def shutoffSpecial(self):
        for resident in self.residents:
            resident.housed = False
        self.residents = []
        self.base.habitatUnits -= self.housingUnits
    
    def fillFromList(self,personList):
        for person in personList:
            if person.housed == False and (len(self.residents)<self.housingUnits):
                self.residents.append(person)
                person.housed = True

    def finishBuild(self):
        self.generalFinish()
        if self.lander == False or self.launch == False:
            self.base.appendHabitatList(self)
        self.base.habitatUnits += self.housingUnits
        if self.passengers > 0:
            self.base.addPeople(self.passengers)
        self.fillFromList(self.base.population)
        print(self.getReport())

class StorageBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.grey
        self.generalStorage = 0
        self.waterStorage = 0
        self.airStorage = 0
        self.foodStorage = 0
        self.powerStorage = 0
    
    def finishBuild(self):
        self.generalFinish()
        self.base.generalStorageCapacity += self.generalStorage
        self.base.water.storageCapacity += self.waterStorage
        self.base.air.storageCapacity += self.airStorage
        self.base.food.storageCapacity += self.foodStorage
        self.base.power.storageCapacity += self.powerStorage

class RecycleBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.aqua
        self.airCapacity = 0
        self.waterCapacity = 0
        self.foodCapacity = 0
        self.automated = True
        self.jobs = []
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0
        self.readoutAnimate = True
        self.readout = 1
        self.multiReadout = [0,0,0] #awo

    def shutoffSpecial(self):
        self.multiReadout = [0,0,0]
    
    def getReadoutTag(self):
        pre = ""
        if self.airCapacity > 0:
            self.readoutTag += pre+"air"
            pre = "/"
        if self.waterCapacity > 0:
            self.readoutTag += pre+"water"
            pre = "/"
        if self.foodCapacity > 0:
            self.readoutTag += pre+"organics"
            pre = "/"
    
    def getReadoutSurface(self,size):
        readoutSurfaceA = d.getTextSurface("+{0:.3f}".format(self.multiReadout[0]),c.aqua,size,False)
        readoutSurfaceW = d.getTextSurface("+{0:.2f}".format(self.multiReadout[1]),c.blue,size,False)
        readoutSurfaceO = d.getTextSurface("+{0:.2f}".format(self.multiReadout[2]),c.darkGreen,size,False)
        toAdd = []
        if self.airCapacity > 0 and self.multiReadout[0] > 0:
            toAdd.append(readoutSurfaceA)
        if self.waterCapacity > 0 and self.multiReadout[1] > 0:
            toAdd.append(readoutSurfaceW)
        if self.foodCapacity > 0 and self.multiReadout[2] > 0:
            toAdd.append(readoutSurfaceO)
        maxW = 1
        maxH = 1
        for surf in toAdd:
            if surf.get_width() > maxW:
                maxW = surf.get_width()
            if surf.get_height() > maxH:
                maxH = surf.get_height()
        readoutSurface = pygame.Surface((maxW,maxH*len(toAdd)))
        readoutSurface.fill(c.trans)
        readoutSurface.set_colorkey(c.trans)
        yLoc = 0
        for surf in toAdd:
            readoutSurface.blit(surf,(0,yLoc))
            yLoc += surf.get_height()
        return readoutSurface

    def finishBuild(self):
        self.getReadoutTag()
        self.generalFinish()
        self.base.appendRecycleList(self)

class PowerBuilding(Building):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.color = c.yellow
        self.powerOutput = 1
        self.automated = False
        self.jobs = []
        self.nuclear = False
        self.solar = False
        self.powerStorage = 0 #battery, stores excess power production
        self.readoutTag = "power"
        self.readoutAnimate = True

    def checkBonusPreview(self,buildingName):
        returnSurface  = None
        if buildingName in scienceBuildings:
            returnSurface = d.getTextSurface("+POWER",c.purple,13)
        return returnSurface
    
    def runBonus(self,callingBuilding):
        outputAdjust = 1.0
        if isinstance(callingBuilding,LabBuilding):
            outputAdjust += (callingBuilding.output/10.0)
        self.powerOutput *= outputAdjust
        if outputAdjust > 1.0:
            self.base.announcements.addAnnouncement(self.buildingName + \
                "'s output up {0:.1f}%.".format(100.0*(outputAdjust-1.0)) + \
                    " Nearby " + callingBuilding.buildingName + " provides engineering.")
    
    def finishBuild(self):
        self.generalFinish()
        self.base.appendPowerList(self)
        self.base.power.storageCapacity += self.powerStorage

#### Habitat buildings ####
mhMsg = ["Small residence","with a slight","psych bonus.","4 units."]
mhCost = [20,0,5,3,0,2,0]
marsHomeCapsule = [["MARS HOME","HAB"],"S",a.whiteXSU,a.whiteXSD,a.whiteXSR,a.whiteXSL,mhMsg,mhCost]
class MarsHome(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 4
        self.buildCost = 15.0
        self.powerUsage = 3.0
        self.maintainCost = 0.015
        self.volume = 1
        self.psychEffect = 1.02 ##* self.buildBonus
        self.buildingName = "MARS HOME"
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        if self.udlr == "u":
            return a.whiteXSU
        elif self.udlr == "d":
            return a.whiteXSD
        elif self.udlr == "l":
            return a.whiteXSL
        elif self.udlr == "r":
            return a.whiteXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

bhMsg = ["Basic humble","Mars dwelling.","6 housing units."]
bhCost = [25,0,10,4,0,1,0]
basicHabitatCapsule = [["BASIC HAB","HAB"],"S",a.whiteSU,a.whiteSD,a.whiteSR,a.whiteSL,bhMsg,bhCost]
class BasicHabitat(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 6
        self.buildCost = 20.0
        self.powerUsage = 4.0
        self.maintainCost = 0.020
        self.volume = 1
        self.psychEffect = 0.98 #* self.buildBonus
        self.buildingName = "BASIC HAB"
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        if self.udlr == "u":
            return a.whiteSU
        elif self.udlr == "d":
            return a.whiteSD
        elif self.udlr == "l":
            return a.whiteSL
        elif self.udlr == "r":
            return a.whiteSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

lhMsg = ["Astronaut transport"," for 6 that can provide","habitat after landing.","Poor psych effect."]
landerHabitatCapsule = [["LANDER HAB","HAB"],"S",a.whiteSU,a.whiteSD,a.whiteSR,a.whiteSL,lhMsg]
class LanderHabitat(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.housingUnits = 6
        self.buildCost = 0.0
        self.powerUsage = 3.0
        self.maintainCost = 0.010
        self.volume = 1
        self.psychEffect = 0.90 #* self.buildBonus
        self.buildingName = "LANDER HAB"
        self.passengers = 6
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        if self.udlr == "u":
            return a.whiteSU
        elif self.udlr == "d":
            return a.whiteSD
        elif self.udlr == "l":
            return a.whiteSL
        elif self.udlr == "r":
            return a.whiteSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

suMsg = ["Orbital delivery of","5 new astronauts. ","Arrives at Spaceport."]
shuttleCapsule = ["SHUTTLE","S",a.whiteXSU,a.whiteXSD,a.whiteXSR,a.whiteXSL,suMsg]
class Shuttle(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        self.launch = True #a.blankTile
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.housingUnits = 0
        self.buildCost = 0.0
        self.powerUsage = 0.0
        self.maintainCost = 0.0
        self.volume = 0.0
        self.psychEffect = 0.0
        self.buildingName = "SHUTTLE"
        self.passengers = 5
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        if self.udlr == "u":
            return a.whiteXSU
        elif self.udlr == "d":
            return a.whiteXSD
        elif self.udlr == "l":
            return a.whiteXSL
        elif self.udlr == "r":
            return a.whiteXSR

    def getSurfaceConstruction(self):
        return a.blankTile

suMsg = ["Bulk crew transport","for 10. Provides no","shelter after landing."]
crewDropCapsule = ["CREW DROP","S",a.whiteSU,a.whiteSD,a.whiteSR,a.whiteSL,suMsg]
class CrewDrop(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.housingUnits = 0
        self.buildCost = 0.0
        self.powerUsage = 0.01
        self.maintainCost = 0.001
        self.volume = 0.05
        self.psychEffect = 0.0 
        self.buildingName = "CREW DROP"
        self.passengers = 15
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        if self.udlr == "u":
            return a.whiteSU
        elif self.udlr == "d":
            return a.whiteSD
        elif self.udlr == "l":
            return a.whiteSL
        elif self.udlr == "r":
            return a.whiteSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

def specialFinish(self):
    self.base.generalStorageCapacity += 65

mtMsg = ["Orbit to surface pod,","delivers 15 astronauts.","provides no shelter."]
marsTranspoCapsule = ["MARS TRANSPO.","S",a.whiteSU,a.whiteSD,a.whiteSR,a.whiteSL,mtMsg]
class MarsTranspo(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.housingUnits = 0
        self.buildCost = 0.0
        self.powerUsage = 0.01
        self.maintainCost = 0.001
        self.volume = 0.05
        self.psychEffect = 0.0
        self.buildingName = "MARS TRANSPO."
        self.passengers = 10
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.whiteSU
        elif self.udlr == "d":
            return a.whiteSD
        elif self.udlr == "l":
            return a.whiteSL
        elif self.udlr == "r":
            return a.whiteSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

    def specialFinish(self):
        self.base.generalStorageCapacity += 50

scMsg = ["Astronaut transport for 3","that also carries supplies.","Poor psych effect","as a habitat."]
smallCrewLanderCapsule = [["SMALL CREW","HAB"],"S",a.whiteXSU,a.whiteXSD,a.whiteXSR,a.whiteXSL,scMsg]
class SmallCrewLander(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.housingUnits = 3
        self.buildCost = 0.0
        self.powerUsage = 1.5
        self.maintainCost = 0.005
        self.volume = 0.5
        self.buildingName = "SMALL CREW"
        self.psychEffect = 0.90 #* self.buildBonus
        self.passengers = 3
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # XS RETURN
        if self.udlr == "u":
            return a.whiteXSU
        elif self.udlr == "d":
            return a.whiteXSD
        elif self.udlr == "l":
            return a.whiteXSL
        elif self.udlr == "r":
            return a.whiteXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    def specialFinish(self):
        self.base.food.storageCapacity += 5
        self.base.air.storageCapacity += 5
        self.base.water.storageCapacity += 25
        self.base.food.quantity += 5
        self.base.air.quantity += 5
        self.base.water.quantity += 25

cqMsg = ["Living quarters for","10 residents, with","slight psych bonus."]
cqCost = [30,0,15,10,0,5,0]
crewQuartersCapsule = [["CREW QUARTERS","HAB"],"M",a.whiteMUR,a.whiteMDL,a.whiteMDR,a.whiteMUL,cqMsg,cqCost]
class CrewQuarters(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 10
        self.buildCost = 25.0
        self.finished = False
        self.powerUsage = 4.0
        self.maintainCost = 0.06
        self.psychEffect = 1.02 #* self.buildBonus
        self.volume = 1.7
        self.buildingName = "CREW QUARTERS"
        self.drawSize = 'M'
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.whiteMUR
        elif self.udlr == "d":
            return a.whiteMDL
        elif self.udlr == "l":
            return a.whiteMUL
        elif self.udlr == "r":
            return a.whiteMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

bnMsg = ["Very basic sleeping","quarters, provides","16 housing units."]
bnCost = [40,0,20,15,0,5,0]
bunksCapsule = [["BUNKS","HAB"],"M",a.whiteMLUR,a.whiteMLDL,a.whiteMLDR,a.whiteMLUL,bnMsg,bnCost]
class Bunks(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 16
        self.buildCost = 30.0
        self.finished = False
        self.powerUsage = 5.0
        self.maintainCost = 0.08
        self.psychEffect = 0.98 #* self.buildBonus
        self.volume = 2.0
        self.buildingName = "BUNKS"
        self.drawSize = 'M'
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.whiteMLUR
        elif self.udlr == "d":
            return a.whiteMLDL
        elif self.udlr == "l":
            return a.whiteMLUL
        elif self.udlr == "r":
            return a.whiteMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR

doMsg = ["Group housing pod","for 24 residents.","Social setting lends","small psych bonus."]
doCost = [60,0,30,20,0,10,0]
dormitoryCapsule = [["DORMITORY","HAB"],"L",a.whiteL,a.whiteL,a.whiteL,a.whiteL,doMsg,doCost]
class Dormitory(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 24
        self.buildCost = 35.0
        self.finished = False
        self.powerUsage = 8.0
        self.maintainCost = 0.15
        self.psychEffect = 1.02 #* self.buildBonus
        self.volume = 3.6
        self.buildingName = "DORMITORY"
        self.drawSize = 'L'
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.whiteL

    def getSurfaceConstruction(self):
        return a.clearL

abMsg = ["Highest capacity Mars","habitat with 32 units."]
abCost = [80,0,45,25,0,10,0]
apartmentBlockCapsule = [["APT. BLOCK","HAB"],"L",a.whiteXL,a.whiteXL,a.whiteXL,a.whiteXL,abMsg,abCost]
class ApartmentBlock(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)

        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 32
        self.buildCost = 40.0
        self.finished = False
        self.powerUsage = 10.0
        self.maintainCost = 0.2
        self.psychEffect = 0.98 #* self.buildBonus
        self.volume = 4
        self.buildingName = "APT. BLOCK"
        self.drawSize = 'L'
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # XL RETURN
        return a.whiteXL

    def getSurfaceConstruction(self):
        return a.clearXL

dhMsg = ["Two person habitat","domed and deluxe.","Strong psych bonus."]
dhCost = [0,0,15,5,0,5,5]
domeHabCapsule = [["DOME HAB","HAB"],"S",a.whiteXSU,a.whiteXSD,a.whiteXSR,a.whiteXSL,dhMsg,dhCost]
class DomeHab(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 2
        self.buildCost = 25.0
        self.powerUsage = 3.5
        self.maintainCost = 0.025
        self.volume = 1
        self.psychEffect = 1.15 #* self.buildBonus
        self.buildingName = "DOME HAB"
        self.drawSize = 'S'
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.whiteXSU
        elif self.udlr == "d":
            return a.whiteXSD
        elif self.udlr == "l":
            return a.whiteXSL
        elif self.udlr == "r":
            return a.whiteXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

laMsg = ["Highest quality housing","for 12 martians.","Strong psych bonus."]
laCost = [0,0,60,30,0,15,15]
luxuryApartmentCapsule = [["LUXURY APT.","HAB"],"L",a.whiteL,a.whiteL,a.whiteL,a.whiteL,laMsg,laCost]
class LuxuryApartment(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)

        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 12
        self.buildCost = 60.0
        self.finished = False
        self.powerUsage = 13.0
        self.maintainCost = 0.3
        self.psychEffect = 1.1 #* self.buildBonus
        self.volume = 4
        self.buildingName = "LUXURY APT."
        self.drawSize = 'L'
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        return a.whiteL

    def getSurfaceConstruction(self):
        return a.clearL

thMsg = ["Row of 6 individual","habitats, well built.","Strong psych bonus."]
thCost = [0,0,30,15,0,10,5]
townhouseCapsule = [["TOWNHOUSE","HAB"],"M",a.whiteMUR,a.whiteMDL,a.whiteMDR,a.whiteMUL,thMsg,thCost]
class Townhouse(HabitatBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.housingUnits = 5
        self.buildCost = 40.0
        self.finished = False
        self.powerUsage = 4.5
        self.maintainCost = 0.1
        self.psychEffect = 1.1 #* self.buildBonus
        self.volume = 2.0
        self.buildingName = "TOWNHOUSE"
        self.drawSize = 'M'
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        if self.udlr == "u":
            return a.whiteMUR
        elif self.udlr == "d":
            return a.whiteMDL
        elif self.udlr == "l":
            return a.whiteMUL
        elif self.udlr == "r":
            return a.whiteMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR


## STORAGE BUILDINGS ##
slMsg = ["Landable storage pod","that arrives with 75.0","water, 10.0 air, 15.0","food, and 20.0 fuel."]
supplyLanderCapsule = [["SUPPLY POD","STORAGE"],"S",a.greySU,a.greySD,a.greySR,a.greySL,slMsg]
class SupplyLander(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.25
        self.maintainCost = 0.005
        self.volume = 0.75
        self.buildingName = "SUPPLY POD"
        self.drawSize = 'S'
        self.waterStorage = 75
        self.airStorage = 10
        self.foodStorage = 15
        self.generalStorage = 50 * self.buildBonus
        # storage class

        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greySU
        elif self.udlr == "d":
            return a.greySD
        elif self.udlr == "l":
            return a.greySL
        elif self.udlr == "r":
            return a.greySR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    # override for adding commodity with storage
    def specialFinish(self):
        self.base.food.quantity += self.foodStorage
        self.base.air.quantity += self.airStorage
        self.base.water.quantity += self.waterStorage
        self.base.meds.quantity += self.generalStorage
        self.base.fuel.quantity += 20


alMsg = ["Landable air storage","that transports 30.0","air from earth."]
airLanderCapsule = ["AIR DROP","S",a.aquaXSU,a.aquaXSD,a.aquaXSR,a.aquaXSL,alMsg]
class AirLander(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.1
        self.maintainCost = 0.002
        self.volume = 0.1
        self.buildingName = "AIR DROP"
        self.drawSize = 'S'
        self.airStorage = 30

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.aquaXSU
        elif self.udlr == "d":
            return a.aquaXSD
        elif self.udlr == "l":
            return a.aquaXSL
        elif self.udlr == "r":
            return a.aquaXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    # override for adding commodity with storage
    def specialFinish(self):
        self.base.air.quantity += self.airStorage


oaMsg = ["Orbital air resupply","that lands 15.0 units","AIR from orbit."]
orbitalAirCapsule = ["ORBITAL AIR","S",a.aquaXSU,a.aquaXSD,a.aquaXSR,a.aquaXSL,oaMsg]
class OrbitalAir(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        self.launch = True #a.blankTile
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.0
        self.maintainCost = 0.0
        self.volume = 0.0
        self.buildingName = "ORBITAL AIR"
        self.drawSize = 'S'
        self.airStorage = 0

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.aquaXSU
        elif self.udlr == "d":
            return a.aquaXSD
        elif self.udlr == "l":
            return a.aquaXSL
        elif self.udlr == "r":
            return a.aquaXSR
    
    def getSurfaceConstruction(self):
        return a.blankTile

    # override for adding commodity with storage
    def specialFinish(self):
        self.base.air.quantity += 15.0

wlMsg = ["Landable water tank","lands with 200.0","water."]
waterLanderCapsule = ["WATER DROP","S",a.blueXSU,a.blueXSD,a.blueXSR,a.blueXSL,wlMsg]
class WaterLander(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.1
        self.maintainCost = 0.002
        self.volume = 0.1
        self.buildingName = "WATER DROP"
        self.drawSize = 'S'
        self.waterStorage = 200

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.blueXSU
        elif self.udlr == "d":
            return a.blueXSD
        elif self.udlr == "l":
            return a.blueXSL
        elif self.udlr == "r":
            return a.blueXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    # override for adding commodity with storage
    def specialFinish(self):
        self.base.water.quantity += self.waterStorage

owMsg = ["Orbital water resource","arrives with 75.0","WATER, requires storage."]
orbitalWaterCapsule = ["ORBITAL WATER","S",a.blueXSU,a.blueXSD,a.blueXSR,a.blueXSL,owMsg]
class OrbitalWater(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        self.launch = True #a.blankTile
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.0
        self.maintainCost = 0.0
        self.volume = 0.0
        self.buildingName = "ORBITAL WATER"
        self.drawSize = 'S'
        self.waterStorage = 0
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.blueXSU
        elif self.udlr == "d":
            return a.blueXSD
        elif self.udlr == "l":
            return a.blueXSL
        elif self.udlr == "r":
            return a.blueXSR

    def getSurfaceConstruction(self):
        return a.blankTile

    # override for adding commodity with storage
    def specialFinish(self):
        self.base.water.quantity += 75.0

ofMsg = ["Space based food","pod that delivers","20.0 FOOD, needs storage."]
orbitalFoodCapsule = ["ORBITAL FOOD","S",a.greenXSU,a.greenXSD,a.greenXSR,a.greenXSL,ofMsg]
class OrbitalFood(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        self.launch = True #a.blankTile
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.0
        self.maintainCost = 0.0
        self.volume = 0.0
        self.buildingName = "ORBITAL FOOD"
        self.drawSize = 'S'
        self.foodStorage = 0
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greenXSU
        elif self.udlr == "d":
            return a.greenXSD
        elif self.udlr == "l":
            return a.greenXSL
        elif self.udlr == "r":
            return a.greenXSR
    
    def getSurfaceConstruction(self):
        return a.blankTile

    # override for adding commodity with storage
    def specialFinish(self):
        self.base.food.quantity += 20.0

flMsg = ["Landable refrigerated","pod that arrives","with 50.0 food."]
foodLanderCapsule = ["FOOD DROP","S",a.greenXSU,a.greenXSD,a.greenXSR,a.greenXSL,flMsg]
class FoodLander(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.1
        self.maintainCost = 0.002
        self.volume = 0.1
        self.buildingName = "FOOD DROP"
        self.drawSize = 'S'
        self.foodStorage = 50
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greenXSU
        elif self.udlr == "d":
            return a.greenXSD
        elif self.udlr == "l":
            return a.greenXSL
        elif self.udlr == "r":
            return a.greenXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    # override for adding commodity with storage
    def specialFinish(self):
        self.base.food.quantity += self.foodStorage

cdMsg = ["Orbital resupply of","30.0 CONCRETE with","storage capacity."]
concreteDropCapsule = [["CONCRETE DROP","STORAGE"],"S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,cdMsg]
class ConcreteDrop(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.01
        self.maintainCost = 0.001
        self.volume = 0.0
        self.buildingName = "CONCRETE DROP"
        self.drawSize = 'S'
        self.generalStorage = 30 * self.buildBonus
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    def specialFinish(self):
        self.base.concrete.quantity += 30
        self.base.generalStorageCapacity += 40

mdMsg = ["Import of luxury goods","from Earth, strong PSYCH","bonus for your base."]
luxuryCargoCapsule = [["LUX. CARGO","STORAGE"],"S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,mdMsg]
class LuxuryCargo(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.015
        self.maintainCost = 0.01
        self.volume = 0.0
        self.buildingName = "LUX. CARGO"
        self.drawSize = 'S'
        self.generalStorage = 30 * self.buildBonus
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    def specialFinish(self):
        self.base.environment.addPsychEffect(1.5,1.5/300,300)
        self.base.environment.psychPoints += 4


mdMsg = ["Orbital resupply of","30.0 METAL with","storage capacity."]
metalDropCapsule = [["METAL DROP","STORAGE"],"S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,mdMsg]
class MetalDrop(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.01
        self.maintainCost = 0.001
        self.volume = 0.0
        self.buildingName = "METAL DROP"
        self.drawSize = 'S'
        self.generalStorage = 30 * self.buildBonus
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    def specialFinish(self):
        self.base.metal.quantity += 30
        self.base.generalStorageCapacity += 40

edMsg = ["Orbital resupply of","20.0 ELECTRONICS."]
electronicsDropCapsule = ["ELECT. DROP","S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,edMsg]
class ElectronicsDrop(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        self.launch = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.0
        self.maintainCost = 0.0
        self.volume = 0.0
        self.buildingName = "ELECT. DROP"
        self.drawSize = 'S'
        self.generalStorage = 0
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR

    def getSurfaceConstruction(self):
        return a.blankTile
    
    def specialFinish(self):
        self.base.electronics.quantity += 20

mdMsg = ["Orbital resupply of","20.0 MEDS."]
medsDropCapsule = ["MEDS DROP","S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,mdMsg]
class MedsDrop(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        self.launch = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.0
        self.maintainCost = 0.0
        self.volume = 0.0
        self.buildingName = "MEDS DROP"
        self.drawSize = 'S'
        self.generalStorage = 0
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR

    def getSurfaceConstruction(self):
        return a.blankTile
    
    def specialFinish(self):
        self.base.meds.quantity += 20

pdMsg = ["Orbital resupply of","20.0 PLASTICS."]
plasticsDropCapsule = ["PLASTICS DROP","S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,pdMsg]
class PlasticsDrop(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        self.launch = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.0
        self.maintainCost = 0.0
        self.volume = 0.0
        self.buildingName = "PLASTICS DROP"
        self.drawSize = 'S'
        self.generalStorage = 0
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR
    
    def getSurfaceConstruction(self):
        return a.blankTile
    
    def specialFinish(self):
        self.base.plastics.quantity += 20

blMsg = ["Supply shipment with","all the construction","essentials, and some","storage capacity."]
builderLanderCapsule = [["BUILDER POD","STORAGE"],"S",a.greySU,a.greySD,a.greySR,a.greySL,blMsg]
class BuilderLander(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.1
        self.maintainCost = 0.002
        self.volume = 0.0
        self.buildingName = "BUILDER POD"
        self.drawSize = 'S'
        self.generalStorage = 300 * self.buildBonus
        # storage class

        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greySU
        elif self.udlr == "d":
            return a.greySD
        elif self.udlr == "l":
            return a.greySL
        elif self.udlr == "r":
            return a.greySR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    # override for adding commodity with storage
    def specialFinish(self):
        self.base.metal.quantity += 100
        self.base.concrete.quantity += 50
        self.base.electronics.quantity += 50
        self.base.plastics.quantity += 25
        self.base.fuel.quantity += 25

shedMsg = ["A simple low",\
                "low cost storage",\
                "option.",\
                "50 STORAGE"]
shedCost = [20,0,5,0,0,0,0]
storeShedCapsule = [["SHED","STORAGE"],"S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,shedMsg,shedCost]
class StoreShed(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 3.0
        self.powerUsage = 0.0
        self.maintainCost = 0.005
        self.volume = 0
        self.buildingName = "SHED"
        self.drawSize = 'S'
        self.generalStorage = 50 * self.buildBonus
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

atMsg = ["Pressurized air",\
                "containment units.",\
                "20 AIR STORAGE"]
atCost = [8,0,0,20,0,0,2]
airTanksCapsule = ["AIR TANKS","S",a.greyXSU,a.greyXSD,a.greyXSR,a.greyXSL,atMsg,atCost]
class AirTanks(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 12.0
        self.powerUsage = 0.0
        self.maintainCost = 0.01
        self.volume = 0
        self.buildingName = "AIR TANKS"
        self.drawSize = 'S'
        self.airStorage = 20
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greyXSU
        elif self.udlr == "d":
            return a.greyXSD
        elif self.udlr == "l":
            return a.greyXSL
        elif self.udlr == "r":
            return a.greyXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

rvMsg = ["Reinforced tank",\
              "for storing the","base's water.",\
              "100 WATER STORAGE"]
rvCost = [10,0,20,10,0,0,0]
reservoirCapsule = ["RESERVOIR","S",a.greySU,a.greySD,a.greySR,a.greySL,rvMsg,rvCost]
class Reservoir(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 12.0
        self.powerUsage = 0.5
        self.maintainCost = 0.01
        self.volume = 0
        self.buildingName = "RESERVOIR"
        self.drawSize = 'S'
        self.waterStorage = 100
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greySU
        elif self.udlr == "d":
            return a.greySD
        elif self.udlr == "l":
            return a.greySL
        elif self.udlr == "r":
            return a.greySR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

pyMsg = ["Specialized food",\
              "storage facility.",\
              "50 FOOD STORAGE"]
pyCost = [13,0,15,10,0,2,0]
pantryCapsule = ["PANTRY","S",a.greySU,a.greySD,a.greySR,a.greySL,pyMsg,pyCost]
class Pantry(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 1.0
        self.maintainCost = 0.015
        self.volume = 0.4
        self.buildingName = "PANTRY"
        self.drawSize = 'S'
        self.foodStorage = 50
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greySU
        elif self.udlr == "d":
            return a.greySD
        elif self.udlr == "l":
            return a.greySL
        elif self.udlr == "r":
            return a.greySR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

vtMsg = ["Mixed life support",\
              "storage facility.",\
              "30 FOOD STORAGE","50 WATER STORAGE","10 AIR STORAGE"]
vtCost = [25,0,20,10,0,3,2]
vitalsCapsule = ["VITALS","M",a.greyMUR,a.greyMDL,a.greyMDR,a.greyMUL,vtMsg,vtCost]
class Vitals(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 1.5
        self.maintainCost = 0.025
        self.volume = 0.5
        self.buildingName = "VITALS"
        self.drawSize = 'M'
        self.foodStorage = 30
        self.waterStorage = 50
        self.airStorage = 10
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.greyMUR
        elif self.udlr == "d":
            return a.greyMDL
        elif self.udlr == "l":
            return a.greyMUL
        elif self.udlr == "r":
            return a.greyMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

hgMsg = ["Large general purpose",\
              "storage building.",\
              "100 STORAGE"]
hgCost = [40,0,15,15,0,0,0,0]
hangarCapsule = [["HANGAR","STORAGE"],"M",a.greyMLUR,a.greyMLDL,a.greyMLDR,a.greyMLUL,hgMsg,hgCost]
class Hangar(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 0.3
        self.maintainCost = 0.01
        self.volume = 0.05
        self.buildingName = "HANGAR"
        self.drawSize = 'M'
        self.generalStorage = 100 * self.buildBonus
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.greyMLUR
        elif self.udlr == "d":
            return a.greyMLDL
        elif self.udlr == "l":
            return a.greyMLUL
        elif self.udlr == "r":
            return a.greyMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR

whMsg = ["Massive storage facility",\
              "for general use.",\
              "200 STORAGE"]
whCost = [75,0,25,20,0,0,0]
warehouseCapsule = [["WAREHOUSE","STORAGE"],"L",a.greyL,a.greyL,a.greyL,a.greyL,whMsg,whCost]
class Warehouse(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 0.4
        self.maintainCost = 0.015
        self.volume = 0.075
        self.buildingName = "WAREHOUSE"
        self.drawSize = 'L'
        self.generalStorage = 200 * self.buildBonus
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # L RETURN
        return a.greyL

    def getSurfaceConstruction(self):
        return a.clearL

dtMsg = ["Multi-use storage hub",\
        "with plenty of space.",\
              "150 STORAGE","25 FOOD STORAGE","35 WATER STORAGE","5 AIR STORAGE"]
dtCost = [75,0,40,25,0,5,5]
depotCapsule = [["DEPOT","STORAGE"],"L",a.greyXL,a.greyXL,a.greyXL,a.greyXL,dtMsg,dtCost]
class Depot(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 40.0
        self.powerUsage = 1.5
        self.maintainCost = 0.025
        self.volume = 0.5
        self.buildingName = "DEPOT"
        self.drawSize = 'L'
        self.generalStorage = 150 * self.buildBonus
        self.foodStorage = 25
        self.waterStorage = 35
        self.airStorage = 5
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # XL RETURN
        return a.greyXL

    def getSurfaceConstruction(self):
        return a.clearXL

dtMsg = ["Large storage excavation",\
        "for general storage, consumes",\
        "much REGOLITH. 250 STORAGE"]
dtCost = [120,0,10,10,0,0,0]
storageTunnelsCapsule = [["STORAGE TUNNELS","STORAGE"],"L",a.greyXL,a.greyXL,a.greyXL,a.greyXL,dtMsg,dtCost]
class StorageTunnels(StorageBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 0.8
        self.maintainCost = 0.02
        self.volume = 0.5
        self.buildingName = "STORAGE TUNNELS"
        self.drawSize = 'L'
        self.generalStorage = 250 * self.buildBonus
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # XL RETURN
        return a.greyXL

    def getSurfaceConstruction(self):
        return a.clearXL

prc = '%'
### RECYCLE BUILDINGS ###
cmMsg = ["Recovers ORGANICS",\
        "from base's food waste.",
        "80" + prc + " EFFICIENT"]
cmCost = [15,0,5,0,0,0,10]
composterCapsule = ["COMPOSTER","S",a.aquaXSU,a.aquaXSD,a.aquaXSR,a.aquaXSL,cmMsg,cmCost]
class Composter(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 1.2
        self.maintainCost = 0.005
        self.volume = 0.05
        self.buildingName = "COMPOSTER"
        self.drawSize = 'S'
        self.foodCapacity = self.base.FOOD_MIN_CONST * 6
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.80

        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.aquaXSU
        elif self.udlr == "d":
            return a.aquaXSD
        elif self.udlr == "l":
            return a.aquaXSL
        elif self.udlr == "r":
            return a.aquaXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

h2Msg = ["Automated waste water",\
        "treatment and recycler.",
        "80" + prc + " EFFICIENT"]
h2Cost = [0,0,15,5,0,2,3]
h2oTreatmentCapsule = ["H2O TREATMENT","S",a.aquaXSU,a.aquaXSD,a.aquaXSR,a.aquaXSL,h2Msg,h2Cost]
class H2oTreatment(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 1.2
        self.maintainCost = 0.005
        self.volume = 0.05
        self.buildingName = "H2O TREATMENT"
        self.drawSize = 'S'
        self.waterCapacity = self.base.WATER_MIN_CONST * 6
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.80

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.aquaXSU
        elif self.udlr == "d":
            return a.aquaXSD
        elif self.udlr == "l":
            return a.aquaXSL
        elif self.udlr == "r":
            return a.aquaXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

afMsg = ["Recirculator that will",\
        "provide breathable air.",
        "80" + prc + " EFFICIENT"]
afCost = [5,0,0,15,0,5,5]
airFiltrationCapsule = ["AIR FILTRATION","S",a.aquaXSU,a.aquaXSD,a.aquaXSR,a.aquaXSL,afMsg,afCost]
class AirFiltration(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 1.2
        self.maintainCost = 0.005
        self.volume = 0.05
        self.buildingName = "AIR FILTRATION"
        self.drawSize = 'S'
        self.airCapacity = self.base.AIR_CONST * 6
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.80

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.aquaXSU
        elif self.udlr == "d":
            return a.aquaXSD
        elif self.udlr == "l":
            return a.aquaXSL
        elif self.udlr == "r":
            return a.aquaXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

bcMsg = ["Food waste processing",\
        "unit that employs one","and outputs ORGANICS.",
        "90" + prc + " EFFICIENT"]
bcCost = [30,0,10,0,0,5,15]
biocyclerCapsule = ["BIOCYCLER","M",a.aquaMUR,a.aquaMDL,a.aquaMDR,a.aquaMUL,bcMsg,bcCost]
class Biocycler(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 2.5
        self.maintainCost = 0.01
        self.volume = 0.15
        self.buildingName = "BIOCYCLER"
        self.drawSize = 'M'
        self.foodCapacity = self.base.FOOD_MIN_CONST * 15
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.90
        t2 = i.Job("BIO TECH",0.2,0.5,0.3,self)
        self.jobs = [t2]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.aquaMUR
        elif self.udlr == "d":
            return a.aquaMDL
        elif self.udlr == "l":
            return a.aquaMUL
        elif self.udlr == "r":
            return a.aquaMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

wwMsg = ["Waste water processing",\
        "unit that employs one,","outputs clean WATER.",
        "90" + prc + " EFFICIENT"]
wwCost = [0,0,30,10,0,5,5]
wastewaterPlantCapsule = ["WASTEWATER PLANT","M",a.aquaMUR,a.aquaMDL,a.aquaMDR,a.aquaMUL,wwMsg,wwCost]
class WastewaterPlant(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 2.5
        self.maintainCost = 0.01
        self.volume = 0.15
        self.buildingName = "WASTEWATER PLANT"
        self.drawSize = 'M'
        self.waterCapacity = self.base.WATER_MIN_CONST * 15
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.90
        t2 = i.Job("WATER TECH",0.2,0.5,0.3,self)
        self.jobs = [t2]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.aquaMUR
        elif self.udlr == "d":
            return a.aquaMDL
        elif self.udlr == "l":
            return a.aquaMUL
        elif self.udlr == "r":
            return a.aquaMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

arMsg = ["Central air recycling",\
        "facility employs one,","outputs breathable AIR.",
        "85" + prc + " EFFICIENT"]
arCost = [5,5,0,30,0,10,10]
airRecyclerCapsule = ["AIR RECYCLER","M",a.aquaMUR,a.aquaMDL,a.aquaMDR,a.aquaMUL,arMsg,arCost]
class AirRecycler(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 2.5
        self.maintainCost = 0.01
        self.volume = 0.15
        self.buildingName = "AIR RECYCLER"
        self.drawSize = 'M'
        self.airCapacity = self.base.AIR_CONST * 15
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.85
        t2 = i.Job("AIR TECH",0.2,0.5,0.3,self)
        self.jobs = [t2]

        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.aquaMUR
        elif self.udlr == "d":
            return a.aquaMDL
        elif self.udlr == "l":
            return a.aquaMUL
        elif self.udlr == "r":
            return a.aquaMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

rhMsg = ["AIR, WATER, and FOOD",\
        "recycling at one plant.","Employs three.",
        "90" + prc + " EFFICIENT"]
rhCost = [10,5,45,25,0,15,20]
recycleHubCapsule = ["RECYCLE HUB","L",a.aquaL,a.aquaL,a.aquaL,a.aquaL,rhMsg,rhCost]
class RecycleHub(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 75.0
        self.powerUsage = 8.0
        self.maintainCost = 0.025
        self.volume = 1.2
        self.buildingName = "RECYCLE HUB"
        self.drawSize = 'L'
        self.airCapacity = self.base.AIR_CONST * 20
        self.waterCapacity = self.base.WATER_MIN_CONST * 20
        self.foodCapacity = self.base.FOOD_MIN_CONST * 20
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.90
        t1 = i.Job("BIO TECH",0.2,0.5,0.3,self)
        t2 = i.Job("AIR TECH",0.2,0.5,0.3,self)
        t3 = i.Job("WATER TECH",0.2,0.5,0.3,self)
        self.jobs = [t1,t2,t3]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # L RETURN
        return a.aquaL

    def getSurfaceConstruction(self):
        return a.clearL

rlMsg = ["Automated recycling bot",\
        "for AIR, WATER, and FOOD.",
        "95" + prc + " EFFICIENT"]
recycleLanderCapsule = ["RECYCLE POD","S",a.aquaSU,a.aquaSD,a.aquaSR,a.aquaSL,rlMsg]
class RecycleLander(RecycleBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 3.0
        self.maintainCost = 0.015
        self.volume = 0.5
        self.buildingName = "RECYCLE POD"
        self.drawSize = 'S'
        self.airCapacity = self.base.AIR_CONST * 6
        self.waterCapacity = self.base.WATER_MIN_CONST * 6
        self.foodCapacity = self.base.FOOD_MIN_CONST * 6
        self.maxEfficiency = 0.95
        self.actualEfficiency = 0.95

        # storage class

        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.aquaSU
        elif self.udlr == "d":
            return a.aquaSD
        elif self.udlr == "l":
            return a.aquaSL
        elif self.udlr == "r":
            return a.aquaSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

## POWER BUILDINGS ##
plMsg = ["Automatic power generation",\
        "with nuclear core.",
        "15.0 POWER OUTPUT"]
powerLanderCapsule = [["EARTH REACTOR","POW"],"S",a.yellowSU,a.yellowSD,a.yellowSR,a.yellowSL,plMsg]
class PowerLander(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.maintainCost = 0.010
        self.volume = 0.2
        self.nuclear = True
        self.automated = True
        self.buildingName = "EARTH REACTOR"
        self.drawSize = 'S'
        self.powerOutput = 15.0
        self.powerStorage = 100.0

        # power class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.yellowSU
        elif self.udlr == "d":
            return a.yellowSD
        elif self.udlr == "l":
            return a.yellowSL
        elif self.udlr == "r":
            return a.yellowSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

plMsg = ["Well built solar unit",\
        "with small battery capacity.",
        "7.5 MAX POWER OUTPUT"]
prefabSolarCapsule = [["PREFAB SOLAR","POW"],"S",a.yellowXSU,a.yellowXSD,a.yellowXSR,a.yellowXSL,plMsg]
class PrefabSolar(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.maintainCost = 0.025
        self.volume = 0.05
        self.buildingName = "PREFAB SOLAR"
        self.drawSize = 'S'
        self.solar = True
        self.automated = True
        self.powerOutput = 7.5
        self.powerStorage = 25.0

        # power class

        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.yellowXSU
        elif self.udlr == "d":
            return a.yellowXSD
        elif self.udlr == "l":
            return a.yellowXSL
        elif self.udlr == "r":
            return a.yellowXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

bcMsg = ["Stores excess POWER",\
        "production for later","use. 100 Units."]
bcCost = [0,10,0,10,0,1,0]
batteryComplexCapsule = ["BATTERY COMPLEX","S",a.yellowXSU,a.yellowXSD,a.yellowXSR,a.yellowXSL,bcMsg,bcCost]
class BatteryComplex(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 0.0
        self.maintainCost = 0.025
        self.volume = 0.0
        self.buildingName = "BATTERY COMPLEX"
        self.drawSize = 'S'
        self.automated = True
        self.powerOutput = 0.0
        self.powerStorage = 100.0
        self.jobs = []
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.yellowXSU
        elif self.udlr == "d":
            return a.yellowXSD
        elif self.udlr == "l":
            return a.yellowXSL
        elif self.udlr == "r":
            return a.yellowXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

gMsg = ["Basic automatic POWER",\
        "generator, consumes FUEL",\
        "resource in operation.",\
        "5 mw max, 25 units storage."]
gCost = [0,0,5,15,0,5,0]
generatorCapsule = [["GENERATOR","POW"],"S",a.yellowXSU,a.yellowXSD,a.yellowXSR,a.yellowXSL,gMsg,gCost]
class Generator(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 12.0
        self.powerUsage = 0.0
        self.maintainCost = 0.02
        self.volume = 0.005
        self.buildingName = "GENERATOR"
        self.drawSize = 'S'
        self.automated = True
        self.powerOutput = 5.0
        self.powerStorage = 25.0
        self.jobs = []
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.yellowXSU
        elif self.udlr == "d":
            return a.yellowXSD
        elif self.udlr == "l":
            return a.yellowXSL
        elif self.udlr == "r":
            return a.yellowXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

spMsg = ["Simple solar panel",\
        "installation, sunlight",\
        "dependant power source.",\
        "5 mw max, 10 units storage."]
spCost = [10,0,0,20,0,5,0]
solarPanelCapsule = [["SOLAR PANEL","POW"],"S",a.yellowXSU,a.yellowXSD,a.yellowXSR,a.yellowXSL,spMsg,spCost]
class SolarPanel(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 0.0
        self.maintainCost = 0.02
        self.volume = 0.01
        self.buildingName = "SOLAR PANEL"
        self.drawSize = 'S'
        self.solar = True
        self.automated = True
        self.powerOutput = 5.0
        self.powerStorage = 10.0
        self.jobs = []
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.yellowXSU
        elif self.udlr == "d":
            return a.yellowXSD
        elif self.udlr == "l":
            return a.yellowXSL
        elif self.udlr == "r":
            return a.yellowXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

smMsg = ["Basic nuclear reactor.",\
        "Employs one, steady",\
        "electrical supply. 20 mw",]
smCost = [0,10,10,10,0,10,5]
simpleReactorCapsule = [["SIMPLE REACTOR","POW"],"S",a.yellowSU,a.yellowSD,a.yellowSR,a.yellowSL,smMsg,smCost]
class SimpleReactor(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 0.0
        self.maintainCost = 0.10
        self.volume = 0.3
        self.buildingName = "SIMPLE REACTOR"
        self.drawSize = 'S'
        self.nuclear = True
        self.powerOutput = 20.0
        t2 = i.Job("TECHNICIAN",0.2,0.5,0.3,self)
        self.jobs = [t2]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.yellowSU
        elif self.udlr == "d":
            return a.yellowSD
        elif self.udlr == "l":
            return a.yellowSL
        elif self.udlr == "r":
            return a.yellowSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

scMsg = ["Small array of solar",\
        "panels, converts sunlight",\
        "into electrical output.",\
        "12 mw max, 10 units storage."]
scCost = [10,0,5,35,0,10,0]
solarClusterCapsule = [["SOLAR CLUSTER","POW"],"M",a.yellowMUR,a.yellowMDL,a.yellowMDR,a.yellowMUL,scMsg,scCost]
class SolarCluster(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 0.0
        self.maintainCost = 0.05
        self.volume = 0.01
        self.buildingName = "SOLAR CLUSTER"
        self.drawSize = 'M'
        self.solar = True
        self.automated = True
        self.powerOutput = 12.0
        self.powerStorage = 10.0
        self.jobs = []
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.yellowMUR
        elif self.udlr == "d":
            return a.yellowMDL
        elif self.udlr == "l":
            return a.yellowMUL
        elif self.udlr == "r":
            return a.yellowMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

frMsg = ["Advanced fusion reactor.",\
        "Employs two, strong base",\
        "POWER source. 45 mw",]
frCost = [0,20,30,20,0,15,10]
fusionReactorCapsule = [["FUSION REACTOR","POW"],"M",a.yellowMLUR,a.yellowMLDL,a.yellowMLDR,a.yellowMLUL,frMsg,frCost]
class FusionReactor(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r": 
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 40.0
        self.powerUsage = 0.0
        self.maintainCost = 0.2
        self.volume = 0.6
        self.buildingName = "FUSION REACTOR"
        self.drawSize = 'M'
        self.nuclear = True
        self.powerOutput = 45.0
        self.powerStorage = 10.0
        t1 = i.Job("ENGINEER",0.2,0.6,0.2,self,1.5)
        t2 = i.Job("TECHNICIAN",0.2,0.5,0.3,self)
        self.jobs = [t1,t2]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.yellowMLUR
        elif self.udlr == "d":
            return a.yellowMLDL
        elif self.udlr == "l":
            return a.yellowMLUL
        elif self.udlr == "r":
            return a.yellowMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR

sfMsg = ["Large solar power",\
        "project, high electrical",\
        "output, sunlight dependant.",\
        "25 mw max, 10 units storage."]
sfCost = [10,0,15,65,0,15,0]
solarFarmCapsule = [["SOLAR FARM","POW"],"L",a.yellowL,a.yellowL,a.yellowL,a.yellowL,sfMsg,sfCost]
class SolarFarm(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 0.0
        self.maintainCost = 0.1
        self.volume = 0.01
        self.buildingName = "SOLAR FARM"
        self.drawSize = 'L'
        self.solar = True
        self.automated = True
        self.powerOutput = 25.0
        self.powerStorage = 10.0
        self.jobs = []
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # L RETURN
        return a.yellowL

    def getSurfaceConstruction(self):
        return a.clearL

srMsg = ["Large reactor complex.",\
        "Employs three, maximum",\
        "POWER generation. 100 mw",
        "Some battery storage."]
srCost = [0,40,60,50,0,20,15]
superReactorCapsule = [["SUPER REACTOR","POW"],"L",a.yellowXL,a.yellowXL,a.yellowXL,a.yellowXL,srMsg,srCost]
class SuperReactor(PowerBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 80.0
        self.powerUsage = 0.0
        self.maintainCost = 0.3
        self.volume = 1.0
        self.buildingName = "SUPER REACTOR"
        self.drawSize = 'L'
        self.nuclear = True
        self.powerOutput = 100.0
        self.powerStorage = 20.0
        t1 = i.Job("ENGINEER",0.2,0.6,0.2,self,1.5)
        t2 = i.Job("TECHNICIAN",0.2,0.5,0.3,self)
        t3 = i.Job("TECHNICIAN",0.2,0.5,0.3,self)
        self.jobs = [t1,t2,t3]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # XL RETURN
        return a.yellowXL

    def getSurfaceConstruction(self):
        return a.clearXL

#LIFE SUPPORT BUILDINGS
gdMsg = ["Small garden pod with",\
        "basic vegetation.",\
        "Outputs some AIR and",
        "ORGANICS. +PSYCH"]
gdCost = [12,0,8,0,0,0,5]
gardenCapsule = [["GARDEN","LS"],"S",a.greenXSU,a.greenXSD,a.greenXSR,a.greenXSL,gdMsg,gdCost]
class Garden(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 8.0
        self.powerUsage = 2.0
        self.maintainCost = 0.02
        self.volume = 0.5
        self.organicsOutput = 0.12
        self.buildingName = "GARDEN"
        self.drawSize = 'S'
        self.jobs = []
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greenXSU
        elif self.udlr == "d":
            return a.greenXSD
        elif self.udlr == "l":
            return a.greenXSL
        elif self.udlr == "r":
            return a.greenXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

    def specialFinish(self):
        self.base.environment.psychPoints += 2

amMsg = ["Pulls Martian CO2 to",\
        "convert to breathable",\
        "AIR, totally automated."]
amCost = [0,0,5,15,0,5,5]
airModCapsule = [["AIR MOD","LS"],"S",a.greenXSU,a.greenXSD,a.greenXSR,a.greenXSL,amMsg,amCost]
class AirMod(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 8.0
        self.powerUsage = 1.0
        self.maintainCost = 0.02
        self.volume = 0.0
        self.airOutput = 0.05
        self.buildingName = "AIR MOD"
        self.drawSize = 'S'
        self.jobs = []
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greenXSU
        elif self.udlr == "d":
            return a.greenXSD
        elif self.udlr == "l":
            return a.greenXSL
        elif self.udlr == "r":
            return a.greenXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

fpMsg = ["Basic Mars hydroponics",\
        "pod, provides FOOD from",\
        "WATER and ORGANICS.",
        "Employs one FARMER."]
fpCost = [15,0,12,0,0,3,10]
farmPodCapsule = [["FARM POD","LS"],"S",a.greenSU,a.greenSD,a.greenSR,a.greenSL,fpMsg,fpCost]
class FarmPod(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 3.0
        self.maintainCost = 0.03
        self.volume = 1
        self.buildingName = "FARM POD"
        self.drawSize = 'S'
        self.foodOutput = 0.15
        farmer = i.Job("FARMER",0.3,0.4,0.3,self)
        self.jobs = [farmer]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.greenSU
        elif self.udlr == "d":
            return a.greenSD
        elif self.udlr == "l":
            return a.greenSL
        elif self.udlr == "r":
            return a.greenSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

    def specialFinish(self):
        x = len(self.base.lifeSupportList)
        self.base.environment.psychPoints += 1

mgMsg = ["Expanded garden space",\
        "that produces ORGANICS",\
        "and lifts PSYCH.",\
        "Employs one GARDENER."]
mgCost = [25,0,20,5,0,0,10]
megaGardenCapsule = [["MEGA GARDEN","LS"],"M",a.greenMUR,a.greenMDL,a.greenMDR,a.greenMUL,mgMsg,mgCost]
class MegaGarden(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 4.0
        self.maintainCost = 0.05
        self.volume = 0.75
        self.organicsOutput = 0.3
        self.airOutput = 0.01
        self.buildingName = "MEGA GARDEN"
        self.drawSize = 'M'
        self.foodOutput = 0.0
        farmer = i.Job("GARDENER",0.3,0.3,0.4,self,1.3)
        self.jobs = [farmer]
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.greenMUR
        elif self.udlr == "d":
            return a.greenMDL
        elif self.udlr == "l":
            return a.greenMUL
        elif self.udlr == "r":
            return a.greenMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

    def specialFinish(self):
        x = len(self.base.lifeSupportList)
        self.base.environment.psychPoints += 4

mlMsg = ["A lab-grown meat",\
        "facility, provides FOOD",\
        "and boosts PSYCH base",\
        "wide. One employee."]
mlCost = [10,0,15,15,0,15,5]
meatLabCapsule = [["MEAT LAB","LS"],"M",a.greenMUR,a.greenMDL,a.greenMDR,a.greenMUL,mlMsg,mlCost]
class MeatLab(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 4.0
        self.maintainCost = 0.05
        self.volume = 0.75
        self.buildingName = "MEAT LAB"
        self.drawSize = 'M'
        self.foodOutput = 0.25
        farmer = i.Job("MEAT TECH",0.2,0.5,0.3,self)
        self.jobs = [farmer]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.greenMUR
        elif self.udlr == "d":
            return a.greenMDL
        elif self.udlr == "l":
            return a.greenMUL
        elif self.udlr == "r":
            return a.greenMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

    def specialFinish(self):
        x = len(self.base.lifeSupportList)
        self.base.environment.psychPoints += 3

ghMsg = ["Enclosed agricultural",\
        "unit, yields FOOD from",\
        "WATER and ORGANICS.",
        "Employs two FARMERS."]
ghCost = [15,0,20,0,0,5,20]
greenHouseCapsule = [["GREENHOUSE","LS"],"M",a.greenMLUR,a.greenMLDL,a.greenMLDR,a.greenMLUL,ghMsg,ghCost]
class GreenHouse(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 6.0
        self.maintainCost = 0.07
        self.volume = 1.75
        self.buildingName = "GREENHOUSE"
        self.drawSize = 'M'
        self.foodOutput = 0.40
        self.airOutput = 0.01
        self.organicsOutput = 0.05
        farmer = i.Job("FARMER",0.3,0.4,0.3,self)
        farmer1 = i.Job("FARMER",0.3,0.4,0.3,self)
        self.jobs = [farmer,farmer1]
        #finally
        self.tile.addBuilding(self)
     
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.greenMLUR
        elif self.udlr == "d":
            return a.greenMLDL
        elif self.udlr == "l":
            return a.greenMLUL
        elif self.udlr == "r":
            return a.greenMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR
    
    def specialFinish(self):
        x = len(self.base.lifeSupportList)
        self.base.environment.psychPoints += 2

trMsg = ["Indoor grow area for",\
        "vegetation and relaxation.",\
        "ORGNANICS produced. PSYCH+",\
        "Employs two GARDENERS."]
trCost = [50,0,40,10,0,0,15]
terrariumCapsule = [["TERRARIUM","LS"],"L",a.greenL,a.greenL,a.greenL,a.greenL,trMsg,trCost]
class Terrarium(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 7.0
        self.maintainCost = 0.1
        self.volume = 1.0
        self.organicsOutput = 0.75
        self.airOutput = 0.03
        self.buildingName = "TERRARIUM"
        self.drawSize = 'L'
        farmer = i.Job("BIOENGINEER",0.0,0.4,0.6,self,1.5)
        farmer1 = i.Job("GARDENER",0.3,0.3,0.4,self,1.3)
        self.jobs = [farmer,farmer1]
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # L RETURN
        return a.greenL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        x = len(self.base.lifeSupportList)
        self.base.environment.psychPoints += 10

fdMsg = ["Domed agricultural area",\
        "for FOOD production from",\
        "WATER and ORGANICS.",
        "Employs three FARMERS."]
fdCost = [30,0,40,0,0,5,45]
farmDomeCapsule = [["FARM DOME","LS"],"L",a.greenL,a.greenL,a.greenL,a.greenL,fdMsg,fdCost]
class FarmDome(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 10.0
        self.maintainCost = 0.12
        self.volume = 3.5
        self.buildingName = "FARM DOME"
        self.drawSize = 'L'
        self.foodOutput = 1.00
        self.airOutput = 0.02
        self.organicsOutput = 0.12
        farmer = i.Job("FARMER",0.3,0.4,0.3,self)
        farmer1 = i.Job("FARMER",0.3,0.4,0.3,self)
        farmer2 = i.Job("FARMER",0.3,0.4,0.3,self)
        self.jobs = [farmer,farmer1,farmer2]
        #finally
        self.tile.addBuilding(self)
      
    def getSurface(self):
        # L RETURN
        return a.greenL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        x = len(self.base.lifeSupportList)
        self.base.environment.psychPoints += 4

ffMsg = ["For production of heavily",\
        "processed and very tasty",\
        "FOOD. Plus PSYCH bonus.",
        "Employs three WORKERS."]
ffCost = [25,0,50,50,0,15,10]
foodFactoryCapsule = [["FOOD FACTORY","LS"],"L",a.greenXL,a.greenXL,a.greenXL,a.greenXL,ffMsg,ffCost]
class FoodFactory(LifeSupportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 75.0
        self.powerUsage = 12.0
        self.maintainCost = 0.15
        self.volume = 3.5
        self.buildingName = "FOOD FACTORY"
        self.drawSize = 'L'
        self.foodOutput = 1.3
        farmer = i.Job("FOOD FOREMAN",0.2,0.5,0.3,self,1.5)
        farmer1 = i.Job("FOOD TECH",0.2,0.6,0.2,self)
        farmer2 = i.Job("FOOD TECH",0.2,0.6,0.2,self)
        self.jobs = [farmer,farmer1,farmer2]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # XL RETURN
        return a.greenXL

    def getSurfaceConstruction(self):
        return a.clearXL

    def specialFinish(self):
        self.base.environment.psychPoints += 7

## EXTRACTION BUILDINGS ##
embMsg = ["Automated lander robot",\
        "that extracts available",\
        "REGOLITH, ORE, RARE, and",
        "WATER if present."]
minerBotLanderCapsule = [["MINER BOT","EX"],"S",a.redSU,a.redSD,a.redSR,a.redSL,embMsg]
class MinerBotLander(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 3.0
        self.maintainCost = 0.075
        self.volume = 0.0
        self.regolith = True
        self.ore = True
        self.rare = True
        self.water = True
        self.extractionEfficiency = 0.2
        self.calculateOutput()
        self.buildingName = "MINER BOT"
        self.drawSize = 'S'
        # storage class

        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.redSU
        elif self.udlr == "d":
            return a.redSD
        elif self.udlr == "l":
            return a.redSL
        elif self.udlr == "r":
            return a.redSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

    def specialFinish(self):
        self.base.generalStorageCapacity += 10

evpMsg = ["Creates small WATER",\
        "output from atmospheric",\
        "moisture. Automated."]
evpCost = [0,0,0,20,0,10,0]
vaporizerCapsule = [["VAPORIZER","EX"],"S",a.redXSU,a.redXSD,a.redXSR,a.redXSL,evpMsg,evpCost]
class Vaporizer(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 10.0
        self.powerUsage = 3.5
        self.maintainCost = 0.03
        self.volume = 0.0
        self.buildingName = "VAPORIZER"
        self.drawSize = 'S'
        self.water = True
        self.atmospheric = True
        self.extractionEfficiency = 1.0
        self.calculateOutput()
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.redXSU
        elif self.udlr == "d":
            return a.redXSD
        elif self.udlr == "l":
            return a.redXSL
        elif self.udlr == "r":
            return a.redXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

eidMsg = ["Pulls WATER resources",\
        "from the ground where",\
        "available. Employs one."]
eidCost = [0,0,10,20,0,10,0]
iceDrillCapsule = [["ICE DRILL","EX"],"S",a.redSU,a.redSD,a.redSR,a.redSL,eidMsg,eidCost]
class IceDrill(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 3.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "ICE DRILL"
        self.drawSize = 'S'
        self.water = True
        self.extractionEfficiency = 0.5
        self.calculateOutput()
        miner = i.Job("ICE MINER",0.4,0.4,0.2,self)
        self.jobs = [miner]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.redSU
        elif self.udlr == "d":
            return a.redSD
        elif self.udlr == "l":
            return a.redSL
        elif self.udlr == "r":
            return a.redSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

evfMsg = ["Intensive effort for",\
        "pulling moisture from",\
        "Martian atmosphere.",
        "Employs one."]
evfCost = [0,0,25,20,0,15,5]
vaporFarmCapsule = [["VAPOR FARM","EX"],"M",a.redMUR,a.redMDL,a.redMDR,a.redMUL,evfMsg,evfCost]
class VaporFarm(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 6.0
        self.maintainCost = 0.07
        self.volume = 0.0
        self.buildingName = "VAPOR FARM"
        self.drawSize = 'M'
        self.water = True
        self.atmospheric = True
        self.extractionEfficiency = 1.75
        self.calculateOutput()
        vFarmer = i.Job("VAPOR FARMER",0.4,0.4,0.2,self,1.2)
        self.jobs = [vFarmer]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.redMUR
        elif self.udlr == "d":
            return a.redMDL
        elif self.udlr == "l":
            return a.redMUL
        elif self.udlr == "r":
            return a.redMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

eipMsg = ["Digs out WATER ice",\
        "from below the surface",\
        "if present. Employs two."]
eipCost = [0,0,20,40,0,20,0]
icePitCapsule = [["ICE PIT","EX"],"M",a.redMLUR,a.redMLDL,a.redMLDR,a.redMLUL,eipMsg,eipCost]
class IcePit(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 4.5
        self.maintainCost = 0.08
        self.volume = 0.4
        self.buildingName = "ICE PIT"
        self.drawSize = 'M'
        self.water = True
        self.extractionEfficiency = 1.0
        self.calculateOutput()
        miner = i.Job("ICE MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("ICE MINER",0.4,0.4,0.2,self)
        self.jobs = [miner,miner2]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.redMLUR
        elif self.udlr == "d":
            return a.redMLDL
        elif self.udlr == "l":
            return a.redMLUL
        elif self.udlr == "r":
            return a.redMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR

eimMsg = ["High output ice mining",\
        "operation, provides WATER",\
        "if present. Employs three."]
eimCost = [0,0,30,50,0,30,10]
iceMineCapsule = [["ICE MINE","EX"],"L",a.redL,a.redL,a.redL,a.redL,eimMsg,eimCost]
class IceMine(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 6.0
        self.maintainCost = 0.15
        self.volume = 1.2
        self.buildingName = "ICE MINE"
        self.drawSize = 'L'
        self.water = True
        self.extractionEfficiency = 1.5
        self.calculateOutput()
        miner = i.Job("ICE MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("ICE MINER",0.4,0.4,0.2,self)
        miner3 = i.Job("ICE MINER",0.4,0.4,0.2,self)
        self.jobs = [miner,miner2,miner3]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # L RETURN
        return a.redL

    def getSurfaceConstruction(self):
        return a.clearL

eifMsg = ["Massive mining unit for",\
        "the extraction of WATER",\
        "if present. Employs four."]
eifCost = [0,0,40,70,0,35,15]
iceFacilityCapsule = [["ICE FACILITY","EX"],"L",a.redXL,a.redXL,a.redXL,a.redXL,eifMsg,eifCost]
class IceFacility(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 70.0
        self.powerUsage = 9.0
        self.maintainCost = 0.25
        self.volume = 1.6
        self.buildingName = "ICE FACILITY"
        self.drawSize = 'L'
        self.water = True
        self.extractionEfficiency = 3.0
        self.calculateOutput()
        minerA = i.Job("ICE FOREMAN",0.2,0.5,0.3,self,2.0)
        miner = i.Job("ICE MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("ICE MINER",0.4,0.4,0.2,self)
        miner3 = i.Job("ICE MINER",0.4,0.4,0.2,self)
        self.jobs = [minerA,miner,miner2,miner3]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # XL RETURN
        return a.redXL

    def getSurfaceConstruction(self):
        return a.clearXL

erpMsg = ["Automated dig for",\
        "harvesting Martian",\
        "REGOLITH."]
erpCost = [8,0,15,5,0,2,0]
regolithPitCapsule = [["REGOLITH PIT","EX"],"S",a.redXSU,a.redXSD,a.redXSR,a.redXSL,erpMsg,erpCost]
class RegolithPit(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 10.0
        self.powerUsage = 2.0
        self.maintainCost = 0.02
        self.volume = 0.0
        self.buildingName = "REGOLITH PIT"
        self.drawSize = 'S'
        self.regolith = True
        self.extractionEfficiency = 0.5
        self.calculateOutput()
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.redXSU
        elif self.udlr == "d":
            return a.redXSD
        elif self.udlr == "l":
            return a.redXSL
        elif self.udlr == "r":
            return a.redXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 10

eopMsg = ["Automated dig for",\
        "harvesting metal ORE."]
eopCost = [8,0,15,5,0,2,0]
orePitCapsule = [["ORE PIT","EX"],"S",a.redXSU,a.redXSD,a.redXSR,a.redXSL,eopMsg,eopCost]
class OrePit(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 10.0
        self.powerUsage = 2.0
        self.maintainCost = 0.02
        self.volume = 0.0
        self.buildingName = "ORE PIT"
        self.drawSize = 'S'
        self.ore = True
        self.extractionEfficiency = 0.5
        self.calculateOutput()
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.redXSU
        elif self.udlr == "d":
            return a.redXSD
        elif self.udlr == "l":
            return a.redXSL
        elif self.udlr == "r":
            return a.redXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

eraMsg = ["Automated mine for",\
        "harvesting Martian",\
        "RARE minerals."]
eraCost = [8,0,15,5,0,2,0]
rareSiteCapsule = [["RARE SITE","EX"],"S",a.redXSU,a.redXSD,a.redXSR,a.redXSL,eraMsg,eraCost]
class RareSite(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 10.0
        self.powerUsage = 2.0
        self.maintainCost = 0.02
        self.volume = 0.0
        self.buildingName = "RARE SITE"
        self.drawSize = 'S'
        self.rare = True
        self.extractionEfficiency = 0.5
        self.calculateOutput()
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.redXSU
        elif self.udlr == "d":
            return a.redXSD
        elif self.udlr == "l":
            return a.redXSL
        elif self.udlr == "r":
            return a.redXSR
        
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 5

ermMsg = ["Dedicated REGOLITH",\
        "mining operation,",\
        "employs one MINER."]
ermCost = [15,0,35,20,0,10,0]
regolithMineCapsule = [["REGOLITH MINE","EX"],"M",a.redMLUR,a.redMLDL,a.redMLDR,a.redMLUL,ermMsg,ermCost]
class RegolithMine(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 3.5
        self.maintainCost = 0.07
        self.volume = 0.5
        self.buildingName = "REGOLITH MINE"
        self.drawSize = 'M'
        self.regolith = True
        self.extractionEfficiency = 1.0
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.redMLUR
        elif self.udlr == "d":
            return a.redMLDL
        elif self.udlr == "l":
            return a.redMLUL
        elif self.udlr == "r":
            return a.redMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 30

eomMsg = ["Dedicated Mars ORE",\
        "mining operation,",\
        "employs one MINER."]
eomCost = [15,0,35,20,0,10,0]
oreMineCapsule = [["ORE MINE","EX"],"M",a.redMLUR,a.redMLDL,a.redMLDR,a.redMLUL,eomMsg,eomCost]
class OreMine(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 3.5
        self.maintainCost = 0.07
        self.volume = 0.5
        self.buildingName = "ORE MINE"
        self.drawSize = 'M'
        self.ore = True
        self.extractionEfficiency = 1.0
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner]
        #finally
        self.tile.addBuilding(self)
     
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.redMLUR
        elif self.udlr == "d":
            return a.redMLDL
        elif self.udlr == "l":
            return a.redMLUL
        elif self.udlr == "r":
            return a.redMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 20

ergMsg = ["Dedicated RARE",\
        "mining operation,",\
        "employs one MINER."]
ergCost = [15,0,35,20,0,10,0]
rareMineCapsule = [["RARE MINE","EX"],"M",a.redMLUR,a.redMLDL,a.redMLDR,a.redMLUL,ergMsg,ergCost]
class RareMine(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 3.5
        self.maintainCost = 0.07
        self.volume = 0.5
        self.buildingName = "RARE MINE"
        self.drawSize = 'M'
        self.rare = True
        self.extractionEfficiency = 1.0
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner]
        #finally
        self.tile.addBuilding(self)
     
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.redMLUR
        elif self.udlr == "d":
            return a.redMLDL
        elif self.udlr == "l":
            return a.redMLUL
        elif self.udlr == "r":
            return a.redMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR

    def specialFinish(self):
        self.base.generalStorageCapacity += 20

ereMsg = ["Large scale REGOLITH",\
        "harvesting operation,",\
        "employs two MINERS."]
ereCost = [20,0,45,45,0,10,0]
regolithExcavationCapsule = [["REGOLITH FIELD","EX"],"L",a.redL,a.redL,a.redL,a.redL,ereMsg,ereCost]
class RegolithExcavation(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 5.0
        self.maintainCost = 0.15
        self.volume = 0.3
        self.buildingName = "REGOLITH FIELD"
        self.drawSize = 'L'
        self.regolith = True
        self.extractionEfficiency = 2.25
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner,miner2]
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # L RETURN
        return a.redL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.generalStorageCapacity += 50

eoeMsg = ["Deep dig for metal",\
        "ORE below the surface,",\
        "employs two MINERS."]
eoeCost = [20,0,45,45,0,10,0]
oreExcavationCapsule = [["ORE EXCAVATION","EX"],"L",a.redL,a.redL,a.redL,a.redL,eoeMsg,eoeCost]
class OreExcavation(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 5.0
        self.maintainCost = 0.15
        self.volume = 0.3
        self.buildingName = "ORE EXCAVATION"
        self.drawSize = 'L'
        self.ore = True
        self.extractionEfficiency = 2.25
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner,miner2]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.redL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.generalStorageCapacity += 50

ehtMsg = ["State of the art mining",\
        "operation for RARE minerals,",\
        "employs two MINERS."]
ehtCost = [0,0,50,50,0,15,5]
hiTechMineCapsule = [["HI-TECH MINE","EX"],"L",a.redL,a.redL,a.redL,a.redL,ehtMsg,ehtCost]
class HiTechMine(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 6.0
        self.maintainCost = 0.20
        self.volume = 1.2
        self.buildingName = "HI-TECH MINE"
        self.drawSize = 'L'
        self.rare = True
        self.extractionEfficiency = 2.25
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner,miner2]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.redL

    def getSurfaceConstruction(self):
        return a.clearL
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 25

essMsg = ["Low cost combination",\
        "surface mining set-up",\
        "for REGOLITH and ORE,",\
        "employs two MINERS."]
essCost = [20,0,20,20,0,2,0]
regolithOreMineCapsule = [["SURFACE SCRAPE","EX"],"M",a.redMLUR,a.redMLDL,a.redMLDR,a.redMLUL,essMsg,essCost]
class RegolithOreMine(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 4.5
        self.maintainCost = 0.08
        self.volume = 0.4
        self.buildingName = "SURFACE SCRAPE"
        self.drawSize = 'M'
        self.regolith = True
        self.ore = True
        self.extractionEfficiency = 0.8
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner,miner2]
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.redMLUR
        elif self.udlr == "d":
            return a.redMLDL
        elif self.udlr == "l":
            return a.redMLUL
        elif self.udlr == "r":
            return a.redMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 40

esmMsg = ["General purpose Mars",\
        "mine, provides REGOLITH,",\
        "ORE, and RARE output.",\
        "Employs one MINER."]
esmCost = [0,0,15,15,0,0,0]
smallMineCapsule = [["SMALL MINE","EX"],"S",a.redSU,a.redSD,a.redSR,a.redSL,esmMsg,esmCost]
class SmallMine(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 3.0
        self.maintainCost = 0.05
        self.volume = 0.5
        self.buildingName = "SMALL MINE"
        self.drawSize = 'S'
        self.regolith = True
        self.ore = True
        self.rare = True
        self.extractionEfficiency = 0.2
        self.calculateOutput()
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [miner]
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.redSU
        elif self.udlr == "d":
            return a.redSD
        elif self.udlr == "l":
            return a.redSL
        elif self.udlr == "r":
            return a.redSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 10

efdMsg = ["Massive mining project",\
        "extracts available REGOLITH,",\
        "ORE, WATER, and RARE.",\
        "Employs four MINERS."]
efdCost = [20,0,60,60,0,10,10]
fullDigCapsule = [["FULL DIG","EX"],"L",a.redXL,a.redXL,a.redXL,a.redXL,efdMsg,efdCost]
class FullDig(ExtractionBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 70.0
        self.powerUsage = 9.0
        self.maintainCost = 0.25
        self.volume = 2.0
        self.buildingName = "FULL DIG"
        self.drawSize = 'L'
        self.water = True
        self.regolith = True
        self.ore = True
        self.rare = True
        self.extractionEfficiency = 1.7
        self.calculateOutput()
        minerA = i.Job("FOREMAN",0.3,0.5,0.2,self,2.0)
        miner = i.Job("MINER",0.4,0.4,0.2,self)
        miner2 = i.Job("MINER",0.4,0.4,0.2,self)
        miner3 = i.Job("MINER",0.4,0.4,0.2,self)
        self.jobs = [minerA,miner,miner2,miner3]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # XL RETURN
        return a.redXL

    def getSurfaceConstruction(self):
        return a.clearXL
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 80

### INDUSTRY BUILDINGS ###

icmMsg = ["Automated production",\
        "of CONCRETE from WATER",\
        "and REGOLITH."]
icmCost = [0,0,0,20,0,10,0]
concreteMixerCapsule = [["CONCRETE MIXER","IC"],"S",a.orangeXSU,a.orangeXSD,a.orangeXSR,a.orangeXSL,icmMsg,icmCost]
class ConcreteMixer(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 10.0
        self.powerUsage = 2.0
        self.maintainCost = 0.03
        self.volume = 0.0
        self.buildingName = "CONCRETE MIXER"
        self.drawSize = 'S'
        self.efficiency = 0.25
        self.industry = self.base.concreteIndustry
        self.readoutTag = "concrete"
        self.automated = True
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeXSU
        elif self.udlr == "d":
            return a.orangeXSD
        elif self.udlr == "l":
            return a.orangeXSL
        elif self.udlr == "r":
            return a.orangeXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

icwMsg = ["Basic CONCRETE",\
        "production building.",\
        "Employs one."]
icwCost = [8,0,15,15,0,2,0]
concreteWorkshopCapsule = [["CONCRETE WORKSHOP","IC"],"S",a.orangeSU,a.orangeSD,a.orangeSR,a.orangeSL,icwMsg,icwCost]
class ConcreteWorkshop(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 3.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "CONCRETE WORKSHOP"
        self.drawSize = 'S'
        self.efficiency = 0.40
        j3 = i.Job("WORKER",0.6,0.2,0.2,self)
        self.jobs = [j3]
        self.industry = self.base.concreteIndustry
        self.readoutTag = "concrete"
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeSU
        elif self.udlr == "d":
            return a.orangeSD
        elif self.udlr == "l":
            return a.orangeSL
        elif self.udlr == "r":
            return a.orangeSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

iclMsg = ["Industrial CONCRETE",\
        "producing building.",\
        "Employs two."]
iclCost = [0,0,30,25,0,5,0]
concretePlantCapsule = [["CONCRETE PLANT","IC"],"M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,iclMsg,iclCost]
class ConcretePlant(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 5.0
        self.maintainCost = 0.10
        self.volume = 0.4
        self.buildingName = "CONCRETE PLANT"
        self.drawSize = 'M'
        self.efficiency = 0.80
        j2 = i.Job("WORKER",0.6,0.2,0.2,self)
        j3 = i.Job("WORKER",0.6,0.2,0.2,self)
        self.jobs = [j3,j2]
        self.industry = self.base.concreteIndustry
        self.readoutTag = "concrete"
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

icfMsg = ["Full scale CONCRETE",\
        "mass-producing facility.",\
        "Employs three. +50 storage."]
icfCost = [0,0,60,50,0,10,0]
concreteFactoryCapsule = [["CONCRETE FACTORY","IC"],"L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,icfMsg,icfCost]
class ConcreteFactory(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 9.0
        self.maintainCost = 0.2
        self.volume = 1.0
        self.buildingName = "CONCRETE FACTORY"
        self.drawSize = 'L'
        self.efficiency = 1.6
        j1 = i.Job("CONCRETE FOREMAN",0.3,0.5,0.2,self,1.5)
        j2 = i.Job("WORKER",0.6,0.2,0.2,self)
        j3 = i.Job("WORKER",0.6,0.2,0.2,self)
        self.jobs = [j1,j2,j3]
        self.industry = self.base.concreteIndustry
        self.readoutTag = "concrete"
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL
    
    def specialFinish(self):
        self.base.generalStorageCapacity += 50

iasMsg = ["Automated production",\
        "of METAL from ORE."]
iasCost = [0,0,10,10,0,10,0]
autoSmelterCapsule = [["AUTO SMELTER","IM"],"S",a.orangeXSU,a.orangeXSD,a.orangeXSR,a.orangeXSL,iasMsg,iasCost]
class AutoSmelter(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 10.0
        self.powerUsage = 2.0
        self.maintainCost = 0.03
        self.volume = 0.0
        self.buildingName = "AUTO SMELTER"
        self.drawSize = 'S'
        self.efficiency = 0.25
        self.industry = self.base.metalIndustry
        self.readoutTag = "metal"
        self.automated = True
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeXSU
        elif self.udlr == "d":
            return a.orangeXSD
        elif self.udlr == "l":
            return a.orangeXSL
        elif self.udlr == "r":
            return a.orangeXSR
        
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

imsMsg = ["Basic METAL work",\
        "production building.",\
        "Employs one."]
imsCost = [8,0,15,15,0,2,0]
metalsmithCapsule = [["METALSMITH","IM"],"S",a.orangeSU,a.orangeSD,a.orangeSR,a.orangeSL,imsMsg,imsCost]
class Metalsmith(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 3.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "METALSMITH"
        self.drawSize = 'S'
        self.efficiency = 0.40
        j3 = i.Job("METAL WORKER",0.6,0.2,0.2,self)
        self.jobs = [j3]
        self.industry = self.base.metalIndustry
        self.readoutTag = "metal"
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeSU
        elif self.udlr == "d":
            return a.orangeSD
        elif self.udlr == "l":
            return a.orangeSL
        elif self.udlr == "r":
            return a.orangeSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

ismMsg = ["Industrial METAL",\
        "production building.",\
        "Employs two."]
ismCost = [0,0,30,25,0,5,0]
steelMillCapsule = [["STEEL MILL","IM"],"M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,ismMsg,ismCost]
class SteelMill(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 5.0
        self.maintainCost = 0.10
        self.volume = 0.4
        self.buildingName = "STEEL MILL"
        self.drawSize = 'M'
        self.efficiency = 0.75
        j2 = i.Job("METAL WORKER",0.6,0.2,0.2,self)
        j3 = i.Job("METAL WORKER",0.6,0.2,0.2,self)
        self.jobs = [j3,j2]
        self.industry = self.base.metalIndustry
        self.readoutTag = "metal"
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

imcMsg = ["Full scale METAL",\
        "mass-producing facility.",\
        "Employs three. +50 storage."]
imcCost = [0,0,60,50,0,10,0]
metalFactoryCapsule = [["METAL FACTORY","IM"],"L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,imcMsg,imcCost]
class MetalFactory(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 9.0
        self.maintainCost = 0.2
        self.volume = 1.0
        self.buildingName = "METAL FACTORY"
        self.drawSize = 'L'
        self.efficiency = 1.5
        j1 = i.Job("METAL FOREMAN",0.3,0.5,0.2,self,1.5)
        j2 = i.Job("METAL WORKER",0.6,0.2,0.2,self)
        j3 = i.Job("METAL WORKER",0.6,0.2,0.2,self)
        self.jobs = [j1,j2,j3]
        self.industry = self.base.metalIndustry
        self.readoutTag = "metal"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.generalStorageCapacity += 50

ielMsg = ["Automated production",\
        "of FUEL using Martian",\
        "atmospheric inputs."]
ielCost = [0,0,0,15,0,10,5]
electrolyserCapsule = [["ELECTROLYSER","IF"],"S",a.orangeXSU,a.orangeXSD,a.orangeXSR,a.orangeXSL,ielMsg,ielCost]
class Electrolyser(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 10.0
        self.powerUsage = 2.5
        self.maintainCost = 0.03
        self.volume = 0.0
        self.buildingName = "ELECTROLYSER"
        self.drawSize = 'S'
        self.efficiency = 0.25
        self.industry = self.base.fuelIndustry
        self.readoutTag = "fuel"
        self.automated = True
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeXSU
        elif self.udlr == "d":
            return a.orangeXSD
        elif self.udlr == "l":
            return a.orangeXSL
        elif self.udlr == "r":
            return a.orangeXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

ifwMsg = ["Basic FUEL refining",\
        "laboratory building.",\
        "Employs one."]
ifwCost = [8,0,15,10,0,5,2]
fuelWorkshopCapsule = [["FUEL WORKSHOP","IF"],"S",a.orangeSU,a.orangeSD,a.orangeSR,a.orangeSL,ifwMsg,ifwCost]
class FuelWorkshop(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 4.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "FUEL WORKSHOP"
        self.readoutTag = "fuel"
        self.drawSize = 'S'
        self.efficiency = 0.40
        j3 = i.Job("WORKER",0.6,0.2,0.2,self)
        self.jobs = [j3]
        self.industry = self.base.fuelIndustry
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeSU
        elif self.udlr == "d":
            return a.orangeSD
        elif self.udlr == "l":
            return a.orangeSL
        elif self.udlr == "r":
            return a.orangeSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

ifpMsg = ["High capacity FUEL",\
        "production facility.",\
        "Employs two."]
ifpCost = [0,0,25,20,0,10,5]
fuelPlantCapsule = [["FUEL PLANT","IF"],"M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,ifpMsg,ifpCost]
class FuelPlant(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 6.5
        self.maintainCost = 0.10
        self.volume = 0.4
        self.buildingName = "FUEL PLANT"
        self.drawSize = 'M'
        self.efficiency = 0.75
        j2 = i.Job("WORKER",0.6,0.2,0.2,self)
        j3 = i.Job("WORKER",0.6,0.2,0.2,self)
        self.jobs = [j3,j2]
        self.industry = self.base.fuelIndustry
        self.readoutTag = "fuel"
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

irfMsg = ["Full scale Martian",\
        "FUEL refining plant.",\
        "Employs three."]
irfCost = [0,0,50,40,0,20,10]
refineryCapsule = [["REFINERY","IF"],"L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,irfMsg,irfCost]
class Refinery(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 11.0
        self.maintainCost = 0.2
        self.volume = 1.0
        self.buildingName = "REFINERY"
        self.drawSize = 'L'
        self.efficiency = 1.5
        j1 = i.Job("FOREMAN",0.3,0.5,0.2,self,1.5)
        j2 = i.Job("WORKER",0.6,0.2,0.2)
        j3 = i.Job("WORKER",0.6,0.2,0.2)
        self.jobs = [j1,j2,j3]
        self.industry = self.base.fuelIndustry
        self.readoutTag = "fuel"
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL

imlMsg = ["Basic medical lab",\
        "producing MEDS from",\
        "RARE adn ORGANICS.",\
        "Employs one."]
imlCost = [0,0,15,5,0,10,10]
medicalLabCapsule = [["MEDICAL LAB","ID"],"S",a.orangeSU,a.orangeSD,a.orangeSR,a.orangeSL,imlMsg,imlCost]
class MedicalLab(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 3.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "MEDICAL LAB"
        self.drawSize = 'S'
        self.efficiency = 0.40
        j3 = i.Job("CHEMIST",0.1,0.8,0.1,self)
        self.jobs = [j3]
        self.industry = self.base.medsIndustry
        self.readoutTag = "meds"
        #finally
        self.tile.addBuilding(self)
 
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeSU
        elif self.udlr == "d":
            return a.orangeSD
        elif self.udlr == "l":
            return a.orangeSL
        elif self.udlr == "r":
            return a.orangeSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

imfMsg = ["Scaled up MEDS",\
        "production facility.",\
        "Employs two."]
imfCost = [0,0,25,10,0,10,15]
medsFacilityCapsule = [["MEDS FACILITY","ID"],"M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,imfMsg,imfCost]
class MedsFacility(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 5.0
        self.maintainCost = 0.10
        self.volume = 0.4
        self.buildingName = "MEDS FACILITY"
        self.drawSize = 'M'
        self.efficiency = 0.75
        j2 = i.Job("CHEMIST",0.1,0.8,0.1,self,1.5)
        j3 = i.Job("WORKER",0.3,0.4,0.3,self)
        self.jobs = [j3,j2]
        self.industry = self.base.medsIndustry
        self.readoutTag = "meds"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

imdMsg = ["Pharmacutical factory",\
        "for mass-producing MEDS.",\
        "Employs three."]
imdCost = [0,0,50,20,0,20,30]
medsFactoryCapsule = [["MEDS FACTORY","ID"],"L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,imdMsg,imdCost]
class MedsFactory(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 9.0
        self.maintainCost = 0.2
        self.volume = 1.0
        self.buildingName = "MEDS FACTORY"
        self.drawSize = 'L'
        self.efficiency = 1.5
        j1 = i.Job("CHEMIST",0.1,0.8,0.1,self,1.5)
        j2 = i.Job("WORKER",0.3,0.4,0.3,self)
        j3 = i.Job("WORKER",0.3,0.4,0.3,self)
        self.jobs = [j1,j2,j3]
        self.industry = self.base.medsIndustry
        self.readoutTag = "meds"
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL

iewMsg = ["Production facility",\
        "making ELECTRONICS out",\
        "of METAL and RARE.",\
        "Employs one."]
iewCost = [0,5,15,10,0,5,5]
electronicsWorkshopCapsule = [["ELECTRONICS SHOP","IE"],"S",a.orangeSU,a.orangeSD,a.orangeSR,a.orangeSL,iewMsg,iewCost]
class ElectronicsWorkshop(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 4.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "ELECTRONICS SHOP"
        self.drawSize = 'S'
        self.efficiency = 0.40
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3]
        self.industry = self.base.electronicsIndustry
        self.readoutTag = "electronics"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeSU
        elif self.udlr == "d":
            return a.orangeSD
        elif self.udlr == "l":
            return a.orangeSL
        elif self.udlr == "r":
            return a.orangeSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

icpMsg = ["Technology manufacture",\
        "building ELECTRONICS out",\
        "of METAL and RARE.",\
        "Employs two."]
icpCost = [0,5,30,10,0,10,5]
circuitPlantCapsule = [["CIRCUIT PLANT","IE"],"M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,icpMsg,icpCost]
class CircuitPlant(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 6.5
        self.maintainCost = 0.10
        self.volume = 0.4
        self.buildingName = "CIRCUIT PLANT"
        self.drawSize = 'M'
        self.efficiency = 0.75
        j2 = i.Job("WORKER",0.3,0.4,0.3,self)
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3,j2]
        self.industry = self.base.electronicsIndustry
        self.readoutTag = "electronics"
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

iemMsg = ["Factory scale unit for",\
        "ELECTRONICS production",\
        "Employs three."]
iemCost = [0,5,60,20,0,20,15]
eManufacturerCapsule = [["E-MANUFACTURER","IE"],"L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,iemMsg,iemCost]
class EManufacturer(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 11.0
        self.maintainCost = 0.2
        self.volume = 1.0
        self.buildingName = "E-MANUFACTURER"
        self.drawSize = 'L'
        self.efficiency = 1.5
        j1 = i.Job("WORKER",0.3,0.4,0.3,self)
        j2 = i.Job("WORKER",0.3,0.4,0.3,self)
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3,j2,j1]
        self.industry = self.base.electronicsIndustry
        self.readoutTag = "electronics"
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.generalStorageCapacity += 20

ippMsg = ["Basic PLASTICS lab",\
        "uses FUEL and ORGANICS.",\
        "Employs one."]
ippCost = [0,0,20,15,0,5,0]
polymerPodCapsule = [["POLYMER POD","IP"],"S",a.orangeSU,a.orangeSD,a.orangeSR,a.orangeSL,ippMsg,ippCost]
class PolymerPod(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 4.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "POLYMER POD"
        self.drawSize = 'S'
        self.efficiency = 0.40
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3]
        self.industry = self.base.plasticsIndustry
        self.readoutTag = "plastics"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeSU
        elif self.udlr == "d":
            return a.orangeSD
        elif self.udlr == "l":
            return a.orangeSL
        elif self.udlr == "r":
            return a.orangeSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

iplMsg = ["Intensive PLASTICS",\
        "production facility.",\
        "Employs two."]
iplCost = [0,0,25,20,0,15,0]
plasticsPlantCapsule = [["PLASTICS PLANT","IP"],"M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,iplMsg,iplCost]
class PlasticsPlant(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 6.5
        self.maintainCost = 0.10
        self.volume = 0.4
        self.buildingName = "PLASTICS PLANT"
        self.drawSize = 'M'
        self.efficiency = 0.75
        j2 = i.Job("WORKER",0.3,0.4,0.3,self)
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3,j2]
        self.industry = self.base.plasticsIndustry
        self.readoutTag = "plastics"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

ipfMsg = ["Large scale PLASTICS",\
        "manufacturer using FUEL",\
        "and ORGANICS.",\
        "Employs three."]
ipfCost = [0,0,50,40,0,30,0]
plasticsFactoryCapsule = [["PLASTICS FACTORY","IP"],"L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,ipfMsg,ipfCost]
class PlasticsFactory(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 11.0
        self.maintainCost = 0.2
        self.volume = 1.0
        self.buildingName = "PLASTICS FACTORY"
        self.drawSize = 'L'
        self.efficiency = 1.5
        j1 = i.Job("WORKER",0.3,0.4,0.3,self)
        j2 = i.Job("WORKER",0.3,0.4,0.3,self)
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3,j2,j1]
        self.industry = self.base.plasticsIndustry
        self.readoutTag = "plastics"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL

iroMsg = ["Automated unit for heating",\
        "WATER vapor from REGOLITH."]
iroCost = [0,0,10,10,0,5,5]
regOvenCapsule = [["REG OVEN","IW"],"S",a.orangeXSU,a.orangeXSD,a.orangeXSR,a.orangeXSL,iroMsg,iroCost]
class RegOven(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 12.0
        self.powerUsage = 4.0
        self.maintainCost = 0.05
        self.volume = 0.05
        self.automated = True
        self.buildingName = "REG OVEN"
        self.drawSize = 'S'
        self.efficiency = 0.25
        self.jobs = []
        self.industry = self.base.waterFromRegolithIndustry
        self.readoutTag = "water"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeXSU
        elif self.udlr == "d":
            return a.orangeXSD
        elif self.udlr == "l":
            return a.orangeXSL
        elif self.udlr == "r":
            return a.orangeXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

ircMsg = ["Extracts WATER from",\
        "REGOLITH through heating.",\
        "Employs one."]
ircCost = [0,0,20,15,0,2,3]
rockCookerCapsule = [["ROCK COOKER","IW"],"S",a.orangeSU,a.orangeSD,a.orangeSR,a.orangeSL,ircMsg,ircCost]
class RockCooker(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 5.0
        self.maintainCost = 0.05
        self.volume = 0.2
        self.buildingName = "ROCK COOKER"
        self.drawSize = 'S'
        self.efficiency = 0.45
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3]
        self.industry = self.base.waterFromRegolithIndustry
        self.readoutTag = "water"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeSU
        elif self.udlr == "d":
            return a.orangeSD
        elif self.udlr == "l":
            return a.orangeSL
        elif self.udlr == "r":
            return a.orangeSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

imeMsg = ["Scaled up extraction",\
        "of WATER from REGOLITH.",\
        "Employs two."]
imeCost = [0,0,25,20,0,10,5]
marsEvaporatorCapsule = [["MARS EVAPORATOR","IW"],"M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,imeMsg,imeCost]
class MarsEvaporator(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 7.75
        self.maintainCost = 0.10
        self.volume = 0.4
        self.buildingName = "MARS EVAPORATOR"
        self.drawSize = 'M'
        self.efficiency = 0.8
        j2 = i.Job("WORKER",0.3,0.4,0.3,self)
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self)
        self.jobs = [j3,j2]
        self.industry = self.base.waterFromRegolithIndustry
        self.readoutTag = "water"
        #finally
        self.tile.addBuilding(self)
       
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

irsMsg = ["Industrial scale WATER",\
        "production from REGOLITH.",\
        "Employs 3. +50 water storage."]
irsCost = [0,0,55,40,0,20,5]
regolithSteamerCapsule = [["REGOLITH STEAMER","IW"],"L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,irsMsg,irsCost]
class RegolithSteamer(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 60.0
        self.powerUsage = 13.5
        self.maintainCost = 0.2
        self.volume = 1.0
        self.buildingName = "REGOLITH STEAMER"
        self.drawSize = 'L'
        self.efficiency = 1.6
        j1 = i.Job("WORKER",0.3,0.4,0.3,self)
        j2 = i.Job("WORKER",0.3,0.4,0.3,self)
        j3 = i.Job("ENGINEER",0.2,0.6,0.2,self,1.25)
        self.jobs = [j3,j2,j1]
        self.industry = self.base.waterFromRegolithIndustry
        self.readoutTag = "water"
        #finally
        self.tile.addBuilding(self)
     
    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.water.storageCapacity += 50


irpMsg = ["Simple ROBOT building pod",\
        "for your BUILDERS to use. Holds",\
        "2 ROBOTS. No full employees."]
irpCost = [0,1,20,3,0,4,2]
roboPodCapsule = ["ROBO-POD","S",a.orangeXSU,a.orangeXSD,a.orangeXSR,a.orangeXSL,irpMsg,irpCost]
class RoboPod(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 2.0
        self.maintainCost = 0.1
        self.volume = 0.2
        self.buildingName = "ROBO-POD"
        self.drawSize = 'S'
        self.efficiency = 0.60
        self.jobs = []
        self.industry = None
        self.robots = True
        self.robotsStorage = 2
        self.readoutTag = "robots"
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.orangeXSU
        elif self.udlr == "d":
            return a.orangeXSD
        elif self.udlr == "l":
            return a.orangeXSL
        elif self.udlr == "r":
            return a.orangeXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

irwMsg = ["Space for your BUILDERS",\
        "to create ROBOTS. Can store",\
        "5 ROBOTS. No full employees."]
irwCost = [0,2,40,5,0,8,5]
robotWorkshopCapsule = ["ROBOT WORKSHOP","M",a.orangeMUR,a.orangeMDL,a.orangeMDR,a.orangeMUL,irwMsg,irwCost]
class RobotWorkshop(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 3.0
        self.maintainCost = 0.15
        self.volume = 0.4
        self.buildingName = "ROBOT WORKSHOP"
        self.drawSize = 'M'
        self.efficiency = 0.75
        self.jobs = []
        self.industry = None
        self.robots = True
        self.robotsStorage = 5
        self.readoutTag = "robots"
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.orangeMUR
        elif self.udlr == "d":
            return a.orangeMDL
        elif self.udlr == "l":
            return a.orangeMUL
        elif self.udlr == "r":
            return a.orangeMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

irfMsg = ["Facility for your BUILDERS",\
        "to work on ROBOTS. Holds up to",\
        "12 ROBOTS. No full employees."]
irfCost = [0,5,75,15,0,15,10]
robotFactoryCapsule = ["ROBOT FACTORY","L",a.orangeL,a.orangeL,a.orangeL,a.orangeL,irfMsg,irfCost]
class RobotFactory(IndustryBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 45.0
        self.powerUsage = 4.5
        self.maintainCost = 0.25
        self.volume = 0.75
        self.buildingName = "ROBOT FACTORY"
        self.drawSize = 'L'
        self.efficiency = 1.0
        self.jobs = []
        self.industry = None
        self.robots = True
        self.robotsStorage = 12
        self.readoutTag = "robots"
        #finally
        self.tile.addBuilding(self)
     
    def getSurface(self):
        # L RETURN
        return a.orangeL

    def getSurfaceConstruction(self):
        return a.clearL            

## LAB BUILDINGS ##
pbMsg = ["Instrument packed Mars",\
        "lander that reveals tile's",\
        "resources on touchdown."]
probeLanderCapsule = ["PROBE","S",a.purpleXSU,a.purpleXSD,a.purpleXSR,a.purpleXSL,pbMsg]
class ProbeLander(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.05
        self.maintainCost = 0.01
        self.volume = 0.0
        self.buildingName = "PROBE"
        self.drawSize = 'S'
        self.output = 0.25
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.purpleXSU
        elif self.udlr == "d":
            return a.purpleXSD
        elif self.udlr == "l":
            return a.purpleXSL
        elif self.udlr == "r":
            return a.purpleXSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    def specialFinish(self):
        if self.tile.explored == False:
            self.base.revealTile(self.tile)
        if self.tile.x > 1:
            if self.base.getTile(self.tile.x-1,self.tile.y).explored == False:
                self.base.revealTile(self.base.getTile(self.tile.x-1,self.tile.y))
        if self.tile.y > 1:
            if self.base.getTile(self.tile.x,self.tile.y-1).explored == False:
                self.base.revealTile(self.base.getTile(self.tile.x,self.tile.y-1))
        if self.tile.x < len(self.base.map.grid):
            if self.base.getTile(self.tile.x+1,self.tile.y).explored == False:
                self.base.revealTile(self.base.getTile(self.tile.x+1,self.tile.y))
        if self.tile.y < len(self.base.map.grid):
            if self.base.getTile(self.tile.x,self.tile.y+1).explored == False:
                self.base.revealTile(self.base.getTile(self.tile.x,self.tile.y+1))
        
        

spMsg = ["Automated Martian soil",\
        "analysis which reveals",\
        "tile's resourses."]
spCost = [0,0,0,15,0,5,0]
surveyPostCapsule = ["SURVEY POST","S",a.purpleXSU,a.purpleXSD,a.purpleXSR,a.purpleXSL,spMsg,spCost]
class SurveyPost(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 8.0
        self.powerUsage = 0.1
        self.maintainCost = 0.01
        self.volume = 0.0
        self.buildingName = "SURVEY POST"
        self.drawSize = 'S'
        self.output = 0.0
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.purpleXSU
        elif self.udlr == "d":
            return a.purpleXSD
        elif self.udlr == "l":
            return a.purpleXSL
        elif self.udlr == "r":
            return a.purpleXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR
    
    def specialFinish(self):
        if self.tile.explored == False:
            self.base.revealTile(self.tile)

flMsg = ["Simple outpost for",\
        "generating Mars SCIENCE.",\
        "Employs SCIENTIST."]
flCost = [20,0,10,5,0,3,2]
fieldLabCapsule = [["FIELD LAB","MED"],"S",a.purpleSU,a.purpleSD,a.purpleSR,a.purpleSL,flMsg,flCost]
class FieldLab(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 12.0
        self.powerUsage = 1.5
        self.maintainCost = 0.05
        self.volume = 0.5
        self.buildingName = "FIELD LAB"
        self.drawSize = 'S'
        self.output = 0.5
        self.medicalFactor = 0.05
        j3 = i.Job("SCIENTIST",0.1,0.7,0.2,self)
        self.jobs = [j3]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.purpleSU
        elif self.udlr == "d":
            return a.purpleSD
        elif self.udlr == "l":
            return a.purpleSL
        elif self.udlr == "r":
            return a.purpleSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

    def specialFinish(self):
        self.base.educationPoints += 1

lbMsg = ["Research facility for",\
        "production of SCIENCE pts.",\
        "Employs two SCIENTISTS."]
lbCost = [10,0,25,10,0,10,5]
laboratoryCapsule = [["LABORATORY","MED"],"M",a.purpleMUR,a.purpleMDL,a.purpleMDR,a.purpleMUL,lbMsg,lbCost]
class Laboratory(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 2.5
        self.maintainCost = 0.07
        self.volume = 0.7
        self.medicalFactor = 0.1
        self.buildingName = "LABORATORY"
        self.drawSize = 'M'
        self.output = 1.0
        j3 = i.Job("RESEARCHER",0.1,0.7,0.2,self,1.3)
        j2 = i.Job("SCIENTIST",0.1,0.7,0.2,self)
        self.jobs = [j3,j2]
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.purpleeMUR
        elif self.udlr == "d":
            return a.purpleMDL
        elif self.udlr == "l":
            return a.purpleMUL
        elif self.udlr == "r":
            return a.purpleMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

    def specialFinish(self):
        self.base.educationPoints += 2

scMsg = ["Full campus for research",\
        "and generating SCIENCE pts.",\
        "Employs three SCIENTISTS."]
scCost = [10,0,25,10,0,10,5]
scienceComplexCapsule = [["SCIENCE COMPLEX","MED"],"L",a.purpleL,a.purpleL,a.purpleL,a.purpleL,scMsg,scCost]
class ScienceComplex(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 4.7
        self.maintainCost = 0.13
        self.volume = 1.3
        self.buildingName = "SCIENCE COMPLEX"
        self.drawSize = 'L'
        self.output = 2.0
        self.medicalFactor = 0.1
        j3 = i.Job("HEAD SCIENTIST",0.0,0.8,0.2,self,1.6)
        j2 = i.Job("SCIENTIST",0.1,0.7,0.2,self)
        j1 = i.Job("SCIENTIST",0.1,0.7,0.2,self)
        self.jobs = [j3,j2,j1]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.purpleL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.educationPoints += 3

mdpMsg = ["Deliverable medical resource",\
        "gives small HEALTH bonus and",\
        "carries 50 MEDS."]
medDepotCapsule = [["MED DEPOT","MED"],"S",a.purpleSU,a.purpleSD,a.purpleSR,a.purpleSL,mdpMsg]
class MedDepot(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 1.75
        self.maintainCost = 0.06
        self.volume = 0.2
        self.buildingName = "MED DEPOT"
        self.drawSize = 'S'
        self.output = 0.0
        self.exploreIncrease = 1.0
        self.medicalFactor = 0.2
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.purpleSU
        elif self.udlr == "d":
            return a.purpleSD
        elif self.udlr == "l":
            return a.purpleSL
        elif self.udlr == "r":
            return a.purpleSR
    
    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR

    def specialFinish(self):
        self.base.meds.quantity += 50.0
        self.base.generalStorageCapacity += 50.0

mbMsg = ["Automated medical station",\
        "that provides HEALTH bonus.",\
        "Slight SCIENCE output."]
mbCost = [0,0,10,5,0,5,5]
medBotCapsule = [["MED BOT","MED"],"S",a.purpleXSU,a.purpleXSD,a.purpleXSR,a.purpleXSL,mbMsg,mbCost]
class MedBot(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 2.0
        self.maintainCost = 0.05
        self.volume = 0.5
        self.buildingName = "MED BOT"
        self.drawSize = 'S'
        self.output = 0.0
        self.exploreIncrease = 1.0
        self.medicalFactor = 0.3
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.purpleXSU
        elif self.udlr == "d":
            return a.purpleXSD
        elif self.udlr == "l":
            return a.purpleXSL
        elif self.udlr == "r":
            return a.purpleXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

fhMsg = ["Healthcare resource for",\
        "your base. HEALTH bonus",\
        "plus some SCIENCE output.",\
        "Employs DOCTOR."]
fhCost = [0,5,30,15,0,15,15]
fieldHospitalCapsule = [["FIELD HOSPITAL","MED"],"M",a.purpleMLUR,a.purpleMLDL,a.purpleMLDR,a.purpleMLUL,fhMsg,fhCost]
class FieldHospital(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 32.0
        self.powerUsage = 3.25
        self.maintainCost = 0.1
        self.volume = 0.75
        self.buildingName = "FIELD HOSPITAL"
        self.drawSize = 'M'
        self.output = 0.1
        self.exploreIncrease = 1.0
        self.medicalFactor = 0.75
        j3 = i.Job("DOCTOR",0.0,0.7,0.3,self,1.15)
        self.jobs = [j3]
        #finally
        self.tile.addBuilding(self)
   
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.purpleMLUR
        elif self.udlr == "d":
            return a.purpleMLDL
        elif self.udlr == "l":
            return a.purpleMLUL
        elif self.udlr == "r":
            return a.purpleMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR
    
    def specialFinish(self):
        self.base.environment.psychPoints += 1

hMsg = ["High tech medical center",\
        "that boosts base-wide health.",\
        "Employs two DOCTORS."]
hCost = [0,10,80,20,0,30,20]
hospitalCapsule = [["HOSPITAL","MED"],"L",a.purpleXL,a.purpleXL,a.purpleXL,a.purpleXL,hMsg,hCost]
class Hospital(LabBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 70.0
        self.powerUsage = 6.0
        self.maintainCost = 0.17
        self.volume = 1.5
        self.buildingName = "HOSPITAL"
        self.drawSize = 'L'
        self.output = 0.25
        self.exploreIncrease = 1.0
        self.medicalFactor = 1.3
        j2 = i.Job("DOCTOR",0.0,0.7,0.3,self,1.15)
        j3 = i.Job("DOCTOR",0.0,0.7,0.3,self,1.15)
        self.jobs = [j2,j3]
        #finally
        self.tile.addBuilding(self)
     
    def getSurface(self):
        # XL RETURN
        return a.purpleXL

    def getSurfaceConstruction(self):
        return a.clearXL

    def specialFinish(self):
        self.base.environment.psychPoints += 1

## ADMIN BUILDINGS ##
acrMsg = ["Command and control relay",\
        "unit for communications with",\
        "Earth, ADMIN and SKILL pts."]
commandRelayLanderCapsule = [["COMM. RELAY","EDU"],"S",a.pinkXSU,a.pinkXSD,a.pinkXSR,a.pinkXSL,acrMsg]
class CommandRelay(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.lander = True
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.buildCost = 0.0
        self.powerUsage = 0.075
        self.maintainCost = 0.02
        self.volume = 0.0
        self.buildingName = "COMM. RELAY"
        self.drawSize = 'S'
        self.output = 0.20
        self.educationFactor = 0.05
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.pinkXSU
        elif self.udlr == "d":
            return a.pinkXSD
        elif self.udlr == "l":
            return a.pinkXSL
        elif self.udlr == "r":
            return a.pinkXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.shadowSU
        elif self.udlr == "d":
            return a.shadowSD
        elif self.udlr == "l":
            return a.shadowSL
        elif self.udlr == "r":
            return a.shadowSR
    
    def specialFinish(self):
        self.base.adminCostFactor *= 0.95
        self.base.environment.psychPoints += 1

attMsg = ["Simple computerized terminal",\
        "for general Mars training.",\
        "Boosts SKILL gains."]
attCost = [0,0,10,0,0,20,0]
trainingTerminalCapsule = [["TRAINING TERM.","EDU"],"S",a.pinkXSU,a.pinkXSD,a.pinkXSR,a.pinkXSL,attMsg,attCost]
class TrainingTerminal(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 8.0
        self.powerUsage = 1.0
        self.maintainCost = 0.05
        self.volume = 0.05
        self.buildingName = "TRAINING TERM."
        self.drawSize = 'S'
        self.output = 0.0
        self.educationFactor = 0.5
        self.jobs = []
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.pinkXSU
        elif self.udlr == "d":
            return a.pinkXSD
        elif self.udlr == "l":
            return a.pinkXSL
        elif self.udlr == "r":
            return a.pinkXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

    def specialFinish(self):
        self.base.educationPoints += 4

aspMsg = ["Educational unit for your",\
        "citizens to build SKILLS.",\
        "Employs one TEACHER."]
aspCost = [25,0,25,0,0,10,0]
schoolPodCapsule = [["SCHOOL POD","EDU"],"M",a.pinkMUR,a.pinkMDL,a.pinkMDR,a.pinkMUL,aspMsg,aspCost]
class SchoolPod(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 1.75
        self.maintainCost = 0.1
        self.volume = 0.7
        self.buildingName = "SCHOOL POD"
        self.drawSize = 'M'
        self.output = 0.0
        self.educationFactor = 1.0
        j2 = i.Job("TEACHER",0.0,0.6,0.4,self)
        self.jobs = [j2]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.pinkMUR
        elif self.udlr == "d":
            return a.pinkMDL
        elif self.udlr == "l":
            return a.pinkMUL
        elif self.udlr == "r":
            return a.pinkMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR
    
    def specialFinish(self):
        self.base.educationPoints += 8
        self.base.environment.psychPoints += 1

ascMsg = ["Campus area for Martians",\
        "to work on their SKILL level.",\
        "Employs two."]
ascCost = [25,0,70,5,0,20,0]
spaceCollegeCapsule = [["SPACE COLLEGE","EDU"],"L",a.pinkL,a.pinkL,a.pinkL,a.pinkL,ascMsg,ascCost]
class SpaceCollege(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 35.0
        self.powerUsage = 3.0
        self.maintainCost = 0.18
        self.volume = 1.4
        self.buildingName = "SPACE COLLEGE"
        self.drawSize = 'L'
        self.output = 0.0
        self.educationFactor = 1.3
        j1 = i.Job("PROFESSOR",0.0,0.9,0.1,self,1.5)
        j2 = i.Job("TEACHER",0.0,0.6,0.4,self)
        self.jobs = [j1,j2]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.pinkL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.educationPoints += 15
        self.base.environment.psychPoints += 1

aopMsg = ["Basic administrative outpost",\
        "to start generating ADMIN pts.",\
        "Employs one."]
aopCost = [20,0,15,0,0,5,0]
officePodCapsule = ["OFFICE POD","S",a.pinkSU,a.pinkSD,a.pinkSR,a.pinkSL,aopMsg,aopCost]
class OfficePod(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 12.0
        self.powerUsage = 1.5
        self.maintainCost = 0.05
        self.volume = 0.5
        self.buildingName = "OFFICE POD"
        self.drawSize = 'S'
        self.output = 0.5
        j3 = i.Job("ADMINISTRATOR",0.1,0.7,0.2,self)
        self.jobs = [j3]
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.pinkSU
        elif self.udlr == "d":
            return a.pinkSD
        elif self.udlr == "l":
            return a.pinkSL
        elif self.udlr == "r":
            return a.pinkSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR

amoMsg = ["Expanded administrative unit",\
        "for building up ADMIN pts.",\
        "Employs two."]
amoCost = [25,0,20,0,0,10,5]
mainOfficeCapsule = ["MAIN OFFICE","M",a.pinkMLUR,a.pinkMLDL,a.pinkMLDR,a.pinkMLUL,amoMsg,amoCost]
class MainOffice(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 2.5
        self.maintainCost = 0.07
        self.volume = 0.7
        self.buildingName = "MAIN OFFICE"
        self.drawSize = 'M'
        self.output = 1.0
        j3 = i.Job("BUREAUCRAT",0.1,0.5,0.4,self,1.3)
        j2 = i.Job("ADMINISTRATOR",0.1,0.7,0.2,self)
        self.jobs = [j3,j2]
        #finally
        self.tile.addBuilding(self)
  
    def getSurface(self):
        # ML RETURN
        if self.udlr == "u":
            return a.pinkMLUR
        elif self.udlr == "d":
            return a.pinkMLDL
        elif self.udlr == "l":
            return a.pinkMLUL
        elif self.udlr == "r":
            return a.pinkMLDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMLUR
        elif self.udlr == "d":
            return a.clearMLDL
        elif self.udlr == "l":
            return a.clearMLUL
        elif self.udlr == "r":
            return a.clearMLDR

ancMsg = ["High tech administravive",\
        "center, generatates ADMIN.",\
        "and some SKILL. Employs one."]
ancCost = [10,2,30,10,0,20,8]
nerveCenterCapsule = [["NERVE CENTER","EDU"],"L",a.pinkL,a.pinkL,a.pinkL,a.pinkL,ancMsg,ancCost]
class NerveCenter(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 6.0
        self.maintainCost = 0.16
        self.volume = 1.3
        self.buildingName = "NERVE CENTER"
        self.drawSize = 'L'
        self.output = 2.0
        self.educationFactor = 0.1
        j3 = i.Job("BUREAUCRAT",0.1,0.5,0.4,self,1.3)
        self.jobs = [j3]
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.pinkL

    def getSurfaceConstruction(self):
        return a.clearL

ahqMsg = ["Administrative center with",\
        "a high output of ADMIN pts.",\
        "Employs three."]
ahqCost = [30,0,75,20,0,25,10]
hqCapsule = [["HQ","EDU"],"L",a.pinkXL,a.pinkXL,a.pinkXL,a.pinkXL,ahqMsg,ahqCost]
class HQ(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 50.0
        self.powerUsage = 4.5
        self.maintainCost = 0.16
        self.volume = 1.3
        self.buildingName = "HQ"
        self.drawSize = 'L'
        self.output = 2.5
        self.educationFactor = 0.1
        j1 = i.Job("COMMANDER",0.1,0.4,0.5,self,1.8)
        j2 = i.Job("BUREAUCRAT",0.1,0.5,0.4,self,1.3)
        j3 = i.Job("BUREAUCRAT",0.1,0.5,0.4,self,1.3)
        self.jobs = [j1,j3,j2]
        #finally
        self.tile.addBuilding(self)
 
    def getSurface(self):
        # XL RETURN
        return a.pinkXL

    def getSurfaceConstruction(self):
        return a.clearXL

aaiMsg = ["Compact and power hungry",\
        "neworked AI node for base", "management, provides many",\
        "ADMIN pts and SKILL."]
aaiCost = [0,10,0,5,0,30,5]
aiNodeCapsule = [["AI NODE","EDU"],"S",a.pinkXSU,a.pinkXSD,a.pinkXSR,a.pinkXSL,aaiMsg,aaiCost]
class AINode(AdminBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 100.0
        self.powerUsage = 2.5
        self.maintainCost = 0.1
        self.volume = 0.1
        self.buildingName = "AI NODE"
        self.jobs = []
        self.drawSize = 'S'
        self.output = 3.5
        self.educationFactor = 0.35
        #finally
        self.tile.addBuilding(self) 
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.pinkXSU
        elif self.udlr == "d":
            return a.pinkXSD
        elif self.udlr == "l":
            return a.pinkXSL
        elif self.udlr == "r":
            return a.pinkXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

    def specialFinish(self):
        self.base.educationPoints += 2

### TRANSPO BUILDINGS ###

teaMsg = ["Communications broadcast",\
        "tower. Allows SPACE launches",\
        "from Earth. Additional units",\
        "lower cost of landers."]
teaCost = [0,2,0,20,0,8,0]
earthAntennaCapsule = ["EARTH ANTENNA","S",a.blueXSU,a.blueXSD,a.blueXSR,a.blueXSL,teaMsg,teaCost]
class EarthAntenna(TransportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 15.0
        self.powerUsage = 0.0
        self.maintainCost = 0.02
        self.volume = 0.01
        self.buildingName = "EARTH ANTENNA"
        self.drawSize = 'S'
        self.earthCostEffect = 0.0
        self.jobs = []
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.blueXSU
        elif self.udlr == "d":
            return a.blueXSD
        elif self.udlr == "l":
            return a.blueXSL
        elif self.udlr == "r":
            return a.blueXSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearXSU
        elif self.udlr == "d":
            return a.clearXSD
        elif self.udlr == "l":
            return a.clearXSL
        elif self.udlr == "r":
            return a.clearXSR

    def restartSpecial(self):
        self.base.earthLaunches = True

    def shutoffSpecial(self):
        antennaCount = 0
        for building in self.base.transportList:
            if isinstance(building,EarthAntenna) and building.shutoff == False:
                antennaCount += 1
        if antennaCount < 1:
            self.base.earthLaunches = False
    
    def specialFinish(self):
        if self.base.earthLaunches == False:
            self.base.earthLaunches = True
        else:
            self.earthCostEffect = 0.02
            
tccMsg = ["Command center for SPACE",\
        "travel. Increases effeciency",\
        "of both launches and landers.",\
        "Employs one. +1 bonus LANDER."]
tccCost = [0,0,25,5,0,10,0]
controlTowerCapsule = ["CONTROL TOWER","S",a.blueSU,a.blueSD,a.blueSR,a.blueSL,tccMsg,tccCost]
class ControlTower(TransportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 20.0
        self.powerUsage = 0.0
        self.maintainCost = 0.10
        self.volume = 0.3
        self.buildingName = "CONTROL TOWER"
        self.drawSize = 'S'
        t2 = i.Job("MISSION CONTROL",0.2,0.5,0.3,self)
        self.jobs = [t2]
        self.earthCostEffect = 0.05
        #finally
        self.tile.addBuilding(self)
    
    def getSurface(self):
        # S RETURN
        if self.udlr == "u":
            return a.blueSU
        elif self.udlr == "d":
            return a.blueSD
        elif self.udlr == "l":
            return a.blueSL
        elif self.udlr == "r":
            return a.blueSR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearSU
        elif self.udlr == "d":
            return a.clearSD
        elif self.udlr == "l":
            return a.clearSL
        elif self.udlr == "r":
            return a.clearSR
    
    def specialFinish(self):
        self.base.availableEarthLaunches += 1
        self.base.announcements.addAnnouncement("CONTROL TOWER reduces earth-mars travel time.")

tccMsg = ["SPACE communications facility.",\
        "Controls costs of landers",\
        "and provides Earth-link.", \
        "Employs two. PSYCH bonus."]
tccCost = [0,5,30,15,0,10,0]
commsCenterCapsule = ["COMMS CENTER","M",a.blueMUR,a.blueMDL,a.blueMDR,a.blueMUL,tccMsg,tccCost]
class CommsCenter(TransportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        if self.udlr == "u":
            self.anchor = self.tile.upAnchor
        elif self.udlr == "d":
            self.anchor = self.tile.downAnchor
        elif self.udlr == "l":
            self.anchor = self.tile.leftAnchor
        elif self.udlr == "r":
            self.anchor = self.tile.rightAnchor
        self.base.appendBuildList(self)
        self.buildCost = 30.0
        self.powerUsage = 0.0
        self.maintainCost = 0.05
        self.volume = 0.01
        self.buildingName = "COMMS CENTER"
        self.drawSize = 'M'
        t1 = i.Job("MISSION COMMANDER",0.0,0.6,0.4,self,1.5)
        t2 = i.Job("COMMS OPS",0.2,0.5,0.3,self)
        self.jobs = [t1,t2]
        self.earthCostEffect = 0.10

        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # M RETURN
        if self.udlr == "u":
            return a.blueMUR
        elif self.udlr == "d":
            return a.blueMDL
        elif self.udlr == "l":
            return a.blueMUL
        elif self.udlr == "r":
            return a.blueMDR

    def getSurfaceConstruction(self):
        if self.udlr == "u":
            return a.clearMUR
        elif self.udlr == "d":
            return a.clearMDL
        elif self.udlr == "l":
            return a.clearMUL
        elif self.udlr == "r":
            return a.clearMDR

    def specialFinish(self):
        self.base.environment.psychPoints += 1

tlpMsg = ["Enables ROCKET launches.",\
        "Allows export of resources",\
        "to SPACE."]
tlpCost = [35,0,80,5,0,0,0]
launchPadCapsule = ["LAUNCH PAD","L",a.blueL,a.blueL,a.blueL,a.blueL,tlpMsg,tlpCost]
class LaunchPad(TransportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 25.0
        self.powerUsage = 0.0
        self.maintainCost = 0.1
        self.volume = 0.01
        self.buildingName = "LAUNCH PAD"
        self.drawSize = 'L'
        self.earthCostEffect = 0.01
        self.jobs = []
        self.queue = []
        self.full = False
        #finally
        self.tile.addBuilding(self)

    def getSurface(self):
        # L RETURN
        return a.blueL

    def getSurfaceConstruction(self):
        return a.clearL

    def specialFinish(self):
        self.base.outbound = True
        self.base.launchPads.append(self)
    
    def createLaunch(self,capsule):
        if capsule[5].tag == "ROBOTS":
            newRocket = RobotRocket(self.base.sol,self.base,self.tile,'u',"L",capsule,self,capsule[5])
        else:
            newRocket = Rocket(self.base.sol,self.base,self.tile,'u',"L",capsule,self,capsule[5])
        self.full = True

tspMsg = ["A hub for SPACE travel.",\
        "Grants lander, helps costs,",\
        "and enables ORBITAL landers.",\
        "Employs two."]
tspCost = [25,5,50,40,0,30,10]
spacePortCapsule = ["SPACEPORT","L",a.blueXL,a.blueXL,a.blueXL,a.blueXL,tspMsg,tspCost]
class SpacePort(TransportBuilding):
    def __init__(self, sol, baseObject, tileObject,udlr, size,adjacencyBonus):
        super().__init__(sol, baseObject, tileObject,udlr, size,adjacencyBonus)
        self.anchor = self.tile.upAnchor
        self.base.appendBuildList(self)
        self.buildCost = 80.0
        self.powerUsage = 0.0
        self.maintainCost = 0.3
        self.volume = 1.0
        self.buildingName = "SPACEPORT"
        self.drawSize = 'L'
        self.earthCostEffect = 0.05
        t1 = i.Job("COMMISAR",0.1,0.5,0.4,self,1.2)
        t2 = i.Job("PORT OPS",0.2,0.5,0.3,self)
        self.jobs = [t1,t2]
        #finally
        self.tile.addBuilding(self) 
    
    def getSurface(self):
        # XL RETURN
        return a.blueXL

    def getSurfaceConstruction(self):
        return a.clearXL

    def restartSpecial(self):
        self.base.orbitalResupply = True

    def shutoffSpecial(self):
        stationCount = 0
        for building in self.base.transportList:
            if isinstance(building,SpacePort) and building.shutoff == False:
                stationCount += 1
        if stationCount < 1:
            self.base.orbitalResupply = False

    def specialFinish(self):
        self.base.availableEarthLaunches += 1
        self.base.orbitalResupply = True
        self.base.announcements.addAnnouncement("SPACEPORT OPEN! New landers available.")
        self.base.environment.psychPoints += 1

allLanderCapsules = [landerHabitatCapsule,shuttleCapsule,crewDropCapsule,marsTranspoCapsule,\
    smallCrewLanderCapsule,supplyLanderCapsule,airLanderCapsule,orbitalAirCapsule,waterLanderCapsule,\
    orbitalWaterCapsule,orbitalFoodCapsule,foodLanderCapsule,concreteDropCapsule,luxuryCargoCapsule,\
    metalDropCapsule,electronicsDropCapsule,medsDropCapsule,plasticsDropCapsule,builderLanderCapsule,\
    recycleLanderCapsule,powerLanderCapsule,prefabSolarCapsule,minerBotLanderCapsule,probeLanderCapsule,\
    commandRelayLanderCapsule]

def getLanderCapsule(tag):
    for capsule in allLanderCapsules:
        if isinstance(capsule[0],str):
            tag2 = capsule[0]
        else:
            tag2 = capsule[0][0]
        if tag == tag2:
            return capsule


## ROCKETS ##
rMsg = ["Orbital rocket for","launching a 50 ton","export payload."]
rrMsg = ["Orbital rocket for","launching up to 3","robots for export."]
rCost = [0,0,0,10,5,1,0]
whiteRocketCapsule = ["CONCRETE","L",a.whiteRocket,a.whiteRocket,a.whiteRocket,a.whiteRocket,rMsg,rCost]
greyRocketCapsule = ["METAL","L",a.greyRocket,a.greyRocket,a.greyRocket,a.greyRocket,rMsg,rCost]
greenRocketCapsule = ["FOOD","L",a.greenRocket,a.greenRocket,a.greenRocket,a.greenRocket,rMsg,rCost]
aquaRocketCapsule = ["AIR","L",a.aquaRocket,a.aquaRocket,a.aquaRocket,a.aquaRocket,rMsg,rCost]
blueRocketCapsule = ["WATER","L",a.blueRocket,a.blueRocket,a.blueRocket,a.blueRocket,rMsg,rCost]
hYellowRocketCapsule = ["ELECTRONICS","L",a.hYellowRocket,a.hYellowRocket,a.hYellowRocket,a.hYellowRocket,rMsg,rCost]
redRocketCapsule = ["ORE","L",a.redRocket,a.redRocket,a.redRocket,a.redRocket,rMsg,rCost]
orangeRocketCapsule = ["FUEL","L",a.orangeRocket,a.orangeRocket,a.orangeRocket,a.orangeRocket,rMsg,rCost]
purpleRocketCapsule = ["MEDS","L",a.purpleRocket,a.purpleRocket,a.purpleRocket,a.purpleRocket,rMsg,rCost]
pinkRocketCapsule = ["RARE","L",a.pinkRocket,a.pinkRocket,a.pinkRocket,a.pinkRocket,rMsg,rCost]
dRedRocketCapsule = ["REGOLITH","L",a.dRedRocket,a.dRedRocket,a.dRedRocket,a.dRedRocket,rMsg,rCost]
dGreenRocketCapsule = ["ORGANICS","L",a.dGreenRocket,a.dGreenRocket,a.dGreenRocket,a.dGreenRocket,rMsg,rCost]
hOrangeRocketCapsule = ["PLASTICS","L",a.hOrangeRocket,a.hOrangeRocket,a.hOrangeRocket,a.hOrangeRocket,rMsg,rCost]
robotRocketCapsule = ["ROBOTS","L",a.whiteRocket,a.whiteRocket,a.whiteRocket,a.whiteRocket,rrMsg,rCost]