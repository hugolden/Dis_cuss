#!/bin/sh
protoc -I ./protos/ --python_out=./py_gen/ --grpc_out=./py_gen/ --plugin=protoc-gen-grpc=`which grpc_python_plugin` protos/*/*.proto protos/*.proto
