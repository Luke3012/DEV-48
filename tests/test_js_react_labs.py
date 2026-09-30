from pathlib import Path
import os
import shutil
import subprocess

import pytest

from dev48.js_react_scaffolds import PLAIN_LABS, lab_files
from dev48.js_react_ui_scaffolds import REACT_LABS
from dev48.models import Catalog
from dev48.runners import run_lab_tests
from dev48.workspace import ensure_lab_workspace

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("lab_id", list(PLAIN_LABS))
def test_plain_lab_starter_fails_and_reference_passes(tmp_path, lab_id):
    if not shutil.which("node") or not shutil.which("npm"):
        pytest.skip("Node/npm unavailable")
    lab = Catalog(ROOT / "content").lab_by_id[lab_id]
    starter = ensure_lab_workspace(tmp_path / "starters", lab)
    if lab_id == "lab-git":
        if not shutil.which("git"):
            pytest.skip("Git unavailable")
        subprocess.run(["node", "setup.mjs"], cwd=starter, check=True, capture_output=True)
    initial = run_lab_tests(starter)
    assert not initial.passed, (lab_id, initial.output)

    completed = tmp_path / "completed" / lab_id
    for name, source in lab_files(lab, completed=True).items():
        path = completed / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    if lab_id == "lab-git":
        subprocess.run(["node", "resolve.mjs"], cwd=completed, check=True, capture_output=True)
    result = run_lab_tests(completed)
    assert result.passed, (lab_id, result.output)


@pytest.mark.parametrize("lab_id", ["lab-js-crud", "lab-react-list"])
def test_revised_lab_creation_preserves_old_and_edited_projects(tmp_path, lab_id):
    lab = Catalog(ROOT / "content").lab_by_id[lab_id]
    old = tmp_path / "old" / lab.id
    old.mkdir(parents=True)
    (old / "package.json").write_text('{"scripts":{"test":"node --test"}}', encoding="utf-8")
    (old / "solution.js").write_text("// lavoro personale\n", encoding="utf-8")
    before = {p.name: p.read_bytes() for p in old.iterdir()}
    assert ensure_lab_workspace(tmp_path / "old", lab) == old
    assert {p.name: p.read_bytes() for p in old.iterdir()} == before

    fresh = ensure_lab_workspace(tmp_path / "fresh", lab)
    assert (fresh / "dev48-scaffold.json").is_file()
    for name in ["solution.mjs", "solution.test.mjs", "README.md", "SOLUTION.md"]:
        (fresh / name).write_text("// modifica personale\n", encoding="utf-8")
    before = {str(p.relative_to(fresh)): p.read_bytes() for p in fresh.rglob("*") if p.is_file()}
    ensure_lab_workspace(tmp_path / "fresh", lab)
    assert {str(p.relative_to(fresh)): p.read_bytes() for p in fresh.rglob("*") if p.is_file()} == before


def test_all_twelve_existing_lab_ids_have_distinct_contracts_and_starters():
    catalog = Catalog(ROOT / "content")
    assert set(PLAIN_LABS) | set(REACT_LABS) == {lab.id for lab in catalog.labs}
    briefs = [lab.requirements for lab in catalog.labs]
    assert len(set(briefs)) == 12
    assert set(PLAIN_LABS).isdisjoint(REACT_LABS)


@pytest.mark.parametrize("lab_id", list(REACT_LABS))
def test_react_lab_starter_fails_and_reference_passes(tmp_path, lab_id):
    modules = os.environ.get("DEV48_REACT_NODE_MODULES")
    if not modules or not Path(modules, "vitest", "package.json").is_file():
        pytest.skip("Set DEV48_REACT_NODE_MODULES to an installed React lab's node_modules for UI execution")
    lab = Catalog(ROOT / "content").lab_by_id[lab_id]
    for completed in [False, True]:
        project = tmp_path / ("completed" if completed else "starter")
        for name, source in lab_files(lab, completed=completed).items():
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding="utf-8")
        destination = project / "node_modules"
        if os.name == "nt":
            # One native PowerShell command; paths are literals and no tree is deleted.
            dest_literal = str(destination).replace("'", "''")
            source_literal = str(Path(modules).resolve()).replace("'", "''")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                f"New-Item -ItemType Junction -Path '{dest_literal}' -Target '{source_literal}' | Out-Null"],
                check=True, capture_output=True)
        else:
            destination.symlink_to(Path(modules).resolve(), target_is_directory=True)
        result = run_lab_tests(project)
        assert result.passed is completed, (lab_id, completed, result.output)
