#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建导入包 modpack.mrpack

从 packwiz 仓库生成 Modrinth 标准 .mrpack:
- modrinth.index.json:含全部 mod/资源包 的 CDN URL + sha1/sha512 哈希
- overrides/:原创内容(config/kubejs/scripts/resourcepacks) + bootstrap 工具链

哈希来源(按优先级):
1. 缓存文件(seed.json,来自原始导入包,避免重新下载)
2. 从 CDN 下载文件计算

用法:
  python build_import_pack.py [--seed 原始mrpack或seed.json] [-o 输出目录]

产出:
  <输出目录>/modpack.mrpack
"""

import json
import os
import re
import sys
import zipfile
import hashlib
import urllib.request
import tempfile
import shutil
import argparse
import io

# 修复 Windows 控制台 GBK 编码无法打印特殊符号的问题
if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("gb"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# packwiz 元数据 → Modrinth index 的字段映射需要 sha1/sha512。
# packwiz .pw.toml 只存 sha1 + 下载 URL。sha512 需从缓存或下载获得。

def read_pw_toml(path):
    """读取 packwiz .pw.toml,返回 dict。"""
    try:
        import tomllib  # Python 3.11+
    except ImportError:
        import tomli as tomllib
    with open(path, "rb") as f:
        return tomllib.load(f)

def load_seed(seed_path):
    """读取 seed 文件(mrpack 或 seed.json),返回 {path: {sha1, sha512, fileSize, downloads}}"""
    seed = {}
    if not seed_path or not os.path.exists(seed_path):
        return seed
    if seed_path.endswith(".mrpack") or seed_path.endswith(".zip"):
        z = zipfile.ZipFile(seed_path)
        idx = json.loads(z.read("modrinth.index.json"))
        for f in idx.get("files", []):
            seed[f["path"]] = {
                "sha1": f.get("hashes", {}).get("sha1"),
                "sha512": f.get("hashes", {}).get("sha512"),
                "fileSize": f.get("fileSize"),
                "downloads": f.get("downloads", []),
            }
    elif seed_path.endswith(".json"):
        seed = json.load(open(seed_path, encoding="utf-8"))
    return seed

def download_bytes(url, timeout=60):
    """下载文件内容。支持重定向。"""
    req = urllib.request.Request(url, headers={"User-Agent": "atl-build/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def compute_hashes(data):
    return {
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha512": hashlib.sha512(data).hexdigest(),
    }

def get_file_info(entry, cache):
    """获取文件的 sha1/sha512/fileSize。优先缓存,否则下载计算。"""
    path = entry["path"]
    url = entry.get("download", {}).get("url", "")
    sha1 = entry.get("download", {}).get("hash", "")

    # 查缓存
    if path in cache:
        c = cache[path]
        if c.get("sha1") and c.get("sha512"):
            return {
                "sha1": c["sha1"],
                "sha512": c["sha512"],
                "fileSize": c.get("fileSize"),
                "downloads": c.get("downloads") or [url],
            }

    # 缓存缺失,下载计算
    if url:
        try:
            data = download_bytes(url)
            h = compute_hashes(data)
            return {
                "sha1": h["sha1"],
                "sha512": h["sha512"],
                "fileSize": len(data),
                "downloads": [url],
            }
        except Exception as e:
            print(f"  [warn] 下载失败 {path}: {e}")

    # 完全无法获取:退化为仅 URL(无哈希,导入器可能报错)
    return {
        "sha1": sha1 or "",
        "sha512": "",
        "fileSize": 0,
        "downloads": [url] if url else [],
    }

def build_index(pack_dir, cache):
    """从仓库 mods/*.pw.toml + resourcepacks/*.pw.toml 生成 modrinth.index.json 的 files 列表。"""
    files = []
    mods_dir = os.path.join(pack_dir, "mods")
    rp_dir = os.path.join(pack_dir, "resourcepacks")

    for folder, prefix in [(mods_dir, "mods"), (rp_dir, "resourcepacks")]:
        if not os.path.isdir(folder):
            continue
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".pw.toml"):
                continue
            meta = read_pw_toml(os.path.join(folder, fn))
            filename = meta.get("filename", "")
            path = f"{prefix}/{filename}"
            url = meta.get("download", {}).get("url", "")
            info = get_file_info(
                {"path": path, "download": {"url": url, "hash": meta.get("download", {}).get("hash", "")}},
                cache,
            )
            # env/side 映射
            side = meta.get("side", "both")
            env = None
            if side == "client":
                env = {"client": "required", "server": "unsupported"}
            elif side == "server":
                env = {"client": "unsupported", "server": "required"}
            entry = {
                "path": path,
                "hashes": {},
                "downloads": info["downloads"],
                "fileSize": info["fileSize"],
            }
            if info["sha1"]:
                entry["hashes"]["sha1"] = info["sha1"]
            if info["sha512"]:
                entry["hashes"]["sha512"] = info["sha512"]
            if env:
                entry["env"] = env
            files.append(entry)
            print(f"  [ok] {path}")

    return files

def collect_overrides(pack_dir):
    """收集 overrides 内容:原创文件 + bootstrap 工具链。
    返回 [(arcname, abs_path)] 列表(arcname 相对 mrpack 根)。"""
    overrides = []
    root = pack_dir

    # 原创内容(config/kubejs/scripts/resourcepacks 里的非 pw.toml 文件)
    for folder in ["config", "kubejs", "scripts", "defaultconfigs", "resourcepacks"]:
        fdir = os.path.join(root, folder)
        if not os.path.isdir(fdir):
            continue
        for dirpath, _, files in os.walk(fdir):
            for fn in files:
                if fn.endswith(".pw.toml"):
                    continue  # 跳过元数据
                if fn.endswith(".jar"):
                    continue  # 跳过 jar
                abs_path = os.path.join(dirpath, fn)
                rel = os.path.relpath(abs_path, root)
                overrides.append((f"overrides/{rel}", abs_path))

    # bootstrap 工具链
    bdir = os.path.join(root, "bootstrap")
    if os.path.isdir(bdir):
        for fn in os.listdir(bdir):
            abs_path = os.path.join(bdir, fn)
            if os.path.isfile(abs_path):
                overrides.append((f"overrides/{fn}", abs_path))

    return overrides

def build_mrpack(pack_dir, output_path, cache, version):
    """构建 modpack.mrpack。"""
    print(f"[1/3] 生成 modrinth.index.json ...")
    files = build_index(pack_dir, cache)
    # 读 pack.toml 获取依赖
    pack_meta = read_pw_toml(os.path.join(pack_dir, "pack.toml"))
    versions = pack_meta.get("versions", {})
    deps = {}
    if versions.get("minecraft"):
        deps["minecraft"] = versions["minecraft"]
    if versions.get("neoforge"):
        deps["neoforge"] = versions["neoforge"]
    if versions.get("forge"):
        deps["forge"] = versions["forge"]

    manifest = {
        "game": "minecraft",
        "formatVersion": 1,
        "versionId": version or pack_meta.get("version", "1.0.0"),
        "name": pack_meta.get("name", "All The Leisures"),
        "files": files,
        "dependencies": deps,
    }

    print(f"[2/3] 收集 overrides(原创内容 + bootstrap)...")
    overrides = collect_overrides(pack_dir)

    print(f"[3/3] 打包 {output_path} ...")
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("modrinth.index.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        zf.writestr("overrides/", "")
        for arcname, abs_path in overrides:
            zf.write(abs_path, arcname)

    print(f"[✓] 完成: {output_path}")
    print(f"    mods/资源包: {len(files)} 个, overrides: {len(overrides)} 个")

def main():
    ap = argparse.ArgumentParser(description="构建导入包 mrpack")
    ap.add_argument("--seed", default=None, help="seed 文件(mrpack/zip/json),提供已知哈希避免下载")
    ap.add_argument("-o", "--output", default="dist/modpack.mrpack", help="输出路径")
    ap.add_argument("--pack-dir", default=".", help="packwiz 仓库根目录")
    ap.add_argument("--version", default=None, help="mrpack versionId(默认用 pack.toml version)")
    args = ap.parse_args()

    cache = load_seed(args.seed)
    print(f"[*] seed 哈希缓存: {len(cache)} 条")
    build_mrpack(args.pack_dir, args.output, cache, args.version)

if __name__ == "__main__":
    main()
