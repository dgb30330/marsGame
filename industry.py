import color as c

class Bonuses:
    def __init__(self):
        self.surfaceBonus = 1.0
        self.surfaceKey = "MARS"
        self.lifeSupportBonus = 1.0
        self.lifeSupportKey = "ORGANIC"
        self.recycleBonus = 1.0
        self.recycleKey = "CONSERVATION"
        self.powerBonus = 1.0
        self.powerKey = "ELECTRICAL"
        self.extractionBonus = 1.0
        self.extractionKey = "GEOLOGY"
        self.industryBonus = 1.0
        self.industryKey = "INDUSTRIAL"
        self.scienceBonus = 1.0
        self.scienceKey = "SCIENTIFIC"
        self.adminBonus = 1.0
        self.adminKey = "INFO-TECH"
        self.transportBonus = 1.0
        self.transportKey = "ROCKETRY"
        self.healthBonus = 1.0
        self.healthKey = "MEDICAL"
        self.psychBonus = 1.0
        self.psychKey = "NEURO"
        self.skillBonus = 1.0
        self.skillKey = "EDUCATION"
        self.surfaceBonus = 1.0
        self.allKeys = [self.surfaceKey,self.lifeSupportKey,self.recycleKey,self.powerKey,self.extractionKey,self.industryKey,\
            self.scienceKey,self.adminKey,self.transportKey,self.healthKey,self.psychKey,self.skillKey]

    def colorFromKey(self,key):
        if key == self.surfaceKey:
            return c.white      
        if key == self.lifeSupportKey:
            return c.green
        if key == self.recycleKey: 
            return c.aqua
        if key == self.powerKey:
            return c.yellow  
        if key == self.extractionKey:
            return c.red
        if key == self.industryKey:
            return c.orange  
        if key == self.scienceKey:
            return c.purple  
        if key == self.adminKey:
            return c.pink   
        if key == self.transportKey:
            return c.blue  
        if key == self.healthKey:
            return c.darkGreen 
        if key == self.psychKey:
            return c.darken(c.aqua,40) 
        if key == self.skillKey:
            return c.boldRed  
            

    def descriptionFromKey(self,key):
        if key == self.surfaceKey:
            return ["Research how","to better exist","on the martian","surface. Bonus","to EXPLORERS","and BUILDERS."]       
        if key == self.lifeSupportKey:
            return ["Fund science to","help improve","the yeilds of","your farms,","and breathable","air production."]   
        if key == self.recycleKey: 
            return ["Increase the","effeciency of","your recycling","facilities."]   
        if key == self.powerKey:
            return ["Get even more","output from","your base's","reactors and","solar panels."]   
        if key == self.extractionKey:
            return ["Provide study","into how to","better mine","resources on","Mars. All","EXTRACTION","output upped."]  
        if key == self.industryKey:
            return ["Research into","industrial","methods and","practices. All","INDUSTRIAL","production up."]   
        if key == self.scienceKey:
            return ["Increase your","base's ability","to cunduct","pure scientific","pursuits. Ups","SCIENCE pts","production."]  
        if key == self.adminKey:
            return ["Improve your","base's use of","data, comms,","and the like","to acheive an","ADMIN bonus."]   
        if key == self.transportKey:
            return ["R&D in the","art of space","travel. Trips","shorter, costs","lower."]  
        if key == self.healthKey:
            return ["Medical study","to improve the","lifespans of","your base's","residents."]   
        if key == self.psychKey:
            return ["Study in the","mental well","being, general","psychic health,","and happiness","of your people."]   
        if key == self.skillKey:
            return ["Develop the","educational","capacities of","your base's","residents. All","increases in","SKILL receive","a bonus."]   

    def bonusFromKey(self,key):
        allBonuses = [self.surfaceBonus,self.lifeSupportBonus,self.recycleBonus,self.powerBonus,\
            self.extractionBonus,self.industryBonus,self.scienceBonus,self.adminBonus,\
                self.transportBonus,self.healthBonus,self.psychBonus,self.skillBonus]        
        i = 0
        for savedKey in self.allKeys:
            if key == savedKey:
                return allBonuses[i]
            i+=1

    def setByKey(self,key,increase):
        if key == self.surfaceKey:
            self.surfaceBonus += increase        
        if key == self.lifeSupportKey:
            self.lifeSupportBonus += increase 
        if key == self.recycleKey: 
            self.recycleBonus += increase 
        if key == self.powerKey:
            self.powerBonus += increase 
        if key == self.extractionKey:
            self.extractionBonus += increase 
        if key == self.industryKey:
            self.industryBonus += increase 
        if key == self.scienceKey:
            self.scienceBonus += increase 
        if key == self.adminKey:
            self.adminBonus += increase 
        if key == self.transportKey:
            self.transportBonus += increase 
        if key == self.healthKey:
            self.healthBonus += increase 
        if key == self.psychKey:
            self.psychBonus += increase 
        if key == self.skillKey:
            self.skillBonus += increase 

