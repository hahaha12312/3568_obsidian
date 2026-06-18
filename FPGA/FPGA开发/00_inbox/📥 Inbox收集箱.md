---
tags:
  - MOC
  - inbox
date: 2026-06-18
---

# 📥 Inbox 收集箱

> 💡 **使用方式**：学到一个零散知识点 → 按 `Ctrl+N` 新建笔记 → 用下方模板快速记录 → 存在本目录下 → 每周整理归类。

---

## ⚡ 快速收集模板

```markdown
---
tags:
  - inbox
  - FPGA
date: {{date}}
status: inbox
---

# {{title}}

## 一句话总结
（用一句话说清楚这是什么知识点）

## 详细内容
（代码、截图、链接……随便写，不用排版）

## 待归类到
- [ ] 10_Syntax（语法理论）
- [ ] 20_Modules（核心模块）
- [ ] 30_Projects（实战项目）
```

---

## 📋 当前 Inbox 待处理

```dataview
TABLE date AS "收集日期", file.cday AS "创建日期"
FROM "FPGA开发/00_inbox"
WHERE status = "inbox" AND file.name != "📥 Inbox收集箱"
SORT file.cday ASC
```

---

## ✅ 已归档的 Inbox 条目

```dataview
TABLE date AS "收集日期", status AS "状态"
FROM "FPGA开发/00_inbox"
WHERE status = "processed" AND file.name != "📥 Inbox收集箱"
SORT date DESC
LIMIT 20
```
