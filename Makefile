#!make
include .env
export

SHELL := '/bin/bash'

build:
	@buf build --exclude-source-info -o -#format=json | jq '.file[] | .package'

ls:
	@buf ls-files

lint:
	@buf lint

mod_update:
	@buf mod update proto

gen:
	@buf generate

generate: gen
	@cp -rnf ~/go/pkg/mod/github.com/grpc-ecosystem/grpc-gateway@v1.16.0/third_party/googleapis/google src/python

swagger:
	@cd docs && \
	 wget https://github.com/swagger-api/swagger-ui/archive/refs/tags/v$(SWAGGER_VERSION).zip && \
	 unzip v$(SWAGGER_VERSION).zip && \
	 mv swagger-ui-$(SWAGGER_VERSION)/dist ./swagger-ui && \
	 rm -rf swagger-ui-$(SWAGGER_VERSION) && \
	 rm v$(SWAGGER_VERSION).zip

start-swagger-ui:
	@docker-compose up -d
	@echo Check out swagger-ui at http://localhost:${SWAGGER_UI_PORT}

stop-swagger-ui:
	@docker-compose stop
	@echo swagger-ui is stop

remove-swagger-ui:
	@docker-compose down
	@echo swagger-ui removed

ssl:
	@openssl req -config certs/openssl.cnf -newkey rsa:4096 -nodes -sha512 -x509 -days 3650 -nodes -out certs/server.crt -keyout certs/server.key

symlink:
	@cd src/go && ln -nsf ../../.env && ln -nsf ../../certs
	@cd src/js && ln -nsf ../../.env && ln -nsf ../../certs
	@cd src/python && ln -nsf ../../.env && ln -nsf ../../certs
	@echo "Creating symlink done!"

go-deps:
	@cd src/go; bash ../../install_go_deps.sh
	@wget https://github.com/grpc/grpc-web/releases/download/1.3.1/protoc-gen-grpc-web-1.3.1-linux-x86_64 \
		-O ~/.local/bin/protoc-gen-grpc-web-1.3.1-linux-x86_64 \
		&& chmod +x ~/.local/bin/protoc-gen-grpc-web-1.3.1-linux-x86_64

python-deps:
	@cd src/python && pip install -r requirements.txt

system-deps:
	@echo Install OpenSSL
	@sudo apt install -y openssl

	@echo Install Protobuf Compilers
	@sudo apt install -y protobuf-compiler
	@sudo apt install -y protobuf-compiler-grpc
	@echo protoc version:
	@echo $(protoc --version)

	@echo Install Golang
	@wget https://go.dev/dl/go${GOLANG_VERSION}.linux-amd64.tar.gz -O go${GOLANG_VERSION}.linux-amd64.tar.gz
	@sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xvzf go${GOLANG_VERSION}.linux-amd64.tar.gz
	@rm go${GOLANG_VERSION}.linux-amd64.tar.gz
	@export PATH=$PATH:/usr/local/go/bin
	@echo Add `/usr/local/go/bin` into system PATH
	@echo Golang version:
	@echo $(go version)

	@echo Install Buf
	@VERSION="1.6.0" \
		wget "https://github.com/bufbuild/buf/releases/download/v${BUF_VERSION}/buf-`uname -s`-`uname -m`.tar.gz" -O buf.tar.gz
	@sudo tar -xvzf buf.tar.gz -C /usr/local/go --strip-components 1
	@rm buf.tar.gz

deps: system-deps go-deps python-deps
all: deps gen mod_update ssl symlink start-swagger-ui