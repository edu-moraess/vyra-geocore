import ast
import os
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src"
FORBIDDEN = {"numpy", "cv2", "torch", "ultralytics", "pytest"}
ALLOWED_OPTIONAL_DIRS = {"adapters"}  # onde bibliotecas pesadas poderão viver (fases 2-3)


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return names


def test_domain_imports_only_stdlib_and_vyra():
    allowed = set(sys.stdlib_module_names) | {"vyra"}
    for path in (SRC / "vyra" / "domain").glob("*.py"):
        extra = _imports(path) - allowed
        assert not extra, f"{path.name} importa fora da stdlib: {sorted(extra)}"


def test_no_heavy_libs_outside_adapters():
    for path in (SRC / "vyra").rglob("*.py"):
        if ALLOWED_OPTIONAL_DIRS & set(path.parts):
            continue
        top_level = _imports(path)
        if path.name == "env.py":  # import de torch é local, opcional e só com --gpu
            top_level = {n for n in top_level if n != "torch"}
        assert not (top_level & FORBIDDEN), f"{path} importa {top_level & FORBIDDEN}"


def test_core_loads_without_heavy_modules():
    code = (
        "import sys, vyra, vyra.domain.contracts, vyra.domain.serialization, vyra.env;"
        "vyra.env.diagnose();"
        f"bad = sorted(m for m in {sorted(FORBIDDEN - {'pytest'})!r} if m in sys.modules);"
        "print(','.join(bad)); sys.exit(1 if bad else 0)"
    )
    env = dict(os.environ, PYTHONPATH=str(SRC))
    res = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert res.returncode == 0, f"módulos pesados carregados: {res.stdout}{res.stderr}"
