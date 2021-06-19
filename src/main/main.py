import pygame
import math

widthTiles = 15
heightTiles = 8

#import shit
pygame.init()
from pygame.locals import *

#screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Garden-Hack")
icon = pygame.image.load('src/main/plant.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('src/main/boi.png')
playerX = 400
playerY = 300
playerDeltaX = 0
playerDeltaY = 0

#plants
treeIMG = pygame.image.load('src/main/big_tree.png')
flowerIMG = pygame.image.load('src/main/carrot.png')
carrotIMG = pygame.image.load('src/main/flowers.png')

#background
currbackground = 0
# backgroundImage1 = pygame.image.load('Pygames_Learning/background1.jpg')
# backgroundImage2 = pygame.image.load('Pygames_Learning/background2.jpg')
# backgroundImage3 = pygame.image.load('Pygames_Learning/background3.jpg')
# currbackgroundImage = backgroundImage1

#Text
text = "you are in the first area"
font = pygame.font.Font('freesansbold.ttf', 32)
holdingText = "you are holding nothing"
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 20
textY = 10

holdingTextX = 20
holdingTextY = 45

#clock
clock = pygame.time.Clock()

def showText(desiredText, desiredHoldingText):
  text = font.render(desiredText, True, (255, 255, 255))
  screen.blit(text, (textX, textY))
  text = font.render(desiredHoldingText, True, (255, 255, 255))
  screen.blit(text, (holdingTextX, holdingTextY))

def player(x, y):
  screen.blit(playerImg, (x, y))
  pygame.draw.circle(screen, (  0,   0, 255), (x + 32,y + 32), 10)
  
background1PlacedImagesPositions = []

def renderAllPlaced():
  if currbackground == 0:
    for IMGandCoordinates in background1PlacedImagesPositions:
      screen.blit(IMGandCoordinates.getImage(), IMGandCoordinates.getCoordinate())

def withinDistance(position1, position2, distance):
  totalDistance = math.sqrt(math.pow(position1.getX() - position2.getX() , 2) + math.pow(position1.getY() - position2.getY() , 2))
  return totalDistance <= distance

allPlants = []

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

  def prevHolding(self):
    if self.currentlyHolding == 0:
      self.currentlyHolding == 5
    else:
      self.currentlyHolding -= 1

  # def useHolding(self, mousePos):
  #   if self.currentlyHolding != 0:
  #     if self.currentlyHolding == 4:
  #       fertilize(mousePos)
  #     elif self.currentlyHolding == 5:
  #       water(mousePos)
  #     else:
  #       plant(self.currentlyHolding, mousePos)


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
      self.water = 5
      self.soilQuality = 5

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

#the following three are not completedf
class Leafy(Plant):
  def __init__(self, soil, soilFertility):
      super().__init__(soil, soilFertility)

class SuccuLent(Plant):
  def __init__(self, soil):
      super().__init__(soil)

class Tree(Plant):
  def __init__(self, soil):
      super().__init__(soil)

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

class imageCoordinateCombo():
  def __init__(self, image, coordinate):
      self.image = image
      self.coordinate = coordinate
  
  def getImage(self):
    return self.image

  def getCoordinate(self):
    return self.coordinate

running = True
currholding = 0

while running:

  mx, my = pygame.mouse.get_pos()

  screen.fill((0,0,0))
  # screen.blit(currbackgroundImage, (0,0))
  showText(text, holdingText)

  pygame.time.delay(2)
  clock.tick(200)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        playerDeltaX = -1
      elif event.key == pygame.K_d:
        playerDeltaX = 1
      elif event.key == pygame.K_w:
        playerDeltaY = -1
      elif event.key == pygame.K_s:
        playerDeltaY = 1
      elif event.key == pygame.K_e:
        if currholding == 5:
          currholding = 0
        else:
          currholding += 1
      elif event.key == pygame.K_q:
        if currholding == 0:
          currholding = 5
        else:
          currholding -= 1
      
      if currholding == 0:
        holdingText = "you are holding nothing"
      elif currholding == 1:
        holdingText = "you are holding a leafy plant"
      elif currholding == 2:
        holdingText = "you are holding a succulent plant"
      elif currholding == 3:
        holdingText = "you are holding a tree"
      elif currholding == 4:
        holdingText = "you are holding fertilizer"
      elif currholding == 5:
        holdingText = "you are holding a watering can"

    if event.type == pygame.KEYUP:
      playerDeltaX = 0
      playerDeltaY = 0

    if event.type == pygame.MOUSEBUTTONDOWN:
      if(withinDistance(Position(playerX + 38, playerY + 50), Position(mx + 32, my + 32), 128)):
        if currholding == 1:
          background1PlacedImagesPositions.append(imageCoordinateCombo(carrotIMG, (mx - 4, my - 6)))
        elif currholding == 2:
          background1PlacedImagesPositions.append(imageCoordinateCombo(flowerIMG, (mx - 5, my - 6)))
        elif currholding == 3:
          background1PlacedImagesPositions.append(imageCoordinateCombo(treeIMG, (mx - 40, my - 40)))

  if playerX <= -32:
    if currbackground == 0:
      playerX = -32
    else:
      playerX = WIDTH - 64

      if currbackground == 1:
        text = "you are in the first area"
        currbackground = 0
      #   currbackgroundImage = backgroundImage1
      elif currbackground == 2:
        text = "you are in the second area"
        currbackground = 1
      #   currbackgroundImage = backgroundImage2
      
      print(currbackground)


  if playerX >= WIDTH - 32:
    if currbackground == 2:
      playerX = WIDTH - 32
    else:
      playerX = 0

      if currbackground == 0:
        text = "you are in the second area"
        currbackground = 1
      #   currbackgroundImage = backgroundImage2
      elif currbackground == 1:
        text = "you are in the third area"
        currbackground = 2
      #   currbackgroundImage = backgroundImage3
      
      print(currbackground)

  #Boundary handling
  if playerY < -32:
    playerY = -32

  elif playerY > HEIGHT - 32:
    playerY = HEIGHT - 32


  #moving
  playerY += playerDeltaY
  playerX += playerDeltaX

  renderAllPlaced()
  player(playerX, playerY)
  pygame.display.update()