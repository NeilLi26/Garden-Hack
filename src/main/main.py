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
backgroundImage1 = pygame.image.load('src/main/Starting_Screen.png')
backgroundImage2 = pygame.image.load('src/main/Tutorial_Screen.png')
# backgroundImage3 = pygame.image.load('src/main/Starting_Screen.png')
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

def withinDistance(position1, position2, distance):
  totalDistance = math.sqrt(math.pow(position1.getX() - position2.getX() , 2) + math.pow(position1.getY() - position2.getY() , 2))
  return totalDistance <= distance

allPlants = []

def addToCurrentThing(currbackground):
  backgroundPlacedImagesPositions = background1PlacedImagesPositions

  if currbackground == 1:
    backgroundPlacedImagesPositions = background2PlacedImagesPositions
  elif currbackground == 2:
    backgroundPlacedImagesPositions = background2PlacedImagesPositions
  elif currbackground == 3:
    backgroundPlacedImagesPositions = background2PlacedImagesPositions
  elif currbackground == 4:
    backgroundPlacedImagesPositions = background2PlacedImagesPositions

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

  def getwWatered(self):
    return self.background
  
  def getFertilized(self):
    return self.background
  
  def getBackground(self):
    return self.background
  
  def makeWatered(self):
    self.watered = True
    print("you watered a plant")

  def makeFertilized(self):
    self.fertilized = True
    print("you fertilized a plant")

class imageCoordinateCombo():
  def __init__(self, image, coordinate):
      self.image = image
      self.coordinate = coordinate
  
  def getImage(self):
    return self.image

  def getCoordinate(self):
    return self.coordinate

#booleans
running = True
QorEPRESSED = False
currholding = 0

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

      if currbackground != 0 and QorEPRESSED:
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
      if currbackground == 1 and currholding == 0:
        if(checkWithinBox(48, 122, 137, 223, mx, my)):
          text = "flowers are great at removing noxious odors"
        elif(checkWithinBox(500, 575, 137, 223, mx, my)):
          text = "trees do a lot to stabilize soil"
        elif(checkWithinBox(10, 85, 353, 440, mx, my)):
          text = "vegetables are an important food source"
        elif(checkWithinBox(702, 778, 341, 427, mx, my)):
          text = "remember to water and fertilize your plants"

      if(withinDistance(Position(playerX + 38, playerY + 50), Position(mx + 32, my + 32), 128)):
        if(currholding >= 4):
          if currholding == 4:
            fertilize()
          elif currholding == 5:
            water()

        else:
          addToCurrentThing(currbackground)
          
        
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
        text = "press the signs while holding nothing for tip"
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
      # currbackgroundImage = backgroundImage1
    else:
      playerY = HEIGHT - 32
      
    print(currbackground)

  #moving
  playerY += playerDeltaY
  playerX += playerDeltaX

  renderAllPlaced()
  player(playerX, playerY)
  pygame.display.update()