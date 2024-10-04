echo "Formatting server code"
cd "$(dirname "$0")/.."
isort .
black .
echo "Done formatting code :)"
