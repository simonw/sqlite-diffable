# sqlite-diffable

[![PyPI](https://img.shields.io/pypi/v/sqlite-diffable.svg)](https://pypi.org/project/sqlite-diffable/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-diffable?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-diffable/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-diffable/blob/main/LICENSE)

Tools for dumping/loading a SQLite database to diffable directory structure

Installation:

    pip install sqlite-diffable

Usage:

    sqlite-diffable dump fixtures.db out/ facetable

This dumps the table called `facetable` from `fixtures.db` into the `out/` directory.

To dump out all tables, use `--all`:

    sqlite-diffable dump fixtures.db out/ --all
