"""Server handling general file read/write requests."""

import sys
import os
import pickle
# import sys path so that it recognize our submodules
dir_path = os.path.dirname(os.path.realpath(__file__))
pdir = os.path.abspath(dir_path + "/../../")
sys.path.append(pdir)

from df.py_gen import api_pb2
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
# A temporary key/value file to map (path, pb)
_DICT_MAP_FILE = os.getcwd() + "/_dict"

class APIServer(api_pb2.BetaFileAPIServicer):
  def __init__(self, fmapFile=_DICT_MAP_FILE):
    self.fmapFile = fmapFile
    # we accept a dict file to make our unit test more convenient
    # init fmap to be an empty dict
    self.fmap = {}
    # currently load saved info from a pure file
    if os.path.isfile(self.fmapFile):
      with open(self.fmapFile, 'rb') as mfile:
        self.fmap = pickle.loads(mfile.read())

  def Read(self, request, context):
    path = request.path
    response = api_pb2.ReadResponse()

    if not self._Exist(path):
      # return with nothing
      return response

    # load mappings
    response.MergeFromString(self.fmap[path])
    return response

  def Write(self, request, context):
    pass

  def Exist(self, request, context):
    response = api_pb2.ExistResponse()
    response.exists = self._Exist(request.path)
    return response

  def _Exist(self, path):
    """To see if a file/dir already exists"""
    return self.fmap and path in self.fmap

def serve():
  server = api_pb2.beta_create_FileAPI_server(APIServer())
  server.add_insecure_port('[::]:12345')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
