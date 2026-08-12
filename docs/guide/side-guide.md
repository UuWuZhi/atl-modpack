# MOD 端别判定手册 — 怎么标记 client/server/both

> 面向维护人。packwiz 用 `side` 字段决定这个 mod 下载到哪:
> - `both` — 客户端 + 服务器都要(绝大多数 mod)
> - `client` — 只有客户端要(小地图、JEI、优化渲染类)
> - `server` — 只有服务器要(服务端插件/逻辑类)

**Modrinth 自己标的 side 很乱,必须人工确认,不能直接信。**

---

## 一、为什么不能信 Modrinth 的标记

Modrinth 的 `client_side`/`server_side` 含义是"**这个 mod 在纯客户端/纯服务器端能否运行**",不是"**整合包是否该两端都装**"。

典型的坑:

| Modrinth 标记 | 实际含义 | 整合包该标 |
|---|---|---|
| `client_side: optional, server_side: required` | 纯客户端也能玩,但**内容主要在服务器生成** | **both**(create、terralith、YUNG 这类世界生成,客户端不装就看不到) |
| `client_side: unsupported, server_side: required` | 官方说纯客户端不适用 | **both**(同上一堆结构/世界 mod,实际客户端需要) |
| `client_side: required, server_side: unsupported` | 纯客户端渲染类 | **client**(小地图、JEI、光影) |

> 我们的整合包是**多人联机**,服务器 + 客户端跑同一套完整内容。所以世界生成/内容/机制类 mod 一律 `both`,只有"纯 UI/渲染/客户端增强"才是 `client`。

---

## 二、判定规则(按优先级)

### 规则 1:崩溃/依赖测试(最准)

改完 side 后,实际进游戏测:
- 客户端进服不报错 → both 或 client
- 服务器启动不报错 → both 或 server
- **若某个 both 改成 client,客户端缺它,进服必然报"requires X"崩溃** → 那它就是 both

### 规则 2:按 mod 类型(经验)

| 类型 | 标记 | 例子 |
|---|---|---|
| 机械/科技(create 系) | **both** | create, createaddition, createaeronautics |
| 世界生成 | **both** | terralith, tectonic, YUNG 系列, c2me |
| 结构/村庄 | **both** | repurposed_structures, Moogs 系列, ctov |
| 内容/物品 | **both** | 绝大多数食物、装饰、生物 mod |
| 库/API | **both** | 几乎所有前置库 |
| 小地图 | **client** | xaero, journeymap |
| JEI/物品管理 | **client** | jei, jeed, inventoryprofilesnext |
| 渲染/优化(纯客户端) | **client** | sodium, iris, reeses-sodium-options |
| 服务端逻辑 | **server** | 几乎没有(整合包场景) |

### 规则 3:不确定 → 标 both

**整合包场景下,不确定就标 both。** 标 both 的唯一代价是服务器多装一个客户端增强 mod(通常无害);标错 server/client 会导致客户端缺 mod 崩溃(灾难)。

---

## 三、怎么改 side

编辑 `mods/xxx.pw.toml`:

```toml
side = "both"    # 或 "client" / "server"
```

改完必须:
```bash
python tools/push.py -m "fix: 调整 xx mod side"
```

这只会推送到 dev,不会刷新 `index.toml`。确认可发布后再运行:

```bash
python tools/push.py --release
```

发布工具会在 main 上执行 `packwiz refresh`,更新 index hash 后再推送给玩家。

---

## 四、批量检查现有 side

```bash
# 查看所有标为 server 的 mod(最可疑,多半该是 both)
grep -l '^side = "server"' mods/*.pw.toml

# 查看所有标为 client 的
grep -l '^side = "client"' mods/*.pw.toml

# 查看分布
grep -h "^side" mods/*.pw.toml | sort | uniq -c
```

---

## 五、当前已知的正确标记

### 必须是 both(已修正,勿改回)
- create 系列:create, createaddition, createaeronautics-bundled, createliquidfuel
- 世界生成:terralith, tectonic, c2me, alltheleaks
- 结构:repurposed_structures, YUNG 全系列, Moogs 全系列, ctov
- 内容:Oh-The-Trees-Youll-Grow, almostunified, cristellib, villagernames 等

### 合理是 client(勿改 both)
- xaero 小地图/世界地图
- jei / jeed / JustEnoughProfessions
- sodium / iris / reeses-sodium-options
- inventoryprofilesnext(一键背包)

> 判断原则:这个 mod 是不是"纯客户端 UI/渲染"?是 → client;不确定 → both。

---

## 六、为什么标错会导致崩溃(回顾)

46 个世界生成/内容 mod 曾被误标 `server` → 客户端更新**不下载** → create 缺失 → 依赖 create 的 mod 全报 `requires create` 崩溃。修复:全改 both,客户端重新更新即恢复。
