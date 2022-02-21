import io
import os
from setuptools import setup, find_packages

VERSION = "0.2.1"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="sqlite-diffable",
    description="Tools for dumping/loading a SQLite database to diffable directory structure",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    version=VERSION,
    license="Apache License, Version 2.0",
    packages=find_packages(exclude="tests"),
    install_requires=["click", "sqlite-utils"],
    extras_require={"test": ["pytest", "black"]},
    entry_points="""
        [console_scripts]
        sqlite-diffable=sqlite_diffable.cli:cli
    """,
    tests_require=["sqlite-diffable[test]"],
    url="https://github.com/simonw/sqlite-diffable",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
