import json
import os

conf = json.loads(
  open(
    os.path.join(
      os.getcwd(),
      'genetic_primes',
      'conf.json'
    ),
    'r'
  ).read()
)

POPULATION_SIZE = conf['population_size']
GENERATIONS = conf['generations']
SMALL_MUTATION_RATE = conf['small_mutation_rate']
MUTATION_RATE = conf['mutation_rate']
EVOLUTION_RATE = conf['evolution_rate']
SUPPRESSION_RATE = conf['suppression_rate']
C_EVOLUTION_RATE = conf['c_evolution_rate']
C_SUPPRESSION_RATE = conf['c_suppression_rate']
STARTING_PRIMES_FOR_EVOLUTION = conf['starting_primes_for_evolution']
PRIMES = conf['primes']