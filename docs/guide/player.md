# 玩家指南 — All The Leisures

> 面向普通玩家。如果你只是想进服玩,看这一篇就够了。

---

## 首次安装

1. **下载导入包**:从 QQ 群 / GitHub Release 下载 `modpack.mrpack`
2. **导入 PCL2**:
   - 打开 PCL2 → 左侧「版本列表」→ 右上角「导入整合包」
   - 选择下载的 `modpack.mrpack` → 确认导入
3. **等待下载**:首次会下载全部 mods(约 560MB),请耐心。**若速度慢,可看文末"下载太慢"一节**
4. **进入整合包文件夹**:
   - 版本列表 → 右键该版本 → 「打开游戏文件夹」
   - 确认里面有:mods 文件夹、config 文件夹、以及 `packwiz-installer-bootstrap.jar`、`启动游戏.bat`、`仅更新.bat`

> 首次安装后,版本目录内**自带更新工具链**,无需手动配置。

---

## 日常游玩

| 情况 | 操作 |
|---|---|
| 更新 + 启动 | 双击 `启动游戏.bat`(先更新,再打开 PCL2) |
| 只想更新 | 双击 `仅更新.bat`(更新完自己开 PCL2 点启动) |
| 服务器维护后 | 先双击 `仅更新.bat` 更新到最新,再进服 |

> **不需要重新下载整个整合包**,更新是增量的(通常几 KB ~ 几十 MB)。

---

## 常见问题

### 双击脚本提示「缺少 packwiz-installer-bootstrap.jar」

说明工具链没进你的版本目录。重新导入一次导入包,或手动从 QQ 群获取 bootstrap jar 放到版本目录。

### 提示「未找到 Java」

安装 Java 21,或确认 PCL2 自带 Java。脚本会自动探测 PCL2 的 java。

### 更新失败 / 网络错误

检查网络后重试;若持续失败,联系维护人。

### 进服报「mod 版本不符」

服务器可能刚维护完,你还没更新。双击 `仅更新.bat` 后再进服。

### 下载太慢(首次导入时)

首次导入要下全部 mods,速度取决于下载源:
- 大部分 mod 走 Modrinth CDN(较快)
- 少部分(纯 CurseForge)走 CurseForge,国内可能慢

**建议**:首次导入时挂梯子(加速 CurseForge),或选网络空闲时段。后续增量更新基本很快。

---

## 更新机制(了解一下)

```
维护人改 mod / 配置 → push 到 GitHub
        ↓ 自动
GitHub Pages 更新(1~3 分钟)
        ↓
你双击 仅更新.bat → bootstrap 对比本地与最新 → 只下载变化的部分
```

- **mod jar** 从 Modrinth/CurseForge CDN 下载
- **config/kubejs 等配置** 从 GitHub Pages 下载
- 更新是**增量**的,不会重下全部

---

## 目录结构说明

```
<版本目录>/
├── mods/              # mod jar(PCL2 导入时自动下载)
├── config/            # 游戏配置
├── kubejs/            # 自定义脚本
├── resourcepacks/     # 资源包
├── packwiz-installer-bootstrap.jar   # 更新工具
├── 启动游戏.bat                       # 更新+启动
└── 仅更新.bat                        # 仅更新
```
