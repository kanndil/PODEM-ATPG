from enum import Enum

# The D_Value Class represents the D value of a gate {0,1,D,D',x}
class D_Value(Enum):
    ZERO = 0        # 0 is (0,0)
    ONE = 1         # 1 is (1,1)
    D = 2           # D is (1,0)
    D_PRIME = 3     # D' is (0,1)
    X = 4           # X is (1, X) or (X, 1) or (X, X) or (0, X) or (X, 0)

class Gate:
    def __init__(self, name, type, inputs):
        self.name = name
        self.type = type
        self.inputs = inputs
        self.output = None
        
        # Distance Parameters
        self.PI_distance = 0
        self.PO_distance = 0
        
        # SCOAP Parameters
        self.CC0 = 0    # Combinational 0-controllability of line l. 
                        # The number of lines from the primary inputs that have to be traced to put a 0 on line l.
                        
        self.CC1 = 0    # Combinational 1-controllability of line l.
                        # The number of lines from the primary inputs that have to be traced to put a 1 on line l.
                        
        self.CCb = 0    # Combinational observability of line l.
                        # The number of lines that have to be traced to observe value of line l on a primary output. 

    def get_previous_gates(self):
        pass
    def evaluate(self):
        """
        Evaluates the output of the gate based on its type.

        This function determines the output of the gate by calling the appropriate evaluation method based on its type. If the gate is of type "AND", it calls the `evaluate_and` method. If the gate is of type "OR", it calls the `evaluate_or` method. If the gate is of type "XOR", it calls the `evaluate_xor` method. If the gate is of type "NOT", it calls the `evaluate_not` method.

        Parameters:
            self (Gate): The gate object.

        Returns:
            None
        """
        if self.type == "AND":
            self.output = self.evaluate_and()
        elif self.type == "OR":
            self.output = self.evaluate_or()
        elif self.type == "XOR":
            self.output = self.evaluate_xor()
        elif self.type == "NOT":
            self.output = self.evaluate_not()
        elif self.type == "NAND":
            self.output = self.evaluate_nand()
        elif self.type == "NOR":
            self.output = self.evaluate_nor()
        elif self.type == "XNOR":
            self.output = self.evaluate_xnor()

    def evaluate_and(self):
        """
        Evaluates the output of an AND gate based on its inputs.

        This function checks the inputs of an AND gate and determines the output based on the following rules:
        - If any input is ZERO, the output is ZERO.
        - If any input is X, the output is X.
        - If both D and D_PRIME are in the inputs, the output is ZERO.
        - If D is in the inputs and all inputs are either ONE or D, the output is D.
        - If D_PRIME is in the inputs and all inputs are either ONE or D_PRIME, the output is D_PRIME.
        - Otherwise, the output is ONE.

        Returns:
            D_Value: The output value of the AND gate.
        """
        # Check if any input is ZERO
        if D_Value.ZERO in self.inputs:
            return D_Value.ZERO
        
        # Check if any input is X
        if D_Value.X in self.inputs:
            return D_Value.X
        
        # Check if both D and D_PRIME are in the inputs
        if D_Value.D in self.inputs and D_Value.D_PRIME in self.inputs:
            return D_Value.ZERO
        
        # Check if D is in the inputs and if all inputs are either ONE or D
        if D_Value.D in self.inputs:
            if all(val in [D_Value.ONE, D_Value.D] for val in self.inputs):
                return D_Value.D
        
        # Check if D_PRIME is in the inputs and if all inputs are either ONE or D_PRIME
        if D_Value.D_PRIME in self.inputs:
            if all(val in [D_Value.ONE, D_Value.D_PRIME] for val in self.inputs):
                return D_Value.D_PRIME
        
        # Return ONE if none of the above conditions are met
        return D_Value.ONE

    def evaluate_or(self):
        """
        Evaluates the output of an OR gate based on its inputs.

        This function checks the inputs of an OR gate and determines the output based on the following rules:
        - If any input is ONE, the output is ONE.
        - If any input is X, the output is X.
        - If both D and D_PRIME are in the inputs, the output is ONE.
        - If D is in the inputs and any input is either ONE or D, the output is D.
        - If D_PRIME is in the inputs and any input is either ONE or D_PRIME, the output is D_PRIME.
        - Otherwise, the output is ZERO.

        Returns:
            D_Value: The output value of the OR gate.
        """
        # Check if any input is ONE
        if D_Value.ONE in self.inputs:
            return D_Value.ONE

        # Check if any input is X
        if D_Value.X in self.inputs:
            return D_Value.X

        # Check if both D and D_PRIME are in the inputs
        if D_Value.D in self.inputs and D_Value.D_PRIME in self.inputs:
            return D_Value.ONE

        # Check if D is in the inputs and if all inputs are either ONE or D
        if D_Value.D in self.inputs:
            if any(val in [D_Value.ONE, D_Value.D] for val in self.inputs):
                return D_Value.D

        # Check if D_PRIME is in the inputs and if all inputs are either ONE or D_PRIME
        if D_Value.D_PRIME in self.inputs:
            if any(val in [D_Value.ONE, D_Value.D_PRIME] for val in self.inputs):
                return D_Value.D_PRIME

        # Return ZERO if none of the above conditions are met
        return D_Value.ZERO

    def evaluate_xor(self):
        """
        Evaluates the output of an XOR gate based on its inputs.

        This function checks the inputs of an XOR gate and determines the output based on the following rules:
        - If any input is X, the output is X.
        - If the count of D and D_PRIME are not equal, the output is determined based on the count of ONE and ZERO.
        - If the count of D and D_PRIME are equal, the output is determined based on the count of ONE and ZERO and the greater count.

        Returns:
            D_Value: The output value of the XOR gate.
        """
        # Count the occurrences of D and D_PRIME
        d_count = self.inputs.count(D_Value.D)
        d_prime_count = self.inputs.count(D_Value.D_PRIME)
        
        # Count the occurrences of ONE and ZERO
        one_count = self.inputs.count(D_Value.ONE)
        zero_count = self.inputs.count(D_Value.ZERO)
        
        # Count the occurrences of X
        x_count = self.inputs.count(D_Value.X)
        
        # If any input is X, the output is X
        if x_count > 0:
            return D_Value.X
        
        # If the count of D and D_PRIME are not equal, the output is determined based on the count of ONE and ZERO
        if d_count % 2 != d_prime_count % 2:
            if one_count % 2 == 0:
                return D_Value.ZERO
            else:
                return D_Value.ONE
        else:
            # If the count of D and D_PRIME are equal, the output is determined based on the count of ONE and ZERO and the greater count
            if one_count % 2 == 0:
                if d_count > d_prime_count:
                    return D_Value.D
                else:
                    return D_Value.D_PRIME
            else:
                if d_count > d_prime_count:
                    return D_Value.D_PRIME
                else:
                    return D_Value.D

    def evaluate_not(self):
        """
        Evaluates the output of a NOT gate based on its input.

        This function checks the input of a NOT gate and determines the output based on the following rules:
        - If the input is D, the output is D_PRIME.
        - If the input is D_PRIME, the output is D.
        - If the input is ONE, the output is ZERO.
        - If the input is ZERO, the output is ONE.
        - If the input is X, the output is X.

        Returns:
            D_Value: The output value of the NOT gate.
        """
        # Check the input value
        input_val = self.inputs[0]
        if input_val == D_Value.D:
            return D_Value.D_PRIME
        elif input_val == D_Value.D_PRIME:
            return D_Value.D
        elif input_val == D_Value.ONE:
            return D_Value.ZERO
        elif input_val == D_Value.ZERO:
            return D_Value.ONE
        else:
            return D_Value.X
    def evaluate_nand(self):
        """
        Evaluates the output of a NAND gate based on its inputs.

        This function creates an AND gate and evaluates its output. Then, it creates a NOT gate for the AND gate's output.

        Returns:
            The output value of the NAND gate.
        """
        # Create an AND gate
        and_gate = Gate("AND", "AND", self.inputs, None)
        and_gate.evaluate()

        # Create a NOT gate for the AND gate's output
        not_gate = Gate("NOT", "NOT", [and_gate.output], None)
        not_gate.evaluate()

        return not_gate.output

    def evaluate_nor(self):
        """
        Evaluates the output of a NOR gate based on its inputs.

        This function creates an OR gate and evaluates its output. Then, it creates a NOT gate for the OR gate's output.

        Returns:
            The output value of the NOR gate.
        """
        # Create an OR gate
        or_gate = Gate("OR", "OR", self.inputs, None)  # Create an OR gate
        or_gate.evaluate()                              # Evaluate the OR gate

        # Create a NOT gate for the OR gate's output
        not_gate = Gate("NOT", "NOT", [or_gate.output], None)  # Create a NOT gate
        not_gate.evaluate()                                      # Evaluate the NOT gate

        return not_gate.output  # Return the output of the NOT gate
    def evaluate_xnor(self):
        """
        Evaluates the output of an XNOR gate based on its inputs.

        This function creates an XOR gate and evaluates its output. Then, it creates a NOT gate for the XOR gate's output.

        Returns:
            The output value of the XNOR gate.
        """
        # Create an XOR gate
        xor_gate = Gate("XOR", "XOR", self.inputs, None)  # Create an XOR gate
        xor_gate.evaluate()                              # Evaluate the XOR gate

        # Create a NOT gate for the XOR gate's output
        not_gate = Gate("NOT", "NOT", [xor_gate.output], None)  # Create a NOT gate
        not_gate.evaluate()                                      # Evaluate the NOT gate

        return not_gate.output  # Return the output of the NOT gate



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
    



# Global Variables
D_Frontier = []                 # The D_Frontier is a list of all the gates which have D/D' input and X output 
                                # and is likely to be on an X-path
Primary_Inputs = []             # List of all Primary Inputs
Primary_Outputs = []            # List of all Primary Outputs
