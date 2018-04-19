import random

from conf import (
  C_EVOLUTION_RATE,
  C_SUPPRESSION_RATE,
  EVOLUTION_RATE,
  MUTATION_RATE,
  SMALL_MUTATION_RATE,
  SUPPRESSION_RATE
)

from models.gene import Gene
from models.chromosome import Chromosome
from models.formula import Formula
from models.functions import FUNCTIONS

class Mutator():
  def __init__(self, individual):
    self.individual = individual

  def mutate_individual(self):
    # SMALL_MUTATION_RATE
    self.mutate_gene()
    # MUTATION_RATE
    self.replace_gene()
    # EVOLUTION_RATE
    self.add_gene()
    # SUPPRESSION_RATE
    self.remove_gene()
    # C_EVOLUTION_RATE
    self.add_chromosome()
    # C_SUPPRESSION_RATE
    self.remove_chromosome()

  def mutate_gene(self):
    if random.random() < SMALL_MUTATION_RATE:
      c_pos = random.randint(0, len(self.individual.chromosomes) - 1)
      g_pos = random.randint(
        0,
        len(self.individual.chromosomes[c_pos].genes) - 1
      )
      func = self.individual.chromosomes[c_pos].genes[g_pos].func
      options = [
        random.random() * 10 - 5
        for _ in range(FUNCTIONS[func])
      ]
      self.individual.chromosomes[c_pos].genes[g_pos].options = options

  def replace_gene(self):
    if random.random() < MUTATION_RATE:
      c_pos = random.randint(0, len(self.individual.chromosomes) - 1)
      g_pos = random.randint(
        0,
        len(self.individual.chromosomes[c_pos].genes) - 1
      )
      self.individual.chromosomes[c_pos].genes[g_pos] = Gene.create_gene()

  def add_gene(self):
    if random.random() < EVOLUTION_RATE:
      self.individual.chromosomes[
        random.randint(0, len(self.individual.chromosomes) - 1)
      ].genes.append(Gene.create_gene())

  def remove_gene(self):
    if (
      len(self.individual.chromosomes) > 1
      and random.random() < SUPPRESSION_RATE
    ):
      c_pos = random.randint(0, len(self.individual.chromosomes) - 1)
      if len(self.individual.chromosomes[c_pos].genes) > 1:
        g_pos = random.randint(
          0,
          len(self.individual.chromosomes[c_pos].genes) - 1
        )
        self.individual.chromosomes[c_pos].genes.pop(g_pos)

  def add_chromosome(self):
    if random.random() < C_EVOLUTION_RATE:
      self.individual.chromosomes.append(Chromosome([Gene.create_gene()]))

  def remove_chromosome(self):
    if (
      len(self.individual.chromosomes) > 1
      and random.random() < C_SUPPRESSION_RATE
    ):
      self.individual.chromosomes.pop(
        random.randint(0, len(self.individual.chromosomes) - 1)
      )
