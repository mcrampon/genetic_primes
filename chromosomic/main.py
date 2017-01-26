from copy import deepcopy
import getopt
import pickle
import random
import time
import sys

from conf import (
  C_EVOLUTION_RATE,
  C_SUPPRESION_RATE,
  EVOLUTION_RATE,
  GENERATIONS,
  MUTATION_RATE,
  POPULATION_SIZE,
  PRIMES,
  SMALL_MUTATION_RATE,
  SUPPRESION_RATE
)
from models import Gene, Chromosome, Formula, my_pow, multiply, FUNCTIONS

# /////////////////////////////////////////
# ///                                   ///
# ///               TO DO               ///
# ///                                   ///
# /////////////////////////////////////////
# ///                                   ///
# ///        Keep populations of        ///
# ///        each kind of species       ///
# ///                                   ///
# /////////////////////////////////////////
# ///                                   ///
# ///       Generate all functions      ///
# ///                                   ///
# /////////////////////////////////////////

def evaluate(formula):
  distance = 0
  for i, j in enumerate(PRIMES):
    result = formula.apply(i+1)
    distance += abs(j - result)
  return distance

def initialize(size):
  formulas = {}
  for index in range(0, size):
    # g1 = Gene(my_pow, [1.101])
    # g2 = Gene(multiply, [4])
    # c = Chromosome([g1, g2])
    c = Chromosome([Gene.create_gene()])
    f = Formula([c])
    formulas[f] = evaluate(f)
  return formulas

def main(argv):
  random.seed(0)
  try:
    f = open(argv[0], 'r')
    generation = int(f.readline().replace('\n', ''))
    formulas = pickle.loads(f.read())
    f.close
  except:
    generation = 0
    formulas = initialize(POPULATION_SIZE)
  try:
    while generation < GENERATIONS:
      safe_copy = deepcopy(formulas)
      if generation % 100 == 0:
        print "GENERATION : " + str(generation)
      new_formulas = {}
      while len(formulas) > 1:
        father = random.choice(formulas.keys())
        new_formulas[father] = formulas.pop(father)
        mother = random.choice(formulas.keys())
        new_formulas[mother] = formulas.pop(mother)

        # Reproduction
        if len(father.chromosomes) != len(mother.chromosomes):
          # individuals of different species cannot reproduce. So sad!
          continue
        child1 = Formula([])
        child2 = Formula([])
        for i in range(0, len(father.chromosomes)):
          if random.random() < 0.5:
            child1.chromosomes.append(deepcopy(father.chromosomes[i]))
            child2.chromosomes.append(deepcopy(mother.chromosomes[i]))
          else:
            child2.chromosomes.append(deepcopy(father.chromosomes[i]))
            child1.chromosomes.append(deepcopy(mother.chromosomes[i]))

        for child in (child1, child2):
          # Small mutation
          if random.random() < SMALL_MUTATION_RATE:
            c_position = random.randint(0, len(child.chromosomes) - 1)
            g_position = random.randint(0, len(child.chromosomes[c_position].genes) - 1)
            func = child.chromosomes[c_position].genes[g_position].func
            options = []
            if FUNCTIONS[func]:
              options.append(random.randint(-5, 4) + random.random())
            child.chromosomes[c_position].genes[g_position].options = options

          # Mutation
          if random.random() < MUTATION_RATE:
            c_position = random.randint(0, len(child.chromosomes) - 1)
            g_position = random.randint(0, len(child.chromosomes[c_position].genes) - 1)
            child.chromosomes[c_position].genes[g_position] = Gene.create_gene()

          # Add / remove genes
          if random.random() < EVOLUTION_RATE:
            child.chromosomes[
              random.randint(0, len(child.chromosomes) - 1)
            ].genes.append(Gene.create_gene())

          if len(child.chromosomes) > 1 and random.random() < SUPPRESION_RATE:
            c_position = random.randint(0, len(child.chromosomes) - 1)
            if len(child.chromosomes[c_position].genes) > 1:
              g_position = random.randint(0, len(child.chromosomes[c_position].genes) - 1)
              child.chromosomes[c_position].genes.pop(g_position)

          # Add / remove chromosomes
          if random.random() < C_EVOLUTION_RATE:
            child.chromosomes.append(Chromosome([Gene.create_gene()]))

          if len(child.chromosomes) > 1 and random.random() < C_SUPPRESION_RATE:
            child.chromosomes.pop(random.randint(0, len(child.chromosomes) - 1))

          new_formulas[child] = evaluate(child)

      # Selection
      formulas = sorted(new_formulas.items(), key=lambda x: x[1])[:POPULATION_SIZE]
      if generation % 100 == 0:
        print formulas[0][1]
        print len(formulas[0][0].chromosomes)
        print len(formulas)
      formulas = dict(formulas)
      generation += 1
  except KeyboardInterrupt:
    print "STOPPED"
    print "SAVING"
    if type(safe_copy) == type([]):
      safe_copy = dict(safe_copy)
    f = open('run_save_' + str(int(time.time())), 'w+')
    f.write(str(generation) + '\n')
    f.write(pickle.dumps(safe_copy))
    f.close()

  f = open('results_' + str(int(time.time())), 'w+')
  print "WINNER :"
  for c in sorted(formulas.items(), key=lambda x: x[1])[0][0].chromosomes:
    for g in c.genes:
      f.write(g.func.__name__ + '\n')
      f.write(str(g.options) + '\n')
    f.write('===========================\n')
  f.close()
  print 'SCORE : ' + str(sorted(formulas.items(), key=lambda x: x[1])[0][1])
  length = sum([len(f[0].chromosomes) for f in formulas.items()]) / float(len(formulas))
  print 'Average number of chromosomes : ' + str(length)

if __name__ == "__main__":
    main(sys.argv[1:])
