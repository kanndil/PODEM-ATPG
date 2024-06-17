from Gate import Gate
from DAlgebra import D_Value

class PODEM:
    """
    The PODEM class .

    """
    def __init__(self, circuit):
        """
        Initializes a PODEM object.

        Args:
            circuit (Circuit): The circuit object representing the design.

        Returns:
            None
        """
        # Assign the circuit object to the PODEM object
        self.circuit = circuit

        # Initialize the objective function
        self.objective = None

        # Initialize the list of gates with D/D' input and X output
        self.D_Frontier = []

    def compute(self, algorithm="basic"):
        """
        Computes the PODEM using the specified algorithm.

        Args:
            algorithm (str): The algorithm to use. Possible values are "basic" and "advanced".
                             Defaults to "basic".

        Returns:
            None

        """
        # algorithm = "basic" or "advanced"
        # Use the specified algorithm to compute the PODEM
        if algorithm == "basic":
            # Use the basic POem algorithm
            self.basic_PODEM()
        elif algorithm == "advanced":
            # Use the advanced Poem algorithm
            self.advanced_PODEM()
        # Return nothing
        return

    def justify(self):
        return

    def X_init(self):
        """
        Initializes the output of each gate to X.

        This function iterates through all the gates in the circuit and sets their output to X.
        """
        for gate in self.circuit.gates:
            # Set the output of each gate to X
            gate.value = D_Value.X
        return

    def get_gate_from_input(self, input):
        return

    def imply_all(self):
        for PI in self.Primary_Inputs:
            self.imply(PI)

        return

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
        if previous_output_value != current_gate.output:
            for next_gate in current_gate.get_next_gates():
                self.imply(next_gate)

        return

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
        if gate.output != D_Value.X:
            return

        # Make sure that the gate's inputs have are available
        # by makeing sure the previous gates have been simulated

        for pre_gate in gate.get_previous_gates():
            self.simulate_gate(pre_gate)

        # evaluate the gate
        gate.evaluate()

        return

    def backtrace(self):
        return

    def check_error_at_primary_outputs(self):
        for output in self.Primary_Outputs:
            if output == D_Value.D or output == D_Value.D_PRIME:
                return True

    def ret_success(self):
        return

    def check_D_in_circuit(self):
        return

    def check_X_path_in_circuit(self):
        return

    def basic_PODEM(self):

        # While PI Branch-and-bound value possible
        for input in self.Primary_Inputs:
            # Get a new PI value
            for value in [0, 1]:
                # Imply new PI value
                self.imply(input)
                # If error at a PO
                # SUCCESS; Exit;
                if self.check_error_at_primary_outputs():
                    return self.ret_success()
                else:
                    if (
                        not self.check_D_in_circuit()
                        or not self.check_X_path_in_circuit()
                    ):
                        continue

        return False

    def advanced_PODEM(self):
        return
