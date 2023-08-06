import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qiskit-han",
    version="0.6.0",
    description="A quantum provider for Qiskit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["quantier"],
    package_dir={"quantier": "quantier"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "qiskit",
        "qiskit-aer"
        "mysql-connector-python",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)