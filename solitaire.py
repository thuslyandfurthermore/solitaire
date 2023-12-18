import random
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class card:
  def __init__(self, cardSuit, cardValue):
    self.suit = cardSuit
    self.value = cardValue
    self.visible = False

#returns a string of the suit and value
#but only if the card actually exists
#i call this so many times its dumb
#so its c()
def c(thing, index):
  suitstr = ''
  valstr = ''
  try:
    if thing[index].visible == False:
      valstr = 'x'
      suitstr = 'x'
    else:
      if thing[index].value == 1:
        valstr = 'a'
      elif thing[index].value == 11:
        valstr = 'j'
      elif thing[index].value == 12:
        valstr = 'q'
      elif thing[index].value == 13:
        valstr = 'k'
      else:
        valstr = str(thing[index].value)
    
      if thing[index].suit == 0:
        suitstr = '♠'
      if thing[index].suit == 1:
        suitstr = '♦'
      if thing[index].suit == 2:
        suitstr = '♣'
      if thing[index].suit == 3:
        suitstr = '♥'
    
  except:
    valstr = ''
    suitstr = ''
    
  return suitstr+valstr

#the last card in each field pile and discard pile should always be visible
def flipTopCard():
  for i in range(7):
    try:
      field[i][-1].visible = True
    except:
      1+1
  
  try:
    discard[-1].visible = True
  except:
    1+1

#tests if one card can be placed on another
def isStackable(src, dest):
  if src.suit % 2 == 0:
    if dest.suit % 2 == 1 and src.value + 1 == dest.value:
      return True
    else:
      return False
  else:
    if dest.suit % 2 == 0 and src.value + 1 == dest.value:
      return True
    else:
      return False

#board state update and display loop
def updateBoard():
  flipTopCard()
  
  #a number, corresponding to a field stack, that is the number of moveable cards in the stack
  for i in range(len(field)):
    pileLength[i] = sum([j.visible for j in field[i]])
  
  #find max height of field
  height = 0
  for i in range(len(field)):
    if len(field[i]) > height:
      height = len(field[i])
  
  cls()
  print(f'{c(stack, -1):6}{c(discard, -1):6}\n')
  
  print(f'{c(foundation[0], -1):5}{c(foundation[1], -1):6}{c(foundation[2], -1):6}{c(foundation[3], -1):6}\n')
  
  #display each field pile up to max height
  for i in range(height):
    print(f'{c(field[0],i):4}{c(field[1],i):4}{c(field[2],i):4}{c(field[3],i):4}{c(field[4],i):4}{c(field[5],i):4}{c(field[6],i):4}')
  
  print(f'\n\n{wins}/{losses} - {(wins / (wins + losses)) * 100:4f}%')

def move(pile, length, dest, reverse = False):
  if reverse == True:
    for i in range(length):
      dest.append(pile.pop())
    return
  else:
    for i in range(length):
      hand.append(pile.pop())
    for i in range(len(hand)):
      dest.append(hand.pop())

