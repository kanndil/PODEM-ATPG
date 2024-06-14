from Gate import Gate
import re


class Circuit:
    ID_index = 0  # index of the gates' IDs in the circuit

    def __init__(self):
        """
        Initializes a Circuit object with default attributes.

        The circuit is represented by a list of gates (Gate objects), a list of primary input gates,
        a list of primary output gates, a dictionary of circuit information, and a dictionary that maps
        each primary input to the corresponding gates.

        Returns:
            None
        """
        # List of all gates in the circuit
        self.gates = []

        # List of all primary input gates
        self.primary_input_gates = []

        # List of all primary output gates
        self.Primary_Output_gates = []

        # Dictionary of circuit information
        self.circuit_info = {}

        # Dictionary that maps each primary input to the corresponding gates
        self.get_gates_from_PI = {}
        
        return

    def parse_file(self, filename):
        """
        Parses a text file describing a circuit and adds the gates to the circuit.

        Args:
            filename (str): The name of the file to parse.

        Returns:
            None
        """
        # Open the file
        with open(filename, "r") as file:
            lines = file.readlines()

            # Define regular expression patterns
            input_pattern = re.compile(r"INPUT\((\d+)\)")  # Matches input gates
            output_pattern = re.compile(r"OUTPUT\((\d+)\)")  # Matches output gates
            gate_pattern = re.compile(r"(\d+) = (\w+)\(([\d, ]+)\)")  # Matches gates

            # Iterate over each line in the file
            for line in lines:
                line = line.strip()

                # Check if the line starts with a comment
                if line.startswith("#"):
                    # Extract the key-value pair from the comment
                    key, value = line[2:].split()
                    # Add the key-value pair to the circuit information dictionary
                    self.circuit_info[key] = value

                # Check if the line matches an input gate pattern
                elif input_match := input_pattern.match(line):
                    # Add the input gate id to the list of primary input gates
                    self.primary_input_gates.append(int(input_match.group(1)))

                # Check if the line matches an output gate pattern
                elif output_match := output_pattern.match(line):
                    # Add the output gate id to the list of primary output gates
                    self.Primary_Output_gates.append(int(output_match.group(1)))

                # Check if the line matches a gate pattern
                elif gate_match := gate_pattern.match(line):
                    # Extract the gate information
                    gate_output = int(gate_match.group(1))
                    gate_type = gate_match.group(2)
                    gate_inputs = list(map(int, gate_match.group(3).split(",")))
                    # Add the gate to the circuit
                    self.add_gate(gate_type, gate_inputs, gate_output)

        # Map each primary input to the corresponding gates
        self.map_gates_to_PI()
        # TODO: if needed, create a dictionary that maps outputs to gates
        return

    def add_gate(self, type, inputs, output):
        """
        Add a gate to the circuit.

        Args:
            type (str): The type of the gate.
            inputs (List[int]): The inputs of the gate.
            output (int): The output of the gate.

        Returns:
            None
        """
        # Create a new gate with the given parameters
        gate = Gate(self.ID_index, type, inputs, output)
        
        # Add the gate to the list of gates in the circuit
        self.gates.append(gate)
        
        # Increment the ID index for the next gate
        self.ID_index += 1
        
        return

    def map_gates_to_PI(self):
        """
        Maps each primary input to the corresponding gates.

        This function creates a dictionary that maps each primary input to a list of gate ids.
        The dictionary is assigned to the `get_gates_from_PI` attribute of the Circuit object.

        Returns:
            None
        """
        # Create a dictionary to map primary input to the corresponding gates
        self.get_gates_from_PI = {i: [] for i in self.primary_input_gates}

        # Iterate over each gate in the circuit
        for gate in self.gates:
            # Iterate over each input of the gate
            for input in gate.inputs:
                # If the input is a primary input, add the gate's id to the list of gates for that input
                if input in self.get_gates_from_PI:
                    self.get_gates_from_PI[input].append(gate.id)
        return
