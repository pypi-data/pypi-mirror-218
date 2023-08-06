import sys
from termcolor import colored
from impkg.harmony import main
import pytest


@pytest.mark.parametrize(
    "inputs, expected_value",
    [
        (["1", "4", "4"], 2.0),
        (["1a", "4", "4"], 0.0),
    ],
)
def test_harmony_all(inputs, expected_value, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)

    main()

    assert capsys.readouterr().out.strip() == colored(expected_value, "red", "on_cyan", attrs=["bold"])
