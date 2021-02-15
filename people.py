import random

#firstNames = ["G.","J.","A.","J.J.","S."]

class People:
    workingAge = 6200 #subject to policy change
    youngestAstronaut = 7200
    oldestAstronaut = 20000
    youngestFertile = 5800
    oldestFertile = 15000
    agingBorder = 12000
    maxAge = 42000
    fertilityRate = 2.5
    YOUTH_ONE = 1.0 / workingAge
    YEARLY_10TH = 0.1 / 350
    YEARLY_20TH = 0.05 / 350
    YEARLY_50TH = 0.02 / 350
    YEARLY_100TH = 0.01 / 350
    femaleFirstNames = ["Jessica","Mary","Jane","Kate","Nina","Lisa","Laura","Amy","Anna","Liz",\
        "Amanda","Maggie","Sarah","Sara","Dolores","Mary","Allison","Heather","Susan","Lauren",\
        "Caroline","Priscilla","Elizabeth","Keilah","Celina","Suzanne","Tina","Lucy","Danielle",\
        "Lydia","Lindsay","Kara","Jill","Pam","Alice","Britney","Alexandria"]
    maleFirstNames = ["Greg","Jon","Allen","Jake","Sean","Doug","Sam","Mitch","Matt","Virgil",\
        "Joe","Max","James","Chris","TJ","BJ","JR","Jack","Phil","Barry","Brad","Ben","Alex",\
        "Dustin","Sean","Abraham","Ryan","Mario","Eddie","Kevin","Rafael","Paul","Ty","Bryan",\
        "George","Donald","Cado","David","Dave","Jeremy","Don","Troy"]
    lastNames = ["Brown","Smith","Jones","Henneman","Armstrong","Harris","Pearson","Christman",\
        "Harrison","Vance","Cruz","Lee","Bell","Washington","Jefferson","Lewis","Cline",\
        "Stone","Lemon","Garcia","Allison","Presley","White","Rivera","Rodriguez","Gonzales",\
        "Martinez","Thompson","Thorn","Reis","Pajo","Black","Rogers","Davis","Parker","Gifford",\
        "Donahue","Tanner","Boylan","McDonald","Fagan","Johnson","Davidson","Robinson","DeLillo",\
        "Carter","Nixon","Winger","Pierce","Barnes","Cortez","Bass","Chambers","Isley","Edison"]
    robotNames = ["375","282","187","13","44B","12","C.H.A.D.","99","L.I.F.T.","1","75","66"]
    def __init__(self,native = False,lastName = "",robot = False,sol=0):
        self.native = native
        self.robot = robot
        self.housed = False
        self.functional = True
        self.diedString = ""
        self.diedSol = 0
        self.diedYear = 0
        if native:
            self.health = 1.0
            self.psych = 1.0
            self.skill = 0.0
            self.age = 0
            self.youthPad = 7200
            self.lastName = lastName
            self.arrivedSol = 0
        else: # these ranges could be set by institution feature
            self.arrivedSol = sol
            if robot:
                self.lastName = "XR"
                self.health = 2.0
                self.psych = 0.0
                self.skill = 0.2
                self.age = 0
                self.youthPad = 0
            else:
                self.health = random.uniform(0.8,1.1)
                self.psych = random.uniform(0.6,1.1)
                self.skill = random.uniform(1.0,1.5)
                self.age = random.randrange(People.youngestAstronaut,People.oldestAstronaut)
                self.youthPad = 0
                self.lastName = People.lastNames[random.randrange(0,len(People.lastNames))]
        #to print age in EY age/350
        if robot:
            self.female = False
            self.name = self.lastName+ "-" + People.robotNames[random.randrange(0,len(People.robotNames))]
            self.aging = 0
            self.lifeMax = 12000
            self.youthPad = 0
            self.pregnancy = 0
            self.alive = True
            self.job = None
            self.sane = True
            self.needCatagory = 0
        else:
            sexSelector = random.randrange(2)
            if sexSelector == 1:
                self.female = True
                self.name = People.femaleFirstNames[random.randrange(0,len(People.femaleFirstNames))] + " " + self.lastName
            else:
                self.female = False
                self.name = People.maleFirstNames[random.randrange(0,len(People.maleFirstNames))] + " " + self.lastName
            self.aging = 0.00004
            self.lifeMax = People.maxAge
            self.youthPad = 40000
            self.pregnancy = 0
            self.alive = True
            self.job = None
            self.sane = True
            self.needCatagory = 0 # used as index for multi-rationing levels

    def insane(self,securityRatio):
        self.sane = False
        if securityRatio > 1.0:
            msg = self.name + " is having a PSYCH CRISIS. Forced to work by SECURITY."
        else:
            if self.job != None: 
                msg = self.name + " has quit work as " + self.job.tag + ". (PSYCH CRISIS)"   
                self.job.fire()
            else:
                msg = self.name + " will not work. (PSYCH CRISIS)"
        return msg

    def pregnant(self):
        if self.female and self.pregnancy == 0 and self.health > 0.75:
            if self.age > People.youngestFertile and self.age < People.oldestFertile:
                chanceRange = int (self.health * self.psych * ((People.oldestFertile - \
                    People.youngestFertile) / People.fertilityRate))
                if 0 == random.randrange(0,chanceRange):
                    self.pregnancy = 250

    def ageSol(self,bonus):
        #print(bonus)
        birth = False
        self.pregnant()
        self.age += 1
        if self.youthPad > 0:
            self.youthPad -= 4
        if bonus > 1.0: # RECOVERY
            if self.age > People.agingBorder:
                factor = 2*(self.age - People.agingBorder)
            else:
                factor = 0
            self.health += (People.YEARLY_100TH/3.0)*bonus*(People.agingBorder/(People.agingBorder+factor))*(1.0/self.health)
        if self.age > People.agingBorder:
            #print(self.name + " health:" + str(self.health))
            self.health -= self.aging * (1.0/(bonus+0.001))
            #print("-"+str(self.aging * (1.0/(bonus+0.001))))
        if self.pregnancy > 0:
            self.pregnancy -= 1
            if self.pregnancy ==1:
                birth = True
                self.pregnancy = 0
        deathChance = (self.youthPad+self.lifeMax) - int(self.lifeMax*(1.0 - self.health))
        #print(deathChance)
        if self.health < 0 or deathChance < 0 or 0 == random.randrange(0,deathChance):
            print("Died")
            self.alive = False
        return birth
            

    def printMe(self):
        meString = self.name + " sol:" + str(self.age) + " F:"+str(self.female) +"\nhealth:" + str(self.health)\
            + "\npsych:" + str(self.psych) + "\nskill:" + str(self.skill)\
                + "\nage EY:" + str(self.age/350)
        print(meString)

