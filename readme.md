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

