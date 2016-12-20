import mock

import dostuff

'''
Some python actions talk to the operating system. While it's impossible to patch the complete
filesystem, it may be deemed necessary to protect the system from actions that may slow tests or
alter state.

In this example, we patch subprocess.Popen but directly in the dostuff namespace. Depending on how
the classes and objects are imported and instantiated, it may be necessary to patch this way.

Rather than have Popen actually open a command line action, we patch Popen which will now return a
mock. The code looks at stdout, so we return a filehandle.
'''


@mock.patch('dostuff.Popen')
def test_count_the_shells(mocked_popen):
  mocked_popen.return_value.stdout = open('testps.out')
  mocked_popen.return_value.wait.return_value = False
  assert dostuff.count_the_shells() == 4
