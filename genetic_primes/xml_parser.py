import xml.etree.ElementTree as ET

from .models import functions
from .models.gene import Gene
from .models.chromosome import Chromosome
from .models.formula import Formula

class XmlParser():
  def parse_formulas(self, file_path):
    formulas_el = ET.parse(file_path).getroot()
    generation = int(formulas_el.attrib['generation'])
    primes_for_evaluation = int(formulas_el.attrib['primes_for_evaluation'])
    formulas = {}
    for formula_el in formulas_el:
      formula, evaluation = self.parse_formula(formula_el)
      formulas[formula] = evaluation
    return [formulas, generation, primes_for_evaluation]

  def parse_formula(self, formula_el):
    chromosomes = [
      self.parse_chromosome(chromosome_el)
      for chromosome_el in formula_el
    ]
    return [Formula(chromosomes), float(formula_el.attrib['evaluation'])]

  def parse_chromosome(self, chromosome_el):
    genes = [
      self.parse_gene(gene_el)
      for gene_el in chromosome_el
    ]
    return Chromosome(genes)

  def parse_gene(self, gene_el):
    options = [
      self.parse_option(option_el)
      for option_el in gene_el
    ]
    return Gene(
      getattr(functions, gene_el.attrib['function']),
      options
    )

  def parse_option(self, option_el):
    return float(option_el.attrib['value'])
