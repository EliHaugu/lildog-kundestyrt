# lildog-kundestyrt

## How to run backend
### 1. Create and enter a venv
This is recommended to avoid issues with differing versions of packages in project and local environment. In addition, this avoids bloat not necessary for the project being added when freezing requirements.

1. If you don't have python3.10-venv already, install it
    - On Ubuntu: `sudo apt install python3.10-venv`
2. Create a venv
    - On Ubuntu: `python3 -m venv venv` (or whatever else you want to name your venv)
3. Enter your venv
    - On Ubuntu: `source venv/bin/activate`

### 2. Install requirements
1. Open the folder where you have this project
2. Open the `server` folder
3. Install the requirements by running `pip install -r requirements.txt`

### 3. Run server
Open the `server` folder and run the following command: `python3 -m server`

## How to update requirements
If you have added new pip packages to the project and want to save them for everyone to use, when in your venv (ensure that you are in the venv so you don't freeze unnecessary packages), run the following command in the server folder: `pip freeze > requirements.txt`

## Testing
### How to write a test
pytest automatically looks for files that match the pattern `test_*.py` or `*_test.py` and within those files finds functions that begin with `test`. To create new tests, follow this pattern and create your file in the `server/tests` folder.

By default, all test functions run the `start_server()` fixture found in the `conftest.py` file to set up the server at the beginning of each test function. If you want to add more setup to your tests, you can do so by using `@pytest.fixture` decorator.

You can also add a `scope` argument to your fixture, like this `@pytest.fixture(scope="function")`, to define when you want to run this setup function (e.g. for each function (`function`)), for each test file (`module`), etc.).

### How to run tests
To run all tests, run `pytest server/tests`. To run a specific test, run `pytest server/tests/test.py`.
