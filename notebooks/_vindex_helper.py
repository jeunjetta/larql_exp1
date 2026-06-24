# _vindex_helper.py — shared by all notebooks, NO marimo dependency
# Mirrors logic from notebooks/_vindex_helper.py in chrishayuk/larql (to migrate to jeunjetta/larql)

"""
Shared helper module for LARQL notebooks.
Provides data detection and setup hints without requiring marimo or larql imports.
"""

from pathlib import Path
from typing import Optional, Dict, Any


def get_vindex_path(name: str = "gemma3-4b-v2.vindex") -> Optional[Path]:
    """Resolve vindex path by searching known locations. Returns Path or None."""
    candidates = [
        Path.cwd() / "output" / name,
        Path(__file__).resolve().parent.parent / "output" / name,
        Path.home() / ".cache" / "larql" / "local" / name,
    ]
    for p in candidates:
        if p.is_dir():
            return p
    return None


def check_setup() -> Dict[str, Any]:
    """Check whether setup has been done. Returns dict with status."""
    larql_ok = False
    try:
        import larql  # noqa: F401
        larql_ok = True
    except ImportError:
        pass
    
    vindex_path = get_vindex_path()
    vindex_ok = vindex_path is not None
    
    if vindex_ok and larql_ok:
        msg = f"✅ Real vindex ready: {vindex_path}"
    elif vindex_ok and not larql_ok:
        msg = "⚠️ Vindex found but `larql` not installed."
    elif not vindex_ok and larql_ok:
        msg = "⚠️ `larql` ready but no vindex found. Run `setup.py` first."
    else:
        msg = "❌ Nothing set up. Run `notebooks/setup.py` first."
    
    return {
        "vindex_available": vindex_ok,
        "vindex_path": str(vindex_path) if vindex_path else None,
        "larql_available": larql_ok,
        "setup_message": msg,
    }


def setup_hint_md() -> str:
    """Return markdown hint pointing to setup.py, empty if ready."""
    check = check_setup()
    if check["vindex_available"] and check["larql_available"]:
        return ""
    return "\n".join([
        "> 💡 **Want real data?** Run the setup notebook first:",
        "> ```bash",
        "> cd notebooks && uv run marimo edit setup.py",
        "> ```",
    ])
