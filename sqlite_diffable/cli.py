import click
import json
import pathlib
import sqlite_utils
import sqlite3
import sys


@click.group()
@click.version_option()
def cli():
    "Tools for dumping/loading a SQLite database to diffable directory structure"
    pass


@cli.command()
@click.argument(
    "dbpath",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    required=True,
)
@click.argument(
    "output", type=click.Path(file_okay=False, dir_okay=True), required=True
)
@click.argument("tables", nargs=-1, required=False)
@click.option("--all", is_flag=True, help="Dump all tables")
def dump(dbpath, output, tables, all):
    """
    Dump a SQLite database out as flat files in the directory

    Usage:

        sqlite-diffable dump my.db output/ --all

    --all dumps ever table. Or specify tables like this:

        sqlite-diffable dump my.db output/ entries tags
    """
    if not tables and not all:
        raise click.ClickException("You must pass --all or specify some tables")
    output = pathlib.Path(output)
    output.mkdir(exist_ok=True)
    conn = sqlite_utils.Database(dbpath)
    if all:
        tables = conn.table_names()
    for table in tables:
        tablename = table.replace("/", "")
        filepath = output / "{}.ndjson".format(tablename)
        metapath = output / "{}.metadata.json".format(tablename)
        # Dump rows to filepath
        with filepath.open("w") as fp:
            for row in conn[table].rows:
                fp.write(json.dumps(list(row.values()), default=repr) + "\n")
            fp.close()
        # Dump out metadata
        metapath.open("w").write(
            json.dumps(
                {
                    "name": table,
                    "columns": [c.name for c in conn[table].columns],
                    "schema": conn[table].schema,
                },
                indent=4,
            )
        )


@cli.command()
@click.argument(
    "dbpath",
    type=click.Path(file_okay=True, allow_dash=False, dir_okay=False),
)
@click.argument(
    "directory",
    type=click.Path(file_okay=False, dir_okay=True),
)
@click.option("--replace", is_flag=True, help="Replace tables if they exist already")
def load(dbpath, directory, replace):
    """
    Load flat files from a directory into a SQLite database

    Usage:

        sqlite-diffable load my.db dump-location/
    """
    db = sqlite_utils.Database(dbpath)
    directory = pathlib.Path(directory)
    metadatas = directory.glob("*.metadata.json")
    for metadata in metadatas:
        info = json.loads(metadata.read_text())
        columns = info["columns"]
        schema = info["schema"]
        if db[info["name"]].exists() and replace:
            db[info["name"]].drop()
        try:
            db.execute(schema)
        except sqlite3.OperationalError as ex:
            msg = str(ex)
            if "already exists" in msg:
                msg += "\n\nUse the --replace option to over-write existing tables"
            raise click.ClickException(msg)
        # Now insert the rows
        ndjson = metadata.parent / metadata.stem.replace(".metadata", ".ndjson")
        rows = (
            dict(zip(columns, json.loads(line)))
            for line in ndjson.open()
            if line.strip()
        )
        db[info["name"]].insert_all(rows)


@cli.command()
@click.argument(
    "filepath",
    type=click.Path(file_okay=True, allow_dash=False, dir_okay=False, exists=True),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=True, allow_dash=True, dir_okay=False),
)
@click.option(
    "--array",
    is_flag=True,
    help="Output JSON array instead of newline-delimited objects",
)
def objects(filepath, output, array):
    """
    Output rows from a .ndjson file as newline-delimited JSON objects

    Usage:

        sqlite-diffable objects dump-location/mytable.ndjson

    This will read the column names from the accompanying .metadata.json file.
    """
    if not filepath.endswith(".ndjson"):
        raise click.ClickException("Must be a .ndjson file")
    path = pathlib.Path(filepath)
    metadata = path.parent / (path.stem + ".metadata.json")
    if not metadata.exists():
        raise click.ClickException("No accompanying .metadata.json file")
    # Read the column names
    info = json.loads(metadata.read_text())
    columns = info["columns"]
    # Output the rows
    out = sys.stdout if output is None else open(output, "w")
    if array:
        out.write("[")
    first = True
    for line in path.open():
        row = json.loads(line)
        if array and not first:
            out.write(",\n")
        else:
            out.write("\n")
        out.write(json.dumps(dict(zip(columns, row))))
        first = False
    if array:
        out.write("\n]\n")
    else:
        out.write("\n")
