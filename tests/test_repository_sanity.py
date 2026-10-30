from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_main_entrypoint_exists() -> None:
    assert (ROOT / "main.pyw").is_file(), "Expected main.pyw at the repository root"


def test_dependency_manifest_exists() -> None:
    assert (ROOT / "requirements.txt").is_file(), "Expected requirements.txt at the repository root"


def test_readme_and_contributing_are_preserved() -> None:
    assert (ROOT / "README.md").is_file(), "README.md is missing"
    assert (ROOT / "CONTRIBUTING.md").is_file(), "CONTRIBUTING.md is missing"
