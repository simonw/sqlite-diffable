# sqlite-diffable

[![PyPI](https://img.shields.io/pypi/v/sqlite-diffable.svg)](https://pypi.org/project/sqlite-diffable/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-diffable?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-diffable/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-diffable/blob/main/LICENSE)

Tools for dumping/loading a SQLite database to diffable directory structure

## Installation

    pip install sqlite-diffable

## Dumping a database

Given a SQLite database called `fixtures.db` containing a table `facetable`, the following will dump out that table to the `dump/` directory:

    sqlite-diffable dump fixtures.db dump/ facetable

To dump out every table in that database, use `--all`:

    sqlite-diffable dump fixtures.db dump/ --all

## Loading a database

To load a previously dumped database, run the following:

    sqlite-diffable load restored.db dump/

This will show an error if any of the tables that are being restored already exist in the database file.

You can replace those tables (dropping them before restoring them) using the `--replace` option:

    sqlite-diffable load restored.db dump/ --replace

## Demo

The repository at [simonw/simonwillisonblog-backup](https://github.com/simonw/simonwillisonblog-backup) contains a backup of the database on my blog, https://simonwillison.net/ - created using this tool.

## Format

Each table is represented as two files. The first, `table_name.metadata.json`, contains metadata describing the structure of the table. For a table called `redirects_redirect` that file might look like this:

```json
{
    "name": "redirects_redirect",
    "columns": [
        "id",
        "domain",
        "path",
        "target",
        "created"
    ],
    "schema": "CREATE TABLE [redirects_redirect] (\n   [id] INTEGER PRIMARY KEY,\n   [domain] TEXT,\n   [path] TEXT,\n   [target] TEXT,\n   [created] TEXT\n)"
}
```

It is an object with three keys: `name` is the name of the table, `columns` is an array of column strings and `schema` is the SQL schema text used for tha table.

The second file, `table_name.ndjson`, contains [newline-delimeted JSON] for every row in the table. Each row is represented as a JSON array with items corresponding to each of the columns defined in the metadata.

That file for the `redirects_redirect.ndjson` table might look like this:

```
[1, "feeds.simonwillison.net", "swn-everything", "https://simonwillison.net/atom/everything/", "2017-10-01T21:11:36.440537+00:00"]
[2, "feeds.simonwillison.net", "swn-entries", "https://simonwillison.net/atom/entries/", "2017-10-01T21:12:32.478849+00:00"]
[3, "feeds.simonwillison.net", "swn-links", "https://simonwillison.net/atom/links/", "2017-10-01T21:12:54.820729+00:00"]
```
