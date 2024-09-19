import argparse
from PODEM import PODEM
from Circuit import Circuit


def main():
    ## Initialize the argument parser
    # parser = argparse.ArgumentParser(description="Run PODEM on a specified input file.")

    ## Add arguments
    # parser.add_argument(
    #    "input_file", type=str, help="The input file to be processed by PODEM"
    # )

    ## Parse arguments
    # args = parser.parse_args()
    # input_file = args.input_file

    input_file = "/Users/youssef/Documents/Work/GSOC/PODEM-ATPG/test/c17.bench"
    #fault_file = "/Users/youssef/Documents/Work/GSOC/PODEM-ATPG/test/c17.fault"
    circuit = Circuit(input_file)

    # Create PODEM agent and parse the input file
    podem_agent = PODEM(circuit=circuit)

    # Compute the PODEM
    podem_agent.compute(algorithm="advanced")


if __name__ == "__main__":
    main()
