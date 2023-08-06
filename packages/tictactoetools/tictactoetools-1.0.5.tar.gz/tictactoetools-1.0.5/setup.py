import setuptools
from pathlib import Path

setuptools.setup(
    name="tictactoetools",
    version="1.0.5",
    author="Simon Valentino",
    author_email="simontvalentino@gmail.com",
    url="https://github.com/SimonValentino/tictactoetools.git",
    description="Creatively build Tic-Tac-Toe matches and store their data in a database of all users.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={
        "tictactoetools": ["data/tic_tac_toe.db"]
    }
)
