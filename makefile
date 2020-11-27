OWNER ?= bpack
REPO ?= pyconsul
VERSION ?= latest

docker.build:
	docker build -t $(OWNER)/$(REPO):$(VERSION) .

docker.run: docker.build
	docker run $(OWNER)/$(REPO)

consul:
	docker run -d -p 8500:8500 \
		-p 8600:8600/udp \
		--name=consul \
		-e CONSUL_LOCAL_CONFIG='{ "acl": { "enabled": true, "default_policy": "deny", "down_policy": "extend-cache" }}' \
		consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

.PHONY: docker.build clean docker.run
