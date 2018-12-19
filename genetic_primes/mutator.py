import random

from .conf import (
  C_EVOLUTION_RATE,
  C_SUPPRESSION_RATE,
  EVOLUTION_RATE,
  MUTATION_RATE,
  SMALL_MUTATION_RATE,
  SUPPRESSION_RATE,
  COMPLETE_OVERRIDE_RATE
)

from .models.gene import Gene
from .models.chromosome import Chromosome
from .models.formula import Formula
from .models.functions import FUNCTIONS

class Mutator():
  def __init__(self, individual):
    self.individual = individual

  def mutate_individual(self):
    # SMALL_MUTATION_RATE
    self._mutate_gene()
    # MUTATION_RATE
    self._replace_gene()
    # EVOLUTION_RATE
    self._add_gene()
    # SUPPRESSION_RATE
    self._remove_gene()
    # C_EVOLUTION_RATE
    self._add_chromosome()
    # C_SUPPRESSION_RATE
    self._remove_chromosome()
    # COMPLETE_OVERRIDE_RATE
    self._complete_override()

  def _mutate_gene(self):
    if random.random() < SMALL_MUTATION_RATE:
      c_index = random.randint(0, len(self.individual.chromosomes) - 1)
      g_index = random.randint(
        0,
        len(self.individual.chromosomes[c_index].genes) - 1
      )
      func = self.individual.chromosomes[c_index].genes[g_index].func
      options = [
        random.random() * 10 - 5
        for _ in range(FUNCTIONS[func])
      ]
      self.individual.chromosomes[c_index].genes[g_index].options = options

  def _replace_gene(self):
    if random.random() < MUTATION_RATE:
      c_index = random.randint(0, len(self.individual.chromosomes) - 1)
      g_index = random.randint(
        0,
        len(self.individual.chromosomes[c_index].genes) - 1
      )
      self.individual.chromosomes[c_index].genes[g_index] = Gene.create_gene()

  def _add_gene(self):
    if random.random() < EVOLUTION_RATE:
      self.individual.chromosomes[
        random.randint(0, len(self.individual.chromosomes) - 1)
      ].genes.append(Gene.create_gene())

  def _remove_gene(self):
    if (
      len(self.individual.chromosomes) > 1
      and random.random() < SUPPRESSION_RATE
    ):
      c_index = random.randint(0, len(self.individual.chromosomes) - 1)
      if len(self.individual.chromosomes[c_index].genes) > 1:
        g_index = random.randint(
          0,
          len(self.individual.chromosomes[c_index].genes) - 1
        )
        self.individual.chromosomes[c_index].genes.pop(g_index)

  def _add_chromosome(self):
    if random.random() < C_EVOLUTION_RATE:
      self.individual.chromosomes.append(Chromosome([Gene.create_gene()]))

  def _remove_chromosome(self):
    if (
      len(self.individual.chromosomes) > 1
      and random.random() < C_SUPPRESSION_RATE
    ):
      self.individual.chromosomes.pop(
        random.randint(0, len(self.individual.chromosomes) - 1)
      )

  def _complete_override(self):
    if (random.random() < COMPLETE_OVERRIDE_RATE):
      self.individual.chromosomes = [
        Chromosome([
          Gene.create_gene() for gene in chromosome.genes
        ]) for chromosome in self.individual.chromosomes
      ]
