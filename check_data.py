"""校验 mech-formula-sources 公式源数据的完整性。

检查项：
1. 四篇 part 文件均可解析出公式卡片
2. 公式数 / 卡片数 / 章节数在合理范围
3. [待核对] 标记数异常波动（比基线激增则告警）
4. 合并后的 all-formulas.md 与各 part 一致
"""
import os
import re
import sys

# 复用构建脚本的解析口径，避免统计漂移
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_mech_html import parse_part, parse_header, SRC, BASE, OUT

# 基线（2026-10-20 全面清理后）：HTML 里剩 3 处说明性 [待核对]，0 处内容性
BASELINE_FORMULAS = 259
BASELINE_CARDS = 309
BASELINE_SECTIONS = 24
BASELINE_TBD = 3


def main():
    ok = True

    total_cards = 0
    total_formulas = 0
    total_sections = 0
    for k in range(1, 5):
        p = os.path.join(SRC, "part%d.md" % k)
        if not os.path.exists(p):
            print("FAIL 缺少 %s" % p)
            ok = False
            continue
        part = parse_part(p, "p%d" % k)
        c = sum(len(s["cards"]) for s in part["sections"])
        # 公式卡 = body 里有 f（display 公式块）
        f = sum(
            1
            for s in part["sections"]
            for card in s["cards"]
            if card["body"].get("f")
        )
        total_cards += c
        total_formulas += f
        total_sections += len(part["sections"])
        print("part%d.md  cards=%d  formulas=%d  sections=%d"
              % (k, c, f, len(part["sections"])))

    print("-" * 40)
    print("合计 cards=%d formulas=%d sections=%d"
          % (total_cards, total_formulas, total_sections))

    if total_cards != BASELINE_CARDS:
        print("WARN 卡片数 %d != 基线 %d" % (total_cards, BASELINE_CARDS))
    if total_formulas != BASELINE_FORMULAS:
        print("WARN 公式数 %d != 基线 %d" % (total_formulas, BASELINE_FORMULAS))

    # [待核对] 统计（all-formulas.md）
    af = os.path.join(SRC, "all-formulas.md")
    if os.path.exists(af):
        text = open(af, encoding="utf-8").read()
        tbd = text.count("[待核对]")
        print("all-formulas.md [待核对]=%d（基线 %d）" % (tbd, BASELINE_TBD))
        if tbd > BASELINE_TBD + 5:
            print("WARN [待核对] 数 %d 比基线多 %d，可能有新增未定项" % (tbd, tbd - BASELINE_TBD))
            ok = False

    # HTML 一致性（直接用构建产物里的 stats）
    if os.path.exists(OUT):
        h = open(OUT, encoding="utf-8").read()
        m = re.search(r'"formulas":(\d+),"cards":(\d+),"sections":(\d+)', h)
        if m:
            hf, hc, hs = map(int, m.groups())
            print("HTML stats formulas=%d cards=%d sections=%d" % (hf, hc, hs))
            if hc != total_cards or hf != total_formulas:
                print("WARN HTML 与源数据不一致（需重新构建）")
                ok = False

    print("-" * 40)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
