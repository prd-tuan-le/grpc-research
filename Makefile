SWAGGER_VERSION := 4.13.0

build:
	@buf build --exclude-source-info -o -#format=json | jq '.file[] | .package'

ls:
	@buf ls-files

lint:
	@buf lint

mod_update:
	@buf mod update proto

python-deps:
	@cd src/python && pip install -r requirements.txt

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

swagger-ui:
	@docker-compose up -d

deps:
	@cd src/go; bash ../../install_go_deps.sh
	@wget https://github.com/grpc/grpc-web/releases/download/1.3.1/protoc-gen-grpc-web-1.3.1-linux-x86_64 \
		-O ~/.local/bin/protoc-gen-grpc-web-1.3.1-linux-x86_64 \
		&& chmod +x ~/.local/bin/protoc-gen-grpc-web-1.3.1-linux-x86_64

ssl:
	@openssl req -config certs/openssl.cnf -newkey rsa:4096 -nodes -sha512 -x509 -days 3650 -nodes -out certs/server.crt -keyout certs/server.key

symlink:
	@cd src/go && ln -nsf ../../.env && ln -nsf ../../certs
	@cd src/js && ln -nsf ../../.env && ln -nsf ../../certs
	@cd src/python && ln -nsf ../../.env && ln -nsf ../../certs
	@echo "Creating symlink done!"