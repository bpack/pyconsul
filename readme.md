## pyconsul
A command-line tool for mirroring a file system structure to key-value pairs in consul.

### Execution
This script will traverse any provided paths and use the directory structure as keys in
Consul with the file contents as the values.

```
usage: pyconsul [-d] [-m MOUNTPOINT] [-p PATHS] [-s] [-t TOKEN] [-u URL]
                [-v]

optional arguments:
  -d, --dryrun          Logs the operations that would be performed instead of
                        executing.
  -m MOUNTPOINT, --mountpoint MOUNTPOINT
                        Defines a top level path in Consul where keys will be
                        written.
  -p PATHS, --paths PATHS
                        The paths on the file system to copy to Consul.
  -s, --no-ssl-verify   Skips SSL verification of the Consul URL. Not
                        recommended.
  -t TOKEN, --token TOKEN
                        The authentication token to use with Consul.
  -u URL, --url URL     The base Consul URL to use.
  -v, --verbose         Controls output logging detail. -v for info, -vv for
                        debug.
```

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
