import mock

import dostuff

'''
Instantiating a mock is as easy as mock.Mock(). Adding fields and behaviors can then be done to the
mocked object.

Implementing return_value in a mock object makes the mock return that thing when it's executed.

In the examples here, we patch requests.get to be a mock object, create additional mock objects with
status_codes, and then assign those mocks to be the return value in pytest.
'''


@mock.patch('requests.get', autospec=True)
def test_get_example_passing(mocked_get):
  mocked_req_obj = mock.Mock()
  mocked_req_obj.status_code = 200
  mocked_get.return_value = mocked_req_obj
  assert dostuff.get_example()
  assert mocked_get.called


'''
The default item returned from any mock object reference that isn't already declared is another mock
object. The default object returned by return_value is another mock. Instead of declaring a mock,
another method is to just directly assign properties to return_value.
'''

@mock.patch('requests.get', autospec=True)
def test_get_example_failing(mocked_get):
  mocked_get.return_value.status_code = 400
  assert not dostuff.get_example()
  assert mocked_get.called
