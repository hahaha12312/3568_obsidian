---
type: moc
title: 概念 MOC
phase: gather
tags:
  - type/moc
created: 2026-09-04
last_reviewed: 2026-09-04
---

# 概念 MOC

> 这里放**跨书**的概念。一个概念只有被两本以上的书从不同角度谈过，才值得在这里立条目 ——
> 否则它还只是某本书的内部术语，留在图书笔记里就行。

## 概念清单

- [[课题分离]]

## 概念之间的张力

> 最有价值的部分。记录两个概念互相矛盾的地方，那里通常藏着还没想透的东西。

| 概念 A | 概念 B | 冲突在哪 | 我的判断 |
| --- | --- | --- | --- |
|  |  |  |  |

## 全部主题分布

```base
filters:
  and:
    - file.hasTag("type/permanent")
    - '!topics.isEmpty()'
views:
  - type: table
    name: 按主题看永久笔记
    order:
      - file.name
      - topics
      - status
    sort:
      - property: file.name
        direction: ASC
```
