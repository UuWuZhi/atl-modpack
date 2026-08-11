# 开发者指南 — All The Leisures

> 面向维护人与团队开发者。本文档涉及完整的开发/构建/发布流程。
> 需要一定技术基础(packwiz、git)。

---

## 一、环境搭建

### 需要安装

| 工具 | 用途 | 获取 |
|---|---|---|
| **packwiz CLI** | 管理 mod、构建索引 | nightly.link → packwiz 最新构建 → Windows 版 |
| **git** | 版本控制 | git-scm.com |
| **Python 3.11+** | 构建脚本 | python.org |
| **PCL2**(或任意启动器) | 建开发实例测试 | PCL 社区 |

### 获取仓库

```bash
git clone https://github.com/UuWuZhi/atl-modpack.git
cd atl-modpack
```

> 仓库里已含 `tools/packwiz-cli/`(如果你没装 packwiz,可从 `tools/` 找;但建议装到 PATH)。

### 建开发实例(测试用)

1. 构建导入包或从 Release 下载 `modpack.mrpack`
2. PCL2 → 导入整合包 → 建一个开发实例
3. 实例内跑一次 `仅更新.bat`,确认能进游戏

> **开发原则**:改代码在「仓库」里做(git 管理),测试在「开发实例」里做(真实环境)。两者通过 push + bootstrap 打通,不需要手动复制文件。

---

## 二、日常开发

### 改 mod(加/删/更新)

```bash
packwiz modrinth install <slug>      # 加 mod(如 packwiz mr install create)
packwiz remove <slug>                # 删 mod
packwiz update --all                 # 更新全部 mod 到最新
packwiz update <slug>                # 更新单个
```

### 改原创内容(config / kubejs / 资源包)

直接编辑仓库里对应文件,然后:

```bash
packwiz refresh        # 重建 index,更新这些文件的哈希
```

### 提交并推送

```bash
git add -A
git commit -m "feat: 描述改动"
git push               # 触发 Pages 自动更新(1~3 分钟)
```

### 测试

push 后,在开发实例里双击 `仅更新.bat`,拉到最新改动,进游戏验证。

> **改完一定要 `packwiz refresh`**,否则 index 哈希对不上,玩家更新会失败。

---

## 三、构建导入包

```bash
python tools/build_import_pack.py --seed tools/cache/seed.json -o dist/modpack.mrpack
```

说明:
- 从仓库生成标准 mrpack(293 个 mod 清单 + 原创内容 overrides + bootstrap 工具链)
- `--seed` 用哈希缓存加速(293 条已入库),**不需要下载计算**
- 产物在 `dist/modpack.mrpack`

---

## 四、发布新版本(release)

```bash
python tools/release.py 1.1.0
```

这个命令会:
1. `packwiz refresh`(更新索引)
2. 构建 `dist/modpack.mrpack`
3. 打 git tag `v1.1.0` 并 push
4. 提示下一步发布

**发布到 GitHub Release**(任选):
```bash
# 方式 A:GitHub CLI(需先装 gh)
gh release create v1.1.0 dist/modpack.mrpack --title "v1.1.0"

# 方式 B:网页操作
# GitHub → Releases → Draft new → 选 tag v1.1.0 → 附上 dist/modpack.mrpack → Publish
```

> 发布后把 mrpack 分享到 QQ 群,玩家导入即可。**大版本才需要发导入包**,日常改动玩家走增量更新。

---

## 五、版本控制策略

| 场景 | 玩家如何收到 |
|---|---|
| 改 config/kubejs | 自动(增量,无感) |
| 更新 mod 版本 | `packwiz update` 后 push,增量拉到 |
| 大版本发布 | `release.py` 打 tag + 发导入包 |

### 锁版本(可选)

若不想某些 mod 自动更新:
```bash
packwiz pin <slug>      # 钉住,不随 update --all 变
packwiz unpin <slug>    # 解除
```

---

## 六、仓库结构

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

## 七、常见问题

### 改了 config 但玩家没更新到

确认 `packwiz refresh` 已跑并 push;等 1~3 分钟 Pages 生效。

### `packwiz update` 某 mod 失败

该 mod 源失效(下架/改版)。换源或移除。

### 构建脚本下载慢

用 `--seed`(哈希缓存)。若 mod 更新导致 seed 缺失,脚本会只下载缺失的,其余走缓存。

### dist/ 不在 git 里

`dist/` 是构建产物,被 `.gitignore` 忽略。正常,它只用于发布时附到 Release。
