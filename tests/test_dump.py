from click.testing import CliRunner
from sqlite_diffable import cli
import sqlite_utils
import json


def test_dump(one_table_db, tmpdir):
    output_dir = tmpdir / "out"
    result = CliRunner().invoke(
        cli.cli, ["dump", one_table_db, str(output_dir), "one_table"]
    )
    assert result.exit_code == 0, result.output
    # out/ should now have a single file in it
    ndjson = output_dir / "one_table.ndjson"
    metadata = output_dir / "one_table.metadata.json"
    assert ndjson.exists()
    assert metadata.exists()
    assert [[1, "Stacey"], [2, "Tilda"], [3, "Bartek"]] == [
        json.loads(line) for line in ndjson.open()
    ]
    assert {
        "name": "one_table",
        "columns": ["id", "name"],
        "schema": "CREATE TABLE [one_table] (\n   [id] INTEGER PRIMARY KEY,\n   [name] TEXT\n)",
    } == json.load(metadata)


def test_dump_all(two_tables_db, tmpdir):
    output_dir = tmpdir / "out"
    result = CliRunner().invoke(
        cli.cli, ["dump", two_tables_db, str(output_dir), "--all"]
    )
    assert result.exit_code == 0, result.output
    assert (output_dir / "one_table.ndjson").exists()
    assert (output_dir / "one_table.metadata.json").exists()
    assert (output_dir / "second_table.ndjson").exists()
    assert (output_dir / "second_table.metadata.json").exists()


def test_load(two_tables_db, tmpdir):
    output_dir = tmpdir / "out"
    restore_db = tmpdir / "restore.db"
    result = CliRunner().invoke(
        cli.cli, ["dump", str(two_tables_db), str(output_dir), "--all"]
    )
    assert result.exit_code == 0, result.output
    # Now load it again
    result2 = CliRunner().invoke(cli.cli, ["load", str(restore_db), str(output_dir)])
    assert result2.exit_code == 0, result2.output
    db = sqlite_utils.Database(str(restore_db))
    assert set(db.table_names()) == {"second_table", "one_table"}
    assert list(db["one_table"].rows) == [
        {"id": 1, "name": "Stacey"},
        {"id": 2, "name": "Tilda"},
        {"id": 3, "name": "Bartek"},
    ]
    assert list(db["second_table"].rows) == [
        {"id": 1, "name": "Cleo"},
    ]
    # Running load a second time should error
    result3 = CliRunner().invoke(cli.cli, ["load", str(restore_db), str(output_dir)])
    assert result3.exit_code == 1
    assert (
        "already exists\n\nUse the --replace option to over-write existing tables\n"
    ) in result3.output
    # Using --replace should work correctly
    (output_dir / "one_table.ndjson").write_text(
        '[1, "Stacey"]\n[2, "Tilda"]\n', "utf-8"
    )
    result4 = CliRunner().invoke(
        cli.cli, ["load", str(restore_db), str(output_dir), "--replace"]
    )
    assert result4.exit_code == 0
    assert list(db["one_table"].rows) == [
        {"id": 1, "name": "Stacey"},
        {"id": 2, "name": "Tilda"},
    ]
