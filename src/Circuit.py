from Gate import Gate
import re

class Circuit():
    ID_index = 0 # index of the gates' IDs in the circuit
    def __init__(self):
        self.gates = []             # List of all gates in the circuit
        self.primary_input_gates = []    # List of all Primary Inputs
        self.Primary_Output_gates = []   # List of all Primary Outputs
        self.circuit_info = {}      # Dictionary of circuit information
        self.get_gates_from_PI = {}  # Dictionary of all primary inputs and their corresponding gates
        return
        
        
    def parse_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            # Define regualr expression patterns
            input_pattern = re.compile(r'INPUT\((\d+)\)')
            output_pattern = re.compile(r'OUTPUT\((\d+)\)')
            gate_pattern = re.compile(r'(\d+) = (\w+)\(([\d, ]+)\)')
            
            for line in lines:
                line = line.strip()
                
                if line.startswith("#"):
                    key, value = line[2:].split()
                    self.circuit_info[key] = value
                    
                elif input_match := input_pattern.match(line):
                    self.primary_input_gates.append(int(input_match.group(1)))
                    
                elif output_match := output_pattern.match(line):
                    self.Primary_Output_gates.append(int(output_match.group(1)))
                elif gate_match := gate_pattern.match(line):
                    gate_output = int(gate_match.group(1))
                    gate_type = gate_match.group(2)
                    gate_inputs = list(map(int, gate_match.group(3).split(',')))
                    self.add_gate(gate_type,gate_inputs, gate_output)
        
        self.map_gates_to_PI(self.primary_input_gates)
        # TODO: if needed make a dictionary between outputs and gates    
        return
    def add_gate(self, type, inputs, output):
        gate = Gate(self.ID_index, type, inputs, output)
        self.gates.append(gate)
        self.ID_index += 1
        return
    def map_gates_to_PI(self, inputs):
        self.get_gates_from_PI = {i: [] for i in self.primary_input_gates}
        
        for gate in self.gates:
            for input in gate.inputs:
                if input in self.get_gates_from_PI:
                    self.get_gates_from_PI[input].append(gate.id)
        return
                