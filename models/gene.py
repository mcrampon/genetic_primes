import random
from functions import FUNCTIONS

class Gene():
  def __init__(self, func, options):
    self.func = func
    self.options = options

  def apply(self, value):
    return self.func(value, *self.options)

  @staticmethod
  def create_gene():
    func = random.choice(FUNCTIONS.keys())
    options = [
      random.random() * 10 - 5
      for _ in range(FUNCTIONS[func])
    ]
    return Gene(func, options)
