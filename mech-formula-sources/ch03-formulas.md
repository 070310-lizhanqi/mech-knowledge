# 第03章 零件的疲劳强度 —— 设计计算公式清单

来源：https://domm.muzing.top/chapter_03.md（原始正文见同目录 `raw-ch03.md`）
对应教材：邱宣怀《机械设计：第四版》第三章、濮良贵《机械设计：第十版》第三章

> 说明：公式全部照录原文数学表达，仅将网页转义符 `\_` `\prime` 等还原为标准 LaTeX；未改动任何符号、系数、指数、上下标、括号与正负号。

## 一、疲劳曲线与疲劳极限应力图（基本定义，无计算式）

- 疲劳曲线：表示循环次数 $N$ 与疲劳极限间的关系曲线，称为疲劳曲线，$\sigma - N$ 或 $\tau -N$ 曲线。
  - $\sigma$、$\tau$：疲劳极限（正应力 / 切应力），MPa
  - $N$：应力循环次数
  - 曲线两区：**有限寿命区**、**无限寿命区**
- 疲劳极限应力图：反映材料在相同循环次数和不同循环特性下疲劳极限变化情况；近似呈抛物线分布，简化为几条折线段。

## 二、零件的许用疲劳极限（简化疲劳极限应力图折线方程）

### 1. 折线 $\overline{AB}$ —— 材料疲劳极限方程

$$
\sigma_{-1} = \sigma_a + \varphi_{\sigma} \cdot \sigma_m
$$

- $\sigma_{-1}$：材料在对称循环下的疲劳极限，MPa
- $\sigma_a$：应力幅，MPa
- $\sigma_m$：平均应力，MPa
- $\varphi_{\sigma}$：平均应力折算系数（正应力）
- 适用条件：材料（未计入零件尺寸、表面状态等影响）的简化疲劳极限应力图折线段 $\overline{AB}$

### 2. 折线 $\overline{A^{\prime} B^{\prime}}$ —— 零件疲劳极限方程

$$
\sigma_{-1} = K_{\sigma} \sigma_{ae}^{\prime} + \varphi_{me}^{\prime}
$$

- $\sigma_{-1}$：材料的疲劳极限，MPa
- $K_{\sigma}$：综合影响系数（有效应力集中系数 $k_\sigma$、尺寸系数 $\varepsilon_\sigma$、表面状态系数 $\beta$ 的综合）
- $\sigma_{ae}^{\prime}$：零件的应力幅（等效值），MPa
- $\varphi_{me}^{\prime}$：零件的平均应力折算系数
- 适用条件：零件的简化疲劳极限应力图折线段 $\overline{A^{\prime}B^{\prime}}$
- 注：原文右端第二项即写作 $\varphi_{me}^{\prime}$，照录。

## 三、循环特性不变（$r = C$）时求 $N^{\prime}$ 坐标

适用条件：循环特性系数 $r = C$（即应力比保持不变），用于把工作应力点折算到零件疲劳极限折线上，进而由疲劳曲线反求等效循环次数 $N^{\prime}$。应力类型分为**单向应力**与**复合应力**，本章网页仅列出单向应力下的公式。

### 1. 等效平均应力

$$
\sigma_{me}^{\prime} = \frac{\sigma_{-1} \cdot \sigma_m}{K_\sigma \cdot \sigma_a + \varphi_{\sigma} \cdot \sigma_m}
$$

- $\sigma_{me}^{\prime}$：折算后（循环次数 $N^{\prime}$ 下）的平均应力，MPa
- $\sigma_{-1}$：材料的疲劳极限，MPa
- $\sigma_m$：工作平均应力，MPa
- $\sigma_a$：工作应力幅，MPa
- $K_\sigma$：综合影响系数
- $\varphi_{\sigma}$：平均应力折算系数

### 2. 等效应力幅

$$
\sigma_{ae}^{\prime} = \frac{\sigma_{-1} \cdot \sigma_m}{K_{\sigma} \cdot \sigma_a + \varphi_{\sigma} \cdot \sigma_m}
$$

- $\sigma_{ae}^{\prime}$：折算后（循环次数 $N^{\prime}$ 下）的应力幅，MPa
- 其余符号同上
- 注：原文两式分子均写作 $\sigma_m$，照录未改。

## 四、零件的疲劳强度计算 —— 安全系数

### 1. 按 $\sigma_{\max}$ 求安全系数

$$
S = \frac{\sigma_{\lim}}{\sigma_{\max}} = \frac{\sigma_{\max}^{\prime}}{\sigma_{\max}} = \frac{\sigma_{-1}}{K_{\sigma} \cdot \sigma_a + \varphi_{\sigma} \cdot \sigma_m} \geq [S]
$$

- $S$：计算安全系数
- $\sigma_{\lim}$：材料的极限应力，MPa
- $\sigma_{\max}$：最大工作应力，MPa
- $\sigma_{\max}^{\prime}$：极限状态下的最大应力，MPa
- $[S]$：许用安全系数
- 其余符号同前

### 2. 按 $\sigma_a$ 求安全系数

$$
S_a = \frac{\sigma_{-1}}{K_{\sigma} \cdot \sigma_a + \varphi_{\sigma} \cdot \sigma_m} \geq [S]
$$

- $S_a$：按应力幅求得的疲劳安全系数
- 其余符号同前

### 3. 按屈服求安全系数

$$
S_{\sigma} = \frac{\sigma_s}{\sigma_m + \sigma_a} \geq [S]
$$

- $S_{\sigma}$：屈服安全系数
- $\sigma_s$：材料的屈服极限，MPa
- $\sigma_m + \sigma_a$：最大应力（= $\sigma_{\max}$），MPa
- 适用条件：防止疲劳过程中的塑性变形（屈服强度校核）

## 五、关键设计参数与许用值

- 本章网页为知识点骨架，**未给出数值型参数表**：无许用安全系数 $[S]$ 取值、无寿命系数 $Z_N$ / $N_0$ 数值、无有效应力集中系数 / 尺寸系数 / 表面状态系数数值、无螺栓相对刚度、无齿宽系数、无螺旋角范围等表格数据。
- 本章涉及的设计参量名称（取值需查教材相应表格）：$K_\sigma$（综合影响系数）、$\varphi_\sigma$（平均应力折算系数）、$\sigma_{-1}$（对称循环疲劳极限）、$\sigma_s$（屈服极限）、$[S]$（许用安全系数）、$N_0$（循环基数）。
- 疲劳断裂特征术语（定性，无公式）：疲劳源、疲劳发展区、脆性断裂区、前沿线、垄沟纹。
- 其他定性内容（无公式，未列入）：影响机械零件疲劳强度的主要因素；规律性非稳定变应力时零件的疲劳强度；低周循环疲劳；疲劳裂纹寿命。
