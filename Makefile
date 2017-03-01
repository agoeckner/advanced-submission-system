SOURCE_DIR = ./src

all: submit
.PHONY: test

# Create the submission executable.
submit:
	pyinstaller $(SOURCE_DIR)/init.py

# Run all test cases.
test:
	cd ./test/ && python3 -m unittest Test*.py; cd ..

clean:
	rm -r -f ./build/ ./dist/ ./*.spec ./src/__pycache__/ ./src/*/__pycache__/ ./test/__pycache__/