class Resource:
    def __init__(self,tag,shortTag,resourceColor,selfStorage,value=0):
        self.tag = tag
        self.shortTag = shortTag
        self.color = resourceColor
        self.quantity = 0.0
        #daily trackers
        self.baseConsumption = 0 #recyclable
        self.industryConsumption = 0 # non recyclable
        self.weeklyConsumption = 0
        self.weeklyConsumptionReports = [self.tag+"C"]
        self.production = 0
        self.weeklyProduction = 0
        self.weeklyProductionReports = [self.tag]
        #traits
        self.selfStorage = selfStorage
        self.storageCapacity = 0
        self.recyclePercent = 0.0
        self.full = True
        self.value = value
        self.deficit = 0
        self.discount = 1.0
        self.storageFreeze = -1.0
    

class Job:
    def __init__(self,tag,hFactor,sFactor,pFactor,building = None,jobWeight = 1.0,importance = 0):
        self.tag = tag
        self.person = None
        self.healthFactor = hFactor
        self.skillFactor = sFactor
        self.psychFactor = pFactor
        self.jobWeight = 1.0
        self.importance = 0
        self.productivity = 0
        self.building = building
        self.psychToll = 0
        self.healthToll = 0
        self.skillBoost = 0

    def __str__(self):
        otherInfo = ""
        if self.building != None:
            otherInfo += "@"+self.building.buildingName
        if self.person != None:
            otherInfo += "/"+self.person.name
        return self.tag + otherInfo

    def updateImportance(self):
        if self.building != None:
            self.importance = self.jobWeight * self.building.weight
        else:
            self.importance = self.jobWeight

    def hire(self,hiredPersonObj):
        self.person = hiredPersonObj
        self.person.job = self
        self.updateProductivity()
        print(self.person.job)

    def fire(self):
        if self.person != None:
            self.person.job = None
        self.person = None
        self.productivity = 0

    def jobTest(self,person):
        hComp = self.healthFactor*person.health
        sComp = self.skillFactor*person.skill
        pComp = self.psychFactor*person.psych
        return (hComp+sComp+pComp)

    def updateProductivity(self,powerFactor = 0.0):
        hComp = self.healthFactor*self.person.health
        sComp = self.skillFactor*self.person.skill
        pComp = self.psychFactor*self.person.psych
        self.productivity = self.jobWeight * (hComp+sComp+pComp)
        if self.person.robot:
            self.productivity *= powerFactor
            if self.person.functional == False:
                self.productivity = 0.0



class Industry:
    def __init__(self,tag,announcements,standardIO = False, inputList = [], inputWeightsList= [],\
        outputResource = None):
        self.tag = tag
        self.announcements = announcements
        self.standardIO = standardIO #if standard, methods need no input
        self.inputs = inputList #list resource objects
        self.inputWeights = inputWeightsList #(qty needed to make one output)
        self.output = outputResource #resourceObj
        self.supplied = True
        self.lowResource = ""

    def run(self,outputCap,productivity,powerFactor,customInput = None): 
        realOutput = outputCap * productivity * powerFactor
        if realOutput < 0:
            realOutput = 0
        if self.standardIO:
            ###print(self.tag + " target prod:" + str(realOutput))
            #calc needs for full production
            inputNeeds = []
            i = 0
            for inp in self.inputWeights:
                need = (realOutput* self.inputs[i].discount) * inp
                inputNeeds.append(need)
                i+=1
            i = 0
            ###print("needs"+str(inputNeeds))
            #check quantities / determine production ratio
            ratios = []
            self.lowResource = ""
            self.supplied = True
            for realInput in self.inputs:
                ###print(realInput.tag + str(realInput.quantity))
                if realInput.quantity < inputNeeds[i]:
                    if inputNeeds[i] > 0:
                        ratio = realInput.quantity / inputNeeds[i]
                    else:
                        ratio = 0.0
                    self.supplied = False
                    self.lowResource = realInput.tag
                else:
                    ratio = 1.0
                ratios.append(ratio)
                i+=1
            #find min production ratio
            if self.supplied == False:
                realRatio = ratios[0]
                for each in ratios:
                    if each < realRatio:
                        realRatio = each
                if realRatio < 0:
                    realRatio = 0.0
            else:
                realRatio = 1.0
            ###print("prod. ratio:" + str(realRatio))
            #adjust output
            realOutput = realRatio*realOutput
            #deduct inputs
            i=0
            for x in self.inputs:
                x.quantity -= inputNeeds[i]*realRatio
                x.industryConsumption += inputNeeds[i]*realRatio
                i+=1
            #add output
            self.output.quantity += realOutput
            self.output.production += realOutput
            ###print(str(realOutput) + " to " + str(self.output.quantity))
        else:
            if customInput != None and realOutput > customInput:
                if productivity > 1.0:
                    productivity = 1.0
                realOutput = customInput * productivity * powerFactor
                if realOutput < 0:
                    realOutput = 0
        return realOutput
        

            


