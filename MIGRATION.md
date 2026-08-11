# All The Leisures — packwiz 迁移与运维指南

> 本文档面向维护人(你)。玩家/服主只读对应小节。

---

## 一、方案总览

- **分发源**:GitHub Pages(public 仓库 `atl-modpack`)
- **增量更新**:packwiz,客户端启动时对比哈希,只下载变化文件
- **mod 下载**:285 个 mod 全部走 Modrinth/CurseForge CDN,不经过 Pages
- **原创内容**:config / kubejs / scripts / resourcepacks(汉化包+数据覆写)入库分发
- **首次安装**:PCL2 导入整合包(含 bootstrap + 启动脚本),约 100MB
- **日常更新**:双击 `启动游戏.bat` → bootstrap 增量更新 → 启动游戏

**关键事实**:packwiz 仓库只存元数据(285+8 个 `.pw.toml`,每个几百字节)和原创内容,不存任何 mod jar。Pages 流量极小。

---

## 二、首次迁移(已完成)

迁移产物已在 `atl-modpack/` 目录就位,**index.toml 已生成、packwiz 已验证**:

```
atl-modpack/
├── pack.toml                     # 清单(已生成,含 NeoForge 21.1.241)
├── index.toml                    # 哈希索引(已生成,1036 个文件)
├── mods/                         # 285 个 .pw.toml(已验证 packwiz list 全部解析)
│   ├── create.pw.toml
│   └── ...
├── resourcepacks/                # 8 个 CDN 资源包元数据 + 原创资源包 + assets
│   ├── *.pw.toml                 # 8 个资源包元数据
│   ├── ResourcePacksJustForATL.zip   # 原创汉化包
│   └── assets/modpackroot.png    # 原创资源(已删 data 缓存)
├── config/                       # 701 个原创配置文件
├── kubejs/                       # 原创 kubejs 脚本
├── scripts/                      # 原创脚本
├── defaultconfigs/               # 原创默认配置
├── bootstrap/
│   ├── packwiz-installer-bootstrap.jar
│   └── 启动游戏.bat
├── server/
│   └── 同步mods.bat
├── tools/
│   ├── migrate.py                # 迁移脚本
│   └── packwiz-cli/packwiz.exe   # packwiz CLI(已解压,git 忽略)
├── .gitignore                    # git 追踪规则
├── .packwizignore                # packwiz 索引排除(维护素材不下发)
└── .github/workflows/build.yml   # Pages 自动部署
```

> 注:index.toml 已生成,可直接用。若未来手动改了 config 等原创文件,重新跑 `packwiz refresh` 即可。

### 剩余步骤(在本地终端执行)

**1. 本地验证**(强烈推荐,花 15 分钟):
```bash
cd "C:/Users/UuWuZhi/Downloads/atl-modpack"
./tools/packwiz-cli/packwiz.exe list          # 确认 293 项正常列出
./tools/packwiz-cli/packwiz.exe serve         # 起本地服务 http://localhost:8080/pack.toml
```
然后临时把 `bootstrap/启动游戏.bat` 里的 `PACK_URL` 改成 `http://localhost:8080/pack.toml`,跑一遍确认 285 个 mod 能下载、游戏能进。验证完改回 Pages 地址。

**2. git 初始化并推送**(见下文 git-bash 建工作区)。

---

## 二点五、用 git-bash 直接建工作区(不依赖 IDE)

> 你提到想用 git-bash 建工作区。下面是完整命令,`C:/Users/UuWuZhi/Downloads/atl-modpack` 已是建好的工作区,直接按 2~6 步走即可。

```bash
# 1. 进入工作区目录
cd "C:/Users/UuWuZhi/Downloads/atl-modpack"

# 2. 初始化仓库(生成 .git 目录)
git init

# 3. 改默认分支名为 main
git branch -M main

# 4. 查看哪些文件会被追踪(检查有没有误伤;绿色 = 会提交,灰色 = 被 .gitignore 忽略)
git status

# 5. 暂存全部文件
git add -A

# 6. 首次提交
git commit -m "feat: 整合包 packwiz 迁移初始化"

# 7. 关联远程仓库(把 <你的用户名> 换成真实的)
git remote add origin https://github.com/<你的用户名>/atl-modpack.git

# 8. 推送
git push -u origin main
```

**之后日常改动的流程**(只记 3 条):
```bash
git add -A
git commit -m "feat: 更新 XXX"
git push
```

**几个常用查看命令**:
- `git status` — 看改了哪些文件
- `git log --oneline` — 看提交历史
- `git diff` — 看未暂存的改动内容
- `git pull` — 拉取远程更新(多人协作时用)

> 小技巧:`.gitignore` 已配好,`git status` 会忽略 mod jar / 运行时产物 / 存档等。提交前建议瞄一眼 `git status` 确认没有意外文件。

---

## 三、日常维护(改 mod)

### 加一个新 mod

```bat
packwiz modrinth install <slug>      :: 例:packwiz modrinth install create
:: 或从 CurseForge:
packwiz curseforge install <id>
```

### 更新所有 mods 到最新

```bat
packwiz update --all
```

### 更新单个 mod

```bat
packwiz update <slug>
```

### 移除 mod

```bat
packwiz remove <slug>
```

### 改动 config / kubejs / 资源包

直接编辑仓库里对应文件即可,`packwiz refresh` 会重新计算哈希。

