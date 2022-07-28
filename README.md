# GRPC Demo

```bash
# Install System Dependencies
make system-deps

# Install Go Dependencies
make go-deps

# Install Python Dependencies
make python-deps

# Create OpenSSL Certificate
make ssl

# Update go.mod
make mod_update

# Generate GRPC / GRPC-gateway / GRPC-web from .proto
make gen

# Start GRPC Server
cd src/python && python server.py

# Start Async GRPC Server
cd src/python && python server_async.py

# Start Go Server with grpc-gateway
cd src/go &&& go run server.go

# Add
# {
#    ...
#    "host": "localhost:8090",
#    ...
# }
# into docs/swagger/api/v1/*.swagger.json
# Then start Swagger UI
make start-swagger-ui
```