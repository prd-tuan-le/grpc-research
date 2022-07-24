import api.v1.calculator_pb2 as calculator_pb2
import api.v1.calculator_pb2_grpc as calculator_pb2_grpc


class CalculatorServiceServicer(calculator_pb2_grpc.CalculatorServiceServicer):
    def Sum(self, request, context):
        print("Sum Request Made:")
        print(request)

        compute_response = calculator_pb2.ComputeResponse()
        compute_response.result = request.num1 + request.num2  # type: ignore

        print("Sum:", compute_response)
        return compute_response

    def Sub(self, request, context):
        print("Sub Request Made:")
        print(request)

        compute_response = calculator_pb2.ComputeResponse()
        compute_response.result = request.num1 - request.num2  # type: ignore

        print("Sub:", compute_response)
        return compute_response

    def Div(self, request, context):
        print("Div Request Made:")
        print(request)

        compute_response = calculator_pb2.ComputeResponse()
        compute_response.result = request.num1 / request.num2  # type: ignore

        print("Div:", compute_response)
        return compute_response

    def Mul(self, request, context):
        print("Mul Request Made:")
        print(request)

        compute_response = calculator_pb2.ComputeResponse()
        compute_response.result = request.num1 * request.num2  # type: ignore

        print("Mul:", compute_response)
        return compute_response
