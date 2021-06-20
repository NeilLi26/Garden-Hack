import pygame
import math
import random

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

#villager initializations
vsadIMG = "src/main/sadgirl.jpg"
vmediumIMG = "src/main/mediumgirl.jpg"
vhappyIMG = "src/main/happygirl.jpg"
villagerIMG = vsadIMG

#plants
treeIMG = pygame.image.load('src/main/big_tree.png')
flowerIMG = pygame.image.load('src/main/carrot.png')
carrotIMG = pygame.image.load('src/main/flowers.png')

#gas
gasIMG = pygame.image.load('src/main/cloud.png')

#background
currbackground = 0
backgroundImage1 = pygame.image.load('src/main/Starting_Screen.png')
backgroundImage2 = pygame.image.load('src/main/Tutorial_Screen.png')
backgroundImage3 = pygame.image.load('src/main/Level_1_Screen.png')
# backgroundImage4 = pygame.image.load('src/main/Starting_Screen.png')
# backgroundImage5 = pygame.image.load('src/main/Starting_Screen.png')
currbackgroundImage = backgroundImage1

#Text
text = "you are in the first area"
font = pygame.font.Font('freesansbold.ttf', 32)
holdingText = ""
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 20
textY = 10

holdingTextX = 20
holdingTextY = 45

#clock
clock = pygame.time.Clock()

def checkWithinBox(xMin, xMax, yMin, yMax, mX,mY):
  withinY = mY < yMax + 5 and mY > yMin - 5
  withinX = mX < xMax + 5 and mX > xMin - 5

  return withinY and withinX

def showText(desiredText, desiredHoldingText):
  text = font.render(desiredText, True, (255, 255, 255))
  screen.blit(text, (textX, textY))
  text = font.render(desiredHoldingText, True, (255, 255, 255))
  screen.blit(text, (holdingTextX, holdingTextY))

def player(x, y):
  screen.blit(playerImg, (x, y))
  pygame.draw.circle(screen, (  0,   0, 255), (x + 32,y + 32), 10)

#backgrounds
background1PlacedImagesPositions = []
background2PlacedImagesPositions = []
background3PlacedImagesPositions = []
background4PlacedImagesPositions = []
background5PlacedImagesPositions = []

#some collections of things
allPlants = []

gasClouds = []

def renderAllPlaced():
  if currbackground == 0:
    for IMGandCoordinates in background1PlacedImagesPositions:
      screen.blit(IMGandCoordinates.getImage(), IMGandCoordinates.getCoordinate())
  elif currbackground == 1:
    for IMGandCoordinates in background2PlacedImagesPositions:
      screen.blit(IMGandCoordinates.getImage(), IMGandCoordinates.getCoordinate())
  elif currbackground == 2:
    for IMGandCoordinates in background3PlacedImagesPositions:
      screen.blit(IMGandCoordinates.getImage(), IMGandCoordinates.getCoordinate())
  elif currbackground == 3:
    for IMGandCoordinates in background4PlacedImagesPositions:
      screen.blit(IMGandCoordinates.getImage(), IMGandCoordinates.getCoordinate())
  elif currbackground == 4:
    for IMGandCoordinates in background5PlacedImagesPositions:
      screen.blit(IMGandCoordinates.getImage(), IMGandCoordinates.getCoordinate())

def renderClouds(currbackground):
  for cloud in gasClouds:
    if cloud.getBackground() == currbackground:
      pos = cloud.getPos()
      screen.blit(gasIMG, (pos.getX(), pos.getY()))


def withinDistance(position1, position2, distance):
  totalDistance = math.sqrt(math.pow(position1.getX() - position2.getX() , 2) + math.pow(position1.getY() - position2.getY() , 2))
  return totalDistance <= distance

def addToCurrentThing(currbackground):
  backgroundPlacedImagesPositions = background1PlacedImagesPositions

  if currbackground == 1:
    backgroundPlacedImagesPositions = background2PlacedImagesPositions
  elif currbackground == 2:
    backgroundPlacedImagesPositions = background3PlacedImagesPositions
  elif currbackground == 3:
    backgroundPlacedImagesPositions = background4PlacedImagesPositions
  elif currbackground == 4:
    backgroundPlacedImagesPositions = background4PlacedImagesPositions

  if currholding == 1:
    backgroundPlacedImagesPositions.append(imageCoordinateCombo(carrotIMG, (mx - 4, my - 6)))
    allPlants.append(Plant(Position(mx - 4, my - 6), currholding - 1, currbackground))
  elif currholding == 2:
    backgroundPlacedImagesPositions.append(imageCoordinateCombo(flowerIMG, (mx - 5, my - 6)))
    allPlants.append(Plant(Position(mx - 5, my - 6), currholding - 1, currbackground))
  elif currholding == 3:
    backgroundPlacedImagesPositions.append(imageCoordinateCombo(treeIMG, (mx - 40, my - 40)))
    allPlants.append(Plant(Position(mx - 40, my - 40), currholding - 1, currbackground))

