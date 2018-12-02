import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="primal-grakn",
    version="0.0.1",
    author="Nick Morley",
    author_email="nick.morley111@gmail.com",
    description="A convenience wrapper around the official grakn-python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclecycle/primal-grakn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['grakn==1.4.2']
)
