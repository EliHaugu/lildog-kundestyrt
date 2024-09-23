echo "Checking server code format"
cd ..
isort --check-only .
flake8
black --check
mypy .

echo "Running tests"
pytest .
