import pytest
import mock

import dostuff

@mock.patch('dostuff.Popen')
def test_count_the_shells(mocked_popen):
  mocked_popen.return_value.stdout = open('testps.out')
  mocked_popen.return_value.wait.return_value = False
  assert dostuff.count_the_shells() == 4
