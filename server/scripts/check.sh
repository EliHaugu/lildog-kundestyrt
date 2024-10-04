echo "Checking server code format"
cd "$(dirname "$0")/.."
echo "isort"
isort --check-only .
echo -e "\nflake8"
flake8 .
echo -e "\nblack"
black --check .
echo -e "\nmypy"
mypy .

echo -e "\nRunning tests"
pytest .
