# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/

# Copyright (c) 2024, Youssef Kandil (youssefkandil@aucegypt.edu) 
# 					  Mohamed Shalan (mshalan@aucegypt.edu)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .DAlgebra import D_Value


class Gate:
    def __init__(self, id, type, input_gates, outputpin):
        self.id = id
        self.type = type
        self.input_gates = input_gates
        self.output_gates = []
        self.outputpin = outputpin
        self.value = D_Value.X
        self.faulty = False
        self.fault_value = None

        if type == "input_pin" or type == "output_pin":
            self.is_pin = True
        else:
            self.is_pin = False

        if type == "NOT" or type == "NAND" or type == "NOR" or type == "XNOR":
            self.inversion_parity = 1
        else:
            self.inversion_parity = 0

        if type == "BUFF" or type == "NOT":
            self.non_controlling_value = D_Value.ONE
        elif type == "OR" or type == "NOR" or type == "XOR" or type == "XNOR":
            self.non_controlling_value = D_Value.ZERO
        elif type == "AND" or type == "NAND":
            self.non_controlling_value = D_Value.ONE

        self.explored = False

        # Distance Parameters
        self.PI_distance = 0
        self.PO_distance = 0

        # SCOAP Parameters
        self.CC0 = 0  # Combinational 0-controllability of line l.
        # The number of lines from the primary input_gates that have to be traced to put a 0 on line l.

        self.CC1 = 0  # Combinational 1-controllability of line l.
        # The number of lines from the primary input_gates that have to be traced to put a 1 on line l.

        self.CCb = 0  # Combinational observability of line l.
        # The number of lines that have to be traced to observe value of line l on a primary output.

        self.is_zero_out_controllable = False
        self.is_one_out_controllable = False

        if self.type in ["AND", "NOR", "XNOR"]:
            self.is_one_out_controllable = False
            self.is_zero_out_controllable = True
        elif ["NOT", "BUFF"]:
            self.is_one_out_controllable = True
            self.is_zero_out_controllable = True
        else:
            self.is_one_out_controllable = True
            self.is_zero_out_controllable = False

        return

    def evaluate(self):
        """
        Evaluates the value of the gate based on its type.

        This function determines the value of the gate by calling the appropriate evaluation method based on its type. If the gate is of type "AND", it calls the `evaluate_and` method. If the gate is of type "OR", it calls the `evaluate_or` method. If the gate is of type "XOR", it calls the `evaluate_xor` method. If the gate is of type "NOT", it calls the `evaluate_not` method.

        Parameters:
            self (Gate): The gate object.

        Returns:
            None
        """
        if self.type == "input_pin":
            pass
        elif self.type == "output_pin":
            self.value = self.input_gates[0].value
        elif self.type == "AND":
            self.value = self.evaluate_and()
        elif self.type == "OR":
            self.value = self.evaluate_or()
        elif self.type == "XOR":
            self.value = self.evaluate_xor()
        elif self.type == "BUFF":
            self.value = self.evaluate_buff()
        elif self.type == "NOT":
            self.value = self.evaluate_not()
        elif self.type == "NAND":
            self.value = self.evaluate_nand()
        elif self.type == "NOR":
            self.value = self.evaluate_nor()
        elif self.type == "XNOR":
            self.value = self.evaluate_xnor()

        if self.faulty:
            tempval = [self.value.value[1], self.fault_value.value[1]]
            if tempval == [1, 0]:
                self.value = D_Value.D
            elif tempval == [0, 1]:
                self.value = D_Value.D_PRIME
            elif tempval == [0, 0]:
                self.value = D_Value.ZERO
            elif tempval == [1, 1]:
                self.value = D_Value.ONE
            elif "X" in tempval:
                self.value = D_Value.X

        return

    def evaluate_and(self):
        """
        Evaluates the value of an AND gate based on its input_gates.

        This function checks the input_gates of an AND gate and determines the value based on the following rules:
        - If any input is ZERO, the value is ZERO.
        - If any input is X, the value is X.
        - If both D and D_PRIME are in the input_gates, the value is ZERO.
        - If D is in the input_gates and all input_gates are either ONE or D, the value is D.
        - If D_PRIME is in the input_gates and all input_gates are either ONE or D_PRIME, the value is D_PRIME.
        - Otherwise, the value is ONE.

        Returns:
            D_Value: The value value of the AND gate.
        """
        temp_input_gates = []
        for g in self.input_gates:
            temp_input_gates.append(g.value)

        # Check if any input is ZERO
        if D_Value.ZERO in temp_input_gates:
            return D_Value.ZERO

        # Check if any input is X
        if D_Value.X in temp_input_gates:
            return D_Value.X

        # Check if both D and D_PRIME are in the input_gates
        if D_Value.D in temp_input_gates and D_Value.D_PRIME in temp_input_gates:
            return D_Value.ZERO

        # Check if D is in the input_gates and if all input_gates are either ONE or D
        if D_Value.D in temp_input_gates:
            if all(val in [D_Value.ONE, D_Value.D] for val in temp_input_gates):
                return D_Value.D

        # Check if D_PRIME is in the input_gates and if all input_gates are either ONE or D_PRIME
        if D_Value.D_PRIME in temp_input_gates:
            if all(val in [D_Value.ONE, D_Value.D_PRIME] for val in temp_input_gates):
                return D_Value.D_PRIME

        # Return ONE if none of the above conditions are met
        return D_Value.ONE

    def evaluate_or(self):
        """
        Evaluates the value of an OR gate based on its input_gates.

        This function checks the input_gates of an OR gate and determines the value based on the following rules:
        - If any input is ONE, the value is ONE.
        - If any input is X, the value is X.
        - If both D and D_PRIME are in the input_gates, the value is ONE.
        - If D is in the input_gates and any input is either ONE or D, the value is D.
        - If D_PRIME is in the input_gates and any input is either ONE or D_PRIME, the value is D_PRIME.
        - Otherwise, the value is ZERO.

        Returns:
            D_Value: The value value of the OR gate.
        """
        temp_input_gates = []
        for g in self.input_gates:
            temp_input_gates.append(g.value)
        # Check if any input is ONE
        if D_Value.ONE in temp_input_gates:
            return D_Value.ONE

        # Check if any input is X
        if D_Value.X in temp_input_gates:
            return D_Value.X

        # Check if both D and D_PRIME are in the input_gates
        if D_Value.D in temp_input_gates and D_Value.D_PRIME in temp_input_gates:
            return D_Value.ONE

        # Check if D is in the input_gates and if all input_gates are either ONE or D
        if D_Value.D in temp_input_gates:
            if any(val in [D_Value.ONE, D_Value.D] for val in temp_input_gates):
                return D_Value.D

        # Check if D_PRIME is in the input_gates and if all input_gates are either ONE or D_PRIME
        if D_Value.D_PRIME in temp_input_gates:
            if any(val in [D_Value.ONE, D_Value.D_PRIME] for val in temp_input_gates):
                return D_Value.D_PRIME

        # Return ZERO if none of the above conditions are met
        return D_Value.ZERO

    def evaluate_xor(self):
        """
        Evaluates the value of an XOR gate based on its input_gates.

        This function checks the input_gates of an XOR gate and determines the value based on the following rules:
        - If any input is X, the value is X.
        - If the count of D and D_PRIME are not equal, the value is determined based on the count of ONE and ZERO.
        - If the count of D and D_PRIME are equal, the value is determined based on the count of ONE and ZERO and the greater count.

        Returns:
            D_Value: The value value of the XOR gate.
        """
        temp_input_gates = []
        for g in self.input_gates:
            temp_input_gates.append(g.value)
        # Count the occurrences of D and D_PRIME
        d_count = temp_input_gates.count(D_Value.D)
        d_prime_count = temp_input_gates.count(D_Value.D_PRIME)

        # Count the occurrences of ONE and ZERO
        one_count = temp_input_gates.count(D_Value.ONE)
        zero_count = temp_input_gates.count(D_Value.ZERO)

        # Count the occurrences of X
        x_count = temp_input_gates.count(D_Value.X)

        # If any input is X, the value is X
        if x_count > 0:
            return D_Value.X

        # If the count of D and D_PRIME are not equal, the value is determined based on the count of ONE and ZERO
        if d_count % 2 != d_prime_count % 2:
            if one_count % 2 == 0:
                return D_Value.ZERO
            else:
                return D_Value.ONE
        else:
            # If the count of D and D_PRIME are equal, the value is determined based on the count of ONE and ZERO and the greater count
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
        Evaluates the value of a NOT gate based on its input.

        This function checks the input of a NOT gate and determines the value based on the following rules:
        - If the input is D, the value is D_PRIME.
        - If the input is D_PRIME, the value is D.
        - If the input is ONE, the value is ZERO.
        - If the input is ZERO, the value is ONE.
        - If the input is X, the value is X.

        Returns:
            D_Value: The value value of the NOT gate.
        """
        temp_input_gates = []
        for g in self.input_gates:
            temp_input_gates.append(g.value)
        # Check the input value
        input_val = temp_input_gates[0]
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

    def evaluate_buff(self):
        """
        Evaluates the value of a BUFF gate based on its input.

        This function checks the input of a BUFF gate and determines the value based on the following rules:
        - If the input is D, the value is D.
        - If the input is D_PRIME, the value is D_PRIME.
        - If the input is X, the value is X.

        Returns:
            D_Value: The value value of the BUFF gate.
        """
        temp_input_gates = []
        for g in self.input_gates:
            temp_input_gates.append(g.value)
        # Check the input value
        return temp_input_gates[0]

    def evaluate_nand(self):
        """
        Evaluates the value of a NAND gate based on its input_gates.

        This function creates an AND gate and evaluates its value. Then, it creates a NOT gate for the AND gate's value.

        Returns:
            The value value of the NAND gate.
        """
        # Create an AND gate
        and_gate = Gate("AND", "AND", self.input_gates, None)
        and_gate.evaluate()

        # Create a NOT gate for the AND gate's value
        not_gate = Gate("NOT", "NOT", [and_gate], None)
        not_gate.evaluate()

        return not_gate.value

    def evaluate_nor(self):
        """
        Evaluates the value of a NOR gate based on its input_gates.

        This function creates an OR gate and evaluates its value. Then, it creates a NOT gate for the OR gate's value.

        Returns:
            The value value of the NOR gate.
        """

        # Create an OR gate
        or_gate = Gate("OR", "OR", self.input_gates, None)  # Create an OR gate
        or_gate.evaluate()  # Evaluate the OR gate

        # Create a NOT gate for the OR gate's value
        not_gate = Gate("NOT", "NOT", [or_gate], None)  # Create a NOT gate
        not_gate.evaluate()  # Evaluate the NOT gate

        return not_gate.value  # Return the value of the NOT gate

    def evaluate_xnor(self):
        """
        Evaluates the value of an XNOR gate based on its input_gates.

        This function creates an XOR gate and evaluates its value. Then, it creates a NOT gate for the XOR gate's value.

        Returns:
            The value value of the XNOR gate.
        """
        # Create an XOR gate
        xor_gate = Gate("XOR", "XOR", self.input_gates, None)  # Create an XOR gate
        xor_gate.evaluate()  # Evaluate the XOR gate

        # Create a NOT gate for the XOR gate's value
        not_gate = Gate("NOT", "NOT", [xor_gate], None)  # Create a NOT gate
        not_gate.evaluate()  # Evaluate the NOT gate

        return not_gate.value  # Return the value of the NOT gate

    def calculate_CC0(self):
        res = 0
        if self.type == "AND":
            res = min(g.CC0 for g in self.input_gates) + 1
        elif self.type == "NAND":
            res = sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "OR":
            res = sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "NOR":
            res = min(g.CC1 for g in self.input_gates) + 1
        elif self.type == "XOR":  # todo: support multiple inputs
            res = (
                min(
                    self.input_gates[0].CC0 + self.input_gates[1].CC0,
                    self.input_gates[0].CC1 + self.input_gates[1].CC1,
                )
                + 1
            )
        elif self.type == "XNOR":  # todo: support multiple inputs
            res = (
                min(
                    self.input_gates[0].CC1 + self.input_gates[1].CC0,
                    self.input_gates[0].CC0 + self.input_gates[1].CC1,
                )
                + 1
            )
        elif self.type == "NOT":
            res = self.input_gates[0].CC1 + 1
        elif self.type == "BUFF":
            res = self.input_gates[0].CC0 + 1
        elif self.type == "input_pin":
            res = 1
        elif self.type == "output_pin":
            res = min(g.CC0 for g in self.input_gates)

        self.CC0 = res

    def calculate_CC1(self):
        res = -1
        if self.type == "AND":
            res = sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "NAND":
            res = min(g.CC0 for g in self.input_gates) + 1
        elif self.type == "OR":
            res = min(g.CC1 for g in self.input_gates) + 1
        elif self.type == "NOR":
            res = sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "XOR":  # todo: support multiple inputs
            res = (
                min(
                    self.input_gates[0].CC0 + self.input_gates[1].CC1,
                    self.input_gates[0].CC1 + self.input_gates[1].CC0,
                )
                + 1
            )
        elif self.type == "XNOR":  # todo: support multiple inputs
            res = (
                min(
                    self.input_gates[0].CC0 + self.input_gates[1].CC0,
                    self.input_gates[0].CC1 + self.input_gates[1].CC1,
                )
                + 1
            )
        elif self.type == "NOT":
            res = self.input_gates[0].CC0 + 1
        elif self.type == "BUFF":
            res = self.input_gates[0].CC1 + 1
        elif self.type == "input_pin":
            res = 1
        elif self.type == "output_pin":
            res = min(g.CC1 for g in self.input_gates)

        self.CC1 = res

    def calculate_CCb(self):
        res = -1
        CCb_output = 0
        if self.output_gates:
            CCb_output = min(g.CCb for g in self.output_gates)
        if self.type == "AND":
            res = CCb_output + sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "NAND":
            res = CCb_output + sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "OR":
            res = CCb_output + sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "NOR":
            res = CCb_output + sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "XOR":  # todo: support XOR
            pass
        elif self.type == "XNOR":  # todo: support XNOR
            pass
        elif self.type == "NOT":
            res = CCb_output + 1
        elif self.type == "BUFF":
            res = CCb_output + 1
        elif self.type == "input_pin":
            res = CCb_output
        elif self.type == "output_pin":
            res = 0

        self.CCb = res

    def check_controllable_value(self, value):
        ret = False
        if value == D_Value.ONE:
            ret = self.is_one_out_controllable
        elif value == D_Value.ZERO:
            ret = self.is_zero_out_controllable

        return ret

    def get_easiest_to_satisfy_gate(self, objective_value):
        easiest_gate = None
        easiest_value = 0
        for gate in self.input_gates:
            if objective_value == D_Value.ZERO:
                if gate.CC0 < easiest_value:
                    easiest_gate = gate
                    easiest_value = gate.CC0
            elif objective_value == D_Value.ONE:
                if gate.CC1 < easiest_value:
                    easiest_gate = gate
                    easiest_value = gate.CC1
        return easiest_gate

    def get_hardest_to_satisfy_gate(self, objective_value):
        hardest_gate = None
        hardest_value = 0
        for gate in self.input_gates:
            if objective_value == D_Value.ZERO:
                if gate.CC0 > hardest_value:
                    hardest_gate = gate
                    hardest_value = gate.CC0
            elif objective_value == D_Value.ONE:
                if gate.CC1 > hardest_value:
                    hardest_gate = gate
                    hardest_value = gate.CC1
        return hardest_gate
