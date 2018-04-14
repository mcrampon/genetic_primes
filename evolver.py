from copy import deepcopy
import random

from conf import (
  C_EVOLUTION_RATE,
  C_SUPPRESSION_RATE,
  EVOLUTION_RATE,
  MUTATION_RATE,
  POPULATION_SIZE,
  PRIMES,
  SMALL_MUTATION_RATE,
  SUPPRESSION_RATE
)

from logger import Logger
from models.gene import Gene
from models.chromosome import Chromosome
from models.formula import Formula
from models.functions import FUNCTIONS

class Evolver():
  def initialize_formulas(self):
    formulas = {}
    for index in range(0, POPULATION_SIZE):
      c = Chromosome([Gene.create_gene()])
      f = Formula([c])
      formulas[f] = f.evaluate(PRIMES)
    return formulas

  def next_generation(self, formulas):
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
      child1, child2 = self.create_children(father, mother)

      for child in (child1, child2):
        self.mutate_individual(child)
        new_formulas[child] = child.evaluate(PRIMES)

    # Selection
    formulas = sorted(
      new_formulas.items(), key=lambda x: x[1]
    )[:POPULATION_SIZE]
    Logger.best_formula(formulas)
    return dict(formulas)

  def create_children(self, father, mother):
    child1 = Formula([])
    child2 = Formula([])
    for i in range(0, len(father.chromosomes)):
      if random.random() < 0.5:
        child1.chromosomes.append(deepcopy(father.chromosomes[i]))
        child2.chromosomes.append(deepcopy(mother.chromosomes[i]))
      else:
        child2.chromosomes.append(deepcopy(father.chromosomes[i]))
        child1.chromosomes.append(deepcopy(mother.chromosomes[i]))
    return [child1, child2]

  def mutate_individual(self, individual):
    # SMALL_MUTATION_RATE
    self.mutate_gene(individual)
    # MUTATION_RATE
    self.replace_gene(individual)
    # EVOLUTION_RATE
    self.add_gene(individual)
    # SUPPRESSION_RATE
    self.remove_gene(individual)
    # C_EVOLUTION_RATE
    self.add_chromosome(individual)
    # C_SUPPRESSION_RATE
    self.remove_chromosome(individual)

  def mutate_gene(self, individual):
    if random.random() < SMALL_MUTATION_RATE:
      c_pos = random.randint(0, len(individual.chromosomes) - 1)
      g_pos = random.randint(0, len(individual.chromosomes[c_pos].genes) - 1)
      func = individual.chromosomes[c_pos].genes[g_pos].func
      options = [
        random.randint(-5, 4) + random.random()
        for _ in range(FUNCTIONS[func])
      ]
      individual.chromosomes[c_pos].genes[g_pos].options = options

  def replace_gene(self, individual):
    if random.random() < MUTATION_RATE:
      c_pos = random.randint(0, len(individual.chromosomes) - 1)
      g_pos = random.randint(0, len(individual.chromosomes[c_pos].genes) - 1)
      individual.chromosomes[c_pos].genes[g_pos] = Gene.create_gene()

  def add_gene(self, individual):
    if random.random() < EVOLUTION_RATE:
      individual.chromosomes[
        random.randint(0, len(individual.chromosomes) - 1)
      ].genes.append(Gene.create_gene())

  def remove_gene(self, individual):
    if len(individual.chromosomes) > 1 and random.random() < SUPPRESSION_RATE:
      c_pos = random.randint(0, len(individual.chromosomes) - 1)
      if len(individual.chromosomes[c_pos].genes) > 1:
        g_pos = random.randint(0, len(individual.chromosomes[c_pos].genes) - 1)
        individual.chromosomes[c_pos].genes.pop(g_pos)

  def add_chromosome(self, individual):
    if random.random() < C_EVOLUTION_RATE:
      individual.chromosomes.append(Chromosome([Gene.create_gene()]))

  def remove_chromosome(self, individual):
    if len(individual.chromosomes) > 1 and random.random() < C_SUPPRESSION_RATE:
      individual.chromosomes.pop(
        random.randint(0, len(individual.chromosomes) - 1)
      )
