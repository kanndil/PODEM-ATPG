import argparse
from PODEM import PODEM
from Ciruit import Circuit


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Run PODEM on a specified input file.")

    # Add arguments
    parser.add_argument(
        "input_file", type=str, help="The input file to be processed by PODEM"
    )

    # Parse arguments
    args = parser.parse_args()

    circuit = Circuit()
    circuit.parse_file(filename=args.input_file)

    # Create PODEM agent and parse the input file
    podem_agent = PODEM(circuit=circuit)

    # Compute the PODEM
    podem_agent.compute(algorithm="basic")


if __name__ == "__main__":
    main()
