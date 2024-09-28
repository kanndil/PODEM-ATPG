from setuptools import setup, find_packages

setup(
    name='podemquest',                # Name of the package
    version='0.1.0',                  # Version of the package
    packages=find_packages('src'),     # Automatically find packages in src
    package_dir={'': 'src'},           # Tell distutils packages are under src
    entry_points={
        'console_scripts': [
            'podemquest=PodemQuest:main',  # Replace with the main function if applicable
        ],
    },
    install_requires=[
        # Add any dependencies your package needs here
    ],
)
