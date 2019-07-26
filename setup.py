import setuptools
import sys


try:
    with open("version.txt", "r") as f:
        version = f.read()
except FileNotFoundError:
    print('You must either provide the file version.txt or build using make')
    sys.exit(1)

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = list()
    for requirement in f.readlines():
        requirement = requirement.strip().split('#')[0].strip()
        if len(requirement) > 0:
            install_requires.append(requirement)

setuptools.setup(
    name = "hypernet",
    version = version,
    author = "Olivier de BLIC",
    author_email = "odeblic@gmail.com",
    description = "A framework exposing different services over multiple networks",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/odeblic/hypernet",
    license = "MIT License",
    python_requires = '>=3.5, <4',
    packages = setuptools.find_packages(),
    #py_modules = ['hypernet'],
    install_requires = install_requires,
    classifiers = [
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {'console_scripts': [
        'hypernet = hypernet.hypernet:main',
        ]},
)

