import copy
import random

import genetic_primes.utils as utils

from genetic_primes.conf import GENERATIONS, STARTING_PRIMES_FOR_EVALUATION
from genetic_primes.evolver import Evolver
from genetic_primes.logger import Logger

def main(path_to_save_file=None):
  random.seed(0)
  formulas = {}
  starting_gen = 0
  primes_for_evaluation = STARTING_PRIMES_FOR_EVALUATION

  if path_to_save_file is None:
    formulas = Evolver.initialize_formulas(primes_for_evaluation)
  else:
    (
      formulas,
      starting_gen,
      primes_for_evaluation
    ) = utils.load_formulas_from_file(path_to_save_file)

  evolver = Evolver(primes_for_evaluation)

  try:
    for generation in range(starting_gen, GENERATIONS):
      Logger.generation(generation)
      safe_copy = copy.deepcopy(formulas)
      formulas = evolver.next_generation(formulas)
      if generation % 5000 == 0:
        utils.save_formulas_to_file(
          safe_copy,
          generation,
          primes_for_evaluation
        )
  except KeyboardInterrupt:
    Logger.stop_save()

  utils.save_formulas_to_file(
    safe_copy,
    generation,
    evolver.primes_for_evaluation
  )

if __name__ == "__main__":
  import sys
  if len(sys.argv[1:]) > 0:
    main(sys.argv[1:][0])
  else:
    main()
