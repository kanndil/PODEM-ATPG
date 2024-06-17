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
            return self.basic_PODEM()
        elif algorithm == "advanced":
            # Use the advanced Poem algorithm
            return self.advanced_PODEM()
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

    def imply_all(self):  # todo: check if needed
        for PI in self.Primary_Inputs:
            self.imply(PI)

        return

    def imply(self, primary_input):
        """
        Propagates a primary input value to all parts of the circuit that it affects.

        This function starts from the primary input, simulates the gate, and recursively calls itself on the next gates.

        Args:
            primary_input (Gate): The primary input gate.

        Returns:
            None
        """
        # Iterate over all output gates connected to the primary input
        for next_gate in primary_input.output_gates:

            # Store the previous output value of the gate
            initial_output_value = next_gate.output

            ## Simulate the gate # todo: check if needed
            # self.simulate_gate(next_gate)

            # Evaluate the gate
            next_gate.evaluate()

            # If the output value of the gate changed, propagate the change to the next gates
            if initial_output_value == next_gate.output:
                continue
            else:
                # Recursively call the imply function on the next gates
                for next_next_gate in next_gate.output_gates:
                    self.imply(next_next_gate)

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
        if gate.value != D_Value.X:
            return

        # Make sure that the gate's inputs have are available
        # by makeing sure the previous gates have been simulated

        for previous_gate in gate.input_gates:
            self.simulate_gate(previous_gate)

        # evaluate the gate
        gate.evaluate()

        return

    def backtrace(self):
        return

    def check_error_at_primary_outputs(self):
        for output in self.circuit.primary_output_gates:
            if output == D_Value.D or output == D_Value.D_PRIME:
                return True

    def ret_success_vector(self):
        """
        Returns the test vector for the circuit by iterating through the primary input gates
        and appending their values to the test vector list.

        Returns:
            list: The test vector for the circuit.
        """
        # Initialize an empty list to store the test vector
        test_vector = []

        # Iterate through the primary input gates
        for PI in self.circuit.primary_input_gates:
            # Append the value of each primary input gate to the test vector
            test_vector.append(PI.value)

        # Return the test vector
        return test_vector

    def check_D_in_circuit(self):
        """
        Check if the circuit contains a gate with D or D' value.

        This function iterates through all the gates in the circuit and checks if any gate has a value of D or D'.

        Returns:
            bool: True if a gate with D or D' value is found, False otherwise.
        """
        # Iterate through all the gates in the circuit
        for gate in self.circuit.gates.values():
            # Check if the gate has a value of D or D'
            if gate.value == D_Value.D or gate.value == D_Value.D_PRIME:
                # If a gate with D or D' value is found, check for an X path
                for output_gate in gate.output_gates:
                    if self.check_X_path(output_gate):
                        return True

        # If no gate with D or D' value is found, return False
        return False

    def check_X_path(self, gate):
        """
        Check if there is an X path from the given gate to an output pin.

        Args:
            gate (Gate): The gate to start the search from.

        Returns:
            bool: True if there is an X path, False otherwise.
        """
        # Base case: If the gate is an output pin, return True
        if gate.type == "output_pin":
            return True

        # Recursive case: If the gate has an X value and there is an X path from one of its output gates, return True
        if gate.value == D_Value.X:
            for output_gate in gate.output_gates:
                if self.check_X_path(output_gate):
                    return True

        # If no X path is found, return False
        return False

    def basic_PODEM(self):
        # While PI Branch-and-bound value possible
        for primary_input in self.circuit.primary_input_gates:
            # Get a new PI value
            for value in [0, 1]:
                # Imply new PI value
                primary_input.value = value
                self.imply(primary_input)
                # If error at a PO
                # SUCCESS; Exit;
                if self.check_error_at_primary_outputs():
                    return True, self.ret_success_vector()
                else:
                    if (
                        not self.check_D_in_circuit()
                        or not self.check_X_path_in_circuit()
                    ):
                        continue

        return False, []

    def advanced_PODEM(self):
        return
