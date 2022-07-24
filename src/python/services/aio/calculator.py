import logging

import grpc

from api.v1.calculator_pb2 import ComputeRequest
from api.v1.calculator_pb2 import ComputeResponse
from api.v1.calculator_pb2_grpc import CalculatorServiceServicer


class CalculatorServiceServicer(CalculatorServiceServicer):
    async def Sum(self, request: ComputeRequest, context: grpc.aio.ServicerContext) -> ComputeResponse:
        logging.info("Sum Request Made:")
        logging.info(request)

        compute_response = ComputeResponse()
        compute_response.result = request.num1 + request.num2  # type: ignore

        logging.info(f"Sum: {compute_response}")
        return compute_response

    async def Sub(self, request: ComputeRequest, context: grpc.aio.ServicerContext) -> ComputeResponse:
        logging.info("Sub Request Made:")
        logging.info(request)

        compute_response = ComputeResponse()
        compute_response.result = request.num1 - request.num2  # type: ignore

        logging.info(f"Sub: {compute_response}")
        return compute_response

    async def Div(self, request: ComputeRequest, context: grpc.aio.ServicerContext) -> ComputeResponse:
        logging.info("Div Request Made:")
        logging.info(request)

        compute_response = ComputeResponse()
        compute_response.result = request.num1 / request.num2  # type: ignore

        logging.info(f"Div: {compute_response}")
        return compute_response

    async def Mul(self, request: ComputeRequest, context: grpc.aio.ServicerContext) -> ComputeResponse:
        logging.info("Mul Request Made:")
        logging.info(request)

        compute_response = ComputeResponse()
        compute_response.result = request.num1 * request.num2  # type: ignore

        logging.info(f"Mul: {compute_response}")
        return compute_response
