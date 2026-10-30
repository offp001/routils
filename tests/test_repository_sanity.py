
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_main_entrypoints_exist() -> None:
    assert (ROOT / "routils_windows" / "main.pyw").is_file(), "Windows main.pyw is missing"
    assert (ROOT / "routils_linux" / "main.pyw").is_file(), "Linux main.pyw is missing"


def test_dependency_manifests_exist() -> None:
    assert (ROOT / "requirements.txt").is_file(), "Root requirements.txt is missing"
    assert (ROOT / "routils_linux" / "requirements.txt").is_file(), "Linux requirements.txt is missing"


def test_readme_and_contributing_are_preserved() -> None:
    assert (ROOT / "README.md").is_file(), "README.md is missing"
    assert (ROOT / "CONTRIBUTING.md").is_file(), "CONTRIBUTING.md is missing"
