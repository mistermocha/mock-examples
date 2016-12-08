import pytest
import mock

import dostuff

@pytest.fixture
def mocked_200_request():
  mocked_req_obj = mock.Mock()
  mocked_req_obj.status_code = 200
  return mocked_req_obj

@pytest.fixture
def mocked_400_request():
  mocked_req_obj = mock.Mock()
  mocked_req_obj.status_code = 400
  return mocked_req_obj

@mock.patch('requests.get', autospec=True)
def test_get_example_passing(mocked_get, mocked_200_request):
  mocked_get.return_value = mocked_200_request
  assert dostuff.get_example()

@mock.patch('requests.get', autospec=True)
def test_get_example_failing(mocked_get, mocked_400_request):
  mocked_get.return_value = mocked_400_request
  assert not dostuff.get_example()


