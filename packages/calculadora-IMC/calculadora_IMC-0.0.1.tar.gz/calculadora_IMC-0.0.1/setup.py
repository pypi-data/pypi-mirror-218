from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()
    
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    
setup(
    name="calculadora_IMC",
    version="0.0.1",
    author="Ytalo Hanieri Brito",
    author_email="hanieri21@gmail.com",
    description="Calculadora de IMC simples",
    long_description_content_type="text/markdown",
    url="https://github.com/Hanieri21/Hanieri21/tree/imc/Calculadora%20IMC",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)