import unittest
import sys
import os
import pickle

# import sys path so that it recognize our submodules
dir_path = os.path.dirname(os.path.realpath(__file__))
pdir = os.path.abspath(dir_path + "/../")
sys.path.append(pdir)

from df.py_gen import api_pb2
from df.server import api_server

_TEST_DICT_MAP_FILE = os.getcwd() + "/_dict_test"

class TestAPIServer(unittest.TestCase):

  def setUp(self):
    # we construct a simple test dict file
    response = api_pb2.ReadResponse()
    chunk1 = response.chunks.add()
    chunk1.fqdn = 'localhost:54321'
    chunk1.seq = 1
    chunk1.bytesize = 302291
    chunk1.path = os.getcwd() + '/thenightwatch.pdf'

    fmap = {}
    fmap['/thenightwatch.pdf'] = response.SerializeToString()

    # dump pickle to test dict file
    with open(_TEST_DICT_MAP_FILE, 'wb') as mfile:
      pickle.dump(fmap, mfile)

    self.Server = api_server.APIServer(_TEST_DICT_MAP_FILE)

  def test_read_exists_one_chunk(self):
    request = api_pb2.ReadRequest()
    request.path = '/thenightwatch.pdf'

    response = self.Server.Read(request, None)
    assert response is not None
    assert len(response.chunks) == 1
    chunk = response.chunks[0]
    assert chunk.fqdn == 'localhost:54321'
    assert chunk.seq == 1
    assert chunk.bytesize == 302291
    assert chunk.path == os.getcwd() + '/thenightwatch.pdf'

  def test_read_non_exists(self):
    request = api_pb2.ReadRequest()
    request.path = '/thelightwatch.pdf'

    response = self.Server.Read(request, None)
    print response

if __name__ == '__main__':
  unittest.main()
