import time

import api.v1.greet_pb2 as greet_pb2
import api.v1.greet_pb2_grpc as greet_pb2_grpc


class GreeterServiceServicer(greet_pb2_grpc.GreeterServiceServicer):
    def SayHello(self, request, context):
        print("SayHello Request Made:")
        print(request)
        hello_response = greet_pb2.HelloResponse()
        hello_response.message = f"{request.greeting} {request.name}"  # type: ignore
        return hello_response

    def ParrotSaysHello(self, request, context):
        print("ParrotSaysHello Request Made:")
        print(request)

        for i in range(3):
            hello_response = greet_pb2.HelloResponse()
            hello_response.message = f"{request.greeting} {request.name} {i + 1}"  # type: ignore
            yield hello_response
            time.sleep(3)

    def ChattyClientSaysHello(self, request_iterator, context):
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print("ChattyClientSaysHello Request Made:")
            print(request)
            delayed_reply.request.append(request)  # type: ignore

        delayed_reply.message = (  # type: ignore
            f"You have sent {len(delayed_reply.request)} messages."  # type: ignore
            "Please expect a delayed response."
        )
        return delayed_reply

    def InteractingHello(self, request_iterator, context):
        for request in request_iterator:
            print("InteractingHello Request Made:")
            print(request)

            hello_response = greet_pb2.HelloResponse()
            hello_response.message = f"{request.greeting} {request.name}"  # type: ignore

            yield hello_response
