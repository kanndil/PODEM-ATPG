.PHONY: install uninstall clean build

# Define the package name
PACKAGE_NAME=podemquest

# Default target
all: install

# Build the package
build:
	@echo "Building $(PACKAGE_NAME)..."
	python setup.py sdist bdist_wheel

# Install the package
install: build
	@echo "Installing $(PACKAGE_NAME)..."
	pip install .

# Uninstall the package
uninstall:
	@echo "Uninstalling $(PACKAGE_NAME)..."
	pip uninstall -y $(PACKAGE_NAME)

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build dist src/$(PACKAGE_NAME).egg-info
