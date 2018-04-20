import math
import sys

def inverse(value):
  if value == 0:
    return sys.maxsize
  return 1.0 / value

def add(value, option):
  return value + option

def substract(value, option):
  return value - option

def multiply(value, option):
  return value * option

def divide(value, option):
  if option == 0:
    return sys.maxsize
  return value / float(option)

def inv_divide(value, option):
  if value == 0:
    return sys.maxsize
  return float(option) / value

def inv_substract(value, option):
  return option - value

def log(value):
  try:
    return math.log(abs(value))
  except ValueError:
    return -sys.maxsize

def exp(value):
  try:
    return math.exp(value)
  except OverflowError:
    return sys.maxsize

def inv_pow(value, option):
  if abs(value * log(option)) > log(sys.maxsize):
    return math.copysign(sys.maxsize, option)
  if value <= 0 and option == 0:
    return 0
  if int(value) != value and option < 0:
    return - pow(- option, value)
  return pow(option, value)

def safe_pow(value, option):
  if abs(option * log(value)) > log(sys.maxsize):
    return math.copysign(sys.maxsize, value)
  if option <= 0 and value == 0:
    return 0
  if int(option) != option and value < 0:
    return - pow(- value, option)
  return pow(value, option)

def sin(value):
  try:
    return math.sin(value)
  except OverflowError:
    # Value too big -> arbitrary choice
    return 0

def cos(value):
  try:
    return math.cos(value)
  except OverflowError:
    # Value too big -> arbitrary choice
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
