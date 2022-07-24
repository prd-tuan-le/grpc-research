import asyncio
import logging

import grpc
from decouple import config

from api.v1.greet_pb2_grpc import add_GreeterServiceServicer_to_server
from api.v1.calculator_pb2_grpc import add_CalculatorServiceServicer_to_server

from services.aio.greet import GreeterServiceServicer
from services.aio.calculator import CalculatorServiceServicer

async def serve():
    SERVER_PORT = config("ASYNC_GRPC_SERVER_PORT", cast=int)
    SERVER_KEY = config("SSL_SERVER_KEY", cast=str)
    SERVER_CRT = config("SSL_SERVER_CRT", cast=str)

    server = grpc.aio.server()

    add_GreeterServiceServicer_to_server(GreeterServiceServicer(), server)
    add_CalculatorServiceServicer_to_server(CalculatorServiceServicer(), server)

    # TSL/SSL Authentication
    with open(SERVER_KEY, "rb") as f:
        private_key = f.read()
    with open(SERVER_CRT, "rb") as f:
        certificate_chain = f.read()

    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))

    # Bind the server to the defined port with TLS/SSL certs above
    server.add_secure_port(f"[::]:{SERVER_PORT}", server_credentials)

    logging.info(f"Serving gRPC on 0.0.0.0:{SERVER_PORT}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
