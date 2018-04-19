from copy import deepcopy
from random import seed
import sys

from conf import GENERATIONS, STARTING_PRIMES_FOR_EVOLUTION
from evolver import Evolver
from logger import Logger
from utils import Utils

def main(argv):
  seed(0)
  formulas = {}
  starting_gen = 0
  primes_for_evaluation = STARTING_PRIMES_FOR_EVOLUTION

  try:
    (
      formulas,
      starting_gen,
      primes_for_evaluation
    ) = Utils.load_formulas_from_file(argv[0])
  except IndexError:
    formulas = Evolver.initialize_formulas(primes_for_evaluation)

  evolver = Evolver(primes_for_evaluation)

  try:
    for generation in range(starting_gen, GENERATIONS):
      Logger.generation(generation)
      safe_copy = deepcopy(formulas)
      formulas = evolver.next_generation(formulas)
      if generation % 5000 == 0:
        Utils.save_formulas_to_file(
          safe_copy,
          generation,
          primes_for_evaluation
        )
  except KeyboardInterrupt:
    Logger.stop_save()

  Utils.save_formulas_to_file(
    safe_copy,
    generation,
    evolver.primes_for_evaluation
  )

if __name__ == "__main__":
  main(sys.argv[1:])
