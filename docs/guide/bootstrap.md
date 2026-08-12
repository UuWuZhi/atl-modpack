# 从零搭建开发环境(只有 git 的环境)

> 适用:拿到一台只有 git 的电脑,从空目录开始建立完整开发环境。
> 目标:能开发、能构建、能发布。

---

## 环境自包含情况

**仓库已自包含**(clone 后就有):

| 组件 | 位置 |
|---|---|
| 整合包清单 | `pack.toml` + `index.toml` |
| 293 个 mod 元数据 | `mods/*.pw.toml` |
| 原创内容 | `config/ kubejs/ scripts/ resourcepacks/` |
| 构建脚本 | `tools/*.py` |
| 哈希缓存 | `tools/cache/seed.json` |
| 玩家工具链 | `bootstrap/*.jar` + `*.bat` |

**唯一需要外部获取**:

| 组件 | 来源 |
|---|---|
| **packwiz.exe** | nightly.link 下载(见下) |
| **Python 3.11+** | python.org |
| **Java 21** | 已有(游戏运行需要) |

---

## 完整流程

### 第一步:安装前置(一次性)

1. **git**:git-scm.com
2. **Python 3.11+**:python.org(勾选 Add to PATH)
3. **(可选)packwiz.exe**:
   - 访问 https://nightly.link/packwiz/packwiz/workflows/go/main
   - 下载 `packwiz-windows-amd64.zip`
   - 解压出 `packwiz.exe`,放到 `atl-modpack/tools/packwiz-cli/`

> 若不下载 packwiz.exe,脚本会 fallback 到 PATH 里的 `packwiz` 命令。

### 第二步:获取仓库

```bash
git clone https://github.com/UuWuZhi/atl-modpack.git
cd atl-modpack
git checkout dev          # 开发用 dev 分支
```

### 第三步:验证工具链

```bash
python tools/cli.py       # 应显示菜单,无报错(退出选 0)
python -c "import hashlib,re,os; idx=open('index.toml',encoding='utf-8').read(); print('index OK, entries:', len(re.findall(r'file =', idx)))"
```

### 第四步:建开发实例(游戏测试用)

1. 构建导入包:
   ```bash
   python tools/build_import_pack.py --seed tools/cache/seed.json -o dist/modpack.mrpack
   ```
2. PCL2 → 导入整合包 → 选 `dist/modpack.mrpack`
3. 实例内跑一次 `仅更新.bat`,确认能进游戏

### 第五步:打通工作区与实例(可选,开发 KubeJS 用)

```bash
python tools/setup_dev_link.py D:\Code\atl-modpack "D:\Minecraft\.minecraft\versions\All The Leisures v1.0.1b"
```

> 只链 `kubejs/` 和 `scripts/`。config 不链接(游戏运行会污染工作区,见 developer.md)。

---

## 日常开发循环

```bash
# 1. 在实例里改 kubejs(符号链接 → 工作区同步)或用编辑器改工作区
# 2. 推送(提交 + 推 dev,不刷新索引)
python tools/push.py -m "改了什么"

# 3. 发布(dev→main,main 刷新索引,玩家可见)
python tools/push.py --release --version 1.1.0
```

---

## 常见问题

### 脚本报 "找不到 packwiz"

装 packwiz 到 PATH,或解压到 `tools/packwiz-cli/packwiz.exe`。

### `git clone` 后 `python tools/push.py` 报错

确认在 dev 分支(`git checkout dev`),Python 版本 ≥3.11。

### 没有 PCL2 怎么测试

任何支持 NeoForge 的启动器都行,或用 `仅更新.bat` + 官方启动器。

### packwiz.exe 版本

仓库脚本不依赖特定版本,只要能用 `packwiz refresh` 即可。若遇兼容问题,更新到最新 nightly。

---

## 服务器侧(可选的同步工具链)

服务器不需要上面这套开发环境。只需:
- `bootstrap/packwiz-installer-bootstrap.jar` + `packwiz-installer.jar`
- `同步mods.bat`(从 `server/` 取)
- 放服务器根目录,开服前双击同步

> 服务器侧细节暂不展开,见 `docs/guide/server.md`。
