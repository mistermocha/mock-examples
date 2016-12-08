import requests
from subprocess import Popen, PIPE

def get_example():
  r = requests.get('http://example.com/')
  if r.status_code == 200:
    return True
  else:
    return False

def count_the_shells():
  p = Popen(['ps', '-a'], stdout=PIPE, stderr=PIPE)
  if p.wait():
    raise Exception('We had a fail')
  count = 0
  for proc in p.stdout.readlines():
    if "-bash" in proc:
       count += 1
  return count


class Gobbler(object):
  __gobblecounter__ = 0
  __name__ = "Default Gobbler"

  def __init__(self, name=None):
    if name:
      self.__name__ = name

  def simplefunc(self):
    return "I am a simple function in {}".format(self.__name__)

  def func_with_args(self, foo, bar):
    return "In the base class {} you passed me foo: {} and bar: {}".format(self.__name__, foo, bar)

  def gobble(self, thing):
    self.__gobblecounter__ += 1
    return "gobbled {}".format(thing)

  def gobble_many(self, args):
    things_gobbled = []
    for arg in args:
      returned = self.gobble(arg)
      things_gobbled.append(returned)
    return things_gobbled

  def gobble_sentence(self, sentence):
    words = sentence.split()
    gobbled = self.gobble_many(words)
    return gobbled

class Devourer(Gobbler):
  def gobble(self, thing):
    self.__gobblecounter__ += 1
    return "devoured {}".format(thing)

  def devourer(self, thing):
    return self.gobble(thing)
