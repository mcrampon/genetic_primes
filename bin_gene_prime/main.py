from models import Gene, Formula
from conf import (
  POPULATION_SIZE,
  PRIMES,
  GENERATIONS,
  MUTATION_RATE,
  BIG_MUTATION_RATE,
  EVOLUTION_RATE,
  SUPPRESION_RATE
)
import random


def evaluate(formula, stopper):
  i = 0
  success = 0
  # init fail to 1 to avoid division by 0. Not important for evaluation
  fail = 1
  while i < len(PRIMES):
    i += 1
    result = formula.apply(i)
    if result == PRIMES[i - 1]:
      success += 1
    else:
      fail += 1
  return float(success) / fail

def initialize(size):
  formulas = {}
  for index in range(0, size):
    genes = [Gene.create_gene() for i in range(0, random.randint(3,10))]
    f = Formula(genes)
    formulas[f] = evaluate(f, 200)
  return formulas

def main():
  random.seed()
  generation = 0
  stopper = 200
  formulas = initialize(POPULATION_SIZE)
  try:
    while generation < GENERATIONS:
      print "GENERATION : " + str(generation)
      new_formulas = {}
      while len(formulas) > 1:
        father = random.choice(formulas.keys())
        new_formulas[father] = formulas.pop(father)
        mother = random.choice(formulas.keys())
        new_formulas[mother] = formulas.pop(mother)

        # Reproduction
        cut_position = random.randint(0, len(father.genes) - 1)
        child1 = Formula(father.genes[:cut_position] + mother.genes[cut_position:])
        child2 = Formula(mother.genes[:cut_position] + father.genes[cut_position:])

        for child in (child1, child2):
          # Mutation
          if random.random() < MUTATION_RATE:
            mutation_position = random.randint(0, len(child.genes) - 1)
            child.genes[mutation_position].target = random.choice(["self", random.randint(0,10)])

          # Big mutation
          if random.random() < BIG_MUTATION_RATE:
            mutation_position = random.randint(0, len(child.genes) - 1)
            child.genes[mutation_position] = Gene.create_gene()

          # Evolution
          if random.random() < EVOLUTION_RATE:
            child.genes.append(Gene.create_gene())

          if len(child.genes) > 1 and random.random() < SUPPRESION_RATE:
            suppression_position = random.randint(0, len(child.genes) - 1)
            child.genes.pop(suppression_position)

          new_formulas[child] = evaluate(child, stopper)

      # Selection
      formulas = sorted(new_formulas.items(), key=lambda x: x[1], reverse=True)[:POPULATION_SIZE]
      print [i[1] for i in formulas[:3]]
      if formulas[0][1] == stopper:
        stopper += 200
      formulas = dict(formulas)
      generation += 1
  except KeyboardInterrupt:
    print "STOPPED"

  print "WINNER :"
  for i in sorted(formulas.items(), key=lambda x: x[1], reverse=True)[0][0].genes:
    print i.func
    print i.target
if __name__ == "__main__":
    main()
