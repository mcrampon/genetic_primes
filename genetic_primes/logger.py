from .conf import PRIMES

class Logger():
  @staticmethod
  def generation(generation, primes_for_evaluation):
    goal = 1 * sum(PRIMES[:primes_for_evaluation]) / 100.0
    if generation % 100 == 0:
      print("GENERATION: " + str(generation))
      print("GOAL: " + str(goal))

  @staticmethod
  def stop_save():
    print("STOPPED")
    print("SAVING")

  @staticmethod
  def best_formula(formulas):
    print(formulas[0][1])

  @staticmethod
  def primes_for_evaluation(value):
    print("PRIMES FOR EVAL: " + str(value))
