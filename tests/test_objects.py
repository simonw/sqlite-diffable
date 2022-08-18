from click.testing import CliRunner
from sqlite_diffable import cli
import pytest


@pytest.mark.parametrize(
    "options,expected_output",
    (
        (
            [],
            (
                '\n{"id": 1, "name": "Stacey"}\n'
                '{"id": 2, "name": "Tilda"}\n'
                '{"id": 3, "name": "Bartek"}\n'
            ),
        ),
        (
            ["--array"],
            (
                '[\n{"id": 1, "name": "Stacey"},\n'
                '{"id": 2, "name": "Tilda"},\n'
                '{"id": 3, "name": "Bartek"}\n]\n'
            ),
        ),
    ),
)
def test_dump(one_table_db, tmpdir, options, expected_output):
    output_dir = tmpdir / "out"
    result = CliRunner().invoke(
        cli.cli, ["dump", one_table_db, str(output_dir), "one_table"]
    )
    assert result.exit_code == 0, result.output
    result2 = CliRunner().invoke(
        cli.cli, ["objects", str(output_dir / "one_table.ndjson")] + options
    )
    assert result2.output == expected_output
