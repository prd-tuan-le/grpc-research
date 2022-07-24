import logging
from concurrent import futures

import grpc
from decouple import config

from api.v1.greet_pb2_grpc import add_GreeterServiceServicer_to_server
from api.v1.calculator_pb2_grpc import add_CalculatorServiceServicer_to_server

from services.greet import GreeterServiceServicer
from services.calculator import CalculatorServiceServicer


def serve():
    SERVER_PORT = config("GRPC_SERVER_PORT", cast=int)
    SERVER_KEY = config("SSL_SERVER_KEY", cast=str)
    SERVER_CRT = config("SSL_SERVER_CRT", cast=str)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

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

    print(f"Serving gRPC on 0.0.0.0:{SERVER_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
