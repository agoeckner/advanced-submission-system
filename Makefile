SOURCE_DIR = ./src

all: submit grades
.PHONY: test

# Create the submission executable.
submit:
	pyinstaller -n "submit" -F --specpath ./build/ $(SOURCE_DIR)/initSubmit.py

# Create the grades executable.
grades:
	pyinstaller -n "grades" -F --specpath ./build/ $(SOURCE_DIR)/initGrades.py

# Run all test cases.
test:
	cd ./test/ && python3 -m unittest Test*.py; cd ..

clean:
	rm -r -f ./build/ ./dist/ ./src/__pycache__/ ./src/*/__pycache__/ ./test/__pycache__/
