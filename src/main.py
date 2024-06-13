import argparse
from PODEM import PODEM

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Run PODEM on a specified input file.")
    
    # Add arguments
    parser.add_argument('input_file', type=str, help='The input file to be processed by PODEM')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create PODEM agent and parse the input file
    podem_agent = PODEM()
    podem_agent.parse_file(args.input_file)
    
    # Compute the PODEM
    podem_agent.compute("basic")

if __name__ == "__main__":
    main()
