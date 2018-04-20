import os
import time
from xml.dom import minidom

from .xml_builder import XmlBuilder
from .xml_parser import XmlParser

def load_formulas_from_file(file_path):
  return XmlParser().parse_formulas(file_path)

def save_formulas_to_file(formulas, generation, primes_for_evaluation):
  if type(formulas) == type([]):
    formulas = dict(formulas)
  _write_xml_to_file(
    minidom.parseString(
      XmlBuilder().build_formulas_element(
        formulas,
        generation,
        primes_for_evaluation
      )
    ).toprettyxml(indent='  ')
  )

def _write_xml_to_file(xml_string):
  dir_path = os.path.join(os.getcwd(), 'results')
  if not os.path.isdir(dir_path):
    os.makedirs(dir_path)
  f = open(
    os.path.join(
      dir_path,
      str(int(time.time())) + '.xml'
    ),
    'w+'
  )
  f.write(xml_string)
  f.close()
