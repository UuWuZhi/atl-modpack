# All The Leisures

> 基于 Minecraft 1.21.1 + NeoForge 21.1.241 的整合包,通过 **packwiz + GitHub Pages** 实现客户端/服务器增量自动更新。

---

## 这是什么

一套**整合包版本管理与分发系统**:

- **管理**:285 个 mod + 原创内容(config/kubejs/资源包)以 packwiz 元数据形式存在 git 仓库
- **分发**:GitHub Pages 托管索引,客户端/服务器通过 packwiz 增量更新(只下变化部分,不重下全部)
- **发布**:一条命令构建导入包 + 打 tag + 发布 Release

## 文档

按角色阅读:

| 文档 | 适用 |
|---|---|
| [玩家指南](docs/guide/player.md) | 普通玩家:首次安装、日常更新 |
| [服务端指南](docs/guide/server.md) | 服主:同步服务器 mods |
| [开发者指南](docs/guide/developer.md) | 维护人/团队开发者:改 mod、构建、发布 |
| [实战:更新 kubeJS 脚本](docs/guide/scenario-kubejs-update.md) | 开发者:改脚本并分发到玩家的完整流程 |
| [完整工作流](WORKFLOW.md) | 维护人:端到端流程总览 |
| [迁移记录](MIGRATION.md) | 维护人:首次迁移的来龙去脉 |

## 快速开始

### 玩家(首次)

1. 下载 `modpack.mrpack`(从 QQ 群或 [GitHub Release](https://github.com/UuWuZhi/atl-modpack/releases))
2. PCL2 → 导入整合包 → 选该文件
3. 导入完成后双击 `启动游戏.bat` 或 `仅更新.bat`

### 服主(每次开服前)

1. 服务器根目录放 `packwiz-installer-bootstrap.jar` + `同步mods.bat`
2. 双击 `同步mods.bat` → 再开 `run.bat`

### 开发者(改 mod/配置)

```bash
git clone https://github.com/UuWuZhi/atl-modpack.git
cd atl-modpack
packwiz modrinth install <slug>   # 加 mod
packwiz refresh                   # 重建索引
git add -A && git commit -m "..." && git push
```

详细见 [开发者指南](docs/guide/developer.md)。

---

## 架构

```
开发者/维护人(改仓库)
   │ git push
   ▼
GitHub Pages(自动,1~3 分钟)
   ├──────────────► 玩家:双击 仅更新.bat → 增量更新
   └──────────────► 服主:双击 同步mods.bat → server 侧同步
```

- mod jar 走 Modrinth/CurseForge CDN
- 原创内容(config/kubejs/资源包)走 GitHub Pages
- 增量更新,只下载变化文件

## 目录结构

```
├── pack.toml            # packwiz 主清单
├── index.toml           # 文件索引
├── mods/                # mod 元数据(285 个 .pw.toml)
├── resourcepacks/       # 资源包元数据 + 原创资源包
├── config/ kubejs/      # 原创内容
├── bootstrap/           # 客户端更新工具链
├── server/              # 服主脚本
├── tools/               # 构建/发布脚本
├── docs/                # 文档
└── .github/             # CI(当前用 GitHub 原生 branch 部署)
```

## 技术栈

- [packwiz](https://packwiz.infra.link/) — modpack 管理
- [packwiz-installer-bootstrap](https://github.com/comp500/packwiz-installer-bootstrap) — 客户端增量更新
- GitHub Pages — 静态托管

## License

MIT(仅原创内容;mod 与资源包遵循各自原始许可)
