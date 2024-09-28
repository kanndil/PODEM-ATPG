# PODEM-ATPG

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains an implementation of the Path-Oriented Decision Making (PODEM) algorithm for Automatic Test Pattern Generation (ATPG). PODEM is a widely used method in digital circuit testing to generate test vectors that can detect faults in combinational circuits.


## How to Build

To build the `podemquest` package, follow these steps:

But before you begin, ensure you have Python and pip installed on your system. You can follow these links for installation instructions:

- [Install Python](https://www.python.org/downloads/)
- [Install pip](https://pip.pypa.io/en/stable/installation/)


1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kanndil/PodemQuest
   cd podemquest
   ```

2. **Install Required Tools:**
   Make sure you have `setuptools` and `wheel` installed. You can install them using pip:
   ```bash
   pip install setuptools wheel
   ```

3. **Build the Package:**
   Run the following command to build the package:
   ```bash
   make
   ```

   This will create the source distribution and wheel files in the dist directory, and link the podemquest executable to your system's PATH.

4. **Verify Installation:**
    After building, you can verify that podemquest is installed by running:
    ```bash
    podemquest --help
    ```
    This command should display the help information for the podemquest executable.


## How to Use

The `podemquest` command-line tool allows you to run the PODEM algorithm on a specified input file. You need to provide the required input and output files as arguments. 

### Command Syntax

```bash
podemquest -i <input_file> -o <output_file> [-r <report_file>]
```

### Arguments

- `-i`, `--input_file`: (Required) Specify the path to the input file that you want to process with PODEM.

- `-o`, `--output_file`: (Required) Specify the path where you want to save the PODEM report.

- `-r`, `--report_file`: (Optional) Specify a path for a detailed report file. If not provided, a default value of `None` will be used.

### Example Usage

To run the tool, use the following command:

```bash
podemquest -i path/to/input_file.txt -o path/to/output_file.txt -r path/to/report_file.txt
```

In this example:
- Replace `path/to/input_file.txt` with the actual path to your input file.
- Replace `path/to/output_file.txt` with the desired output file path for the PODEM report.
- Optionally, you can specify a report file path using the `-r` flag.

### Notes
- Ensure that the specified input file exists and is in the correct format expected by the PODEM algorithm.
- The output and report files will be created or overwritten as specified.


## License

This project is licensed under the Apache License 2.0. You may obtain a copy of the License at:

[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)

### Copyright

Copyright (c) 2024, Youssef Kandil (youssefkandil@aucegypt.edu)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at the link above.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.



