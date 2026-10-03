# 受控中文技术写作技能（ASD-STE100 中文化）

把含糊、啰嗦、容易被误读的中文技术文本，改写成受控中文：一句一动作、主动语态、一词一义、去名词化、
去营销形容词与套话。

读者是**没有追问机会的另一方**：另一个 agent、翻译管线、非母语读者、半年后的你自己。

这个仓库是英文技能 [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) 的中文对应物，
**不是翻译**：ASD-STE100 是为了让航空维修工不可能读错英文而做的受控英语，中文的失败模式不一样
（虚动词、套话、同义轮换、分号串联、翻译腔），所以规则按中文重写。差异清单见 [NOTICE.md](NOTICE.md)。

## 前后对照

| 原文 | 改写后 |
|---|---|
| 本工具将会尝试对已经配置好的各个后端进行状态同步，如果检测到冲突，则会根据所设置的策略对其进行处理；否则将把冲突提交人工复核。 | 本工具同步各个已配置后端的状态。如果发现冲突，本工具读取已配置的策略。策略允许自动处理时，本工具直接处理冲突。策略不允许时，本工具把冲突交给人工复核。 |
| 需要注意的是，该任务已经完成了，产物已经生成出来了，相关的文件都已经保存好了。 | 任务已完成，产物可读。全部输出文件已写入 `dist/`。 |
| 这是一个一站式、全方位的解决方案，可以赋能开发者快速构建强大的应用，让开发体验丝滑顺畅。 | 这个库把构建、测试、部署三步合成一条命令：`dev up`。默认配置下，一条命令可以跑起本地环境（Node 20+，首次约 40 秒）。 |

更多（工具描述、报错、agent 间指令、状态汇报、PR、README、system prompt、日志）见
[`examples/before-after.md`](examples/before-after.md)。

## 安装

### Claude Code / 支持 Agent Skills 的客户端

```bash
npx skills add lemonhall/asd-ste100-skill-zh
```

或者克隆到个人技能目录：

```bash
git clone https://github.com/lemonhall/asd-ste100-skill-zh ~/.claude/skills/ste-zh
```

### Codex / 其它读 AGENTS.md 的 agent

把下面这段放进项目的 `AGENTS.md`（或全局指令文件）即可：

> 改写中文技术文本时套用受控中文规则：一句一动作、主动语态、一词一义（同一概念全篇同一个词）、
> 不用分号连接动作、句长（指令 ≤ 25 字、说明 ≤ 40 字）、去掉虚动词（进行 / 加以 + 名词）、
> 套话（需要注意的是、在一定程度上）、营销形容词（无缝、强大、赋能、闭环）与含糊词（若干、一些、相关）；
> **不得改动情态**（可能 / 也许）：置信度是内容。机械首查用
> `python <repo>/scripts/ste-lint-zh.py <文件>`。

### DSH（DeepSeek Harness）

DSH 的 `skill` 工具只认**已注册**的技能，`~/.dsh/skills` 与 `~/.agents/skills` 目录不会被扫到。
可靠做法是由一个本地宿主插件在启动时注册：

```js
ctx.inject(['skills'], (scoped) => {
  scoped.skills.register({
    name: 'ste-zh',
    description: '把含糊、啰嗦、易误读的中文改写成受控中文……',
    content: readFileSync('E:/development/asd-ste100-skill-zh/SKILL.md', 'utf8').replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ''),
    source: 'runtime',
    path: 'E:/development/asd-ste100-skill-zh/SKILL.md',
  })
})
```

宿主侧改动热生效，注册完 `skill({ name: 'ste-zh' })` 当场可加载。

## 用法

```
把这段报错改写清楚
按受控中文改一遍这个工具描述
这段 README 读起来绕，帮我顺一下
给这段 agent 指令消歧义
```

默认只返回改写后的正文。想看清改了哪几处，加一句「给我看 diff」或「违反了哪些规则」，
会输出「违反的规则 / 原文 / 改写后」的表格。

## linter

仅标准库，Python 3.8+：

```bash
python scripts/ste-lint-zh.py <文件...>          # 检查文件（不给文件则读 stdin）
python scripts/ste-lint-zh.py --json <文件>      # 结构化输出
python scripts/ste-lint-zh.py --max-chars 25 f   # 程序步骤用 25 字上限
python scripts/ste-lint-zh.py --baseline 12 f    # 存量文档：容忍 12 处硬违规
python scripts/ste-lint-zh.py --disable vague-word,synonym-rotation f
python scripts/ste-lint-zh.py --list-rules       # 列出全部规则
python scripts/ste-lint-zh.py --selftest         # 自检（20 项）
```

硬违规：`semicolon`、`long-sentence`、`nominalization`、`marketing-adjective`、`empty-phrase`、
`synonym-rotation`（超过 `--baseline` 时退出码 1）。
建议类：`passive-voice`、`compound-aspect`、`vague-word`、`halfwidth-punct`、`dash-join`（只报告）。
**永不标记情态** —— 自检里有一条断言：「请求可能已失败。」必须干净。

linter 只做机械首查：它不比较原文与改写、不判断情态强度、不证明原意保留。零违规只说明这几项机械检查没发现问题。

## 仓库结构

```
SKILL.md                     技能正文（规则、模式、流程、输出格式、边界）
references/writing-rules.md  规则全集 + 与上游九节 53 条的对应 + 中文特有的坑
examples/before-after.md     8 组前后对照；after-only.md 是改写列的 lint 夹具（硬违规 0）
scripts/ste-lint-zh.py       确定性 linter（stdlib-only，含 --selftest）
NOTICE.md                    与上游的关系、差异清单、许可
```

自检：

```bash
python scripts/ste-lint-zh.py --selftest          # 应打印 selftest OK
python scripts/ste-lint-zh.py examples/after-only.md  # 应打印 硬违规 0 处（退出码 0）
```

## 许可

MIT。规则分类参考上游 danyuchn/asd-ste100-skill（MIT）；未复制其文字、示例与代码。
ASD-STE100 标准正文与受控词表不在本仓库中。
