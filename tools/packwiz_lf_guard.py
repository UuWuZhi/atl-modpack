#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guard packwiz refresh from CRLF-sensitive hash mismatches."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

LF_REQUIRED_SUFFIXES = {
    ".cfg",
    ".ini",
    ".js",
    ".json",
    ".json5",
    ".jsonc",
    ".md",
    ".properties",
    ".snbt",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
    ".zs",
}

LF_REQUIRED_ROOTS = (
    "mods",
    "config",
    "defaultconfigs",
    "kubejs",
    "scripts",
    "resourcepacks",
)


def requires_lf(path):
    name = path.name.casefold()
    return name.endswith(".pw.toml") or path.suffix.casefold() in LF_REQUIRED_SUFFIXES


def iter_lf_required_files():
    pack = ROOT / "pack.toml"
    if pack.is_file():
        yield pack

    for rel_root in LF_REQUIRED_ROOTS:
        root = ROOT / rel_root
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and requires_lf(path):
                yield path


def find_non_lf_files():
    bad = []
    for path in iter_lf_required_files():
        data = path.read_bytes()
        if b"\r\n" in data or b"\r" in data:
            bad.append(path.relative_to(ROOT).as_posix())
    return bad


def normalize_lf_required_files():
    """Convert refresh-sensitive text files to LF before packwiz hashes them."""
    changed = []
    for path in iter_lf_required_files():
        data = path.read_bytes()
        if b"\r\n" not in data and b"\r" not in data:
            continue
        normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if normalized != data:
            path.write_bytes(normalized)
            changed.append(path.relative_to(ROOT).as_posix())
    return changed


def ensure_lf_before_refresh():
    """Normalize indexed text files to LF, then stop if any CR remains."""
    changed = normalize_lf_required_files()
    if changed:
        print(f"[*] 已将 {len(changed)} 个 refresh 敏感文本文件统一为 LF。")
        for item in changed[:20]:
            print(f"  - {item}")
        if len(changed) > 20:
            print(f"  ... 以及 {len(changed) - 20} 个文件")

    bad = find_non_lf_files()
    if not bad:
        return

    print("[错误] 检测到 CRLF/CR 行尾,已停止 packwiz refresh。")
    print("这些文件会导致 index.toml hash 与 GitHub Pages 实际文件不一致:")
    for item in bad[:50]:
        print(f"  - {item}")
    if len(bad) > 50:
        print(f"  ... 以及 {len(bad) - 50} 个文件")
    print("请先把上述文件统一为 LF 后再发布。")
    sys.exit(1)
