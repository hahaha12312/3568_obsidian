---
type: doc
title: 03-GoodNotes与OCR
tags:
  - type/meta
---

# GoodNotes 导出与 OCR

> 目标：让手写摘抄**变成可搜索的文字**。做到了，Obsidian 全文搜索、PDF++ 划词、以及后面接的 AI
> 才能读到你写的内容；做不到，这些 PDF 在库里就只是一堆不透明的图片。

## 第一步：先测一下，可能根本不用 OCR

GoodNotes 自带手写识别。导出 PDF 时**如果它把识别结果写成了文字层，就不需要额外 OCR**。

测试方法（30 秒）：

1. 从 GoodNotes 导出任意一页为 PDF
2. 拖进 Obsidian 打开
3. 试着用鼠标选中手写的字

- **能选中** → 已有文字层，直接用，跳过下面所有步骤
- **选不中** → 只有图像，继续往下

> 导出时留意 GoodNotes 的导出选项，若有「可搜索文本 / OCR」之类的开关，打开它再试一次。

## 第二步：需要 OCR 的话，用 OCRmyPDF

**不要用 Obsidian 的 OCR 插件。** `obsidian-ocr` 自述「早期开发中」，而且它把识别结果存成独立的
transcript 文件，**不写回 PDF 文字层** —— 结果就是 Obsidian 搜索、PDF++、AI 全都读不到，等于白做。

用 [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF)（3.4 万星，活跃维护），它把文字层**写进 PDF 本身**。

### 安装

```bash
# Windows (推荐用 pip，需要先装 Python)
pip install ocrmypdf
# 还需要 Tesseract 与中文语言包，从下面地址装并勾选 Chinese (Simplified)
# https://github.com/UB-Mannheim/tesseract/wiki

# macOS
brew install ocrmypdf tesseract-lang
```

### 使用

```bash
# 单个文件，中英混排
ocrmypdf --skip-text -l chi_sim+eng "被讨厌的勇气-摘抄.pdf" "被讨厌的勇气-摘抄.pdf"

# 批量处理 Attachments/Books 下所有 PDF（PowerShell）
Get-ChildItem "Attachments\Books\*.pdf" | ForEach-Object {
    ocrmypdf --skip-text -l chi_sim+eng $_.FullName $_.FullName
}
```

- `--skip-text` 表示已有文字层的页面跳过，可以安全地重复运行
- `-l chi_sim+eng` 同时识别简体中文和英文；繁体用 `chi_tra`

### 手写识别效果不好怎么办

Tesseract 对**手写体**中文的识别率一般。两个更好的选择：

- **macOS**：[OCRmyPDF-AppleOCR](https://github.com/mkyt/OCRmyPDF-AppleOCR) —— 调用 Apple Vision（就是「实况文本」的引擎），中文手写识别明显更强
- **跨平台**：[OCRmyPDF-EasyOCR](https://github.com/ocrmypdf/OCRmyPDF-EasyOCR) —— 基于深度学习，中日韩支持不错

## 第三步：OCR 失败也不影响使用

这点很重要，不要在 OCR 上钻牛角尖。

**即使识别率是 0，PDF++ 的矩形选区嵌入照样能用** —— 你在手写页上框一个方框，它就把那块区域嵌进笔记，
渲染成实时裁图。字迹再潦草也没关系。

所以合理的策略是：

| 情况 | 做法 |
| --- | --- |
| OCR 效果好 | 划词复制成引用文本，可搜索、AI 可读，最理想 |
| OCR 效果一般 | 重要的段落划词，识别烂的段落用矩形嵌入 |
| OCR 完全失败 | 全部用矩形嵌入；**在提炼时用自己的话把想法打成文字** |

最后一行其实揭示了一件事：**真正要被搜索、被 AI 读到的，本来就应该是你的永久笔记，而不是原始摘抄。**
OCR 只是锦上添花，提炼才是主线。

## 命名与存放约定

```
Attachments/
├── Books/      书名-摘抄.pdf      ← GoodNotes 导出，一书一档
├── Research/   网上找的资料
├── AI/         日期-主题.pdf      ← AI 对话导出
└── _inline/    笔记里随手粘贴的图片（Obsidian 自动放这）
```

## 仓库体积

GoodNotes 导出通常 5-50 MB，而且**写完就不再改动**。这种「一次写入」的二进制文件普通 git 处理得很好，
**不需要 git-lfs**（LFS 的价值在于频繁改动的大文件，而且 GitHub 免费额度只有 1 GB，用 PDF 很容易撑爆）。

需要留意的时候：

- 单个文件接近 100 MB（GitHub 硬上限）→ 先压缩，或考虑 LFS
- 附件总量超过 1 GB，克隆变慢 → 考虑把 `Attachments/` 移出 git，改用网盘同步

用 [[附件管理.base]] 的「大文件」视图随时盯着体积。
