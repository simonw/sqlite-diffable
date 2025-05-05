import sqlite_diffable
import json
import sqlite_utils

def test_dump_module(one_table_db, tmpdir):
    output_dir = tmpdir / "out"
    sqlite_diffable.dump(one_table_db, str(output_dir), tables=["one_table"])
    
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

def test_dump_all_module(two_tables_db, tmpdir):
    output_dir = tmpdir / "out"
    sqlite_diffable.dump(two_tables_db, str(output_dir), all=True)
    assert (output_dir / "one_table.ndjson").exists()
    assert (output_dir / "one_table.metadata.json").exists()
    assert (output_dir / "second_table.ndjson").exists()
    assert (output_dir / "second_table.metadata.json").exists()

def test_load(two_tables_db, tmpdir):
    output_dir = tmpdir / "out"
    restore_db = str(tmpdir / "restore.db")
    sqlite_diffable.dump(two_tables_db, str(output_dir), all=True)

    sqlite_diffable.load(restore_db, str(output_dir))

    db = sqlite_utils.Database(restore_db)
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
    result = sqlite_diffable.load(restore_db, str(output_dir))
    assert not result

    (output_dir / "one_table.ndjson").write_text(
        '[1, "Stacey"]\n[2, "Tilda"]\n', "utf-8"
    )
    result = sqlite_diffable.load(restore_db, str(output_dir), replace=True)
    assert result
    assert list(db["one_table"].rows) == [
        {"id": 1, "name": "Stacey"},
        {"id": 2, "name": "Tilda"},
    ]    

