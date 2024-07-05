from Gate import Gate
import re


class Circuit:

    index_id = 0

    def __init__(self):
        """
        Initializes a Circuit object with default attributes.

        The circuit is represented by a list of gates (Gate objects), a list of primary input gates,
        a list of primary output gates, a dictionary of circuit information, and a dictionary that maps
        each primary input to the corresponding gates.

        Returns:
            None
        """
        # Dictionary of all gates in the circuit mapped to the ID of their output pins
        # This mapping is very useful for when searching for neighbouring gates
        self.gates = {}

        # List of all primary input gates
        self.primary_input_gates = []

        # List of all primary output gates
        self.primary_output_gates = []

        # Dictionary that maps each primary input to the corresponding gates
        self.get_gates_from_PI = {}
        
        # List of all faults in the circuit
        self.faults = []

        return

    def parse_circuit_file(self, filename):
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
                    continue

                # Check if the line matches an input gate pattern
                elif input_match := input_pattern.match(line):
                    # Add the input gate id to the list of primary input gates
                    self.add_gate("input_pin", [], str(input_match.group(1)).strip())

                # Check if the line matches an output gate pattern
                elif output_match := output_pattern.match(line):
                    # Add the output gate id to the list of primary output gates
                    self.add_gate(
                        "output_pin",
                        [
                            str(output_match.group(1)).strip(),
                        ],
                        "output_pin_"+str(output_match.group(1)).strip(),
                    )

                # Check if the line matches a gate pattern
                elif gate_match := gate_pattern.match(line):
                    # Extract the gate information
                    gate_output = str(gate_match.group(1)).strip()
                    gate_type = gate_match.group(2).strip()
                    gate_inputs = list(map(lambda x: x.strip(), gate_match.group(3).split(",")))
                    # Add the gate to the circuit
                    self.add_gate(gate_type, gate_inputs, gate_output)

        self.build_graph()
        # Map each primary input to the corresponding gates
        return

    def add_gate(self, type, inputs, output_pin_id):
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
        gate = Gate(self.index_id, type, inputs, output_pin_id)

        if type == "input_pin":
            self.primary_input_gates.append(gate)
        elif type == "output_pin":
            self.primary_output_gates.append(gate)

 
        # Add the gate to the dictionary of gates based on the output id
        self.gates[str(output_pin_id)] = gate

        self.index_id += 1
        return

    def map_gates_to_PI(self):  # todo: remove this (build graph fulfills the purpose)
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

    def build_graph(self):
        """
        Builds the graph representation of the circuit, connecting the gates based on their input and output pins.

        This function iterates over all the gates in the circuit and connects them based on their input pins.
        For each gate, it retrieves its input pins and clears the list of input gates.
        Then, for each input pin, it retrieves the corresponding gate from the circuit's dictionary of gates,
        and connects the current gate to it as an input gate.
        It also connects the previous gate to the current gate as an output gate.

        Returns:
            None
        """
        # Iterate over each gate in the circuit
        for current_gate in self.gates.values():
            # Get the input pins of the gate
            input_ids = current_gate.input_gates[:]
            # Clear the list of input gates
            current_gate.input_gates.clear()
            # Iterate over each input pin
            for input_id in input_ids:
                # Retrieve the corresponding previoud gate from the circuit's dictionary of gates
                previous_gate = self.gates[input_id]
                # Connect the current gate to the previous gate as an input gate
                current_gate.input_gates.append(previous_gate)
                # Connect the previous gate to the current gate as an output gate
                previous_gate.output_gates.append(current_gate)

    def print_circuit(self):
        
        print("--------------------------- ---------------------------")
        for gate in self.gates.values():
            print(gate.outputpin)
            print(gate.type)
            print(gate.value)
            print()
        print("---------------------------")


    def parse_fault_file(self, fault_file):
        """
        Parses a fault file and stores the fault information in the circuit object.

        Args:
            fault_file (str): The path to the fault file.

        Returns:
            None
        """
        # Open the fault file
        with open(fault_file, 'r') as file:
            # Read all the lines from the file
            lines = file.readlines()

            # Iterate through the lines two at a time
            for i in range(0, len(lines), 2):
                # Get the net name from the first line
                net_name = lines[i].strip()
                # Get the fault value from the second line and convert it to an integer
                fault_value = int(lines[i+1].strip())
                # Append the net name and fault value to the circuit's faults list
                self.faults.append((net_name, fault_value))

        # Return None, as this function does not return anything
        return
    