psychMultiplier = 1.8
class Environment:
    def __init__(self):
        self.psychBackground = 0.0
        self.psychPoints = 0
        self.psychEffects = [] # list of 2 el lists, (EY effect magnitude,daysToLive (-1 perm.))
        self.nativeRatio = self.updateNativeRatio([])
        #build skill / education here?
    
    def calcPsychBackground(self,pop,cumulativePsych):
        effectPoints = 0
        toRemove = []
        for effect in self.psychEffects:
            effectPoints += effect[0]
            effect[0]-=effect[1]
            effect[2]-=1
            if effect[2] == 0:
                toRemove.append(effect)
        for x in toRemove:
            self.psychEffects.remove(x)
        weightedPsychPoints = 0
        ptValue = 1.0
        ptCount = 0
        while ptCount < self.psychPoints:
            if ptCount > pop:
                if pop > 0:
                    ptValue *= ((pop-1)/pop)
                else:
                    ptValue = 0.0
            weightedPsychPoints+=ptValue
            ptCount += 1
        numer = (weightedPsychPoints+((cumulativePsych/4.0)+((3*pop)/4.0))+effectPoints)
        if pop > 0:
            self.psychBackground = numer / (pop*psychMultiplier)
        else:
            self.psychBackground = 0.0

    def addPsychEffect(self,magnitude,decay,timeToLive):
        psychE = [magnitude,decay,timeToLive]
        self.psychEffects.append(psychE)

    def updateNativeRatio(self,populationList):
        totalPopulation = 0
        totalNatives = 0
        for p in populationList:
            totalPopulation += 1
            if p.native:
                totalNatives += 1
        if totalPopulation != 0:
            self.nativeRatio = totalNatives/totalPopulation
        else: 
            self.nativeRatio = 0.0
        return self.nativeRatio
        

"""
count = 10
totalAge = 0
babyCount = 0
while count > 0:
    count-=1
    p = People()
    while p.alive:
        birth = p.ageSol(.4)
        if birth:
            print("BABY!")
            babyCount += 1
    p.printMe()
    totalAge += p.age
print("Avg life exp: " + str((totalAge/10)/350))
print("Babies: " + str(babyCount))
""
tester = Environment()
tester.psychPoints = 300
population = 88
avgPsych = 1.0
cumPsych = population*avgPsych
tester.calcPsychBackground(population,cumPsych)
print(tester.psychBackground)
"""

    