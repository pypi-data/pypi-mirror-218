from setuptools import setup, find_packages

setup(
    name="linestar",
    version="0.0.1",
    description="Python client library for PLC Magnet Mover using Ethernet/IP communication",
    author="21e8",
    author_email="ops@21e8.tech",
    url="https://github.com/21e8tech/linestar",
    packages=find_packages(),
    install_requires=[
        "pycomm3",
        "python-dotenv"
    ],
)