### 发布(每次改完统一动作)

```bat
packwiz refresh
git add . && git commit -m "feat: 更新 XXX"
git push
```

push 后 GitHub Actions 自动部署到 Pages,玩家 1~3 分钟内能增量更新到。

---

## 四、待人工处理清单(首次迁移后核对)

### 1. 48 个纯 CurseForge mod 的 update 块

这 48 个 mod 没有 Modrinth 源,`.pw.toml` 里写的是 `[update.curseforge]` + `file-id`。`file-id` 由下载 URL 解析(如 `8409/394` → `8409394`),**需人工在 CurseForge 页面确认正确性**。若确认无误,`packwiz update` 才能正常更新它们。完整清单见 `_missing_update.json`(含文件名 + file-id)。

### 2. side 标记核对

脚本按 Modrinth 的 client_side/server_side 自动判定 side。分布:191 both / 48 client / 46 server。**建议重点核对标为 `client` 的 48 个**(确保真不用于服务器,避免服务器缺依赖)。

### 3. 资源包差异

可玩实例里 `Minecraft-Mod-Language-Modpack-Converted-1.21.1.zip` 由 I18nUpdateMod 自动维护,**不纳入仓库**(正确)。若发现缺其他资源包,补进 `resourcepacks/`。

### 4. 客户端 bootstrap 里的 URL

`启动游戏.bat` 和 `同步mods.bat` 里的 `PACK_URL` 目前是占位符 `https://USER.github.io/atl-modpack/pack.toml`,**发布前必须替换**为你的真实 Pages 地址。

---

## 五、玩家操作手册(发给玩家)

### 首次安装

1. 从 QQ 群下载 `All The Leisures 导入包.zip`
2. PCL2 → 版本列表 → **导入整合包** → 选择下载的 zip
3. 导入完成后,进入整合包版本文件夹(可右键版本 → 打开文件夹)
4. 把 `启动游戏.bat` 发送到桌面快捷方式(或直接双击版本目录里的)

### 日常游玩

- **双击 `启动游戏.bat`**:
  - 自动检查更新(增量,通常几 KB~几十 MB)
  - 完成后自动打开 PCL2
  - 在 PCL2 里点启动游戏
- **无需重新下载整个整合包**,除非首次。

### 常见问题

| 现象 | 处理 |
|---|---|
| 双击脚本提示缺 java | 安装 Java 21,或用 PCL2 自带 Java(见脚本内注释) |
| 提示更新失败 | 检查网络;重试 |
| 进服报 mod 版本不符 | 等服务器维护完,重新双击脚本更新 |

---

## 六、服主操作手册(发给服主)

服务器根目录放 `同步mods.bat` + `packwiz-installer-bootstrap.jar`,每次开服前:

1. **双击 `同步mods.bat`**
   - 自动从 Pages 拉取 **server/both 侧** mods 到 `mods/`(纯客户端 mod 自动跳过,不会崩服)
   - 提示同步完成
2. **运行 `run.bat` 开服**(原有脚本)

> 服主无需懂 packwiz / git,只需双击 `同步mods.bat`。

---

## 七、发布新导入包(低频,可选)

当"首发/换人/大规模改动"时,重新打一个导入包:

1. 从当前可玩实例导出(不含 mods jar,含 config 等原创内容)
2. 把 `bootstrap/packwiz-installer-bootstrap.jar` 和 `启动游戏.bat` 放进包根目录
3. 上传到 QQ 群文件

玩家首次用这个新导入包,bootstrap 会自动补全到最新。之后仍走增量更新。

---

## 八、风险与兜底

| 风险 | 兜底 |
|---|---|
| Pages 被墙/慢 | 客户端 bootstrap URL 指向 Pages;若实测慢,可换成 SakuraFrp 自托管(见下) |
| 某 mod 下架 | `packwiz update` 报错 → 手动换源或移除 |
| NeoForge 版本升级 | 改 `pack.toml` 的 `versions.neoforge`,同时核对所有 mod 兼容 |
| 玩家脚本丢失 | 重新从导入包拷贝 bootstrap + 脚本 |
| 更新到一半断网 | bootstrap 有回滚机制;重跑脚本即可 |

### SakuraFrp 自托管备选

若 GitHub Pages 在你地区访问不畅,可在常开的 PC 上:

1. 下载 [packwiz CLI](https://nightly.link/packwiz/packwiz/workflows/go/main)
2. 在 `atl-modpack` 目录跑 `packwiz serve`(默认 8080 端口)
3. SakuraFrp 映射该端口 → 得到公网地址 `http://<frp地址>/pack.toml`
4. 把玩家/服主脚本里的 `PACK_URL` 改成该地址

> 注意:jar 仍走 CDN,自托管只承担几 MB 的小文件流量。两边 URL 随时可切换。

---

## 九、仓库约定

- **分支**:main 即 Pages 源,不要直接在 main 上乱改(用 PR 或至少 commit 信息规范)
- **.gitignore**:已配置,mod jar / 运行时产物 / 存档 / 个人设置均不入库
- **原创内容**:config、kubejs、scripts、resourcepacks/assets、resourcepacks/data、ResourcePacksJustForATL.zip 均为原创,入库分发
- **许可**:MIT(仅原创内容;mod/资源包遵循各自许可,仓库不含它们)
