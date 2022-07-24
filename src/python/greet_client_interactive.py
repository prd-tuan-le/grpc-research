import time
from typing import Iterable

import grpc
from decouple import config

from api.v1.greet_pb2 import HelloRequest
from api.v1.greet_pb2_grpc import GreeterServiceStub


def get_client_stream_requests() -> Iterable[HelloRequest]:
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")

        if name == "":
            break

        hello_request = HelloRequest(greeting="Hello", name=name)
        yield hello_request
        time.sleep(1)


def run():
    SERVER_HOST = config("GRPC_SERVER_HOST", cast=str)
    SERVER_PORT = config("GRPC_SERVER_PORT", cast=int)
    SERVER_CRT = config("SSL_SERVER_CRT", cast=str)

    # Enable TSL/SSL for client-server communication
    with open(SERVER_CRT, "rb") as f:
        creds = grpc.ssl_channel_credentials(f.read())

    with grpc.secure_channel(f"{SERVER_HOST}:{SERVER_PORT}", creds) as channel:
        # Unary asynchronous
        # https://github.com/grpc/grpc/issues/16329#issuecomment-412286997
        stub = GreeterServiceStub(channel)

        print("1. SayHello - Unary")
        print("2. ParrotSaysHello - Server Side Streaming")
        print("3. ChattyClientSaysHello - Client Side Streaming")
        print("4. InteractingHello - Both Streaming")
        rpc_call = input("Which rpc would you like to make: ")

        if rpc_call == "1":
            hello_request = HelloRequest(greeting="Bonjour", name="YouTube")
            hello_reply = stub.SayHello(hello_request)
            print("SayHello Response Received:")
            print(hello_reply)

        elif rpc_call == "2":
            hello_request = HelloRequest(greeting="Bonjour", name="YouTube")
            hello_replies = stub.ParrotSaysHello(hello_request)

            for hello_reply in hello_replies:
                print("ParrotSaysHello Response Received:")
                print(hello_reply)

        elif rpc_call == "3":
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())

            print("ChattyClientSaysHello Response Received:")
            print(delayed_reply)

        elif rpc_call == "4":
            responses = stub.InteractingHello(get_client_stream_requests())

            for response in responses:
                print("InteractingHello Response Received: ")
                print(response)


if __name__ == "__main__":
    run()
