from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lytics-smm-demo",
    version="0.1.1",
    author="Lytics SMM",
    description="A Python package for interacting with the Lytics SMM API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/accesstokens/lytics-smm-demo",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    python_requires=">=3.6",
)
