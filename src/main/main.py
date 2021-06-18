class Positionable():
  def __init__(self, Position):
      self.Position = Position

  def getPos(self):
      return self.Position

#not completed
class Player(Positionable):
  def __init__(self, Position):
      super().__init__(Position)
      self.Direction = 2
      self.currentlyHolding = 0
      #0 for nothing, 1 for leafy, 2 for succulent, 3 for tree, 4 for fertilizer, 5 for water

  def nextHolding(self):
    if self.currentlyHolding == 5:
      self.currentlyHolding == 0
    else:
      self.currentlyHolding += 1

  def goNorth(self):
    self.Position.setY(self.Position.getY() - 1)
    self.faceNorth()

  def faceNorth(self):
    self.Direction = 0

  def goEast(self):
    self.Position.setX(self.Position.getX() + 1)
    self.faceNorth()

  def faceEast(self):
    self.Direction = 1

  def goSouth(self):
    self.Position.setY(self.Position.getY() + 1)
    self.faceNorth()

  def faceSouth(self):
    self.Direction = 2

  def goWest(self):
    self.Position.setX(self.Position.getX() + 1)
    self.faceNorth()

  def faceWest(self):
    self.Direction = 3

  def getDirection(self):
    return self.Direction

class Position():
  def __init__(self, x, y) -> None:
      self.x = x
      self.y = y

  def getX(self):
    return self.x

  def getY(self):
    return self.y

  def setX(self, x):
    self.x = x
  
  def setY(self, y):
    self.y = y

class Soil(Positionable):
  def __init__(self, Position):
      super().__init__(Position)
      self.onSoil = 0
      #0 for nothing, 1 for non-harmful, 2 for harm-ful, 3 for good
      self.waterLevel = 5
      self.soilFertility = 5
  
  def getWaterLevel(self):
    return self.waterLevel

  def getSoilFertility(self):
    return self.soilFertility

  def getOnSOil(self):
    return self.onSoil

  def setOnSoil(self, onSoil):
    self.onSoil = onSoil

  def water(self):
    self.waterLevel += 4

  def fertilize(self):
    self.soilFertility += 4

  def nourishPlant(self):
    self.soilFertility -= 1
    self.waterLevel -= 1

class onSOil():
  def __init__(self, soil, onSoil):
      self.soil = soil
      self.soil.setOnSoil(onSoil)

  def getSoil(self):
    return self.soil

class Plant(onSOil):
  def __init__(self, soil):
      super().__init__(soil, 1)
      self.growthState = 0 
      # three grow states, 0-4 is seedling, 5-9 is sapling, 10+ is fully grown
  
  def getGS(self):
    return self.growthState
  
  def grow(self):
    currentSoil = self.soil

    if currentSoil.getWaterLevel() > 6 and currentSoil.getWaterLevel() < 10 and currentSoil.getSoilFertility() > 6 and currentSoil.getSoilFertility() < 10:
      self.growthState += 2
    elif currentSoil.getWaterLevel() > 6 and currentSoil.getWaterLevel() < 10 and currentSoil.getSoilFertility() > 6 and currentSoil.getSoilFertility() < 10:
      self.growthState += 1

    if currentSoil.getWaterLevel() > 0 and currentSoil.getSoilFertility() > 0:
      currentSoil.nourishPlant()

#the following three are not completed
class Leafy(Plant):
  def __init__(self, soil, soilFertility):
      super().__init__(soil, soilFertility)

class SuccuLent(Plant):
  def __init__(self, soil):
      super().__init__(soil)

class Tree(Plant):
  def __init__(self, soil):
      super().__init__(soil)

class Map():
  def __init__(self, horizontalSize, verticalSize):
      self.Horizontal = []
      self.Vertical = []

#not completed
class Villager(onSOil):
  def __init__(self, soil):
      super().__init__(soil, 0)
      self.mood = 0
      #0-4 is sad, 5-9 is alright, 10+ is happy
  
  def getMood(self):
   return self.mood

  def nearToxin(self):
    soilState = self.soil.getOnSoil

    if soilState == 2:
      self.mood == 0
    elif soilState == 3:
      self.mood += 2

class ToxinGas(onSOil):
  def __init__(self, soil):
      super().__init__(soil, 2)

  def setAffectedToToxic(self):
    self.soil.setOnSoil(2)

#just some testing stuff, could ditch
def main():
  pos = Position(2, 3)
  print(pos.getX())
  print(pos.getY())

  player = Player(pos)
  player.goWest()

  print(player.getPos().x)
  print(player.getPos().y)
  print(player.getDirection())

  print("hello world")

main()