from models import Gene, Formula, my_pow, multiply, FUNCTIONS
from conf import (
  EVOLUTION_RATE,
  GENERATIONS,
  MUTATION_RATE,
  POPULATION_SIZE,
  PRIMES,
  SMALL_MUTATION_RATE,
  SUPPRESION_RATE
)
import random

def evaluate(formula):
  distance = 0
  for i, j in enumerate(PRIMES):
    result = formula.apply(i)
    distance += abs(j - result)
  return distance

def initialize(size):
  formulas = {}
  for index in range(0, size):
    # g = Gene.create_gene()
    g1 = Gene(my_pow, [1.101])
    g2 = Gene(multiply, [4])
    f = Formula([g1, g2])
    formulas[f] = evaluate(f)
  return formulas

def main():
  random.seed(0)
  generation = 0
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
          # Small mutation
          if random.random() < SMALL_MUTATION_RATE:
            mutation_position = random.randint(0, len(child.genes) - 1)
            func = child.genes[mutation_position].func
            options = []
            if FUNCTIONS[func]:
              options.append(random.randint(-5,4) + random.random())
            child.genes[mutation_position].options = options

          # Mutation
          if random.random() < MUTATION_RATE:
            mutation_position = random.randint(0, len(child.genes) - 1)
            child.genes[mutation_position] = Gene.create_gene()

          # Evolution
          if random.random() < EVOLUTION_RATE:
            child.genes.append(Gene.create_gene())

          if len(child.genes) > 1 and random.random() < SUPPRESION_RATE:
            suppression_position = random.randint(0, len(child.genes) - 1)
            child.genes.pop(suppression_position)

          new_formulas[child] = evaluate(child)

      # Selection
      formulas = sorted(new_formulas.items(), key=lambda x: x[1], reverse=False)[:POPULATION_SIZE]
      print formulas[0][1]
      formulas = dict(formulas)
      generation += 1
  except KeyboardInterrupt:
    print "STOPPED"

  print "WINNER :"
  for i in sorted(formulas.items(), key=lambda x: x[1], reverse=False)[0][0].genes:
    print i.func
    print i.options


if __name__ == "__main__":
    main()
