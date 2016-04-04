from models import Gene, Formula
from conf import POPULATION_SIZE, PRIMES, GENERATIONS, MUTATION_RATE, EVOLUTION_RATE
import random

def evaluate(formula, stopper):
  i = 0
  success = 0
  found = []
  while i < stopper:
    i += 1
    result = formula.apply(i)
    if result in PRIMES and result not in found:
      success += 1
      found.append(result)
  return success

def initialize(size):
  formulas = {}
  for index in range(0, size):
    g = Gene.create_gene()
    f = Formula([g])
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
        if len(father.genes) != len(mother.genes):
          # individuals of different species cannot reproduce. So sad!
          continue
        cut_position = random.randint(0, len(father.genes) - 1)
        child1 = Formula(father.genes[:cut_position] + mother.genes[cut_position:])
        child2 = Formula(mother.genes[:cut_position] + father.genes[cut_position:])

        for child in (child1, child2):
          # Mutation
          if random.random() < MUTATION_RATE:
            mutation_position = random.randint(0, len(child.genes) - 1)
            child.genes[mutation_position] = Gene.create_gene()

          # Evolution
          if random.random() < EVOLUTION_RATE:
            child.genes.append(Gene.create_gene())

          new_formulas[child] = evaluate(child, stopper)

      # Selection
      formulas = sorted(new_formulas.items(), key=lambda x: x[1], reverse=True)[:POPULATION_SIZE]
      print formulas[0][1]
      if formulas[0][1] == stopper:
        stopper += 200
      formulas = dict(formulas)
      generation += 1
  except KeyboardInterrupt:
    print "STOPPED"

  print "WINNER :"
  for i in sorted(formulas.items(), key=lambda x: x[1], reverse=True)[0][0].genes:
    print i.func
    print i.options


if __name__ == "__main__":
    main()
