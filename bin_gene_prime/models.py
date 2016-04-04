import random

class Formula():
  def __init__(self, genes):
    self.genes = genes

  def apply(self, value):
    result = value
    for gene in self.genes:
      result = gene.apply(value)
    return result

class Gene():
  def __init__(self, func, target):
    self.func = func
    self.target = target

  def apply(self, value):
    if self.target == "self":
      return self.func(value, value)
    else:
      return self.func(value, self.target)

  @staticmethod
  def create_gene():
    func = random.choice(FUNCTIONS)
    target = random.choice(["self", random.randint(0,10)])
    return Gene(func, target)

def bin_and(value, target):
  return value & target

def bin_or(value, target):
  return value | target

def bin_not(value, target):
  return ~ value

def bin_xor(value, target):
  return value & ~ target

def inv_bin_xor(value, target):
  return target & ~ value

FUNCTIONS = [
  bin_not,
  bin_or,
  bin_and,
  bin_xor,
  inv_bin_xor
]
