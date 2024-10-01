echo "Formatting server code"
cd ..
isort .
black .
echo "Done formatting code :)"
