# Pypi

## test

```shell
python setup.py sdist
python setup.py sdist bdist_wheel
```

Upload to test

```shell
python -m twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*
```

### Reference

[Using TestPyPI](https://packaging.python.org/en/latest/guides/using-testpypi/)
