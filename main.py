from copy import deepcopy
from random import seed
import sys

from conf import GENERATIONS
from evolver import Evolver
from logger import Logger
from utils import Utils

def main(argv):
  seed(0)
  evolver = Evolver()

  formulas = {}
  starting_gen = 0

  try:
    formulas, starting_gen = Utils.load_formulas_from_file(argv[0])
  except:
    formulas = evolver.initialize_formulas()

  try:
    for generation in range(starting_gen, GENERATIONS):
      Logger.generation(generation)
      safe_copy = deepcopy(formulas)
      formulas = evolver.next_generation(formulas)
  except KeyboardInterrupt:
    Logger.stop_save()
    Utils.save_formulas_to_file(safe_copy, generation)

if __name__ == "__main__":
    main(sys.argv[1:])
