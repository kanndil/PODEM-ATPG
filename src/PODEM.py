from Gate import Gate
from DAlgebra import D_Value
import math


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
        
        self.fault_is_activated = False

        # Initialize the list of gates with D/D' input and X output
        self.D_Frontier = []
        
        # fault gate and value 
        
        self.fault_gate = None
        self.fault_value = None

    def compute(self, algorithm="basic"):
        """
        Computes the PODEM using the specified algorithm.

        Args:
            algorithm (str): The algorithm to use. Possible values are "basic" and "advanced".
                             Defaults to "basic".

        Returns:
            None

        """

        self.circuit.calculate_SCOAP()
        if algorithm == "basic":
            for fault in self.circuit.faults:
                self.init_PODEM()
                # Use the basic POem algorithm
                for PI in self.circuit.primary_input_gates:
                    PI.explored = False
                ret = self.basic_PODEM(fault)
                if ret == True:
                    print("Fault: ", fault)
                    print("test vector: ", self.ret_success_vector())
                else:
                    print("Fault: ", fault)
                    print("test vector: NOT FOUND ")
        elif algorithm == "advanced":
            for fault in self.circuit.faults:
                fault_site = fault[0]
                self.fault_gate = self.circuit.gates[fault_site]
                self.fault_gate.faulty = True
                if fault[1] == 0:
                    self.fault_value = D_Value.ZERO
                    self.fault_gate.fault_value = D_Value.ZERO
                elif fault[1] == 1:
                    self.fault_value = D_Value.ONE
                    self.fault_gate.fault_value = D_Value.ONE
                
                self.init_PODEM()
                print("Fault: ", fault)
                ret = self.advanced_PODEM()
                self.fault_gate.faulty = False
                if ret == True:
                    print("test vector: ", self.ret_success_vector())
                else:
                    print("test vector: NOT FOUND ")


        return

    def init_PODEM(self):
        """
        Initializes the output of each gate to X.

        This function iterates through all the gates in the circuit and sets their output to X.
        """
        self.fault_is_activated = False
        for gate in self.circuit.gates.values():
            # Set the output of each gate to X
            gate.value = D_Value.X

        return

    def imply_all(self):  # todo: check if needed
        for PI in self.Primary_Inputs:
            self.imply(PI)

        return

    def imply(self, _input_gate):
        """
        Propagates a _input_gate's value to all parts of the circuit that it affects.

        This function starts from the primary input, simulates the gate, and recursively calls itself on the next gates.

        Args:
            primary_input (Gate): The primary input gate.

        Returns:
            None
        """
        initial_output_value = _input_gate.value
        _input_gate.evaluate()

        ## Simulate the gate # todo: check if needed
        # self.simulate_gate(next_gate)

        if (
            initial_output_value == _input_gate.value
            and _input_gate.type != "input_pin"
        ):
            return

        # Iterate over all output gates connected to the primary input
        for next_gate in _input_gate.output_gates:
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
        if gate.value != D_Value.X:
            return

        # Make sure that the gate's inputs have are available
        # by makeing sure the previous gates have been simulated

        for previous_gate in gate.input_gates:
            self.simulate_gate(previous_gate)

        # evaluate the gate
        gate.evaluate()

        return

    def backtrace(self, objective_gate, objective_value):
        """
        Traverse upwards from the objective gate to find the primary input gate that affects the objective gate.
        It tracks the inversion parity along the way.

        Then, it finds the primary input gate that affects the objective gate. If the inversion parity is odd, it inverts
        the objective value.
        Args:
            objective_gate (Gate): The gate that the primary input gate is affecting.
            objective_value (D_Value): The value of the objective gate.

        Returns:
            tuple: A tuple containing the primary input gate that affects the objective gate and a boolean
                   indicating if the objective value is D or D'.
        """
        # Initialize variables
        target_PI = objective_gate
        target_PI_value = None
        inversion_parity = target_PI.inversion_parity

        # Traverse upwards from the objective gate
        while target_PI.type != "input_pin":

            # Find the previous gate with X value
            for previous_gate in target_PI.input_gates:
                if previous_gate.value == D_Value.X:
                    target_PI = previous_gate
                    break

            # Update the inversion parity
            inversion_parity += target_PI.inversion_parity

        # Determine the target primary input value
        if inversion_parity % 2 == 1:
            if objective_value == D_Value.ONE:
                target_PI_value = D_Value.ZERO
            elif objective_value == D_Value.ZERO:
                target_PI_value = D_Value.ONE
        else:
            target_PI_value = objective_value

        # Return the target primary input gate and a boolean indicating if the objective value is D or D'
        return target_PI, target_PI_value
    
     
    def check_error_at_primary_outputs(self):
        """
        Checks if there is an error at the primary outputs of the circuit.

        This function iterates through the primary output gates and checks if any of them have a value
        of D or D'. If such a gate is found, it returns True, indicating that there is an error.

        Returns:
            bool: True if there is an error at the primary outputs, False otherwise.
        """
        # Iterate through the primary output gates
        for output_gate in self.circuit.primary_output_gates:
            # Check if the gate has a value of D or D'
            if output_gate.value == D_Value.D or output_gate.value == D_Value.D_PRIME:
                # If an error is found, return True
                return True

        # If no error is found, return False
        return False

    def ret_success_vector(self):
        """
        Returns the test vector for the circuit by iterating through the primary input gates
        and appending their values to the test vector list.

        Returns:
            list: The test vector for the circuit.
        """
        # Initialize an empty list to store the test vector
        test_vector = ""

        # Iterate through the primary input gates
        for PI in self.circuit.primary_input_gates:
            # Append the value of each primary input gate to the test vector
            test_vector += str(PI.value.value[0])

        # Return the test vector
        return test_vector

    def check_D_in_circuit(self):
        """
        Check if the circuit contains a gate with D or D' value. If so, check for an X path.

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

    def basic_PODEM(self, fault):

        self.activate_fault(fault)

        # While PI Branch-and-bound value possible
        for primary_input in self.circuit.primary_input_gates:
            if primary_input.explored:
                continue
            # Get a new PI value
            for value in [D_Value.ZERO, D_Value.ONE]:

                primary_input.explored = True
                # Imply new PI value
                primary_input.value = value
                self.imply(primary_input)
                # If error at a PO
                # SUCCESS; Exit;
                # self.circuit.print_circuit()
                if self.check_error_at_primary_outputs():
                    return True
                else:
                    if self.check_D_in_circuit():
                        break

        return False, ""


    def generate_d_frontier(self):
        self.D_Frontier = []
        for gate in self.circuit.gates.values():
            if gate.value == D_Value.X:
                for input_gate in gate.input_gates:
                    if input_gate.value == D_Value.D or input_gate.value == D_Value.D_PRIME:
                        if self.check_X_path(gate):
                            self.D_Frontier.append(gate)
                            
                        break
        return


    def activate_fault(self, fault):
            """
            Activate the specified fault in the circuit.

            Args:
                fault (Tuple): A tuple containing the fault site and fault type.

            Returns:
                None
            """
            # Extract relevant information from the fault tuple
            fault_site = fault[0]
            faulty_gate = self.circuit.gates[fault_site]
            faulty_gate.faulty = True

            # Determine the fault value based on the fault type
            if fault[1] == 0:
                fault_value = D_Value.ONE
                faulty_gate.fault_value = D_Value.D
            elif fault[1] == 1:
                fault_value = D_Value.ZERO
                faulty_gate.fault_value = D_Value.D_PRIME

            # Backtrace to determine the target primary input and its value
            target_primary_input, target_primary_input_value = self.backtrace(
                faulty_gate, fault_value
            )

            # Imply the target primary input value
            target_primary_input.value = target_primary_input_value
            self.imply(target_primary_input)
            target_primary_input.explored = True

            return
            


    def get_easiest_to_satisfy_gate(self, objective_gate, objective_value):
        """
        Find the input gate with the smallest CC0 or CC1 value, depending on the objective value.

        Args:
            objective_gate (Gate): The gate for which we want to find the easiest gate to satisfy.
            objective_value (D_Value): The value we want to satisfy.

        Returns:
            Gate: The input gate with the smallest CC0 or CC1 value.
        """
        easiest_gate = None
        easiest_value = math.inf  # Initialize with an impossible value

        # Iterate over all input gates
        for gate in objective_gate.input_gates:
            # Check if the gate is not set and the value is X
            if gate.value == D_Value.X:
                # If the objective value is ZERO, check if the CC0 value is smaller than the current best
                if objective_value == D_Value.ZERO:
                    if gate.CC0 < easiest_value:
                        easiest_gate = gate
                        easiest_value = gate.CC0

                # If the objective value is ONE, check if the CC1 value is smaller than the current best
                elif objective_value == D_Value.ONE:
                    if gate.CC1 < easiest_value:
                        easiest_gate = gate
                        easiest_value = gate.CC1

        # Return the easiest gate
        return easiest_gate
                

    def get_hardest_to_satisfy_gate(self, objective_gate, objective_value):
        """
        Find the input gate with the largest CC0 or CC1 value, depending on the objective value.

        Args:
            objective_gate (Gate): The gate for which we want to find the hardest gate to satisfy.
            objective_value (D_Value): The value we want to satisfy.

        Returns:
            Gate: The input gate with the largest CC0 or CC1 value.
        """
        hardest_gate = None  # The gate with the largest CC0 or CC1 value
        hardest_value = -math.inf  # The largest CC0 or CC1 value

        # Iterate over all input gates
        for gate in objective_gate.input_gates:
            # Check if the gate is not set and the value is X
            if gate.value == D_Value.X:
                # If the objective value is ZERO, check if the CC0 value is larger than the current hardest
                if objective_value == D_Value.ZERO:
                    if gate.CC0 > hardest_value:
                        hardest_gate = gate
                        hardest_value = gate.CC0

                # If the objective value is ONE, check if the CC1 value is larger than the current hardest
                elif objective_value == D_Value.ONE:
                    if gate.CC1 > hardest_value:
                        hardest_gate = gate
                        hardest_value = gate.CC1

        # Return the hardest gate
        return hardest_gate
    


    def oppositeVal(self, value):
        if value == D_Value.ZERO:
            return D_Value.ONE
        elif value == D_Value.ONE:
            return D_Value.ZERO


    def get_objective(self):
    
        if self.fault_gate.value == D_Value.D or self.fault_gate.value == D_Value.D_PRIME:
            self.fault_is_activated = True
            
        if self.fault_is_activated == False:
            if self.fault_gate.value == D_Value.ONE or self.fault_gate.value == D_Value.ZERO:
                return None, None 

            return self.fault_gate , self.oppositeVal(self.fault_value)
            
        else: 
        
            self.generate_d_frontier()
            if len(self.D_Frontier) == 0:
                return None, None  
             
            g = min(self.D_Frontier, key=lambda gate: gate.CCb)
            
            objective_gate = None
            objective_value = None
            for input_gate in g.input_gates:
                if input_gate.value == D_Value.X:
                    objective_gate = input_gate
                    objective_value = g.non_controlling_value
             
                    break

        return objective_gate , objective_value

    def check_imply_gate(self, gate, value):
        if value == D_Value.ONE:
            if gate.type == "OR" or gate.type == "NAND":
                return False
            else:
                return True

        elif value == D_Value.ZERO:
            if gate.type == "AND" or gate.type == "NOR":
                return False
            else:
                return True
    

    def backtrace_advanced(self, objective_gate, objective_value):
        """
        Traverse backward from the objective gate to find the primary input that affects the objective gate.
        It tracks the inversion parity along the way to determine the primary input value.

        Args:
            objective_gate (Gate): The gate that the primary input gate is affecting.
            objective_value (D_Value): The value to be set to the objective gate.

        Returns:
            tuple: A tuple containing the primary input gate that affects the objective gate and its value.
        """
        # Initialize variables
        target_PI = objective_gate  
        target_PI_value = objective_value  

        # Traverse backward from the objective gate
        while target_PI.type != "input_pin":
            
            # If the target_PI has an inversion parity, flip the target_PI_value
            if target_PI.inversion_parity :
                target_PI_value = self.oppositeVal(target_PI_value)
            
            if (self.check_imply_gate(target_PI, target_PI_value)):
                target_PI = self.get_hardest_to_satisfy_gate(objective_gate, objective_value)
            else:
                target_PI = self.get_easiest_to_satisfy_gate(objective_gate, objective_value)
                
            # Recursively call the function to traverse backward
            target_PI, target_PI_value = self.backtrace_advanced(target_PI, target_PI_value)

        # Return the target primary input gate and value
        return target_PI, target_PI_value


    def advanced_PODEM(self):
        
        if self.check_error_at_primary_outputs():
            return True
        
        objective_gate , objective_value = self.get_objective()
        
        if objective_gate == None:
            return False
        
        target_PI, target_PI_value = self.backtrace_advanced(objective_gate, objective_value)
        target_PI.value = target_PI_value
        self.imply(target_PI)
        
        if self.advanced_PODEM(): 
            return True
        
        target_PI_value = self.oppositeVal(target_PI_value)
        self.imply(target_PI)
        if self.advanced_PODEM():
            return True

        # release PI as unknown
        target_PI_value = D_Value.X
        self.imply(target_PI)
        
        return False
