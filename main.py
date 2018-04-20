from copy import deepcopy
from random import seed

from genetic_primes.conf import GENERATIONS, STARTING_PRIMES_FOR_EVOLUTION
from genetic_primes.evolver import Evolver
from genetic_primes.logger import Logger
from genetic_primes.utils import Utils

def main(path_to_save_file=None):
  seed(0)
  formulas = {}
  starting_gen = 0
  primes_for_evaluation = STARTING_PRIMES_FOR_EVOLUTION

  if path_to_save_file is None:
    formulas = Evolver.initialize_formulas(primes_for_evaluation)
  else:
    (
      formulas,
      starting_gen,
      primes_for_evaluation
    ) = Utils.load_formulas_from_file(path_to_save_file)

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
  import sys
  if len(sys.argv[1:]) > 0:
    main(sys.argv[1:][0])
  else:
    main()
