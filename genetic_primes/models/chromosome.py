class Chromosome():
  def __init__(self, genes):
    self.genes = genes

  def apply(self, value):
    result = value
    if len(self.genes) == 0:
      return 0
    for gene in self.genes:
      result = gene.apply(result)
    return result
