# 国标计算工具（Mechtool）齿轮 / V 带强度与设计公式 —— 交叉核对

> 核对人：机械设计公式核对助手
> 数据来源（在线工具页）：
> - 齿轮：https://www.mechtool.cn/calculation/calculation_geardrive.html （说明页 PDF：`res/article/calculation/calculation_geardrivedescription`）
> - V 带：https://www.mechtool.cn/calculation/calculation_beltdrive.html （计算引擎 JS：`dist/js/mechtool/beltdrivedesign.min.js`）
> 通用教材对照源：本目录 `ch10-formulas.md`（齿轮传动，濮良贵《机械设计》第 10 章）、`ch08-formulas.md`（带传动，第 8 章）。
> 工具页声明依据标准：齿轮 **GB/T 3480-1997**《渐开线圆柱齿轮承载能力计算方法》；V 带 **GB/T 13575-2008**《普通和窄 V 带传动》。

---

## 一、齿轮（GB/T 3480-1997）

### 1.1 从工具页逐字抽取的核心设计公式

工具页的两条强度设计公式由 MathType 生成、GIF 内嵌 MathML，已逐字抽取并转写为 LaTeX（与 MathML 语义一一对应）。

**齿面接触疲劳强度设计式（求小齿轮最小分度圆直径 $d_1$）**

$$
d_1 \geq \sqrt[3]{\frac{2KT_1}{\phi_d}\cdot\frac{u+1}{u}\cdot\left(\frac{Z_E\,Z_\varepsilon\,Z_H\,Z_\beta}{[\sigma_H]}\right)^{2}}
$$

**齿根弯曲疲劳强度设计式（求最小法向模数 $m_n$）**

$$
m_n \geq \sqrt[3]{\frac{2KT_1\cos^{2}\beta\;Y_\varepsilon Y_\beta}{\phi_d\,z_1^{2}}\cdot\frac{Y_{Fa}Y_{Sa}}{[\sigma_F]}}
$$

其中 MathML 原文分子为 $2\,K\,T_1\,\cos^2\beta\,Y_\varepsilon\,Y_\beta$，分母为 $\phi_d\,z_1^{2}$，再乘 $\dfrac{Y_{Fa}Y_{Sa}}{[\sigma_F]}$，整体开三次方。

### 1.2 工具页同时给出的规则（文字层逐字）

- 载荷系数：接触 $K=K_A K_V K_{H\alpha}K_{H\beta}$；弯曲 $K=K_A K_V K_{F\alpha}K_{F\beta}$。
- 许用应力：$[\sigma_H]=\dfrac{K_{HN}\sigma_{H\lim}}{S_{H\min}}$，$S_{H\min}\approx 1.1$；$[\sigma_F]=\dfrac{K_{FN}\sigma_{FE}}{S_{F\min}}$，$S_{F\min}\approx 1.4$。
- 应力循环次数：$N=60\,n\,j\,L_h$。
- 螺旋角处理：$\varepsilon_\beta>1$ 时按 $\varepsilon_\beta=1$；$\beta>30^{\circ}$ 时按 $\beta=30^{\circ}$。
- 设计原则：软齿面闭式——按接触强度设计、校核弯曲；硬齿面闭式——按弯曲强度设计、校核接触；开式——只按弯曲强度设计，模数加大 10%~15%。

### 1.3 与通用教材（濮良贵 ch10）逐条对照

