package main

import (
	"context"
	"log"

	api_pb "go/api/v1"

	"google.golang.org/grpc"
)

func main() {
	var conn *grpc.ClientConn
	conn, err := grpc.Dial(":50051", grpc.WithInsecure())

	if err != nil {
		log.Fatalf("Could not connect: %s", err)
	}
	defer conn.Close()

	c := api_pb.NewGreeterServiceClient(conn)

	request := api_pb.HelloRequest{
		Name:     "Hello",
		Greeting: "World",
	}

	response, err := c.SayHello(context.Background(), &request)

	if err != nil {
		log.Fatalf("Error when calling SayHello: %s", err)
	}

	log.Printf("Response from Server: %s", response.Message)
}