def water():
  plantsInSameBackground = []

  for plant in allPlants:
    if plant.getBackground() == currbackground:
      plantsInSameBackground.append(plant)

  for plant in plantsInSameBackground:
    if withinDistance(plant.getPos(), Position(playerX, playerY), 128):
      plant.makeWatered()

def fertilize():
  plantsInSameBackground = []

  for plant in allPlants:
    if plant.getBackground() == currbackground:
      plantsInSameBackground.append(plant)

  for plant in plantsInSameBackground:
    if withinDistance(plant.getPos(), Position(playerX, playerY), 128):
      plant.makeFertilized()
      
def checkForNearbyTrees(linePos):
  treesInSameBackground = []

  for plant in allPlants:
    if plant.getBackground() == currbackground and plant.getType() == 2:
      treesInSameBackground.append(plant)

  for tree in treesInSameBackground:
    if withinDistance(tree.getPos(), Position(tree.getPos().getX(), linePos), 128) and tree.getHappiness():
      return True

  return False

def checkForHappyPlants():
  for plant in allPlants:
    if plant.getWatered() and plant.getFertilized():
      plant.makeHappy()
      print("a plant was made happy")
      for plant in allPlants:
        print(plant.getType())
        print(plant.getHappiness())

def clearGasClouds(gasClouds):
  flowersInSameBackground = []

  for plant in allPlants:
    if plant.getBackground() == currbackground and plant.getType() == 0:
      flowersInSameBackground.append(plant)

  filteredGasClouds = []
  
  for flower in flowersInSameBackground:
    for cloud in gasClouds:
      if withinDistance(flower.getPos(), cloud.getPos(), 128) and flower.getHappiness():
        gasClouds.remove(cloud)
  
  # gasClouds = filteredGasClouds

class Positionable():
  def __init__(self, Position):
      self.Position = Position

  def getPos(self):
      return self.Position

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

class Plant(Positionable):
  def __init__(self, Position, type, background):
      super().__init__(Position)
      self.happiness = False
      self.watered = False
      self.fertilized = False
      self.type = type
      self.background = background
      # 0 for leafy, 1 for succlent, 2 for trees

  def getHappiness(self):
    return self.happiness
  
  def makeHappy(self):
    self.happiness = True

  def getType(self):
    return self.type

  def getWatered(self):
    return self.watered
  
  def getFertilized(self):
    return self.fertilized
  
  def getBackground(self):
    return self.background
  
  def makeWatered(self):
    self.watered = True
    print("you watered a plant")

  def makeFertilized(self):
    self.fertilized = True
    print("you fertilized a plant")

#gas with size 64 x 64
class Gas(Positionable):
  def __init__(self, Position, background):
      super().__init__(Position)
      self.background = background

  def getBackground(self):
    return self.background

class imageCoordinateCombo():
  def __init__(self, image, coordinate):
      self.image = image
      self.coordinate = coordinate
  
  def getImage(self):
    return self.image

  def getCoordinate(self):
    return self.coordinate

all_villagers = pygame.sprite.Group()

class Villager(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Villager,self).__init__()
        self.surf = pygame.image.load(villagerIMG)
        self.mood = 0

        #changing the size of image
        self.surf = pygame.transform.scale(self.surf, (80,120))
        self.rect = self.surf.get_rect(
        center=(
            x,
            y,
            )
        )
    def update(self):
      self.mood = 0
      for cloud in gasClouds:
        cloudPos = cloud.getPos()
        if withinDistance(Position(cloudPos.getX(), cloudPos.getY()), Position(self.rect.centerx, self.rect.centery), 128):
          self.mood = 1
          break
        
      if self.mood == 1:
        flowers = []
        for plant in allPlants:
          if plant.getType() == 0:
            flowers.append(plant)

        for flower in flowers:
          if withinDistance(Position(flower.getPos().getX(), flower.getPos().getY()), Position(self.rect.centerx, self.rect.centery), 256):
              villagerIMG = vmediumIMG
              self.surf = pygame.image.load(villagerIMG)
              #Resize
              self.surf = pygame.transform.scale(self.surf, (80,120))  
              break

      elif self.mood == 0:
        deliciousPlants = []
        for plant in allPlants:
          if plant.getType() == 1:
            deliciousPlants.append(plant)

        #Villager happiness
        for plant in deliciousPlants:
          if abs(self.rect.centerx - plant.getPos().getX()) < 80 and abs(self.rect.centery - plant.getPos().getY()) < 80:
            if plant.getHappiness():
              villagerIMG = vhappyIMG
              self.surf = pygame.image.load(villagerIMG)
              #Resize
              self.surf = pygame.transform.scale(self.surf, (80,120))
              break
            else:
              villagerIMG = vmediumIMG
              self.surf = pygame.image.load(villagerIMG)
              #Resize
              self.surf = pygame.transform.scale(self.surf, (80,120))  
              break


