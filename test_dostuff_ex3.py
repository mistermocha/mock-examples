import mock
import pytest

from dostuff import Gobbler

def test_gobbler_init():
  _gobbler = Gobbler()
  assert _gobbler.__gobblecounter__ == 0
  assert _gobbler.__name__ == "Default Gobbler"


### Use of a patch decorator
@mock.patch('dostuff.Gobbler.simplefunc')
def test_gobbler_simple(patched_simple):
  '''
  A patch decorator - the namespace in the first argument of mock.patch() gets replaced with a
  mock() object, and then the reference to that object is passed in as an argument to the test
  function. This permits operations on the mock object.

  return_value sets the value returned when the given item is called as a function.
  '''
  patched_value = "This is a patched value"
  patched_simple.return_value = patched_value
  _gobbler = Gobbler()
  assert _gobbler.simplefunc() == patched_value

  '''
  Calls to the mock get tracked.

  called() returns boolean if the function has been called
  call_args() returns a "call" object with the last used arguments
  '''
  assert patched_simple.called
  assert patched_simple.call_args == mock.call()


@pytest.fixture
def gobbler():
  return Gobbler()


def test_gobbler_gobble(gobbler):
  assert gobbler.gobble("foo") == "gobbled foo"


### Directly modifying an object with a mock
def test_gobbler_many(gobbler):
  '''
  Instantiating a mock and patching a live object can be done directly too, as needed. In this case,
  we want to persist the instantiated object, but only mock an underlying function. To do this, we
  replace the "gobble" function with a mock object and fake the "gobble" function. If there's a case
  of a function being expensive, or there's a change of external state that we want to prohibit when
  testing, this is when you might replace something.

  In this example, we use a side_effect. Using return_value gives back a static return value, but
  side_effect can be written in as a proper function. This gets executed when the mock is executed.

  The change becomes a namespace change, so the self reference gets dropped.
  '''
  def fake_gobble(string):
      return "fake gobble {}".format(string)

  patch_gobble = mock.Mock()
  patch_gobble.side_effect = fake_gobble
  gobbler.gobble = patch_gobble

  assert gobbler.gobble_many(["foo", "bar", "baz"]) == [
    "fake gobble foo",
    "fake gobble bar",
    "fake gobble baz",
  ]
  assert gobbler.gobble_sentence("this is a test") == [
    "fake gobble this",
    "fake gobble is",
    "fake gobble a",
    "fake gobble test",
  ]
  assert patch_gobble.call_count == 7
