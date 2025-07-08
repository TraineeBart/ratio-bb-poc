# setup.py
from setuptools import setup, find_packages

setup(
    name="ratio-bb-poc",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests",
        "pandas",
        # … vul hier eventueel je overige requirements in …
    ],
)