# Testing

## Unit Tests
- assertions done with [unittest](https://docs.python.org/3/library/unittest.html)

- unit tests should be in `tests/` dir and file name should be in this format: `<module_name>.test.py`

- To run:
```bash
python -m unittest discover -s tests -p "*.test.py"
```

## Setup for Running pyautogui in a Virtual Dispplay on Docker

### Steps

- change directory into `tests/e2e`

    - `cd tests/e2e`

- Build an image

  - `docker build -t <IMAGE_NAME> .`

- Run an interactive container from this image

  - `docker run -it --name <CONTAINER_NAME> <IMAGE_NAME>`

- start a virtual display (with given arbitary display number)

  - `source ./start_virtual_display.sh 8`

- Run the virtual environment

  - `source /opt/venv/bin/activate`

- Stop the virtual display (started with the number chosen above)

  - `./stop_virtual_display.sh 8`

- Exit the shell by `Ctrl + C`


### Copy files from docker container to local dir

- `docker cp <CONTAINER_NAME>:/home/screenshots .`