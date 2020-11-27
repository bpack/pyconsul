## pyconsul
A command-line tool for mirroring a file system structure to key-value pairs in consul.

### Notes to Self
Install and run locally.

```
pipenv shell
pipenv install --dev
pipenv install -e .

pipenv run pyconsul -vv --dryrun --paths $PYCONSUL_TEST_PATH --token ABCDE-12345 --url http://localhost

pipenv run pytest
```

Testing with consul locally
```
make consul

docker exec consul-test consul acl bootstrap
# capture secretID
# export CONSUL_HTTP_TOKEN=...

docker exec -e CONSUL_HTTP_TOKEN=... consul consul members

docker run -v `pwd`/test/data:/consul/data --link consul -e CONSUL_TOKEN=$CONSUL_HTTP_TOKEN bpack/pyconsul -vv --url http://consul:8500 --paths /consul/data

```
