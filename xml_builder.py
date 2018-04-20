import xml.etree.ElementTree as ET

class XmlBuilder():
  def build_formulas_element(self, formulas, generation, primes_for_evaluation):
    formulas_el = ET.Element(
      'Formulas',
      {
        'generation' : str(generation),
        'primes_for_evaluation': str(primes_for_evaluation)
      }
    )
    for formula, evaluation in formulas.items():
      self.build_formula_element(formulas_el, formula, evaluation)
    return ET.tostring(formulas_el, encoding='utf8', method='xml')

  def build_formula_element(self, formulas_el, formula, evaluation):
    formula_el = ET.SubElement(
      formulas_el,
      'Formula',
      { 'evaluation': str(evaluation) }
    )
    for chromosome in formula.chromosomes:
      self.build_chromosome_element(formula_el, chromosome)

  def build_chromosome_element(self, formula_el, chromosome):
    chromosome_el = ET.SubElement(formula_el, 'Chromosome')
    for gene in chromosome.genes:
      self.build_gene_element(chromosome_el, gene)

  def build_gene_element(self, chromosome_el, gene):
    gene_el = ET.SubElement(
      chromosome_el,
      'Gene',
      { 'function': gene.func.__name__ }
    )
    for option in gene.options:
      ET.SubElement(gene_el, 'Option', { 'value': str(option) })