#Spawn villagers
level1Viilagers = []
level1Viilagers.append(Villager(200, 400))
level1Viilagers.append(Villager(480, 220))

#booleans
running = True
QorEPRESSED = False
thirdBackgroundRiverBlocking = True
currholding = 0

#gas clouds
gasClouds.append(Gas(Position(120, 450), 2))
gasClouds.append(Gas(Position(368, 270), 2))

while running:

  mx, my = pygame.mouse.get_pos()

  screen.fill((0,0,0))
  screen.blit(currbackgroundImage, (0,0))
  showText(text, holdingText)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        playerDeltaX = -2
      elif event.key == pygame.K_d:
        playerDeltaX = 2
      elif event.key == pygame.K_w:
        playerDeltaY = -2
      elif event.key == pygame.K_s:
        playerDeltaY = 2
      elif event.key == pygame.K_e:
        QorEPRESSED = True
        if currholding == 5:
          currholding = 0
        else:
          currholding += 1
      elif event.key == pygame.K_q:
        QorEPRESSED = True
        if currholding == 0:
          currholding = 5
        else:
          currholding -= 1
      elif event.key == pygame.K_ESCAPE:
        exit()

      if currbackground != 0 and QorEPRESSED:
        if currholding == 0:
          holdingText = "you are holding nothing"
        elif currholding == 1:
          holdingText = "you are holding a flowery plant"
        elif currholding == 2:
          holdingText = "you are holding a delicious plant"
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
      if currholding == 0:
        if currbackground == 1:
          if(checkWithinBox(48, 122, 137, 223, mx, my)):
            text = "flowers are great at removing noxious odors"
          elif(checkWithinBox(500, 575, 137, 223, mx, my)):
            text = "trees do a lot to stabilize soil"
          elif(checkWithinBox(10, 85, 353, 440, mx, my)):
            text = "vegetables are an important food source"
          elif(checkWithinBox(702, 778, 341, 427, mx, my)):
            text = "remember to water and fertilize your plants"
        elif currbackground == 2:
          if(checkWithinBox(33, 126, 239, 322, mx, my)):
            text = "villagers are not happy around oders"
          elif(checkWithinBox(354, 446, 443, 516, mx, my)):
            text = "well maintained flowers remove airborne toxins"
      
      if(withinDistance(Position(playerX + 38, playerY + 50), Position(mx + 32, my + 32), 128)):
        if(currholding >= 4):
          if currholding == 4:
            fertilize()
          elif currholding == 5:
            water()

        else:
          addToCurrentThing(currbackground)

      checkForHappyPlants()
      clearGasClouds(gasClouds)
          
  if playerX <= -32:
    if currbackground == 0 or currbackground == 2:
      playerX = -32
    else:
      playerX = WIDTH - 40

      if currbackground == 1:
        text = "you are in the first area"
        currbackground = 0
        currbackgroundImage = backgroundImage1
      elif currbackground == 3:
        text = "you are in the third area"
        currbackground = 2
        # currbackgroundImage = backgroundImage3
      elif currbackground == 4:
        text = "you are in the fourth area"
        currbackground = 3
        # currbackgroundImage = backgroundImage4
      
      print(currbackground)

  if playerX >= WIDTH - 32:
    if currbackground == 1 or currbackground == 4:
      playerX = WIDTH - 32
    else:
      playerX = -28

      if currbackground == 0:
        text = "click the signs while holding nothing for tips"
        holdingText = "press q and e to hold different items"
        currbackground = 1
        currbackgroundImage = backgroundImage2
      elif currbackground == 2:
        text = "you are in the fourth area"
        currbackground = 3
      #   currbackgroundImage = backgroundImage4
      elif currbackground == 3:
        text = "you are in the fifth area"
        currbackground = 4
        # currbackgroundImage = backgroundImage5
      
      print(currbackground)

  #Boundary handling
  if playerY < -32:
    if currbackground == 2:
      playerY = HEIGHT - 40
      text = "you are in the second area"
      currbackground = 1
      currbackgroundImage = backgroundImage2
    else:
      playerY = -32
      
    print(currbackground)

  #Boundary handling
  if playerY > HEIGHT - 32:
    if currbackground == 1:
      playerY = -28
      text = "you are in the third area"
      currbackground = 2
      currbackgroundImage = backgroundImage3
    else:
      playerY = HEIGHT - 32
      
    print(currbackground)

  #third thing event
  if currbackground == 2:
    if thirdBackgroundRiverBlocking:
      if playerY >= 300:
        playerY = 300

      thirdBackgroundRiverBlocking = checkForNearbyTrees(300)

  #moving
  playerY += playerDeltaY
  playerX += playerDeltaX
  
  clock.tick(120)

  renderAllPlaced()
  renderClouds(currbackground)
  player(playerX, playerY)
  
  #rendering villagers
  if currbackground == 2:
    for villager in level1Viilagers:
      villager.update()
      screen.blit(villager.surf, villager.rect)

  pygame.display.update()