| 项 | 教材（濮良贵 ch10） | Mechtool（GB/T 3480-1997） | 结论 |
| --- | --- | --- | --- |
| 斜齿轮接触设计式 | $d_1\geq\sqrt[3]{\frac{2K_HT_1}{\phi_d}\frac{u\pm1}{u}(\frac{Z_HZ_EZ_\varepsilon Z_\beta}{[\sigma_H]})^2}$ | $d_1\geq\sqrt[3]{\frac{2KT_1}{\phi_d}\frac{u+1}{u}(\frac{Z_EZ_\varepsilon Z_HZ_\beta}{[\sigma_H]})^2}$ | **一致**；仅记法差异（外啮合教材写 $u\pm1$、工具写 $u+1$；系数乘积顺序不同，无实质差别） |
| 斜齿轮弯曲设计式 | $m_n\geq\sqrt[3]{\frac{2K_FT_1Y_\varepsilon Y_\beta\cos^2\beta}{\phi_d z_1^2}\frac{Y_{Fa}Y_{Sa}}{[\sigma_F]}}$ | $m_n\geq\sqrt[3]{\frac{2KT_1\cos^2\beta Y_\varepsilon Y_\beta}{\phi_d z_1^2}\frac{Y_{Fa}Y_{Sa}}{[\sigma_F]}}$ | **一致**；$K$ 即弯曲载荷系数 $K_F=K_AK_VK_{F\alpha}K_{F\beta}$ |
| 许用应力公式 | $[\sigma]=\frac{K_N\sigma_{\lim}}{S}$ | $[\sigma_H]=\frac{K_{HN}\sigma_{H\lim}}{S_{H\min}}$，$[\sigma_F]=\frac{K_{FN}\sigma_{FE}}{S_{F\min}}$ | 公式结构**一致** |
| 循环次数 | $N=60njL_h$ | $N=60\,n\,j\,L_h$ | **一致** |

### 1.4 差异点（齿轮）

- **D1 接触安全系数取值不同**：工具页（GB/T 3480-1997）明确 $S_{H\min}\approx 1.1$；教材（濮良贵）对接触取 $S_H=1$。即工具页比教材略保守（1.1 对 1.0）。弯曲侧：工具 $S_{F\min}\approx 1.4$，落在教材 $S_F=1.25\sim1.5$ 区间内，无矛盾。
- **D2 齿轮系数（$Z_H,Z_E,Z_\varepsilon,Z_\beta,\varepsilon_\alpha,\varepsilon_\beta,Y_\varepsilon,Y_\beta$）未能逐字转录**：这些系数在工具页以 **PNG 图片**呈现，PNG 内**不含 MathML**（已检索确认），且当前会话模型**不具备图像输入能力**，故无法逐字读取。以下给出教材/GB/T 3480 标准形式供对照，建议后续以图像能力复核工具页图片：
  - $Z_H=\sqrt{\dfrac{2\cos\beta_b}{\cos\alpha_t\sin\alpha_t}}$（斜齿区域系数）
  - $Z_\beta=\sqrt{\cos\beta}$（接触螺旋角系数）
  - $Y_\varepsilon=0.25+\dfrac{0.75}{\varepsilon_{\alpha v}}$（弯曲重合度系数）
  - $Y_\beta=1-\varepsilon_\beta\dfrac{\beta}{120^{\circ}}$（弯曲螺旋角系数）

---

## 二、V 带（GB/T 13575-2008）

> 说明：V 带各设计公式在工具页同样以 MathType 图片呈现，但这些 beltdrive GIF **不含内嵌 MathML**（已逐字节检索确认无 `<math`/`MathType`/`MTEF` 标记），且无图像输入能力。为取得"逐字"依据，改从**工具自身计算引擎** `beltdrivedesign.min.js` 反混淆读取了客户端直接实现的公式；服务端实现的公式（$L_{d0},a,\alpha_1,F_0,F_Q$）给出 GB/T 13575 / 教材标准形式并标注来源。

### 2.1 已从工具客户端 JS 逐字确认的公式

- **设计功率**：$P_d=K_A P$
- **传动比**：$i=\dfrac{n_1}{n_2}$
- **大带轮基准直径（含弹性滑动）**：
  $$d_{d2}=i\,d_{d1}(1-\varepsilon),\quad \varepsilon=0.01\sim0.02$$
  （JS 实现：`dd2 = dd1 * i * (1 - ε)`，取整显示）
- **带速**：
  $$v=\frac{\pi\,d_{d1}\,n_1}{60\times1000}\ \ (\mathrm{m/s})$$
  （JS 实现：`(Math.PI*dd1*n1/60)/1000`）
- **初定中心距范围**：
  $$0.7(d_{d1}+d_{d2})\leq a_0\leq 2(d_{d1}+d_{d2})$$
  （JS 实现：`a0min=0.7*(dd1+dd2)`，`a0max=2*(dd1+dd2)`）
