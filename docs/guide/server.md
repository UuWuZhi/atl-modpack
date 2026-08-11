# 服务端指南 — All The Leisures

> 面向服主。维护服务器,把 mods 同步到最新。

---

## 首次准备

服务器需要以下文件(放服务器根目录,与 `run.bat` 同级):

| 文件 | 来源 |
|---|---|
| `packwiz-installer-bootstrap.jar` | 从导入包 / 仓库 `bootstrap/` 目录获取 |
| `同步mods.bat` | 从仓库 `server/` 目录获取 |
| `run.bat`(已有) | 原有开服脚本 |

> 服务器**不需要**装 packwiz、不需要 git、不需要理解版本控制。只需双击脚本。

---

## 日常开服流程

每次维护/开服前:

1. **双击 `同步mods.bat`**
   - 自动从 GitHub Pages 拉取 **server/both 侧** mods 到服务器 `mods/`
   - 纯客户端 mod(小地图、JEI 等)自动跳过,不会上服务器
   - 完成后提示「mods 已同步」
2. **双击 `run.bat` 开服**(原有脚本)

> 就这么简单。服主唯一要做的事 = 开服前双击同步脚本。

---

## 工作原理

```
服务器双击 同步mods.bat
        ↓
bootstrap 读 Pages 的 pack.toml + index.toml
        ↓
按 side 过滤(只要 server/both 侧)
        ↓
对比本地 mods/ → 下载变化的部分
        ↓
mods 就绪 → 开服
```

- mod jar 从 Modrinth/CurseForge CDN 下载
- 增量更新,不会重下全部
- `packwiz.json`(状态文件)会生成在服务器根目录,勿删

---

## 常见问题

### 同步失败 / 网络错误

检查服务器网络;重试。若 Pages 不通,联系维护人。

### 提示「缺少 packwiz-installer-bootstrap.jar」

把 bootstrap jar 复制到服务器根目录(与 `同步mods.bat` 同级)。

### 玩家进服报 mod 版本不符

服务器 mods 和玩家不同步了:
1. 确认服务器跑过 `同步mods.bat`
2. 让玩家双击 `仅更新.bat` 更新到最新

### 想查看当前服务器 mods

看 `mods/` 文件夹里的 jar。`同步mods.bat` 只管理整合包内的 mod,你自己额外加的 mod 不受影响(但可能导致玩家不同步)。

---

## 建议

- **维护前先同步**:改 mod 前先 `同步mods.bat`,避免开着旧版改。
- **保留备份**:`simplebackups` 或自建备份,防止同步出问题。
- **只同步不改**:不要在服务器 `mods/` 手动增删 mod,否则会被 `同步mods.bat` 覆盖或导致不一致。
