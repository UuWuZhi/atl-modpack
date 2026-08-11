# 开发者指南 — All The Leisures

> 面向维护人与团队开发者。本文档涉及完整的开发/构建/发布流程。
> 需要一定技术基础(packwiz、git)。

---

## 〇、核心概念:开发与发布分离

```
【开发】所有开发者 → 推 dev 分支(玩家不可见)
【发布】维护人验证后 → merge dev→main(玩家增量更新)
```

- **Pages 只部署 main**:dev 分支的推送**不会**触发玩家更新
- **开发随意,发布谨慎**:实验性改动留在 dev,确认无 bug 才发布

### 工具总览

| 入口 | 用法 | 适合 |
|---|---|---|
| **交互式** `python tools\cli.py` | 菜单选择,无需记参数 | 新手 / 服主 |
| **参数式** `python tools\push.py --release` | 一行命令 | 熟练开发者 / AI |

参数式脚本(可单独调用):
- `push.py` — 推 dev / merge 到 main / 打 tag / 一站式 release
- `setup_dev_link.py` — 建立/断开符号链接
- `build_import_pack.py` — 构建导入包
- `release.py` — 构建 + tag + 发布

---

## 一、环境搭建

### 需要安装

| 工具 | 用途 | 获取 |
|---|---|---|
| **packwiz CLI** | 管理 mod、构建索引 | nightly.link → packwiz 最新构建 → Windows 版 |
| **git** | 版本控制 | git-scm.com |
| **Python 3.11+** | 构建脚本 | python.org |
| **PCL2**(或任意启动器) | 建开发实例测试 | PCL 社区 |

### 获取仓库(注意切换到 dev 分支)

```bash
git clone https://github.com/UuWuZhi/atl-modpack.git
cd atl-modpack
git checkout dev          # 开发都在 dev 分支
```

### 建开发实例(测试用)

1. 构建导入包或从 Release 下载 `modpack.mrpack`
2. PCL2 → 导入整合包 → 建一个开发实例
3. 实例内跑一次 `仅更新.bat`,确认能进游戏

### 打通工作区与实例(关键:符号链接)

**在实例里改 kubejs/config = 改工作区文件**,无需手动复制:

```bat
python tools\setup_dev_link.py D:\Code\atl-modpack "D:\Minecraft\.minecraft\versions\All The Leisures v1.0.1b"
```

> 不想记参数?直接运行 `python tools\cli.py`,选「5. 建立/断开开发符号链接」交互式操作。

作用:
- 把实例的 `config/`、`kubejs/`、`scripts/` 链接到工作区(同一份文件)
- 在实例里改脚本、`/kubejs reload` 热重载 → 工作区 git 立即可见
- 实例原来的文件备份为 `xxx.bak`

断开链接:

```bat
python tools\setup_dev_link.py --remove "D:\Minecraft\.minecraft\versions\All The Leisures v1.0.1b"
```

> **为什么需要它**:KubeJS 开发强依赖热重载(要看物品 ID、配方 ID、游戏内验证),只能在实例里做。符号链接让"实例编辑"与"工作区 git"合一,消灭手动复制。

---

## 二、日常开发

### 改原创内容(config / kubejs / scripts)

通过符号链接,**直接在开发实例里编辑** → 工作区文件同步变化。

### 改 mod(加/删/更新)

```bash
packwiz modrinth install <slug>      # 加 mod(如 packwiz mr install create)
packwiz remove <slug>                # 删 mod
packwiz update --all                 # 更新全部 mod 到最新
packwiz update <slug>                # 更新单个
```

### 推送(用 push.py 一键完成)

```bash
python tools/push.py -m "改了什么"     # 自动 refresh + 提交 + 推 dev
```

> 推 dev = 玩家不可见。可放心推实验性改动。

---

## 三、发布(维护人)

```bash
python tools/push.py --release -m "版本说明"   # merge dev→main + 推 main
python tools/push.py --release --version 1.1.0  # 发布时可选打 tag
```

