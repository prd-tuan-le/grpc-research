import time
from typing import Iterable

import grpc

# messages
from api.v1.greet_pb2 import HelloRequest
from api.v1.greet_pb2 import HelloResponse
from api.v1.greet_pb2 import DelayedReply

# services
from api.v1.greet_pb2_grpc import GreeterServiceServicer


class GreeterServiceServicer(GreeterServiceServicer):
    async def SayHello(self, request: HelloRequest, context: grpc.aio.ServicerContext) -> HelloResponse:
        print("SayHello Request Made:")
        print(request)

        response = HelloResponse()
        response.message = f"{request.greeting} {request.name}"  # type: ignore
        return response

    async def ParrotSaysHello(self, request: HelloRequest, context: grpc.aio.ServicerContext):
        print("ParrotSaysHello Request Made:")
        print(request)

        for i in range(3):
            response = HelloResponse()
            response.message = f"{request.greeting} {request.name} {i + 1}"  # type: ignore
            yield response
            time.sleep(3)

    async def ChattyClientSaysHello(self, request_iterator, context: grpc.aio.ServicerContext):
        delayed_reply = DelayedReply()
        async for request in request_iterator:
            print("ChattyClientSaysHello Request Made:")
            print(request)
            delayed_reply.request.append(request)  # type: ignore

        delayed_reply.message = (  # type: ignore
            f"You have sent {len(delayed_reply.request)} messages." "Please expect a delayed response."  # type: ignore
        )
        return delayed_reply

    async def InteractingHello(self, request_iterator, context: grpc.aio.ServicerContext):
        async for request in request_iterator:
            print("InteractingHello Request Made:")
            print(request)

            hello_response = HelloResponse()
            hello_response.message = f"{request.greeting} {request.name}"  # type: ignore

            yield hello_response
