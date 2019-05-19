import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "hypernet",
    version = "0.1",
    author = "Olivier de BLIC",
    author_email = "odeblic@gmail.com",
    description = "A framework exposing different services over multiple networks",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/odeblic/hypernet",
    license = "MIT License",
    python_requires = '>=3.6, <4',
    packages = setuptools.find_packages(),
    py_modules = ['hypernet'],
    install_requires = [
        'bidict',
        'nltk',
        'pyyaml',
        ],
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

