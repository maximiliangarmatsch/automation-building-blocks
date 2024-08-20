# Testing

## Unit Tests
- assertions done with [unittest](https://docs.python.org/3/library/unittest.html)

- unit tests should be in `tests/` dir and file name should be in this format: `<module_name>.test.py`

- To run:
```bash
python -m unittest discover -s tests -p "*.test.py"
```