# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/

# Copyright (c) 2024, Youssef Kandil (youssefkandil@aucegypt.edu)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3

import argparse
import time
from .PODEM import PODEM
from .Circuit import Circuit


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Run PODEM on a specified input file.")

    # Add input, output, and report file arguments
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        required=True,
        help="The input file to be processed by PODEM",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required=True,
        help="The output file to save the PODEM report",
    )
    parser.add_argument(
        "-r",
        "--report_file",
        type=str,
        help="The file to save the detailed PODEM report",
        default=None,
    )

    ## Parse arguments
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    report_file = args.report_file

    # Create Circuit object from the input file
    circuit = Circuit(input_file)

    # Create PODEM agent and pass the circuit
    podem_agent = PODEM(circuit=circuit, output_file=output_file)

    # Start timing the PODEM computation
    start_time = time.time()

    # Compute the PODEM algorithm
    podem_agent.compute(algorithm="advanced")

    # End timing
    end_time = time.time()

    # Calculate total time taken
    total_time = end_time - start_time

    # Generate the PODEM report
    report = podem_agent.report()

    # Combine time taken with the report
    combined_report = f"""
    ================== PODEM Fault Coverage Report ==================

        {report.strip()}

    ------------------------------------------------------------------
    Total Time Taken: {total_time:.4f} seconds

    ==================================================================
    """

    # Optionally print the report to the console
    # print(combined_report)

    # If a report file is specified, write the detailed report to it
    if report_file:
        with open(report_file, "w") as f:
            f.write(combined_report)


if __name__ == "__main__":
    main()
