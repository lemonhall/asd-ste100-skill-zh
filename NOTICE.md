# 归属与差异

## 上游

- **英文版技能**：[danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)（MIT License, Copyright (c) danyuchn）。
  它把 ASD-STE100 的规则类别做成了 Claude Code / agent 技能，并提供英文 linter `scripts/ste-lint.py`。
- **标准本身**：ASD-STE100（Simplified Technical English），ASD 发布，Issue 9（2025-01）。标准免费获取，
  但正文与约 900 词的受控词表**不可自由再分发**。上游与本仓库都只复述规则类别，不含其正文与词表。

## 本仓库做了什么

不是翻译，是按中文的失败模式重写：

| | 上游 | 本仓库 |
|---|---|---|
| 语言 | 英文 | 中文 |
| 主要失败模式 | 一词多义、结构歧义 | 虚动词、套话、同义轮换、分号串联、翻译腔 |
| 词表 | 依赖 ASD 的 ~900 词受控词表（不复制） | 中文没有对应标准，词汇规则明确降级为「方向」 |
| 句长口径 | 按词：程序 ≤ 20、说明 ≤ 25 | 按字：指令 ≤ 25、说明 ≤ 40（linter 默认 40） |
| linter | `scripts/ste-lint.py` | `scripts/ste-lint-zh.py`（另写，非移植） |
| 情态 | 不标记 | 不标记，并写进自检断言 |

规则类别与上游对应关系见 [`references/writing-rules.md`](references/writing-rules.md) 第二节。

## 许可

本仓库 MIT（见 LICENSE）。上游同为 MIT，规则类别属思想与分类，不受版权限制；
上游的具体文字、示例与代码未被复制到本仓库。
