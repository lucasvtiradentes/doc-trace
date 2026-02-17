import tempfile
from pathlib import Path

from docsync.commands.check import check_refs
from docsync.commands.sync import generate_sync_prompt
from docsync.core.config import Config, validate_config


def test_check_refs_valid():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        src_dir = tmppath / "src"
        src_dir.mkdir()
        (src_dir / "module.py").write_text("# module")
        doc = docs_dir / "test.md"
        doc.write_text("""# Test

related sources:
- src/module.py - module
""")
        config = Config({})
        results = list(check_refs(docs_dir, config, repo_root=tmppath))
        assert len(results) == 1
        assert results[0].ok


def test_check_refs_missing_source():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        doc = docs_dir / "test.md"
        doc.write_text("""# Test

related sources:
- src/notexist.py - missing
""")
        config = Config({})
        results = list(check_refs(docs_dir, config, repo_root=tmppath))
        assert len(results) == 1
        assert not results[0].ok
        assert len(results[0].errors) == 1
        assert "not found" in results[0].errors[0].message


def test_check_refs_missing_doc():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        doc = docs_dir / "test.md"
        doc.write_text("""# Test

related docs:
- docs/notexist.md - missing
""")
        config = Config({})
        results = list(check_refs(docs_dir, config, repo_root=tmppath))
        assert len(results) == 1
        assert not results[0].ok
        assert "not found" in results[0].errors[0].message


def test_check_refs_ignores_patterns():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "test.md").write_text("# Test\n\nrelated sources:\n- src/x.py - x")
        (docs_dir / "ignore.md").write_text("# Ignore\n\nrelated sources:\n- src/notexist.py - bad")
        config = Config({"ignored_paths": ["docs/ignore.md"]})
        results = list(check_refs(docs_dir, config, repo_root=tmppath))
        assert len(results) == 1
        assert results[0].doc_path.name == "test.md"


def test_sync_prompt_ordered():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        (tmppath / ".git").mkdir()
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "base.md").write_text("# Base\n\nrelated sources:\n- src/base.py - base")
        (docs_dir / "child.md").write_text("# Child\n\nrelated docs:\n- docs/base.md - base")
        config = Config({})
        prompt = generate_sync_prompt(docs_dir, config, incremental=False, parallel=False)
        assert "Phase 1" in prompt
        assert "Phase 2" in prompt
        assert "base.md" in prompt
        assert "child.md" in prompt


def test_sync_prompt_parallel():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        (tmppath / ".git").mkdir()
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        (docs_dir / "a.md").write_text("# A\n\nrelated sources:\n- src/a.py - a")
        (docs_dir / "b.md").write_text("# B\n\nrelated sources:\n- src/b.py - b")
        config = Config({})
        prompt = generate_sync_prompt(docs_dir, config, incremental=False, parallel=True)
        assert "PARALLEL" in prompt
        assert "Phase" not in prompt


def test_sync_prompt_no_docs():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        (tmppath / ".git").mkdir()
        docs_dir = tmppath / "docs"
        docs_dir.mkdir()
        config = Config({})
        prompt = generate_sync_prompt(docs_dir, config)
        assert "No docs to sync" in prompt


def test_validate_config_valid():
    errors = validate_config({"ignored_paths": ["*.md"], "cascade_depth_limit": 2})
    assert errors == []


def test_validate_config_unknown_key():
    errors = validate_config({"unknown_key": "value"})
    assert len(errors) == 1
    assert "unknown key" in errors[0]


def test_validate_config_invalid_ignored_paths():
    errors = validate_config({"ignored_paths": "not_a_list"})
    assert len(errors) == 1
    assert "must be a list" in errors[0]


def test_validate_config_invalid_cascade_depth():
    errors = validate_config({"cascade_depth_limit": "not_an_int"})
    assert len(errors) == 1
    assert "must be null or integer" in errors[0]
