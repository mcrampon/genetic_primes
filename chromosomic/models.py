import math
import random
import sys

class Formula():
  def __init__(self, chromosomes):
    self.chromosomes = chromosomes

  def apply(self, value):
    result = 0
    for chromosome in self.chromosomes:
      result += chromosome.apply(value)
    return result

class Chromosome():
  def __init__(self, genes):
    self.genes = genes

  def apply(self, value):
    result = value
    for gene in self.genes:
      result = gene.apply(result)
    return result

class Gene():
  def __init__(self, func, options):
    self.func = func
    self.options = options

  def apply(self, value):
    return self.func(value, *self.options)

  @staticmethod
  def create_gene():
    func = random.choice(FUNCTIONS.keys())
    options = []
    if FUNCTIONS[func]:
      options.append(random.randint(-5,4) + random.random())
    return Gene(func, options)

def inv_pow(value, option):
  if abs(value) > 30:
    return sys.maxint
  if value <= 0 and option == 0:
    return 0
  try:
    if int(value) != value and option < 0:
      return - pow(- option, value)
    return pow(option, value)
  except:
    return sys.maxint if option > 0 else - sys.maxint

def my_pow(value, option):
  if abs(option) > 30:
    return sys.maxint
  if option <= 0 and value == 0:
    return 0
  try:
    if int(option) != option and value < 0:
      return - pow(- value, option)
    return pow(value, option)
  except:
    return sys.maxint if value > 0 else - sys.maxint

def inverse(value):
  if value == 0:
    return sys.maxint
  return 1.0 / value

def add(value, option):
  return value + option

def substract(value, option):
  return value - option

def multiply(value, option):
  return value * option

def divide(value, option):
  if option == 0:
    return sys.maxint
  return value / float(option)

def inv_divide(value, option):
  if value == 0:
    return sys.maxint
  return float(option) / value

def inv_substract(value, option):
  return option - value

def log(value):
  try:
    return math.log(abs(value))
  except:
    return -sys.maxint

def exp(value):
  try:
    return math.exp(value)
  except:
    return sys.maxint

# Functions that can be used to build genes, and the number of arguments
# that have to be passed, apart from the value
FUNCTIONS = {
  log: 0,
  exp: 0,
  inverse: 0,
  my_pow: 1,
  inv_pow: 1,
  add: 1,
  substract: 1,
  multiply: 1,
  divide: 1,
  inv_divide: 1,
  inv_substract: 1
}
