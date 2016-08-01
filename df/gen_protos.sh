#!/bin/sh
protoc -I ./protos/ --python_out=./ --grpc_out=./ --plugin=protoc-gen-grpc=`which grpc_python_plugin` protos/*/*.proto
