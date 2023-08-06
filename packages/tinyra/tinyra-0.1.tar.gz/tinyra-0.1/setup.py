from setuptools import setup

setup(
    name="tinyra",
    version="0.1",
    packages=["tinyra"],
    entry_points={
        "console_scripts": [
            "tinyra = tinyra.main:main",
        ],
    },
)
