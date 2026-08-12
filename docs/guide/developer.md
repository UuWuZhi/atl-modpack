# 开发者指南 — All The Leisures

> 面向维护人与团队开发者。本文档涉及完整的开发/构建/发布流程。
> 需要一定技术基础(packwiz、git)。

---

## 〇、核心概念:开发与发布分离

```
【开发】所有开发者 → 推 dev 分支(玩家不可见)
【发布】维护人验证后 → dev 合并到 main,main 刷新索引(玩家增量更新)
```

- **Pages 只部署 main**:dev 分支的推送**不会**触发玩家更新
- **开发随意,发布谨慎**:实验性改动留在 dev,确认无 bug 才发布
- **索引只在 main 生成**:日常 dev 推送不刷新 `index.toml` / `pack.toml`,减少多人协作冲突;发布时合并到 main 后由工具统一刷新并提交。

### 工具总览

| 入口 | 用法 | 适合 |
|---|---|---|
| **交互式** `python tools\cli.py` | 菜单选择,无需记参数 | 新手开发者 / 非专业人员 |
| **参数式** `python tools\push.py --release` | 一行命令 | 熟练开发者 / AI |

参数式脚本(可单独调用):
- `push.py` — 推 dev / merge 到 main / 打 tag / 一站式 release
- `setup_dev_link.py` — 建立/断开符号链接
- `manage_external_resource.py` — 交互式添加/移除/本地反查外部 mod 或资源包 / 设定 side
- `build_import_pack.py` — 构建导入包

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

**在实例里改 kubejs/scripts = 改工作区文件**,无需手动复制:

```bat
python tools\setup_dev_link.py D:\Code\atl-modpack "D:\Minecraft\.minecraft\versions\All The Leisures v1.0.1b"
```

> 不想记参数?直接运行 `python tools\cli.py`,选「5. 建立/断开开发符号链接」交互式操作。

作用:
- 把实例的 `kubejs/`、`scripts/` 链接到工作区(同一份文件)
- 在实例里改脚本、`/kubejs reload` 热重载 → 工作区 git 立即可见
- 实例原来的文件备份为 `xxx.bak`

> **为什么不链 config**:游戏运行会大量改写 config(默认值、线程数、日志开关),
> 链接后这些运行时改动会污染工作区 git。所以 config 默认不链接,
> 改 config 走「工作区改 → 发布 → 玩家拉取」流程即可。

断开链接:

```bat
python tools\setup_dev_link.py --remove "D:\Minecraft\.minecraft\versions\All The Leisures v1.0.1b"
```

> **为什么需要它**:KubeJS 开发强依赖热重载(要看物品 ID、配方 ID、游戏内验证),只能在实例里做。符号链接让"实例编辑"与"工作区 git"合一,消灭手动复制。

---

## 二、日常开发

### 改原创内容(config / kubejs / scripts)

通过符号链接,**直接在开发实例里编辑** → 工作区文件同步变化。

### 改外部资源(mod / 资源包)

```bash
packwiz modrinth install <slug>      # 加 mod(如 packwiz mr install create)
packwiz remove <slug>                # 删 mod
packwiz update --all                 # 更新全部 mod 到最新
packwiz update <slug>                # 更新单个
```

或者直接用交互式入口:
```bash
python tools/cli.py                  # 选「6. 外部资源管理」
python tools/manage_external_resource.py  # 直接运行
```

> 非原创资源只提交 `.pw.toml` 元数据,不要把第三方 jar/zip 放进仓库或 Pages。
> 手上已有 jar/zip 时优先用「本地文件反查」,按 hash 精确匹配远端文件,避免搜索命中整合包或同名项目。
> 直链 URL 缺少依赖解析和可靠更新信息,优先使用 Modrinth / CurseForge。

> **标 side(客户端/服务端/双端)**:Modrinth 标记不可信,需人工确认。
> 判断规则、常见坑、批量检查见 [side 判定手册](side-guide.md)。核心原则:不确定就标 `both`。

### 推送(用 push.py 一键完成)

```bash
python tools/push.py -m "改了什么"     # 提交 + 推 dev,固定不 refresh
```

> 推 dev = 玩家不可见。dev 上不要提交日常 refresh 产生的 `index.toml` / `pack.toml` 变更;发布工具会在 main 上统一生成。

---

## 三、发布(维护人)

```bash
python tools/push.py --release -m "版本说明"   # dev→main + main refresh + 回灌 dev
python tools/push.py --release --version 1.1.0  # main refresh 后打 tag,再回灌 dev
```

作用:
1. 确认 dev/main 可快进同步远端,否则停止并要求维护人手动处理分叉
2. 推送 dev,切到 main,用 `--no-ff` 合并 dev
3. 在 main 上执行 `packwiz refresh`,单独提交 `index.toml` / `pack.toml` 更新
4. `--version` 在 main 的发布索引提交上打 git tag(供 Release 关联)
5. 推送 main/tag,再切回 dev,用 `--no-ff` 把 main 发布结果合并回 dev

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

**发布 = dev→main + main refresh + tag + 回灌 dev + 构建 mrpack**。

```bash
# 方式 A(推荐):push.py 一步完成发布/tag/回灌,再手动构建 mrpack
python tools/push.py --release --version 1.1.0 -m "v1.1.0"
python tools/build_import_pack.py --seed tools/cache/seed.json -o dist/modpack.mrpack

# 方式 B:build_import_pack.py(纯构建 mrpack)
python tools/build_import_pack.py --seed tools/cache/seed.json -o dist/modpack.mrpack
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
| 确认可发布 | release 到 main | 增量,无感(1~3 分钟) |
| 更新 mod 版本 | dev 开发,main 发布 | 增量拉到 |
| 大版本发布 | main + tag + mrpack | 重新导入 |

### 分支约定

- **dev**:所有开发者日常推送,玩家不可见
- **main**:只有发布时合并与 refresh,Pages 部署,玩家可见
- 发布回灌:main 的索引提交会用 `--no-ff` 合并回 dev,保留明确同步点
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
├── tools/               # 工具链(python)
│   ├── cli.py               # 交互式总入口
│   ├── manage_external_resource.py # 添加/移除/本地反查外部资源
│   ├── push.py              # 推 dev / merge / tag / release
│   ├── setup_dev_link.py    # 工作区↔实例 符号链接
│   ├── build_import_pack.py # 构建导入包
│   ├── packwiz-cli/         # packwiz 可执行文件
│   └── cache/seed.json      # 哈希缓存
├── docs/                # 文档
├── .gitignore           # git 忽略
└── .packwizignore       # packwiz 索引忽略(工具/文档不下发)
```

---

## 八、常见问题

### 改了 config 但玩家没更新到

确认已执行 `python tools/push.py --release`;只有 main 上 refresh 并 push 后玩家才会收到更新。等 1~3 分钟 Pages 生效。

### `packwiz update` 某 mod 失败

该 mod 源失效(下架/改版)。换源或移除。

### 构建脚本下载慢

用 `--seed`(哈希缓存)。若 mod 更新导致 seed 缺失,脚本会只下载缺失的,其余走缓存。

### dist/ 不在 git 里

`dist/` 是构建产物,被 `.gitignore` 忽略。正常,它只用于发布时附到 Release。
