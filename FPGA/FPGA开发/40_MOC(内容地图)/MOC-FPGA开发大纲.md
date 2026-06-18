---
tags:
  - MOC
  - FPGA
date: 2026-06-18
---

# 🗺️ FPGA 开发知识地图

> 这是你的 FPGA 学习中枢。从这里出发，可以抵达任何知识点。

---

## 📥 Inbox 收集箱（待整理）

> 碎片知识先丢这里，定期归类到对应目录。

```dataview
TABLE file.cday AS "创建日期", tags AS "标签"
FROM "FPGA开发/00_inbox"
WHERE file.name != "📥 Inbox收集箱"
SORT file.cday DESC
```

---

## 📚 语法与理论

| 笔记 | 说明 |
|:---|:---|
| [[Verilog常用语法速查表]] | 快速查阅常用语法 |
| [[Verilog常用逻辑语法]] | 经典逻辑电路写法 |
| [[Verilog经典例题]] | 行波进位加法器等例题 |

```dataview
TABLE date AS "日期", tags AS "标签"
FROM "FPGA开发/10_Syntax_&_Theory"
WHERE file.name != "image" AND file.name != "image-1" AND file.name != "image-2"
SORT date DESC
```

---

## 🧩 核心模块库

> 可复用的模块积累。

```dataview
TABLE date AS "日期", tags AS "标签"
FROM "FPGA开发/20_Modules_&_IP"
SORT date DESC
```

---

## 🚀 实战项目

```dataview
TABLE date AS "日期", status AS "状态"
FROM "FPGA开发/30_Projects"
SORT date DESC
```

---

## 📝 最近更新的笔记

```dataview
TABLE file.mday AS "最后修改", tags AS "标签"
FROM "FPGA开发"
WHERE file.name != "MOC-FPGA开发大纲"
SORT file.mday DESC
LIMIT 10
```

---

## 🏷️ 按标签浏览

```dataview
TABLE file.tags AS "标签", date AS "日期"
FROM "FPGA开发"
WHERE file.tags
FLATTEN file.tags AS 标签
GROUP BY 标签
SORT rows.length DESC
```

---

## 🔗 学习路线

→ [[FPGA学习路线图]]

## 🔄 定期回顾

→ [[定期回顾]]