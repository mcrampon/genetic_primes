from sys import maxsize

class Formula():
  def __init__(self, chromosomes):
    self.chromosomes = chromosomes

  def apply(self, value):
    result = 0
    for chromosome in self.chromosomes:
      result += chromosome.apply(value)
    return result

  def evaluate(self, primes):
    distance = 0
    for n, nth_prime in enumerate(primes):
      result = self.apply(n + 1)
      try:
        distance += (nth_prime - result)**2
      except OverflowError:
        distance = maxsize
    return distance
