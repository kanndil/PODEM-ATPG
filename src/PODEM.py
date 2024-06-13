from Gate import Gate
from DAlgebra import D_Value

class PODEM:
    """
    The PODEM class .

    """
    def __init__(self, gates, lines, Primary_Inputs, Primary_Outputs):
        self.objective = None
        self.gates = []             # List of all gates in the circuit
        self.lines =[]              # List of all lines in the circuit
        self.D_Frontier = []        # List of all gates with D/D' input and X output
        self.Primary_Inputs = []    # List of all Primary Inputs
        self.Primary_Outputs = []   # List of all Primary Outputs
        pass
    def parse_file(self, filename):
        pass
    def compute(self):
        pass
    def justify(self):
        pass
    def X_init(self):
        """
        Initializes the output of each gate to X.

        This function iterates through all the gates in the circuit and sets their output to X.
        """
        for gate in self.gates:
            # Set the output of each gate to X
            gate.output = D_Value.X

    def get_gate_from_input(self, input):
        pass
    def imply_all(self):
        for PI in self.Primary_Inputs:
            self.imply(PI)

    def imply(self, input):
        """
        Propagates a primary input value to all parts of the circuit that it affects.

        This function starts from the primary input, simulates the gate, and recursively calls itself on the next gates.

        Args:
            input (Gate): The primary input gate.
        """
        # Get the gate corresponding to the input
        current_gate = self.get_gate_from_input(input)
        
        # If the gate is an output, there is nothing to propagate
        if current_gate.is_output():
            return
        
        # Store the previous output value of the gate
        previous_output_value = current_gate.output
        
        # Simulate the gate
        self.simulate_gate(current_gate)
        
        # If the output value of the gate changed, propagate the change to the next gates
        if (previous_output_value != current_gate.output):
            for next_gate in current_gate.get_next_gates():
                self.imply(next_gate)

        
    def simulate_gate(self, gate):
        """
        Simulates a gate and recursively simulates its previous gates.

        This function is called to simulate a gate and its previous gates. 
        
        This function is called recursively until the gate has been simulated.
        
        This function is a helper function for justification. 
        
        Args:
            gate (Gate): The gate to be simulated.
        """
        # Break condition: return if the gate has already been simulated
        if (gate.output != D_Value.X):
            return
        
        # Make sure that the gate's inputs have are available
        # by makeing sure the previous gates have been simulated
        
        for pre_gate in gate.get_previous_gates():
            self.simulate_gate(pre_gate)
        
        # evaluate the gate
        gate.evaluate()
        
    def backtrace(self):
        pass
    def check_error_at_primary_outputs(self):
        for output in self.Primary_Outputs:
            if output == D_Value.D or output == D_Value.D_PRIME:
                return True
    def ret_success(self):
        pass
    
    def check_D_in_circuit(self):
        pass
    def check_X_path_in_circuit(self):
        pass
    def basic_PODEM(self):
        
        # While PI Branch-and-bound value possible
        for input in self.Primary_Inputs:
            #Get a new PI value
            for value in [0,1]:
                #Imply new PI value
                self.imply(input)
                #If error at a PO
                #SUCCESS; Exit;
                if (self.check_error_at_primary_outputs()):
                    return self.ret_success()
                else:
                    if (not self.check_D_in_circuit() or not self.check_X_path_in_circuit()):
                        continue
                    
        return False    
            
            
     
