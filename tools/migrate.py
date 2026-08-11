#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mrpack → packwiz 迁移脚本
读取 Modrinth .mrpack 的 modrinth.index.json,为每个文件生成 packwiz 元数据 (.pw.toml)。

用法:
  python migrate.py <modpack.mrpack> <输出目录>

输出:
  <输出目录>/mods/*.pw.toml     — 每个 mod 的元数据
  <输出目录>/_missing_update.json — 无 Modrinth update 块的文件清单(纯 CurseForge,需人工处理)
  <输出目录>/_side_report.json    — side 判定报告(待人工核对)

依赖:
  Python 3.6+, 需要网络访问 Modrinth API (https://api.modrinth.com)
"""

import json
import re
import sys
import os
import urllib.request
import time
import hashlib

# 修复 Windows 控制台 GBK 编码无法打印特殊符号的问题
if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("gb"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MODRINTH_CDN_RE = re.compile(
    r"https://cdn\.modrinth\.com/data/([^/]+)/versions/([^/]+)/",
    re.IGNORECASE,
)
CURSEFORGE_URL_RE = re.compile(
    r"https?://[^/]+/files/(\d+)/(\d+)/", re.IGNORECASE
)

def modrinth_api(path, api_key=None):
    """调用 Modrinth API,返回解析后的 JSON。带简单重试与限速。"""
    url = f"https://api.modrinth.com/v2/{path}"
    headers = {"User-Agent": "atl-modpack-migrate/1.0"}
    if api_key:
        headers["Authorization"] = api_key
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt == 2:
                return {"error": str(e)}
            time.sleep(2 * (attempt + 1))
    return {"error": "unknown"}


def cf_file_id_to_project(file_id, api_key):
    """(预留)用 CurseForge API 把 file-id 反查 project-id。
    需要 CURSEFORGE_API_KEY 环境变量;无 key 时返回 None。"""
    key = api_key or os.environ.get("CURSEFORGE_API_KEY")
    if not key:
        return None
    url = f"https://api.curseforge.com/v1/mods/{file_id}"
    try:
        req = urllib.request.Request(
            url, headers={"Accept": "application/json", "x-api-key": key}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", {}).get("id")
    except Exception:
        return None


def make_pw_toml(file_entry, side, update_block, name):
    """生成 packwiz .pw.toml 内容。"""
    path = file_entry["path"]
    filename = os.path.basename(path)
    sha1 = file_entry.get("hashes", {}).get("sha1", "")
    downloads = file_entry.get("downloads", [])
    # 优先 Modrinth CDN(对国内玩家通常比 CurseForge 可达),其次第一个可用源
    url = ""
    for u in downloads:
        if "modrinth.com" in u:
            url = u
            break
    if not url and downloads:
        url = downloads[0]

    # 文件名中若含非法字符,packwiz 文件名需清理
    safe_name = re.sub(r"[^a-zA-Z0-9_.+\\-]", "_", name or filename)

    lines = []
    lines.append(f'name = "{name or filename}"')
    lines.append(f'filename = "{filename}"')
    if side:
        lines.append(f'side = "{side}"')
    lines.append("")
    lines.append("[download]")
    lines.append(f'url = "{url}"')
    lines.append('hash-format = "sha1"')
    lines.append(f'hash = "{sha1}"')
    if update_block:
        lines.append("")
        lines.append("[update]")
        lines.append(update_block)
    return "\n".join(lines) + "\n", safe_name


def build_update_block(file_entry):
    """根据文件 URL 生成 [update.modrinth] 或 [update.curseforge] 块。
    返回 (block_str, update_type) ;无来源时返回 (None, None)。"""
    downloads = file_entry.get("downloads", [])
    for u in downloads:
        m = MODRINTH_CDN_RE.search(u)
        if m:
            mod_id, version_id = m.group(1), m.group(2)
            return (
                f'[update.modrinth]\n'
                f'mod-id = "{mod_id}"\n'
                f'version = "{version_id}"',
                "modrinth",
            )
    for u in downloads:
        m = CURSEFORGE_URL_RE.search(u)
        if m:
            file_id = f"{m.group(1)}{m.group(2)}"
            return (
                f'[update.curseforge]\n'
                f'file-id = {file_id}',
                "curseforge",
            )
    return None, None


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    mrpack_path, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(out_dir, "mods"), exist_ok=True)

    # 读 mrpack
    with open(mrpack_path, "rb") as f:
        mrpack = json.loads(json.load(f) or b"{}") if mrpack_path.endswith(".json") else None
    # mrpack 是 zip,内嵌 modrinth.index.json
    import zipfile
    with zipfile.ZipFile(mrpack_path) as z:
        index = json.loads(z.read("modrinth.index.json"))

    files = index["files"]
    print(f"[*] 共 {len(files)} 个文件")
    deps = index.get("dependencies", {})
    print(f"[*] Minecraft {deps.get('minecraft')} / NeoForge {deps.get('neoforge')}")

    missing_update = []
    side_report = []
    generated = []

    # 若目标 .pw.toml 已存在,跳过 side 的 API 查询(幂等快速重跑)
    def target_exists(fe):
        _name = os.path.splitext(os.path.basename(fe["path"]))[0]
        _safe = re.sub(r"[^a-zA-Z0-9_.+\\-]", "_", _name)
        _dir = "mods" if fe["path"].startswith("mods/") else "resourcepacks"
        return os.path.exists(os.path.join(out_dir, _dir, f"{_safe}.pw.toml"))

    for i, fe in enumerate(files):
        path = fe["path"]
        # 仅处理有下载源的路径(排除 overrides 里的原创文件,那些直接复制入库)
        if not fe.get("downloads"):
            continue
        is_mod = path.startswith("mods/")
        is_rp = path.startswith("resourcepacks/")
        if not is_mod and not is_rp:
            continue

        # 若目标 .pw.toml 已存在,跳过全部处理(保留人工修正,仅记入统计)
        if target_exists(fe):
            # 读取现有 side 计入报告
            _name = os.path.splitext(os.path.basename(fe["path"]))[0]
            _safe = re.sub(r"[^a-zA-Z0-9_.+\\-]", "_", _name)
            _dir = "mods" if fe["path"].startswith("mods/") else "resourcepacks"
            _existing = open(os.path.join(out_dir, _dir, f"{_safe}.pw.toml"), encoding="utf-8").read()
            _sm = re.search(r'^side = "(\w+)"', _existing, re.M)
            _um = re.search(r"^\[update\.(\w+)\]", _existing, re.M)
            side_report.append({
                "path": fe["path"], "source": "existing",
                "side": _sm.group(1) if _sm else None,
                "update": _um.group(1) if _um else None,
            })
            generated.append(fe["path"])
            continue

        # 解析 update 块
        update_block, update_type = build_update_block(fe)

        # side 判定(mods 才需要;资源包侧不重要)
        side = None
        if is_mod and update_type == "modrinth":
            mod_id = None
            for u in fe.get("downloads", []):
                m = MODRINTH_CDN_RE.search(u)
                if m:
                    mod_id = m.group(1)
                    break
            if not mod_id:
                side_report.append({
                    "path": path, "mod_id": None,
                    "error": "build_update_block 判定 modrinth 但未找到 mod-id", "side": None,
                })
            else:
                proj = modrinth_api(f"project/{mod_id}")
                if "error" not in proj:
                    cs, ss = proj.get("client_side"), proj.get("server_side")
                    if cs and ss:
                        if cs == "required" and ss == "required":
                            side = "both"
                        elif cs == "required" and ss in ("optional", "unsupported"):
                            side = "client"
                        elif cs in ("optional", "unsupported") and ss == "required":
                            side = "server"
                        else:
                            side = "both"  # 默认
                    side_report.append({
                        "path": path, "mod_id": mod_id,
                        "client_side": cs, "server_side": ss, "side": side,
                    })
                else:
                    side_report.append({
                        "path": path, "mod_id": mod_id,
                        "error": proj.get("error"), "side": None,
                    })
                time.sleep(0.1)  # 限速,避免 300/min 上限
        elif is_mod and update_type == "curseforge":
            # 纯 CF:侧人工核对(默认 both,记入报告)
            side_report.append({
                "path": path, "source": "curseforge",
                "note": "纯 CurseForge,side 默认 both,请人工核对", "side": "both",
            })
            side = "both"
            missing_update.append({
                "path": path, "reason": "无 Modrinth update 块,update.curseforge 需人工确认 file-id",
            })
        elif is_mod:
            side_report.append({
                "path": path, "source": "unknown",
                "note": "无已知下载源,需人工处理", "side": None,
            })
            missing_update.append({"path": path, "reason": "无已知下载源"})

        # 生成 .pw.toml
        name = os.path.splitext(os.path.basename(path))[0]
        content, safe_name = make_pw_toml(fe, side, update_block, name)
        out_dir_file = "mods" if is_mod else "resourcepacks"
        os.makedirs(os.path.join(out_dir, out_dir_file), exist_ok=True)
        out_path = os.path.join(out_dir, out_dir_file, f"{safe_name}.pw.toml")
        # 幂等:已存在的文件不重写(保留人工修正)
        if not os.path.exists(out_path):
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
        generated.append(out_path)
        if (i + 1) % 25 == 0:
            print(f"[*] 已处理 {i + 1}/{len(files)}")

    # 写报告
    with open(os.path.join(out_dir, "_missing_update.json"), "w", encoding="utf-8") as f:
        json.dump(missing_update, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "_side_report.json"), "w", encoding="utf-8") as f:
        json.dump(side_report, f, ensure_ascii=False, indent=2)

    print(f"[✓] 生成 {len(generated)} 个 .pw.toml")
    print(f"[!] 待处理 update: {len(missing_update)} 个(见 _missing_update.json)")
    print(f"[!] side 判定: {len(side_report)} 个(见 _side_report.json)")


if __name__ == "__main__":
    main()
