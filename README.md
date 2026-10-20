# 机械设计公式速查手册

自包含单文件 HTML 速查手册，公式逐字照录濮良贵《机械设计》（第 9 版）教材知识点整理，多源交叉核对。

**在线使用**：直接双击打开 `mech-formula-handbook.html`（无需联网、无需服务器）。

## 内容规模

- 259 条公式 · 309 张卡片 · 24 节 · 4 篇
- 3 组交叉核对差异速查

| 篇 | 内容 |
| --- | --- |
| 一 | 总论与疲劳强度 |
| 二 | 螺纹连接、键/花键、焊接 |
| 三 | 带传动、链传动、齿轮传动、蜗杆传动 |
| 四 | 滑动轴承、滚动轴承、联轴器/离合器、轴 |

## 功能

- 全文搜索（公式编号 / 名称 / 符号）
- 19 个高频公式内置计算器（轴承寿命、轴径估算、齿面接触强度、当量动载荷等）
- 深色 / 浅色主题切换
- 仅看差异 / 存疑条目
- 打印 / 存 PDF
- 移动端响应式 + 可折叠目录
- 公式来源与核对说明（含 10 份外部核对来源）

## 目录结构

```
mech-formula-handbook.html   成品（自包含单文件，可直接打开）
mech-formula-sources/        公式源数据（Markdown）
  _header.md                 目录 + 交叉核对差异汇总
  part1.md ~ part4.md        四篇正文
  all-formulas.md            合并后的完整公式库（由构建生成）
mech-template.html           HTML 模板（含样式 + 渲染 JS + 计算器）
build_mech_html.py           构建脚本（Markdown → 单文件 HTML）
check_data.py                数据校验脚本
```

## 构建

```bash
python build_mech_html.py
```

把 `mech-formula-sources/` 下的 Markdown 公式库编译成自包含单文件 HTML。重新合并源文件：

```bash
# 在 mech-formula-sources/ 目录下
cat _header.md part1.md part2.md part3.md part4.md > all-formulas.md
python build_mech_html.py
```

## 数据校验

```bash
python check_data.py
```

校验公式数、卡片数、章节数、待核对标记数是否异常。

## 编辑约定

- 公式**逐字照录**，未修正符号、系数、指数、上下标、括号、正负号与运算顺序
- 方括号 `[ ]` 表示许用值（与原文一致）
- 原文笔误照录并标注「原文如此·疑笔误」
- 来源未给出的公式、数值、符号定义一律不补写，标 `[待核对]` 或「查表（原文未给数值）」

## 许可证

MIT License，见 [LICENSE](LICENSE)。
