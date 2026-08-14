#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility wrapper for the unified external resource manager."""

import runpy
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TARGET = Path(__file__).with_name("manage_external_resource.py")


if __name__ == "__main__":
    print("[提示] add_mod.py 已并入 manage_external_resource.py。")
    print("      将打开统一的外部资源管理界面。")
    runpy.run_path(str(TARGET), run_name="__main__")
