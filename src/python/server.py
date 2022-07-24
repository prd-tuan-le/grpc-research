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

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    add_GreeterServiceServicer_to_server(GreeterServiceServicer(), server)
    add_CalculatorServiceServicer_to_server(CalculatorServiceServicer(), server)

    server.add_insecure_port(f"[::]:{SERVER_PORT}")

    print(f"Serving gRPC on 0.0.0.0:{SERVER_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
