#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式管理外部资源(Mod / Resourcepack)。

外部资源指由 packwiz 通过 Modrinth / CurseForge / 直链追踪的文件:
  - 添加: 生成 .pw.toml 元数据,不把第三方 jar/zip 放进仓库/Pages
  - 移除: 删除 .pw.toml 元数据,并删除工作区中同名落地文件
  - 每次变更后自动 packwiz refresh
"""

import shutil
import subprocess
import sys
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from packwiz_lf_guard import ensure_lf_before_refresh

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PACKWIZ_EXE = ROOT / "tools" / "packwiz-cli" / "packwiz.exe"
MODRINTH_API = "https://api.modrinth.com/v2"
USER_AGENT = "atl-modpack-tool/1.0 (packwiz metadata helper)"
RESOURCE_KINDS = {
    "1": {
        "name": "Mod",
        "folder": ROOT / "mods",
        "meta_folder": "mods",
        "default_side": "both",
        "extensions": {".jar"},
        "modrinth_type": "mod",
    },
    "2": {
        "name": "Resourcepack",
        "folder": ROOT / "resourcepacks",
        "meta_folder": "resourcepacks",
        "default_side": "client",
        "extensions": {".zip"},
        "modrinth_type": "resourcepack",
    },
}


def resolve_packwiz():
    if PACKWIZ_EXE.exists():
        return [str(PACKWIZ_EXE)]
    if shutil.which("packwiz"):
        return ["packwiz"]
    raise FileNotFoundError("找不到 packwiz.exe,也找不到 PATH 中的 packwiz 命令")


def run(cmd):
    print(f"> {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def read_meta(path):
    with path.open("rb") as fh:
        return tomllib.load(fh)


def metadata_paths(folder):
    if not folder.is_dir():
        return []
    return sorted(folder.glob("*.pw.toml"))


def snapshot_metadata(folder):
    return {path: path.read_bytes() for path in metadata_paths(folder)}


def detect_changed_metadata(folder, before):
    changed = []
    for path in metadata_paths(folder):
        data = path.read_bytes()
        if path not in before or before[path] != data:
            changed.append(path)
    return sorted(changed)


def rollback_metadata(folder, before):
    touched = False
    current = set(metadata_paths(folder))
    for path in sorted(current):
        if path not in before:
            path.unlink()
            print(f"已回滚新增元数据: {path.relative_to(ROOT)}")
            touched = True
        elif path.read_bytes() != before[path]:
            path.write_bytes(before[path])
            print(f"已恢复元数据: {path.relative_to(ROOT)}")
            touched = True
    for path, data in before.items():
        if not path.exists():
            path.write_bytes(data)
            print(f"已恢复被删除元数据: {path.relative_to(ROOT)}")
            touched = True
    return touched


def source_of(meta):
    update = meta.get("update", {})
    if "modrinth" in update:
        return "Modrinth"
    if "curseforge" in update:
        return "CurseForge"
    return "Direct URL"


def http_get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise RuntimeError(f"HTTP {exc.code}: {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"请求失败: {url}: {exc.reason}") from exc


def modrinth_project(project_id):
    safe_id = urllib.parse.quote(project_id, safe="")
    return http_get_json(f"{MODRINTH_API}/project/{safe_id}")


def hash_file(path, algorithm):
    h = hashlib.new(algorithm)
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_metadata(kind, paths):
    errors = []
    warnings = []
    expected_ext = kind["extensions"]
    expected_type = kind["modrinth_type"]

    for path in paths:
        try:
            meta = read_meta(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)} 无法读取: {exc}")
            continue

        filename = meta.get("filename", "")
        suffix = Path(filename).suffix.casefold()
        if suffix not in expected_ext:
            exts = "/".join(sorted(expected_ext))
            errors.append(
                f"{path.relative_to(ROOT)} 的 filename 是 {filename!r},不符合 {kind['name']} 预期扩展名 {exts}"
            )

        update = meta.get("update", {})
        modrinth = update.get("modrinth")
        if modrinth:
            project_id = modrinth.get("mod-id")
            if not project_id:
                errors.append(f"{path.relative_to(ROOT)} 缺少 update.modrinth.mod-id")
                continue
            try:
                project = modrinth_project(project_id)
            except RuntimeError as exc:
                warnings.append(f"{path.relative_to(ROOT)} 未能复核 Modrinth 项目类型: {exc}")
                continue
            if not project:
                errors.append(f"{path.relative_to(ROOT)} 对应的 Modrinth 项目不存在: {project_id}")
                continue
            actual_type = project.get("project_type")
            if actual_type != expected_type:
                title = project.get("title", project_id)
                errors.append(
                    f"{path.relative_to(ROOT)} 指向 Modrinth {actual_type!r} 项目 {title!r},"
                    f"但当前选择的是 {kind['name']}"
                )

    return errors, warnings


def validate_or_rollback(kind, folder, before, changed):
    errors, warnings = validate_metadata(kind, changed)
    for warning in warnings:
        print(f"[警告] {warning}")
    if not errors:
        return True

    print("\n[错误] 新增/变更的外部资源未通过类型复核:")
    for error in errors:
        print(f"  - {error}")
    rollback_metadata(folder, before)
    refresh()
    print("已回滚本次添加。")
    return False


def format_candidate(path):
    try:
        meta = read_meta(path)
    except Exception:
        return str(path.relative_to(ROOT))
    name = meta.get("name", path.stem)
    filename = meta.get("filename", "")
    side = meta.get("side", "both")
    source = source_of(meta)
    extra = f" | {filename}" if filename else ""
    return f"{path.relative_to(ROOT)} | {name}{extra} | {source} | side={side}"


def pick_candidate(paths, prompt):
    if not paths:
        return None
    if len(paths) == 1:
        print(f"已选择: {format_candidate(paths[0])}")
        return paths[0]

    print()
    for idx, path in enumerate(paths, 1):
        print(f"  {idx}. {format_candidate(path)}")

    while True:
        choice = input(prompt).strip()
        if not choice:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(paths):
            return paths[int(choice) - 1]
        print("无效选择。")


def set_side(path, side):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    side_line = f'side = "{side}"'

    for idx, line in enumerate(lines):
        if line.strip().startswith("side = "):
            lines[idx] = side_line
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return

    insert_at = len(lines)
    for idx, line in enumerate(lines):
        if line.startswith("["):
            insert_at = idx
            break

    lines.insert(insert_at, side_line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def choose_side(default_side):
    print("\n设置 side:")
    print("  1. both(客户端 + 服务器)")
    print("  2. client(仅客户端)")
    print("  3. server(仅服务器)")
    print(f"  0. 使用默认({default_side})")

    mapping = {"1": "both", "2": "client", "3": "server"}
    while True:
        choice = input("请选择: ").strip()
        if choice == "0" or choice == "":
            return default_side
        if choice in mapping:
            return mapping[choice]
        print("无效选择。")


def confirm_warning(lines):
    print("\n警告:")
    for line in lines:
        print(f"  - {line}")
    answer = input("确认继续? 输入 YES: ").strip()
    return answer == "YES"


def choose_kind():
    print("\n资源类型:")
    print("  1. Mod")
    print("  2. Resourcepack")
    print("  0. 返回")
    choice = input("请选择: ").strip()
    if choice in RESOURCE_KINDS:
        return RESOURCE_KINDS[choice]
    if choice == "0" or choice == "":
        return None
    print("无效选择。")
    return None


def choose_source():
    print("\n来源:")
    print("  1. Modrinth")
    print("  2. CurseForge")
    print("  3. 本地文件反查")
    print("  4. 直链 URL")
    print("  0. 返回")
    choice = input("请选择: ").strip()
    if choice in {"1", "2", "3", "4"}:
        return choice
    if choice == "0" or choice == "":
        return None
    print("无效选择。")
    return None


def add_resource():
    kind = choose_kind()
    if not kind:
        print("已取消。")
        return
    kind_name = kind["name"]
    folder = kind["folder"]
    meta_folder = kind["meta_folder"]
    default_side = kind["default_side"]

    source = choose_source()
    if not source:
        print("已取消。")
        return

    warnings = [
        "这是第三方外部资源,只应提交 packwiz 元数据;不要把非原创 jar/zip 提交进仓库或 Pages。",
        "资源可用性、许可和下架风险由原站点/作者决定,维护人需要自行确认分发许可。",
    ]
    if source == "3":
        if add_from_local_file(kind):
            print("完成。")
        return

    if source == "4":
        warnings.append("直链 URL 通常没有依赖解析和自动更新信息;优先使用 Modrinth/CurseForge 条目。")
    if not confirm_warning(warnings):
        print("已取消。")
        return

    before = snapshot_metadata(folder)
    cmd = resolve_packwiz()
    if source == "1":
        query = input("输入 Modrinth URL / slug / 项目 ID / 搜索词: ").strip().strip('"')
        if not query:
            print("已取消。")
            return
        cmd += ["--meta-folder", meta_folder, "modrinth", "add", query]
    elif source == "2":
        query = input("输入 CurseForge URL / slug / ID / 搜索词: ").strip().strip('"')
        if not query:
            print("已取消。")
            return
        default_category = "mc-mods" if kind_name == "Mod" else "texture-packs"
        category = input(f"CurseForge category(回车默认 {default_category}): ").strip() or default_category
        game = input("CurseForge game(回车默认 minecraft): ").strip()
        cmd += ["--meta-folder", meta_folder, "curseforge", "add", "--category", category]
        if game:
            cmd += ["--game", game]
        cmd.append(query)
    else:
        name = input("资源显示名称: ").strip()
        url = input("直接下载 URL: ").strip().strip('"')
        if not name or not url:
            print("已取消。")
            return
        meta_name = input("元数据文件名(可选,不含 .pw.toml): ").strip()
        cmd += ["--meta-folder", meta_folder, "url", "add", name, url]
        if meta_name:
            cmd += ["--meta-name", meta_name]

    print()
    run(cmd)

    changed = detect_changed_metadata(folder, before)
    if not changed:
        print("\n未检测到新增/变更的 .pw.toml 文件,仍将刷新索引。")
        refresh()
        return

    if not validate_or_rollback(kind, folder, before, changed):
        return

    target = pick_candidate(changed, "选择主条目(回车跳过 side 设置): ")
    if target:
        side = choose_side(default_side)
        set_side(target, side)
        print(f"\n已更新 {target.relative_to(ROOT)} 的 side = \"{side}\"")

    refresh()
    print("完成。")


def resolve_local_file(kind):
    path_text = input("输入本地文件路径: ").strip().strip('"')
    if not path_text:
        print("已取消。")
        return None
    path = Path(path_text)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    if not path.is_file():
        print(f"文件不存在: {path}")
        return None
    suffix = path.suffix.casefold()
    if suffix not in kind["extensions"]:
        exts = "/".join(sorted(kind["extensions"]))
        print(f"{kind['name']} 反查只接受 {exts},当前文件是 {path.name}")
        return None
    return path


def choose_reverse_source(kind):
    print("\n反查来源:")
    print("  1. Modrinth(hash 精确匹配)")
    if kind["name"] == "Mod":
        print("  2. CurseForge(packwiz detect,实验功能)")
    print("  0. 返回")
    choice = input("请选择: ").strip()
    if choice == "1":
        return "modrinth"
    if choice == "2" and kind["name"] == "Mod":
        return "curseforge"
    if choice == "0" or choice == "":
        return None
    print("无效选择。")
    return None


def modrinth_version_from_file(path):
    sha512 = hash_file(path, "sha512")
    sha1 = hash_file(path, "sha1")
    url = f"{MODRINTH_API}/version_file/{sha512}?algorithm=sha512"
    version = http_get_json(url)
    if not version:
        return None

    matched_file = None
    for item in version.get("files", []):
        hashes = item.get("hashes", {})
        if hashes.get("sha512") == sha512 or hashes.get("sha1") == sha1:
            matched_file = item
            break
    if not matched_file:
        raise RuntimeError("Modrinth 返回了版本,但未找到与本地 hash 完全匹配的文件")

    project = modrinth_project(version["project_id"])
    if not project:
        raise RuntimeError(f"Modrinth 项目不存在: {version['project_id']}")
    return {
        "version": version,
        "project": project,
        "file": matched_file,
    }


def add_from_local_file(kind):
    path = resolve_local_file(kind)
    if not path:
        return False
    reverse_source = choose_reverse_source(kind)
    if not reverse_source:
        print("已取消。")
        return False

    warnings = [
        "将通过本地文件 hash 反查远端文件,只有 hash 完全匹配时才会生成 packwiz 元数据。",
        "添加完成后仍只提交 .pw.toml;本地 jar/zip 不会进入仓库或 Pages。",
    ]
    if reverse_source == "curseforge":
        warnings.append("CurseForge 反查依赖 packwiz curseforge detect,这是实验功能,且仅支持 mods 目录中的 jar。")
    if not confirm_warning(warnings):
        print("已取消。")
        return False

    if reverse_source == "modrinth":
        return add_from_local_modrinth(kind, path)
    return add_from_local_curseforge(kind, path)


def add_from_local_modrinth(kind, path):
    print("\n查询 Modrinth 文件 hash ...")
    try:
        match = modrinth_version_from_file(path)
    except RuntimeError as exc:
        print(f"[错误] Modrinth 反查失败: {exc}")
        return False
    if not match:
        print("[错误] Modrinth 未找到与该文件 hash 匹配的版本。")
        return False

    project = match["project"]
    version = match["version"]
    file_info = match["file"]
    expected_type = kind["modrinth_type"]
    actual_type = project.get("project_type")
    if actual_type != expected_type:
        print(
            f"[错误] hash 匹配到 Modrinth {actual_type!r} 项目 {project.get('title', project['id'])!r},"
            f"但当前选择的是 {kind['name']}。"
        )
        return False

    print("匹配结果:")
    print(f"  - 项目: {project.get('title', project['id'])} ({project.get('slug', project['id'])})")
    print(f"  - 类型: {actual_type}")
    print(f"  - 版本: {version.get('version_number')} ({version['id']})")
    print(f"  - 文件: {file_info['filename']}")
    if not confirm_warning(["确认按上述精确匹配结果添加该外部资源。"]):
        print("已取消。")
        return False

    folder = kind["folder"]
    before = snapshot_metadata(folder)
    cmd = resolve_packwiz() + [
        "--meta-folder", kind["meta_folder"],
        "modrinth", "add",
        "--project-id", project["id"],
        "--version-id", version["id"],
        "--version-filename", file_info["filename"],
    ]
    print()
    run(cmd)

    changed = detect_changed_metadata(folder, before)
    if not changed:
        print("\n未检测到新增/变更的 .pw.toml 文件,仍将刷新索引。")
        refresh()
        return True
    if not validate_or_rollback(kind, folder, before, changed):
        return False

    target = pick_candidate(changed, "选择主条目(回车跳过 side 设置): ")
    if target:
        side = choose_side(kind["default_side"])
        set_side(target, side)
        print(f"\n已更新 {target.relative_to(ROOT)} 的 side = \"{side}\"")

    refresh()
    return True


def add_from_local_curseforge(kind, path):
    if kind["name"] != "Mod":
        print("[错误] CurseForge detect 只支持本地 mod jar。")
        return False

    folder = kind["folder"]
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / path.name
    copied = False
    same_target = False
    try:
        same_target = target.exists() and path.samefile(target)
    except OSError:
        same_target = False

    if target.exists() and not same_target:
        print(f"[错误] mods 目录已存在同名文件,为避免覆盖已取消: {target.relative_to(ROOT)}")
        return False

    before = snapshot_metadata(folder)
    try:
        if not same_target:
            shutil.copy2(path, target)
            copied = True
            print(f"已临时复制到 {target.relative_to(ROOT)}")

        run(resolve_packwiz() + ["--meta-folder", kind["meta_folder"], "curseforge", "detect"])
    finally:
        if copied and target.exists():
            target.unlink()
            print(f"已删除临时文件 {target.relative_to(ROOT)}")

    changed = detect_changed_metadata(folder, before)
    if not changed:
        print("\n未检测到新增/变更的 .pw.toml 文件。")
        return False
    if not validate_or_rollback(kind, folder, before, changed):
        return False

    if same_target and target.exists():
        target.unlink()
        print(f"已删除工作区 jar {target.relative_to(ROOT)}")

    target_meta = pick_candidate(changed, "选择主条目(回车跳过 side 设置): ")
    if target_meta:
        side = choose_side(kind["default_side"])
        set_side(target_meta, side)
        print(f"\n已更新 {target_meta.relative_to(ROOT)} 的 side = \"{side}\"")

    refresh()
    return True


def find_resources(folder, keyword):
    keyword = keyword.casefold()
    matches = []
    for path in metadata_paths(folder):
        haystack = str(path.name)
        try:
            meta = read_meta(path)
            haystack += f" {meta.get('name', '')} {meta.get('filename', '')}"
        except Exception:
            pass
        if keyword in haystack.casefold():
            matches.append(path)
    return matches


def remove_resource():
    kind = choose_kind()
    if not kind:
        print("已取消。")
        return
    kind_name = kind["name"]
    folder = kind["folder"]

    resources = metadata_paths(folder)
    if not resources:
        print(f"{kind_name} 没有可移除的外部资源元数据。")
        return

    keyword = input("输入名称/文件名关键词筛选(回车显示全部): ").strip()
    matches = find_resources(folder, keyword) if keyword else resources
    if not matches:
        print("未找到匹配条目。")
        return

    target = pick_candidate(matches, "选择要移除的条目(回车取消): ")
    if not target:
        print("已取消。")
        return

    try:
        meta = read_meta(target)
    except Exception:
        meta = {}
    filename = meta.get("filename")
    payload = target.parent / filename if filename else None

    print("\n将移除:")
    print(f"  - 元数据: {target.relative_to(ROOT)}")
    if payload and payload.exists():
        print(f"  - 工作区文件: {payload.relative_to(ROOT)}")
    elif filename:
        print(f"  - 工作区文件: {target.parent.relative_to(ROOT) / filename}(当前不存在)")

    if not confirm_warning([
        "移除后该资源不再被 packwiz 追踪,玩家后续更新不会再下载它。",
        "如果工作区存在同名 jar/zip,会同时删除以满足“不存在于工作区”。",
    ]):
        print("已取消。")
        return

    target.unlink()
    print(f"已删除 {target.relative_to(ROOT)}")
    if payload and payload.exists():
        payload.unlink()
        print(f"已删除 {payload.relative_to(ROOT)}")

    refresh()
    print("完成。")


def refresh():
    print("\n刷新 packwiz 索引 ...")
    ensure_lf_before_refresh()
    run(resolve_packwiz() + ["refresh"])


def main():
    while True:
        print("=" * 52)
        print("  外部资源管理(Mod / Resourcepack)")
        print("=" * 52)
        print("  1. 添加外部资源")
        print("  2. 移除外部资源")
        print("  0. 返回")
        print("-" * 52)
        choice = input("请选择: ").strip()

        if choice == "1":
            add_resource()
        elif choice == "2":
            remove_resource()
        elif choice == "0" or choice == "":
            print("已返回。")
            break
        else:
            print("无效选择。")

        print()
        input("按回车继续...")
        print()


if __name__ == "__main__":
    main()
