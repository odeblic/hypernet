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
    python_requires = '==3.6.*, ==3.7.*',
    packages = setuptools.find_packages(),
    py_modules = ['hypernet'],
    install_requires = [
        'pyyaml',
        'bidict',
        'nltk',
        ],
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

