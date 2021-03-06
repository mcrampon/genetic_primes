import copy
import random

from .conf import POPULATION_SIZE, PRIMES

from .logger import Logger
from .models.gene import Gene
from .models.chromosome import Chromosome
from .models.formula import Formula
from .mutator import Mutator

class Evolver():
  @staticmethod
  def initialize_formulas(primes_for_evaluation):
    formulas = {}
    for _ in range(POPULATION_SIZE):
      chromosome = Chromosome([Gene.create_gene()])
      formula = Formula([chromosome])
      formulas[formula] = formula.evaluate(PRIMES[:primes_for_evaluation])
    return formulas

  def __init__(self, primes_for_evaluation):
    self.primes_for_evaluation = primes_for_evaluation

  def next_generation(self, formulas):
    new_formulas = {}
    while len(formulas) > 1:
      father = random.choice(list(formulas.keys()))
      new_formulas[father] = formulas.pop(father)
      mother = random.choice(list(formulas.keys()))
      new_formulas[mother] = formulas.pop(mother)
      # Reproduction
      if len(father.chromosomes) != len(mother.chromosomes):
        # individuals of different species cannot reproduce. So sad!
        continue
      child1, child2 = self._create_children(father, mother)

      for child in (child1, child2):
        Mutator(child).mutate_individual()
        new_formulas[child] = child.evaluate(
          PRIMES[:self.primes_for_evaluation]
        )

    # Selection
    formulas = self._select_formulas(new_formulas)
    Logger.best_formula(formulas)

    # Modify environment
    next_primes = self._next_primes_for_evaluation(formulas)
    if next_primes != self.primes_for_evaluation:
      Logger.primes_for_evaluation(next_primes)
      self.primes_for_evaluation = next_primes
      formulas = self._evaluate_formulas(formulas)

    return dict(formulas)

  def _select_formulas(self, formulas):
    return sorted(
      formulas.items(),
      key=lambda formula: formula[1]
    )[:POPULATION_SIZE]

  def _evaluate_formulas(self, formulas):
    return sorted(
      [
        [formula[0], formula[0].evaluate(PRIMES[:self.primes_for_evaluation])]
        for formula in formulas
      ],
      key=lambda formula: formula[1]
    )

  def _create_children(self, father, mother):
    child1 = Formula([])
    child2 = Formula([])
    for c_index in range(len(father.chromosomes)):
      if random.random() < 0.5:
        child1.chromosomes.append(copy.deepcopy(father.chromosomes[c_index]))
        child2.chromosomes.append(copy.deepcopy(mother.chromosomes[c_index]))
      else:
        child2.chromosomes.append(copy.deepcopy(father.chromosomes[c_index]))
        child1.chromosomes.append(copy.deepcopy(mother.chromosomes[c_index]))
    return [child1, child2]

  def _next_primes_for_evaluation(self, formulas):
    if formulas[0][1] < self._threshold():
      return min(self.primes_for_evaluation + 1, 10**4)
    else:
      return self.primes_for_evaluation

  def _threshold(self):
    if self.primes_for_evaluation < 100:
      return 1.0 * sum(PRIMES[:self.primes_for_evaluation]) / 100
    else:
      return (
        1.0 * sum(PRIMES[:self.primes_for_evaluation]) /
        self.primes_for_evaluation
      )
