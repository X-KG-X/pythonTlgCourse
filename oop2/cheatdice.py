#!/usr/bin/env python3
from random import randint

# Create player class
class Player:
  def __init__(self):
    self.dice = []

  def roll(self):
    self.dice = [] # clears current dice
    for i in range(3):
      self.dice.append(randint(1,6))

  def get_dice(self):
    return self.dice

class Cheat_Swapper(Player):
  #every time the last roll will be swapped with value 6
  def cheat(self):
    self.dice[-1] = 6

class Cheat_Loaded_Dice(Player):
    #each roll value is incremented by the value of 1
  def cheat(self):
    i = 0
    while i < len(self.dice):
      if self.dice[i] < 6:
        self.dice[i] += 1
      i += 1

