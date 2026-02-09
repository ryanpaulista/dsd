#!/bin/bash
# Gera os arquivos Python a partir do .proto

cd "$(dirname "$0")"

python -m grpc_tools.protoc \
    -I../proto \
    --python_out=. \
    --grpc_python_out=. \
    ../proto/chat.proto

echo "✅ Arquivos gerados: chat_pb2.py e chat_pb2_grpc.py"
