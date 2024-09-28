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

from setuptools import setup, find_packages

setup(
    name="podemquest",  # Name of the package
    version="0.1.0",  # Version of the package
    packages=find_packages("src"),  # Automatically find packages in src
    package_dir={"": "src"},  # Tell distutils packages are under src
    entry_points={
        "console_scripts": [
            "podemquest=PodemQuest:main",  # Replace with the main function if applicable
        ],
    },
    install_requires=[
        # Add any dependencies your package needs here
    ],
    authors="Youssef Kandil, Mohamed Shalan",
    author_email="youssefkandil@aucegypt.edu, mshalan@aucegypt.edu",
)
