# remote-cmder

## Prerequisites

### Deps:

```shell
poetry install
```

### pre-commit

```shell
pre-commit install --install-hooks
# or
pre-commit autoupdate
```

## Quick Start

### Start

```shell
$ python main.py
```

### MD5

```shell
$ curl -F 'file=@test.txt' -F 'file=@test.txt' http://127.0.0.1:8888/md5
================= file =================
file: ba1f2511fc30423bdbb183fe33f3dd0f
================= file =================
file: ba1f2511fc30423bdbb183fe33f3dd0f
```

## Run test

```shell
pytest .
```