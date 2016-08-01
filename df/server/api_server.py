"""Server handling general file read/write requests."""

import sys
import os
# import sys path so that it recognize our submodules
pdir = os.path.abspath(os.getcwd() + "/../")
sys.path.append(pdir)

import api_pb2
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class APIServer(api_pb2.BetaFileAPIServicer):

  def Read(self, request, context):
    pass

  def Write(self, request, context):
    pass

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
