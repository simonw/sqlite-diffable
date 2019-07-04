from click.testing import CliRunner
from sqlite_diffable import cli
import json


def test_dump(one_table_db, tmpdir):
    output_dir = tmpdir / "out"
    result = CliRunner().invoke(
        cli.cli, ["dump", one_table_db, str(output_dir), "one_table"]
    )
    assert 0 == result.exit_code, result.output
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
