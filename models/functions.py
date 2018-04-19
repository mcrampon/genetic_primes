import math
import sys

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

def safe_pow(value, option):
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

def sin(value):
  try:
    return math.sin(value)
  except ValueError:
    # Value == inf -> arbitrary choice
    return 0

def cos(value):
  try:
    return math.cos(value)
  except ValueError:
    # Value == inf -> arbitrary choice
    return 1

# Functions that can be used to build genes, and the number of arguments
# that have to be passed, apart from the value
FUNCTIONS = {
  sin: 0,
  cos: 0,
  log: 0,
  exp: 0,
  inverse: 0,
  safe_pow: 1,
  inv_pow: 1,
  add: 1,
  substract: 1,
  multiply: 1,
  divide: 1,
  inv_divide: 1,
  inv_substract: 1
}