- **带的根数**：
  $$z=\frac{P_d}{(P_1+\Delta P_1)K_\alpha K_L}$$
  （JS 实现：`z = powerD / power1`，其中 `power1=(P1+ΔP1)*Kα*KL`，结果向上取整并按标准根数系列选取）

### 2.2 服务端实现 / 标准形式的公式（GB/T 13575）

- **初算带长**：
  $$L_{d0}\approx 2a_0+\frac{\pi}{2}(d_{d1}+d_{d2})+\frac{(d_{d2}-d_{d1})^{2}}{4a_0}$$
- **实际中心距**：$a\approx a_0+\dfrac{L_d-L_{d0}}{2}$；且 $a_{\min}=a-0.015L_d$，$a_{\max}=a+0.03L_d$
- **小带轮包角**：
  $$\alpha_1\approx180^{\circ}-(d_{d2}-d_{d1})\frac{57.3^{\circ}}{a}\ \geq\ 120^{\circ}$$
- **单根初拉力**：
  $$F_0=500\,\frac{P_d}{z\,v}\left(\frac{2.5}{K_\alpha}-1\right)+qv^{2}$$
  （$q$ 为每米带长质量，kg/m）
- **压轴力**：
  $$F_Q=2zF_0\sin\frac{\alpha_1}{2}$$

### 2.3 工具页文字层给出的选速/选型限值（逐字）

- 带速上限：普通 V 带 $v_{\max}=25\sim30\ \mathrm{m/s}$；窄 V 带 $v_{\max}=35\sim40\ \mathrm{m/s}$；一般 $v\geq5\ \mathrm{m/s}$，宜取 $v\approx20\ \mathrm{m/s}$。
- 小带轮包角 $\alpha_1$ 不应小于 $120^{\circ}$。

### 2.4 与通用教材（濮良贵 ch08）逐条对照

| 项 | 教材（濮良贵 ch08） | Mechtool（GB/T 13575-2008） | 结论 |
| --- | --- | --- | --- |
| 设计功率 | $P_{ca}=K_AP$ | $P_d=K_AP$ | **一致**（记法 $P_{ca}$/$P_d$） |
| 大带轮直径（设计步） | $d_{d2}=i\,d_{d1}$（滑动仅在传动比关系 $i=\frac{n_1}{n_2}=\frac{d_{d2}}{(1-\varepsilon)d_{d1}}$ 中体现） | $d_{d2}=i\,d_{d1}(1-\varepsilon)$，$\varepsilon=0.01\sim0.02$ | **差异（见 D3）**：工具页把弹性滑动因子 $(1-\varepsilon)$ 直接并入直径选取步 |
| 带速 | $v=\pi d_{d1}n_1/(60\times1000)$ | 同 | **一致** |
| 初定中心距 | $0.7(d_{d1}+d_{d2})\leq a_0\leq 2(d_{d1}+d_{d2})$ | 同 | **一致**（教材抽取稿此处有笔误 $2(d_{d2}+d_{d2})$，工具页正确） |
| 初算带长 | $L_{d0}\approx2a_0+\frac{\pi}{2}(d_{d1}+d_{d2})+\frac{(d_{d2}-d_{d1})^2}{4a_0}$ | 同 | **一致** |
| 实际中心距 | $a\approx a_0+\frac{L_d-L_{d0}}{2}$；$a_{\min}=a-0.015L_d$；$a_{\max}=a+0.03L_d$ | 同 | **一致** |
| 小带轮包角 | $\alpha_1\approx180^{\circ}-(d_{d2}-d_{d1})\frac{57.3^{\circ}}{a}\geq120^{\circ}$ | 同 | **一致** |
| 带的根数 | $z=\frac{P_{ca}}{P_r}=\frac{K_AP}{(P_0+\Delta P_0)K_\alpha K_L}$ | $z=\frac{P_d}{(P_1+\Delta P_1)K_\alpha K_L}$ | **一致**（$P_1\equiv P_0,\ \Delta P_1\equiv\Delta P_0$） |
| 初拉力 | $F_0=500\frac{(2.5-K_\alpha)P_{ca}}{K_\alpha zv}+qv^2$ | $F_0=500\frac{P_d}{zv}(\frac{2.5}{K_\alpha}-1)+qv^2$ | **一致**（两种等价因式分解） |
| 压轴力 | $F_p=2zF_0\sin\frac{\alpha_1}{2}$ | $F_Q=2zF_0\sin\frac{\alpha_1}{2}$ | **一致**（记法 $F_p$/$F_Q$） |

