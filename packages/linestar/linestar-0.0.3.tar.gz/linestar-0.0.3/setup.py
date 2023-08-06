from setuptools import setup, find_packages

f = open('README.md', 'r')
fileString = f.read()

setup(
    name="linestar",
    version="0.0.3",
    description="Python client library for PLC Magnet Mover using Ethernet/IP communication",
    long_description=fileString,
    long_description_content_type='text/markdown',
    author="21e8",
    author_email="ops@21e8.tech",
    url="https://github.com/21e8tech/linestar",
    packages=find_packages(),
    install_requires=[
        "pycomm3",
        "python-dotenv",
        "click",
        "flask",
        "flask-restplus"
    ],
)
