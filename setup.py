from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="BrowserAutomator",
    version="1.0.3",
    author="EDEKA DIGITAL",
    description="A package to simplify browser automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edekadigital/BrowserAutomator",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "ruamel.yaml",
        "requests",
    ],
    python_requires='>=3.3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    exclude=["config"]
)
