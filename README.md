# code-to-mermaid-flowchart

从软件仓库的**真实源代码执行路径**生成、审核和维护 Mermaid 算法流程图的可复用 Agent Skill。

以代码为执行逻辑依据，以用户指定的论文为数学符号依据，保留初始化、约束、循环、终止、异常和回退语义。适用于 Python、C++、JavaScript、TypeScript 等项目，不绑定特定仓库或算法。

## 用途与任务模式

| 模式 | 用途 |
| --- | --- |
| 生成 | 阅读实现，建立源码追踪记录并生成 Mermaid flowchart |
| 审核 | 只读比较已有流程图和代码，报告遗漏或错误 |
| 同步 | 根据代码变更更新流程图及来源证据 |
| Web 集成 | 在指定的现有页面集成搜索、选择、缩放、全屏与下载 |
| 验收 | 检查语法、数学排版、浏览器交互及 SVG/PNG 导出 |

模式可以组合。仅要求数值求解或性能优化、没有流程图任务时，不应触发此技能。

主要规则：

- 默认使用 `flowchart TD`，一个节点原则上只表达一个操作或判断。
- 真实外部调用使用双边框子程序节点；不为复用图形而虚构辅助函数。
- 根据实际控制流、约束及失败语义区分算法变体。
- 为节点和分支记录实现文件、函数、行号、源码哈希与 Git commit。
- 使用论文符号前先解释含义，区分论文定义与工程变量。
- 数学表达式采用目标 Mermaid 版本支持的 KaTeX 语法。
- Web 功能按任务需要实施；不默认给所有项目增加工作台。
- 不默认改变算法、运行昂贵实验、修改实验结果、提交或推送业务仓库。

## 文件结构

| 文件 | 作用 |
| --- | --- |
| `SKILL.md` | 技能元数据、模式选择、主工作流和资源索引 |
| `agents/openai.yaml` | UI 展示信息与默认调用提示 |
| `references/code-tracing.md` | 源码追踪方法与 JSON 证据格式 |
| `references/variant-analysis.md` | 算法差异矩阵及图形复用规则 |
| `references/mermaid-style.md` | 节点、分支、循环和调用边界规范 |
| `references/math-notation.md` | 论文符号映射与 KaTeX 排版规则 |
| `references/browser-acceptance.md` | 真实浏览器、交互和导出验收流程 |
| `references/deliverables.md` | 交付物、任务边界和结果状态 |
| `references/application-example.md` | Spherical-Flow / FastMonoPaper 可选案例 |
| `references/evaluation.md` | 技能正向、负向触发与行为评估场景 |
| `scripts/validate-trace.py` | 校验追踪记录与本地源码的一致性 |
| `scripts/test-trace.py` | 校验器的隔离回归测试 |
| `README.md` | 安装与使用说明 |
| `LICENSE` | MIT 许可证 |

## 安装

### Codex 用户级安装

需要 Git。首次安装时，将整个仓库克隆到用户级技能目录；目标目录应尚不存在。

**Linux、macOS 或 Git Bash：**

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/ncut-d1z/code-to-mermaid-flowchart.git "$HOME/.agents/skills/code-to-mermaid-flowchart"
```

**Windows PowerShell：**

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
git clone https://github.com/ncut-d1z/code-to-mermaid-flowchart.git "$HOME/.agents/skills/code-to-mermaid-flowchart"
```

