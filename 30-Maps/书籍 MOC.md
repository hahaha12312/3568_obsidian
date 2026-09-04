---
type: moc
title: 书籍 MOC
phase: gather
tags:
  - type/moc
created: 2026-09-04
last_reviewed: 2026-09-04
---

# 书籍 MOC

> 这里不是书单，是**阅读地图**。按「这些书在回答什么问题」分组，而不是按学科分类。
> 一本书可以出现在多个问题下面。

## 我为什么活成现在这样

- [[被讨厌的勇气]]

## 怎么想得更清楚

<!-- 认知、思维、决策 -->

## 世界是怎么运转的

<!-- 历史、社会、经济 -->

## 怎么把事做成

<!-- 方法、管理、创作 -->

## 待归位

> 新建的图书笔记先扔这里，月度复盘时再决定它属于哪个问题。

```base
filters:
  and:
    - type == "book"
    - '!file.inFolder("50-Meta/Templates")'
    - '!file.hasLink(this)'
views:
  - type: table
    name: 尚未挂进 MOC 的书
    order:
      - file.name
      - author
      - status
    sort:
      - property: file.ctime
        direction: DESC
```