def nextMove():
  
  global desperationCounter, deathCounter
  
  #move any available cards into foundation
  for i in range(len(field)):
    try:
      if field[i][-1].value == foundation[field[i][-1].suit][-1].value + 1:
        move(field[i],1,foundation[field[i][-1].suit])
        desperationCounter = 0
        return
    except:
      1+1
  try:
    if discard[-1].value == foundation[discard[-1].suit][-1].value + 1:
      move(discard, 1, foundation[discard[-1].suit])
      desperationCounter = 0
      return
  except:
    1+1
  
  #king piles should go in empty field piles
  for i in range(len(field)):
    try:
      if field[i][-pileLength[i]].value == 13:
        for j in range(len(field)):
          try: #try to access a value
            field[j][-1].value == 0
          except: #if theres no card its an empty pile
          
          #if moving the king would leave behind an empty pile, dont
            if len(field[i]) == pileLength[i]:
              break
            else:
              move(field[i], pileLength[i], field[j])
              desperationCounter = 0
              return
    except:
      1+1
  try:
    if discard[-1].value == 13:
      for j in range(len(field)):
        try: #try to access a value
            field[j][-1].value == 0
        except: #if theres no card its an empty pile
          move(discard, 1, field[j])
          desperationCounter = 0
          return
  except:
    1+1
  
  #find matches for foundation and try to reveal them
  for i in range(len(foundation)):
    for j in range(len(field)):
      for k in range(len(field[j])):
        try:
          if field[j][k].suit == foundation[i][-1].suit and field[j][k].value == foundation[i][-1].value + 1 and field[j][k].visible:
            for l in range(len(field)):
              try:
                if isStackable(field[j][k + 1], field[l][-1]):
                  move(field[j], (len(field[j]) - k) - 1, field[l])
                  return
              except:
                1 + 1
        except:
          1 + 1
  
  #if you can move an entire pile to another card, do so
  for i in range(len(field)):
    for j in range(len(field)):
      try:
        if isStackable(field[i][-pileLength[i]], field[j][-1]):
          move(field[i], pileLength[i], field[j])
          desperationCounter = 0
          return
      except:
        1+1
  #and again for discard
  for j in range(len(field)):
    try:
      if isStackable(discard[-1], field[j][-1]):
        move(discard, 1, field[j])
        desperationCounter = 0
        return
    except:
      1+1
  
  #desperation tactics!!
  if desperationCounter > 2 and deathCounter % 2 == 0:
    #pull from foundations
    for i in range(len(foundation)):
      for j in range(len(field)):
        try:
          if isStackable(foundation[i][-1], field[j][-1]) and foundation[i][-1].visible:
            move(foundation[i], 1, field[j])
        except:
          1 + 1
    #check if u can move stuff around
    for i in range(len(field)):
      for j in range(len(field)):
        try:
          if isStackable(field[i][-pileLength[i]], field[j][-1]):
            move(field[i], pileLength[i], field[j])
        except:
          1 + 1
    #advance towards death
    deathCounter += 1
    desperationCounter = 0
  
  #idk move some shit around
  if desperationCounter > 2 and deathCounter % 2 == 1:
    for i in range(len(field)):
      #i think if u check backwards itll just go right back so only check forwards
      for j in range(i, len(field)):
        for k in range(len(field[i])):
          try:
            if field[i][k].visible:
              try:
                if isStackable(field[i][k], field[j][-1]):
                  move(field[i], len(field[i]) - k, field[j])
              except:
                1 + 1
          except:
            1 + 1
    #advance towards death
    deathCounter += 1
    desperationCounter = 0
  
  #if nothing else, pull from stack
  if len(stack) != 0:
    move(stack, 1, discard)
    return
  else:
    move(discard, len(discard), stack, True)
    for i in range(len(stack)):
      stack[i].visible = False
    desperationCounter += 1
    return

def reshuffle():
  global wins, losses
  loser = False
  #check if we lost
  for i in range(len(field)):
    if len(field[i]) > 0:
      loser = True
  if loser:
    losses +=1
  else:
    wins += 1
  
  #clear all cards
  for i in range(len(field)):
    for j in range(len(field[i])):
      try:
        field[i].pop()
      except:
        1+1
  
  for i in range(len(foundation)):
    for j in range(len(foundation[i])):
      try:
        foundation[i].pop()
      except:
        1+1
  
  for i in range(len(stack)):
    try:
      stack.pop()
    except:
      1+1
  
  for i in range(len(discard)):
    try:
      discard.pop()
    except:
      1+1
    
  for i in range(len(foundation)):
    foundation[i].append(card(0,0))
  
  #create cards
  for j in range(4):
    for i in range(13):
      stack.append(card(j, i + 1))

  random.shuffle(stack) #lol

  #deal
  for j in range(7):
    for i in range(j+1):
      field[j].append(stack.pop())
  

field = []
for i in range(7):
  field.append([])

foundation = []
for i in range(4):
  foundation.append([card(0,0)])

pileLength = [1,1,1,1,1,1,1]

stack = []
discard = []

hand = []

desperationCounter = 0
deathCounter = 0
wins = -1
losses = 0

reshuffle()

while True:
  updateBoard()
  nextMove()
  #input()
  if deathCounter > 4:
    deathCounter = 0
    reshuffle()
    
