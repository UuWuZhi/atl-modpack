# 实战演练:开发者更新 kubeJS 脚本并分发到玩家

> **场景**:一位开发者(已有工作区 + 可运行实例)修改了 kubeJS 脚本,
> 需要推送到 GitHub 仓库,并让已装好工具链的玩家通过更新脚本下载到最新内容。

---

## 前置条件

| 角色 | 状态 |
|---|---|
| 开发者 | 已 clone 仓库(`atl-modpack`),有可运行实例(内含 `仅更新.bat`) |
| 玩家 | 已导入整合包,版本目录内有完整工具链(`仅更新.bat` + bootstrap) |
| 仓库 | main 分支,Pages 已开启(自动部署) |

---

## 一、开发者侧:修改 + 推送

### 第 1 步:改 kubeJS 脚本

在**工作区**里编辑对应文件(不是开发实例):

```bash
# 在仓库根目录
vim kubejs/client_scripts/main.js   # 或任何编辑器
# 添加你的改动...
```

> **关键原则**:改代码在「仓库」,测试在「实例」。两者通过 push + bootstrap 打通。

### 第 2 步:重建索引(packwiz refresh)

```bash
cd atl-modpack
packwiz refresh
```

**这一步做了什么**(重要,理解才不易出错):
- 重新计算所有文件的 sha256
- 更新 `index.toml` 里 **main.js 的 hash**(因为内容变了)
- 更新 `pack.toml` 里 **整个 index 的 hash**

> 实测:改 main.js 后 refresh,index 里 main.js hash 从 `3df46f...` → `6cc4431...`,pack.toml 的 index hash 也变了。

### 第 3 步:检查改动(可选但推荐)

```bash
git status          # 看改了哪些文件(应含 kubejs/*.js + index.toml + pack.toml)
git diff index.toml # 确认只有预期文件的 hash 变了
```

### 第 4 步:提交 + 推送

```bash
git add -A
git commit -m "feat: 更新 kubeJS 脚本,新增 XX 功能"
git push
```

### 第 5 步:本地测试(在自己的实例)

在**开发实例**里:

```bash
# 双击 仅更新.bat,或命令行:
java -jar packwiz-installer-bootstrap.jar -g https://uuwuzhi.github.io/atl-modpack/pack.toml
```

启动游戏,验证改动生效。

> 若 push 后立即测,Pages 可能要 1~3 分钟才更新。可以等一会再测。

---

## 二、玩家侧:拉取最新内容

### 玩家操作(已装好工具链)

双击版本目录里的 **`仅更新.bat`**(或 `启动游戏.bat`):

```
[1/2] 检查更新中...
[2/2] ...（下载变化的部分）
[完成] 整合包已是最新。
```

**发生了什么**:
1. bootstrap 读取 `https://uuwuzhi.github.io/atl-modpack/pack.toml`
2. 对比本地 `packwiz.json` 记录的文件与最新 `index.toml`
3. 发现 `kubejs/client_scripts/main.js` 的 hash 与本地不同
4. **只下载这一个文件**(增量),从 Pages 拉取
5. 更新本地 hash 记录

> 玩家**不需要重新下载整个整合包**,只下载变化的几个文件(通常几十 KB)。

---

## 三、服务器侧(若本次改动影响服务器)

如果改动涉及 `kubejs/server_scripts/`(服务端脚本),服主需要同步:

1. 双击服务器根目录的 `同步mods.bat`
2. 重启服务器让脚本生效

> kubeJS 的 server_scripts 在服务器上运行,必须同步到服务器。

---

## 四、原理图

```
开发者改 kubejs/main.js
   │  packwiz refresh (index.toml hash 更新)
   │  git push
   ▼
GitHub Pages(1~3 分钟自动部署)
   │  index.toml: main.js hash = 6cc4431...
   │  kubejs/client_scripts/main.js (新内容)
   ▼
玩家双击 仅更新.bat
   │  bootstrap 读 Pages index → 对比本地
   │  main.js hash 不同 → 只下载 main.js
   ▼
玩家 main.js 更新到最新
```

---

## 五、常见问题

### 玩家更新后没变化

1. 确认 push 已完成且 Pages 部署成功(等 1~3 分钟)
2. 确认 `packwiz refresh` 已跑(否则 index 里 hash 是旧的)
3. 玩家可能没跑更新脚本,或 bootstrap 下载被网络中断(重试)

### 改了 config 而不是 kubejs

流程**完全一样**:改文件 → `packwiz refresh` → push。config 文件同样被 index 管理,玩家增量拉取。

### 删除了一个 mod

`packwiz remove <slug>` → refresh → push。玩家 bootstrap 会**删除本地多余的 mod**。

### 玩家报"hash 对不上"错误

可能是行尾(CRLF/LF)导致 hash 不一致。已通过 `.gitattributes` 强制 LF 规避。若仍出现,让玩家删掉对应文件再更新。

### 改了 server_scripts 但玩家没到

server_scripts 是**服务端**的,玩家端不加载。只需同步服务器即可(第三节)。

---

## 六、检查清单(发布前)

- [ ] `packwiz refresh` 已执行
- [ ] `git status` 确认只改了预期的文件
- [ ] `git add -A && git commit && git push` 完成
- [ ] 等 1~3 分钟 Pages 部署
- [ ] (可选)自己在开发实例测试一次
- [ ] 若涉及服务端,通知服主同步
