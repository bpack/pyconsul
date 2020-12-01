OWNER ?= bpack
REPO ?= pyconsul
VERSION ?= latest

clean:
	docker rm testconsul
	docker rmi $(OWNER)/$(REPO)

docker.build:
	docker build -t $(OWNER)/$(REPO):$(VERSION) .

docker.run: docker.build
	docker run $(OWNER)/$(REPO)

docker.stop:
	docker stop testconsul

docker.push: docker.build
	docker login -u $(OWNER)
	docker push $(OWNER)/$(REPO):$(VERSION)

consul:
	docker run -d -p 8500:8500 \
		-p 8600:8600/udp \
		--name=testconsul \
		-e CONSUL_LOCAL_CONFIG='{ "acl": { "enabled": true, "default_policy": "deny", "down_policy": "extend-cache" }}' \
		consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

.PHONY: docker.build clean docker.run docker.push consul