作用:
1. 切到 main,merge dev,push main → Pages 更新 → 玩家增量拉到(1~3 分钟)
2. `--version` 打 git tag(供 Release 关联)
3. 自动回到 dev 继续开发

> 发布 = 你确认无 bug、不损坏存档后的动作。发布前务必在实例里测试。

---

## 四、构建导入包

```bash
python tools/build_import_pack.py --seed tools/cache/seed.json -o dist/modpack.mrpack
```

说明:
- 从仓库生成标准 mrpack(293 个 mod 清单 + 原创内容 overrides + bootstrap 工具链)
- `--seed` 用哈希缓存加速(293 条已入库),**不需要下载计算**
- 产物在 `dist/modpack.mrpack`

---

## 五、发布新版本(release)

**发布 = merge dev→main + 打 tag + 构建 mrpack**。

```bash
# 方式 A(推荐):push.py 一步完成 merge+push,再手动构建 mrpack
python tools/push.py --release -m "v1.1.0"
python tools/build_import_pack.py --seed tools/cache/seed.json -o dist/modpack.mrpack

# 方式 B:release.py(会打空 release commit,可能触发 Pages 空部署)
python tools/release.py 1.1.0
```

**发布到 GitHub Release**(任选):
```bash
# 方式 A:GitHub CLI(需先装 gh)
gh release create v1.1.0 dist/modpack.mrpack --title "v1.1.0"

# 方式 B:网页操作
# GitHub → Releases → Draft new → 选 tag v1.1.0 → 附上 dist/modpack.mrpack → Publish
```

> 发布后把 mrpack 分享到 QQ 群,玩家导入即可。**大版本才需要发导入包**,日常改动玩家走增量更新。

---

## 六、版本控制策略

| 场景 | 推哪 | 玩家如何收到 |
|---|---|---|
| 开发中改动(实验) | dev | 看不到 |
| 确认可发布 | merge dev→main | 增量,无感(1~3 分钟) |
| 更新 mod 版本 | dev→main | 增量拉到 |
| 大版本发布 | main + tag + mrpack | 重新导入 |

### 分支约定

- **dev**:所有开发者日常推送,玩家不可见
- **main**:只有发布时 merge,Pages 部署,玩家可见
- 冲突解决:`git pull origin dev` 后手动 merge 或用 `git merge`

### 锁版本(可选)

若不想某些 mod 自动更新:
```bash
packwiz pin <slug>      # 钉住,不随 update --all 变
packwiz unpin <slug>    # 解除
```

---

## 七、仓库结构

```
atl-modpack/
├── pack.toml            # packwiz 主清单(MC/NeoForge 版本)
├── index.toml           # 文件索引(哈希表)
├── mods/                # 285 个 .pw.toml 元数据(无 jar)
├── resourcepacks/       # 资源包元数据 + 原创资源包
├── config/ kubejs/ scripts/ defaultconfigs/   # 原创内容
├── bootstrap/           # 更新工具链(玩家/服主从这拿)
├── server/              # 服主脚本
├── tools/               # 构建脚本 + packwiz CLI + 哈希缓存
│   ├── migrate.py           # (一次性)mrpack→packwiz 迁移
│   ├── build_import_pack.py # 构建导入包
│   ├── release.py           # 构建+发版
│   └── cache/seed.json      # 哈希缓存
├── docs/                # 文档
├── .gitignore           # git 忽略
└── .packwizignore       # packwiz 索引忽略(工具/文档不下发)
```

---

## 八、常见问题

### 改了 config 但玩家没更新到

确认 `packwiz refresh` 已跑并 push;等 1~3 分钟 Pages 生效。

### `packwiz update` 某 mod 失败

该 mod 源失效(下架/改版)。换源或移除。

### 构建脚本下载慢

用 `--seed`(哈希缓存)。若 mod 更新导致 seed 缺失,脚本会只下载缺失的,其余走缓存。

### dist/ 不在 git 里

`dist/` 是构建产物,被 `.gitignore` 忽略。正常,它只用于发布时附到 Release。
