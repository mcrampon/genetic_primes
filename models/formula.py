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
    for i, j in enumerate(primes):
      result = self.apply(i + 1)
      distance += abs(j - result)
    return distance
