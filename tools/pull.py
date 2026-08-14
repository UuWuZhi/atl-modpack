#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interactive git pull helper with explicit conflict choices."""

import subprocess
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent


def git(args, check=True, capture=True):
    cmd = ["git", *args]
    print(f"> {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if capture:
        if result.stdout.strip():
            print(result.stdout.rstrip())
        if result.stderr.strip():
            print(result.stderr.rstrip())
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result


def ask(prompt, allowed):
    allowed = set(allowed)
    while True:
        choice = input(prompt).strip()
        if choice in allowed:
            return choice
        print("无效选择。")


def confirm_exact(prompt, expected):
    print(prompt)
    answer = input(f"请输入 {expected} 确认: ").strip()
    return answer == expected


def current_branch():
    result = git(["branch", "--show-current"])
    branch = result.stdout.strip()
    if not branch:
        print("[错误] 当前处于 detached HEAD,请先切回 dev/main 等分支。")
        raise SystemExit(1)
    return branch


def status_porcelain():
    return git(["status", "--porcelain"], check=False).stdout.strip()


def ensure_origin_branch(branch):
    result = git(["rev-parse", "--verify", f"origin/{branch}"], check=False)
    if result.returncode != 0:
        print(f"[错误] 找不到 origin/{branch}。请确认远程分支存在。")
        raise SystemExit(1)


def rev_parse(ref):
    return git(["rev-parse", ref]).stdout.strip()


def merge_base(left, right):
    return git(["merge-base", left, right]).stdout.strip()


def abort_in_progress_operations():
    git_dir = ROOT / ".git"
    if (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists():
        print("[提示] 检测到 rebase 进行中。")
        print("  1. 终止 rebase")
        print("  0. 退出,手动处理")
        if ask("请选择: ", {"1", "0"}) == "1":
            git(["rebase", "--abort"], check=False)
        else:
            raise SystemExit(1)
    if (git_dir / "MERGE_HEAD").exists():
        print("[提示] 检测到 merge 进行中。")
        print("  1. 终止 merge")
        print("  0. 退出,手动处理")
        if ask("请选择: ", {"1", "0"}) == "1":
            git(["merge", "--abort"], check=False)
        else:
            raise SystemExit(1)


def handle_dirty_worktree(branch):
    dirty = status_porcelain()
    if not dirty:
        return

    print("[提示] 工作区有未提交改动,直接拉取可能覆盖或产生冲突:")
    for line in dirty.splitlines()[:30]:
        print(f"  {line}")
    if len(dirty.splitlines()) > 30:
        print("  ...")
    print()
    print("  1. 暂存本地改动(stash),拉取后自动恢复")
    print("  2. 覆盖本地未提交改动(reset --hard + clean -fd),然后拉取")
    print("  0. 取消,我先手动处理")
    choice = ask("请选择: ", {"1", "2", "0"})

    if choice == "0":
        raise SystemExit(1)
    if choice == "2":
        if not confirm_exact("[危险] 这会删除所有未提交改动和未追踪文件。", "OVERWRITE LOCAL"):
            print("已取消。")
            raise SystemExit(1)
        git(["reset", "--hard"])
        git(["clean", "-fd"])
        return

    git(["stash", "push", "-u", "-m", f"before pull {branch}"])
    pull_current_branch(branch)
    print("[*] 正在恢复 stash ...")
    result = git(["stash", "pop"], check=False)
    if result.returncode != 0:
        print("[错误] stash pop 产生冲突。")
        print("可选处理:")
        print("  - 手动解决冲突后提交")
        print("  - 放弃恢复: git reset --hard && git stash drop")
        raise SystemExit(result.returncode)
    print("[✓] 拉取完成,本地改动已恢复。")
    raise SystemExit(0)


def pull_current_branch(branch):
    print(f"[*] 拉取 origin/{branch} ...")
    result = git(["pull", "--ff-only", "origin", branch], check=False)
    if result.returncode == 0:
        print("[✓] 已快进到远程最新。")
        return
    print("[错误] 快进拉取失败。")
    print("这通常表示本地和远程已分叉,需要选择 rebase/merge/覆盖策略。")
    handle_diverged(branch)


def handle_diverged(branch):
    local = rev_parse("HEAD")
    remote = rev_parse(f"origin/{branch}")
    base = merge_base("HEAD", f"origin/{branch}")

    if local == remote:
        print("[✓] 本地已经是最新。")
        return
    if local == base:
        git(["pull", "--ff-only", "origin", branch])
        print("[✓] 已快进到远程最新。")
        return
    if remote == base:
        print("[提示] 本地领先远程,无需拉取。若要同步远程,请执行推送。")
        return

    print("[冲突] 本地和远程分支已分叉。")
    print("  1. 保留本地提交,变基到远程之上(git pull --rebase)")
    print("  2. 建立合并提交(git merge --no-ff origin/当前分支)")
    print("  3. 覆盖本地,完全采用远程(git reset --hard origin/当前分支)")
    print("  4. 覆盖远程,强制推送本地(git push --force-with-lease)")
    print("  0. 取消,我先手动处理")
    choice = ask("请选择: ", {"1", "2", "3", "4", "0"})

    if choice == "0":
        raise SystemExit(1)
    if choice == "1":
        result = git(["pull", "--rebase", "origin", branch], check=False)
        if result.returncode != 0:
            print("[错误] rebase 产生冲突。")
            print("处理方式:")
            print("  - 解决冲突后: git add <文件> && git rebase --continue")
            print("  - 放弃本次操作: git rebase --abort")
            raise SystemExit(result.returncode)
        print("[✓] rebase 拉取完成。")
        return
    if choice == "2":
        result = git(["merge", "--no-ff", "--no-edit", f"origin/{branch}"], check=False)
        if result.returncode != 0:
            print("[错误] merge 产生冲突。")
            print("处理方式:")
            print("  - 解决冲突后: git add <文件> && git commit")
            print("  - 放弃本次操作: git merge --abort")
            raise SystemExit(result.returncode)
        print("[✓] 合并完成。")
        return
    if choice == "3":
        if not confirm_exact("[危险] 这会丢弃本地未推送提交,完全采用远程。", "OVERWRITE LOCAL"):
            print("已取消。")
            raise SystemExit(1)
        git(["reset", "--hard", f"origin/{branch}"])
        print("[✓] 已覆盖本地为远程版本。")
        return
    if choice == "4":
        if not confirm_exact("[危险] 这会改写远程分支历史。仅在确认远程错误时使用。", "OVERWRITE REMOTE"):
            print("已取消。")
            raise SystemExit(1)
        git(["push", "--force-with-lease", "origin", branch])
        print("[✓] 已用本地分支覆盖远程。")


def main():
    abort_in_progress_operations()
    branch = current_branch()
    handle_dirty_worktree(branch)
    result = git(["fetch", "origin", "--prune"], check=False)
    if result.returncode != 0:
        print("[错误] 拉取远程信息失败。请检查网络、代理或 GitHub 访问状态后重试。")
        raise SystemExit(result.returncode)
    ensure_origin_branch(branch)
    handle_diverged(branch)


if __name__ == "__main__":
    main()
