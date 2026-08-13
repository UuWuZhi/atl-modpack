# All The Leisures

> 基于 Minecraft 1.21.1 + NeoForge 21.1.241,通过 **packwiz + GitHub Pages** 实现增量自动更新。

---

## 这是什么

- **管理**:285 个 mod + 原创内容(config/kubejs/scripts)以 packwiz 元数据存于 git
- **分发**:GitHub Pages 托管索引,客户端增量更新(只下变化文件)
- **开发/发布分离**:dev 分支开发(玩家不可见),发布时合并到 main 并刷新索引

## 文档

| 文档 | 适用 |
|---|---|
| [玩家指南](docs/guide/player.md) | 普通玩家:安装、更新、常见问题 |
| [服务端指南](docs/guide/server.md) | 服主:同步服务器 mods |
| [开发者指南](docs/guide/developer.md) | 维护人/团队:开发、发布、构建 |
| [从零搭建环境](docs/guide/bootstrap.md) | 新电脑/新成员:只有 git 时建立完整环境 |

## 快速开始

### 玩家(首次)
1. 下载 `modpack.mrpack`(QQ 群或 [GitHub Release](https://github.com/UuWuZhi/atl-modpack/releases))
2. PCL2 → 导入整合包 → 选该文件
3. 双击 `仅更新.bat` 更新,`启动游戏.bat` 更新+启动

### 开发者(日常)
```bash
git clone https://github.com/UuWuZhi/atl-modpack.git
cd atl-modpack && git checkout dev
python tools/cli.py          # 交互式菜单;或参数式见下
python tools/push.py -m "改动"        # 推 dev(开发,不刷新索引)
python tools/push.py --release --version 1.1.0  # 发布(main 刷新索引并打 tag)
```

### 工具一览

```bash
python tools/cli.py          # 交互式总入口(新手)
python tools/push.py         # 推 dev / merge / tag / release(熟练)
python tools/manage_external_resource.py  # 添加/移除/本地反查外部 mod/资源包
python tools/setup_dev_link.py   # 工作区↔实例 符号链接
python tools/build_import_pack.py  # 构建导入包
```

## 架构

```
开发者/维护人(改仓库)
   │ git push dev(开发) / release 到 main(发布时刷新索引)
   ▼
GitHub Pages(1~3 分钟)
   ├──► 玩家:双击 仅更新.bat → 增量更新
   └──► 服主:双击 更新服务端.bat → server 侧更新
```

- mod jar 走 Modrinth/CurseForge CDN
- 原创内容走 GitHub Pages
- 增量更新,只下载变化文件

## License

MIT(仅原创内容;mod 与资源包遵循各自许可)
