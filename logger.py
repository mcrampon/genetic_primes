class Logger():
  @staticmethod
  def generation(generation):
    if generation % 100 == 0:
      print("GENERATION: " + str(generation))

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
