import time
import logging
import asyncio

import grpc
from decouple import config

# messages
from api.v1.greet_pb2 import HelloRequest

# services
from api.v1.greet_pb2_grpc import GreeterServiceStub


async def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")
        if name == "":
            break

        request = HelloRequest(greeting="Hello", name=name)
        yield request
        time.sleep(1)

async def run():
    SERVER_HOST = config("ASYNC_GRPC_SERVER_HOST", cast=str)
    SERVER_PORT = config("ASYNC_GRPC_SERVER_PORT", cast=int)
    SERVER_CRT = config("SSL_SERVER_CRT", cast=str)

    # Enable TSL/SSL for client-server communication
    with open(SERVER_CRT, "rb") as f:
        creds = grpc.ssl_channel_credentials(f.read())

    async with grpc.aio.secure_channel(f"{SERVER_HOST}:{SERVER_PORT}", creds) as channel:
        stub = GreeterServiceStub(channel)

        print("1. SayHello - Unary")
        print("2. ParrotSaysHello - Server Side Streaming")
        print("3. ChattyClientSaysHello - Client Side Streaming")
        print("4. InteractingHello - Both Streaming")
        rpc_call = input("Which rpc would you like to make: ")

        if rpc_call == "1":
            request = HelloRequest(greeting="Bonjour", name="YouTube")
            response = await stub.SayHello(request)

            print("SayHello Response Received:")
            print(response)

        elif rpc_call == "2":
            request = HelloRequest(greeting="Bonjour", name="YouTube")

            # Read stream data from an async generator
            async for response in stub.ParrotSaysHello(request):
                print("ParrotSaysHello Response Received:")
                print(response)

        elif rpc_call == "3":
            delayed_reply = await stub.ChattyClientSaysHello(get_client_stream_requests())

            print("ChattyClientSaysHello Response Received:")
            print(delayed_reply)

        elif rpc_call == "4":
            # Direct read stream data from the stub
            response_stream = stub.InteractingHello(get_client_stream_requests())

            while True:
                response = await response_stream.read()
                if response == grpc.aio.EOF:
                    break
                print("InteractingHello Response Received: ")
                print(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
