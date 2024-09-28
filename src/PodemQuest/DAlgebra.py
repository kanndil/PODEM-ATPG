# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/

# Copyright (c) 2024, Youssef Kandil (youssefkandil@aucegypt.edu) 
#                     Mohamed Shalan (mshalan@aucegypt.edu)
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

from enum import Enum


class D_Value(Enum):
    """
    The D_Value class represents the D value of a gate {0,1,D,D',x}.
    """

    ZERO = [0, 0]
    ONE = [1, 1]
    D = [1, 0]
    D_PRIME = [0, 1]
    X = ["X", "X"]
