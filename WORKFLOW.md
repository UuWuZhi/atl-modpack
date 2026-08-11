# All The Leisures — 完整工作流手册

> 本文档面向所有人:维护人(你)、团队开发者、服主、玩家。
> 按角色找到你该做的事。

---

## 一、前提部署(一次性,各角色要准备什么)

### 玩家(需要下载)

| 需要 | 说明 |
|---|---|
| **Java 21** | PCL2 一般自带,无需手动装 |
| **PCL2 启动器** | 主流玩家已有 |
| **导入包** `All The Leisures 导入包.zip` | 从 QQ 群下载,**首次**安装用。PCL2 → 导入整合包 → 选 zip |
| 后续更新 | **无需再下载任何东西**,双击 `仅更新.bat` 或 `启动游戏.bat` 即可 |

> 导入包路径:.minecraft/versions/All The Leisures v1.0.1b/,内含 mods 元数据、config、kubejs、bootstrap jar、两个脚本。

### 团队开发者(需要下载)

| 需要 | 说明 |
|---|---|
| **packwiz CLI** | 从 nightly.link 下载 Windows 版,放任意位置 |
| **git** | 建工作区/提交用 |
| **仓库 clone** | `git clone https://github.com/UuWuZhi/atl-modpack.git` |
| **packwiz 命令行熟悉** | 加/删/更新 mod 的 3 条命令(见下) |

### 服主(需要下载)

| 需要 | 说明 |
|---|---|
| **packwiz-installer-bootstrap.jar** | 从导入包/仓库的 `bootstrap/` 目录拿 |
| **同步mods.bat** | 从仓库 `server/` 目录拿,放服务器根目录 |
| **run.bat**(已有) | 原开服脚本 |

### 你(维护人)

| 需要 | 说明 |
|---|---|
| **本地工作区** | `D:\Code\atl-modpack`(已建好) |
| **packwiz CLI** | `tools/packwiz-cli/packwiz.exe`(已解压) |
| **git** | 已配好 |
| **GitHub 仓库** | `UuWuZhi/atl-modpack`(已建,pages 已开) |

---

## 二、日常工作流

### A. 加一个 mod / 更新 mod(你或开发者)

```bash
# 在工作区
packwiz modrinth install <slug>      # 加 mod
packwiz update --all                 # 更新全部
packwiz remove <slug>                # 删 mod
packwiz refresh                      # 重建索引(改动后必须)
git add -A
git commit -m "feat: 新增/更新 XXX"
git push
```

push 后 **GitHub Pages 自动更新**(branch 部署),1~3 分钟内玩家可见。

### B. 团队开发者提交(不涉及 mod 的原创内容)

> 例如:改了 config、kubejs 脚本、资源包。**这些文件在仓库里,和 mod 一样走 packwiz。**

```bash
git pull                          # 先同步
# 编辑 config/ 或 kubejs/ 等文件
packwiz refresh                   # 重新计算这些文件的 hash
git add -A
git commit -m "fix: 调整 XX 配置"
git push
```

**关键点:非 mod 原创内容( config/kubejs/scripts/resourcepacks )同样通过 packwiz index 分发。** 改动后 `packwiz refresh` 会更新这些文件的 hash,玩家 bootstrap 增量拉取到最新。**不需要重新打包、不需要玩家重新下载。**

### C. 玩家侧(日常)

- 想顺手启动游戏:**双击 `启动游戏.bat`**(先更新,再开 PCL2)
- 只想更新不启动:**双击 `仅更新.bat`**(更新完自己开 PCL2)
- 首次:**导入包安装后**,跑一次更新脚本即可

### D. 服务器同步(服主,开服前)

1. 双击 `同步mods.bat`(服务器根目录)
2. 提示完成后,双击 `run.bat` 开服

> 同步的是 server/both 侧 mods,纯客户端 mod 自动跳过,不会崩服。

---

## 三、更新如何到达所有人(核心机制)

```
改仓库(你/开发者)
   │  git push
   ▼
GitHub Pages(自动,1-3分钟)
   │  更新 index.toml + config/kubejs/资源包 hash + mods 元数据
   ├──────────────► 玩家:双击 仅更新.bat / 启动游戏.bat
   │                   bootstrap 读 Pages index → 对比本地 → 只下载变化文件
   │                   (mod jar 从 Modrinth/CF CDN 拉,config 等从 Pages 拉)
   └──────────────► 服主:双击 同步mods.bat
                        bootstrap -s server 读 Pages → 同步 server/both 侧 mods
```

**三种角色覆盖**:
- **玩家**:通过 bootstrap 增量更新,永远到最新
- **服务器**:通过 `同步mods.bat`,同步到最新
- **开发者**:通过 `git pull` 拿到最新仓库(含全部元数据)

> 注意:玩家和服务器通过 **Pages** 更新;开发者通过 **git** 更新。两条通道并行,互不干扰。

---

## 四、各角色命令速查

### 开发者 / 你

| 场景 | 命令 |
|---|---|
| 加 mod | `packwiz modrinth install <slug>` |
| 删 mod | `packwiz remove <slug>` |
| 更新全部 | `packwiz update --all` |
| 改完原创文件 | `packwiz refresh` |
| 提交 | `git add -A && git commit && git push` |
| 拉取团队改动 | `git pull` |

### 玩家

| 场景 | 操作 |
|---|---|
| 首次安装 | 导入包 → PCL2 导入 |
| 更新+启动 | 双击 `启动游戏.bat` |
| 仅更新 | 双击 `仅更新.bat` |

### 服主

| 场景 | 操作 |
|---|---|
| 开服前同步 | 双击 `同步mods.bat` |
| 开服 | 双击 `run.bat` |

---

## 五、多人协作约定

- **git 工作流**:所有开发者 push 到 main,Pages 自动部署。改动小、频率低,不需要 PR 分支。
- **冲突处理**:若 `git pull` 提示冲突,手动解决后 `git add -A && git commit && git push`。
- **权限**:写权限给 你 + 服主 + 技术型开发者;其他人走 QQ 通知你代改。
- **不要在 main 上改无关内容**:保持仓库干净,只提交整合包相关内容。

---

## 六、常见问题

| 问题 | 处理 |
|---|---|
| 玩家更新后进服 mod 版本不符 | 服务器维护完,玩家重新跑 `仅更新.bat` |
| `packwiz update` 某 mod 失败 | 该 mod 源失效,换源或移除 |
| 玩家双击脚本提示缺 java | 用 PCL2 自带 Java(脚本已自动探测),或装 Java 21 |
| 改 config 后玩家没更新到 | 确认 `packwiz refresh` 已跑并 push,等 1~3 分钟 |
