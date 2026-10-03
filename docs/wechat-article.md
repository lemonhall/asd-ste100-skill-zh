# K 神让 AI 去学 40 年前的航空维修手册，我把它变成了中文技能

![封面：左边是写满绕句子、画着航空图纸的手册，右边是同一份内容变成整齐的清单](https://cdn.jsdelivr.net/gh/lemonhall/asd-ste100-skill-zh@main/docs/images/cover-2.35x1.png)

> 公众号文章草稿。仓库：https://github.com/lemonhall/asd-ste100-skill-zh

## 一、事情从 Karpathy 的一条推文开始

10 月 2 日，Andrej Karpathy 发了一条推，讲的是「怎么让大模型的输出变得更容易理解」，浏览量 460 万。

他给了四条技巧，一条比一条激进。先是让模型好好写字，然后画图，然后直接生成网页，最后干脆做成讲解视频。

但他放在第一条、也是唯一一条「Writing」里的建议，最出人意料：

> Ask your LLM to explain something in ASD-STE100, it's a controlled language specification originally developed for aerospace maintenance documentation.

翻译过来：**让大模型用 ASD-STE100 来解释一件事 —— 那是一套最初为航空维修文档开发的受控语言规范。**

ASD-STE100 是什么？1986 年，欧洲的航空公司遇到一个具体问题：维修手册要发给各国的技术人员看。这些人母语大多不是英语，身边也没有作者可以打电话问「你这句到底什么意思」。飞机上读错一条指令是会死人的。

于是航空业干了一件很极端的事 —— **给英语本身加限制**：

- 每个词只能有一个意思、一种词性（受控词表约 900 个词）。
- 一句话只准有一个动作。
- 程序性指令不超过 20 个词，说明性文字不超过 25 个词。
- 分号直接禁用。
- 一个名词短语最多堆 3 层。

最新的是 Issue 9（2025 年 1 月），53 条写作规则，9 个章节。

Karpathy 说他自己经常这么做，而且会**放松一点**：

> Sometimes I've tried to soften it a bit e.g. ask for "80% of the way to ASD-STE100" because the spec is quite stringent.

「我有时候会要求它做到 ASD-STE100 的 80%，因为这套规范相当严苛。」

他后面三条更激进：

> But even better: Diagrams / images. Instead of writing, ask your LLM to create a diagram.
>
> But even better: Web pages. Ask for output "in HTML" to get a beautiful, interactive webpage.
>
> But even better: Explainer videos. The output format I am most bullish on is fully custom / bespoke explainer videos generated on any arbitrary topic.

画图、网页、定制讲解视频 —— 他最后总结的那段话，是整条推的落点：

> As LLMs get better, they will do more and more of the legwork autonomously, and a lot more of our work will rise up the abstractions into oversight and understanding.
>
> Luckily, LLMs can help here too because as intelligence and code are increasingly abundant, you can ask for **large, custom, discardable software artifacts** that would never have made sense to create before.

**大模型把活干完，人的工作就往上移到「监督」和「理解」。幸运的是，AI 也能帮人做这部分工作。因为智能和代码越来越便宜，你可以为一件具体的事，临时造一个以前根本不值得造的产物。**

## 二、为什么这套规范对 Agent 特别有用

Karpathy 是从「人读模型输出」的角度讲的。但我觉得这套东西对**模型读模型输出**更狠。

一个 agent 读另一个 agent 写的工具描述或报错信息时，处境和技师一样：**没有追问的机会**。当年那个技师在停机坪上翻手册，身边也没有作者可问。它也不能回一句「你这里的『处理』是指删除还是重试」。

而中文的问题和英文还不一样。英文主要栽在两件事上：一个词多个意思、一句话多种结构。中文栽的地方很不一样：

| 中文的坏习惯 | 例子 |
| --- | --- |
| 虚动词 | 「对日志**进行分析**」而不是「分析日志」 |
| 套话 | 「**需要注意的是**，缓存会过期」 |
| 同义轮换 | 同一篇里「检查 / 校验 / 核对 / 确认」轮着用，读者不知道是一个动作还是四个 |
| 一句串三件事 | 「先开票**；**再发货」，或者「……**并且**……**从而**……」 |
| 翻译腔 | 「基于……的情况下」「对于……而言」 |
| 含糊词 | 「**若干**」「**一些**」「**相关**」 |

这些不是文风问题，是**信息损耗**。模型读到「进行适当的调整」，只能猜；读到「重试 2 次，间隔 3 秒」，不用猜。

## 三、我先装了英文版，然后发现不对味

社区在两个多月前就有人把 ASD-STE100 做成了开源技能：[danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)（现在近 3000 star，MIT）。它把规则用到工具描述、报错信息、system prompt、agent 间指令上，还分了两档：

- **Strict** —— 程序步骤、报错、工具描述这类「读错有代价」的文本。
- **STE-flavored** —— README、PR 描述这类说明文，保留句长与结构纪律，但不锁死用词。

我把它装进了我的 DSH（我日常跑的 Agent 环境），跑起来很顺。但用在自己身上就发现一个问题：**它是英文的，而我的绝大多数文本是中文。**

把英文规则直译过来，治不了上面那张表里的任何一条。因为中文的失败模式不是「一词多义」，也不是「分号」。比如「对日志进行分析」这种虚动词结构，英文里压根没有对应物。

## 四、于是我写了中文版

仓库：**https://github.com/lemonhall/asd-ste100-skill-zh**（MIT）

它不是翻译，是按中文的失败模式重写的：

- **规则重写**：虚动词、套话、同义轮换、分号串联、翻译腔、含糊词，每条都给「这样做 / 不要这样」的对照。
- **两档模式**：Strict（误读有代价的文本）与「中文-顺」（README、PR、说明文）。
- **一条铁律**：**情态是内容。「可能已失败」不能改成「失败」，「可能是 X 导致的」不能改成「X 是原因」。** 丢掉一个「可能」，不是简化，是换了一个结论。这是受控改写最常见的翻车方式，因为句长上限最容易引诱人去掉的正是这些词。

仓库里有一个只依赖标准库的 linter (`scripts/ste-lint-zh.py`)，11 条规则，硬违规 6 条、建议类 5 条：

```bash
python scripts/ste-lint-zh.py <文件>
python scripts/ste-lint-zh.py --selftest        # 20 项断言
python scripts/ste-lint-zh.py --max-chars 25 f  # 程序步骤用 25 字上限
python scripts/ste-lint-zh.py --baseline 12 f   # 存量文档：容忍 12 处硬违规
```

拿一段很典型的「AI 味中文」试一下：

> 本工具将会尝试对已经配置好的各个后端进行状态同步，如果检测到冲突，则会根据所设置的策略对其进行处理；否则将把冲突提交人工复核。需要注意的是，这套方案强大且无缝。用户可以在必要时做一些适当的调整。

linter 输出 10 处发现，其中 7 处硬违规：

- 57 字长句
- 同义轮换（配置 / 设置）
- 虚动词「进行处理」
- 分号串联
- 套话
- 两个营销形容词
- 三个含糊词

改写之后是：

> 本工具同步各个已配置后端的状态。如果发现冲突，本工具读取已配置的策略。策略允许自动处理时，本工具直接处理冲突。策略不允许时，本工具把冲突交给人工复核。

仓库里还有 8 组前后对照：工具描述、报错、agent 间指令、状态汇报、PR、README、system prompt、日志。每一组都标出违反了哪条规则，以及改写为什么没有丢失信息。

## 五、怎么装

**在 DSH 里，一句话就够。** 对着你的 agent 说：

> 把这个技能装给你自己：https://github.com/lemonhall/asd-ste100-skill-zh

它会自己 clone 到本地、在宿主插件里注册这个技能、跑一遍 `--selftest` 验证，然后告诉你装好了。之后你说「把这段报错改写清楚」「这段 README 读起来绕，帮我顺一下」，它就会用这套规则。

（DSH 的一个坑：`~/.dsh/skills` 和 `~/.agents/skills` 这两个目录它**不认**，技能必须是宿主插件在运行时注册的。所以别手动拷文件，让 agent 自己接。）

**Claude Code / 支持 Agent Skills 的客户端：**

```bash
npx skills add lemonhall/asd-ste100-skill-zh
```

**读 AGENTS.md 的 agent（Codex 等）：** 把仓库 README 里那段规则粘进 `AGENTS.md` 就行，那一段本身就是用受控中文写的。

英文文本还是用上游的 [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)，两个技能在我这儿并存：中文走 `ste-zh`，英文走 `asd-ste100`。

## 六、最后

Karpathy 那条推的真正意思是：**当智能和代码变得便宜，你可以为一件事临时造一个以前不值得造的产物。** 一份技能文件、一个 200 行的 linter，都属于这类东西。它们不会是产品，但它们让你每天写的东西清楚一点。

而「写清楚」最容易忽略的地方在于：受益人不止是读你文档的人，还有**下一个读你输出的模型**。给机器写的东西，越不含糊，它越不会跑偏。

规范和工具都在那儿了，改不改，就看你了。

*（这篇稿子自己也被 linter 过了一遍：`python scripts/ste-lint-zh.py --max-chars 45 docs/wechat-article.md`。剩下的命中全落在文中引用的病句上 —— 那是它们能当例子、不能当正文的证据。）*

---

*仓库：https://github.com/lemonhall/asd-ste100-skill-zh*
*上游：https://github.com/danyuchn/asd-ste100-skill*
*Karpathy 原推：https://x.com/karpathy/status/2105819303471976479*