确保 `SKILL.md` 直接位于 `code-to-mermaid-flowchart` 目录下。Codex 支持用户级 `~/.agents/skills` 目录；如果新增技能没有出现，重启 Codex。参见 [官方技能文档](https://learn.chatgpt.com/docs/build-skills)。

如仅供某个项目使用，也可将完整技能目录放在该项目的 `.agents/skills/code-to-mermaid-flowchart/`。避免同时安装多份同名技能。

### 更新

先确认安装目录中的本地修改已经妥善保存，然后执行：

```bash
git -C "$HOME/.agents/skills/code-to-mermaid-flowchart" pull --ff-only origin main
```

若出现冲突或分支分叉，先检查差异，不要直接覆盖本地改动。

### ChatGPT Work / 浏览器环境

本地安装不会自动安装到另一台设备或浏览器运行环境。需要在目标环境支持的技能机制中安装，或按其插件规范打包分发；参见 [插件技能文档](https://developers.openai.com/plugins/build/skills)。

技能提供工作流，不提供仓库访问凭据、浏览器或执行权限。读取私有仓库、运行脚本和真实浏览器验收，需要目标环境具备对应工具与授权。

## 使用

在已安装技能的 Codex 会话中显式输入 `$code-to-mermaid-flowchart`，也可以用自然语言提出匹配的流程图任务，由宿主决定是否自动选择技能。

### 从代码生成流程图

```text
$code-to-mermaid-flowchart
分析当前仓库 main 分支的 solve 入口和相关后端。
先建立源码追踪表、算法变体差异矩阵，再生成 Mermaid flowchart。
将结果写入 docs/flowcharts/，不运行数值实验，不修改算法实现。
```

### 只读审核

```text
$code-to-mermaid-flowchart
只读审核 docs/solver.mmd 是否与当前源码一致。
检查初始化、循环更新、退出条件和失败回退，给出代码位置及修改建议。
不要修改任何文件。
```

### 同步与 Web 验收

```text
$code-to-mermaid-flowchart
比较指定基线 commit 与当前 commit，更新受影响的算法流程图。
集成到现有程序流程图页面，保留搜索、缩放及全屏算法切换。
使用项目固定的 Mermaid/KaTeX 版本，在真实浏览器验证源码、SVG 和 PNG 下载。
逐项报告 PASS、FAIL、BLOCKED 或 NOT APPLICABLE。
```

请将“指定基线 commit”替换为实际 SHA。任务中可配置仓库、分支、commit、算法列表、参考论文、输出路径、集成位置和测试方式。

### Spherical-Flow 案例

```text
$code-to-mermaid-flowchart
读取 https://github.com/ncut-d1z/Spherical-Flow-beats-RANSAC 的实际实现，
参考 https://github.com/ncut-d1z/FastMonoPaper 的相关符号定义。
先分析实际存在的 Gram/Thin-SVD、LEGACY/CHECKED、unsigned/halfspace 差异，
再生成相应流程图。本轮仅生成文档，不修改算法或运行实验。
```

此案例不会成为其他项目的默认配置。若需要工作台集成，请额外指定页面和交付范围。

## 脚本与验证

脚本使用 Python 标准库，建议 Python 3.9 或更新版本，并确保 `python` 指向 Python 3。回归测试还需要 Git。Mermaid、KaTeX 和浏览器依赖由目标项目提供；本技能不强制安装统一的前端依赖。

在技能仓库根目录执行回归测试：

```bash
python scripts/test-trace.py
```

测试使用临时目录，覆盖有效记录、缺失分支证据、过期哈希、越界行号、路径越界、无效数据、Git 来源和工作区状态等情况。

按 [源码追踪格式](references/code-tracing.md) 创建实际任务的 `trace.json`，再执行：

```bash
python scripts/validate-trace.py /path/to/trace.json --root /path/to/source-repository
```

| 退出码 | 含义 |
| --- | --- |
| 0 | PASS：源码证据结构及本地引用检查通过 |
| 1 | FAIL：记录格式、哈希、位置或其他检查不符 |
| 2 | BLOCKED：根目录、清单或必要 Git 来源不可用 |

**校验器不解析 Mermaid，也不能证明流程图与代码在语义上等价。** 节点/边 ID 的检查限于证据清单内部；与实际 Mermaid 图的对应关系需要另外检查。

真实浏览器与导出验收遵循 [验收规范](references/browser-acceptance.md)，使用项目实际环境执行。没有运行的测试不能标记为通过；PNG 检查清晰度与完整性，SVG 还需检查数学内容、结构和独立显示效果。

## 许可证

本项目采用 [MIT License](LICENSE)，版权声明为 `Copyright (c) 2026 ncut-d1z`。