### 2.5 差异点（V 带）

- **D3 大带轮直径公式形式不同**：工具页 $d_{d2}=i\,d_{d1}(1-\varepsilon)$ 将弹性滑动率 $(1-\varepsilon)$ 直接并入直径选取步；教材设计步为 $d_{d2}=i\,d_{d1}$，弹性滑动仅在传动比关系式中体现。两者物理等价、结果一致，但**公式写法不同**——工具页更直接，教材分两步。
- **D4 标准版本混用（工具页自身的不一致）**：工具页正文声明依据 **GB/T 13575-2008**，但其参考数据表注明"摘自 **GB/T 13575.1-1992**"，而带长修正系数 $K_L$ 又注明"摘自 **GB/T 13575.1-2008**"。即同一工具混用了 1992 与 2008 两个版本的表格数据。教材（濮良贵）则按单一版次引用。此为工具页的版本标注差异，需注意。

---

## 三、差异点汇总

| 编号 | 类别 | 差异 | 性质 |
| --- | --- | --- | --- |
| D1 | 齿轮 安全系数 | 接触 $S_{H\min}\approx1.1$（工具/GB-T 3480）对 $S_H=1$（教材）；弯曲 $S_{F\min}\approx1.4$ 落在教材 $1.25\sim1.5$ 内 | 取值不同（工具略保守） |
| D2 | 齿轮 系数 | $Z_H,Z_E,Z_\varepsilon,Z_\beta,\varepsilon_\alpha,\varepsilon_\beta,Y_\varepsilon,Y_\beta$ 图片无 MathML 且无图像输入，未能逐字转录 | 转录局限（非公式错误） |
| D3 | V带 直径 | $d_{d2}=i d_{d1}(1-\varepsilon)$（工具）对 $d_{d2}=i d_{d1}$（教材设计步） | 公式写法不同，物理等价 |
| D4 | V带 标准版本 | 工具页混用 GB/T 13575.1-1992 与 GB/T 13575.1-2008 | 工具页版本标注不一致 |

除上述外，齿轮与 V 带的强度/设计主公式与通用教材（濮良贵《机械设计》ch10 / ch08）**实质一致**；其余均为记法差异（$P_d/P_{ca}$、$F_Q/F_p$、通用 $K$ 与 $K_H/K_F$、$u+1$ 与 $u\pm1$）。

---

## 四、核对方法与局限（备查）

1. 齿轮两条设计公式：工具页 GIF 内嵌 MathML，已 `fetch`→二进制→定位 `<math>…</math>` **逐字抽取**后转写为 LaTeX，可信度高。
2. V 带：beldrive GIF **不含 MathML**（逐字节检索无 `<math`/`MathType`/`MTEF`），改读工具自身客户端 JS `beltdrivedesign.min.js`（经混淆），逐字确认了 $P_d,\ i,\ d_{d2},\ v,\ a_0$ 范围、$z$ 六项；$L_{d0},a,\alpha_1,F_0,F_Q$ 由服务端（AJAX `polyvBeltLenChange`）计算，客户端不可见，故以 GB/T 13575 / 教材标准形式给出并标注。
3. **未逐字读取的图片公式**：齿轮 8 个系数 PNG、V 带公式图——均无内嵌 MathML，且当前模型无图像输入能力。如需严格逐字，请在具备图像能力的会话中用 `read_image` 打开 `_formula_imgs/` 下已下载的 V 带 GIF（`belt_v_5 / belt_a0_6 / belt_Ld0_7 / belt_a_9 / belt_alpha1_11 / belt_z_13 / belt_F0_14 / belt_FQ_15.gif`）目视复核。
4. 环境备注：PowerShell 因 TLS 无法直连 mechdoc.cn，图片经浏览器 `fetch`→base64→本机解码落盘。
