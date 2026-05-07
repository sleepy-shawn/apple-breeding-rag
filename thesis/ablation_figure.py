"""
ablation_figure.py
------------------
图5-3：消融实验各配置堆叠柱状图（4维得分）

数据来源：workspace/default/evaluation/ablation_v2/
输出：ablation_figure.png（300 dpi）
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ── 中文字体 ────────────────────────────────────────────
matplotlib.rcParams["font.family"] = ["sans-serif"]
matplotlib.rcParams["font.sans-serif"] = [
    "Hiragino Sans GB", "STHeiti", "Songti SC",
    "Arial Unicode MS", "PingFang SC", "Microsoft YaHei",
    "Noto Sans CJK SC", "DejaVu Sans",
]
matplotlib.rcParams["axes.unicode_minus"] = False

# ── 数据（28题，满分10分） ───────────────────────────────
configs = ["No-RAG", "仅论文\n(Papers-only)", "仅基因\n(Genes-only)", "混合\n(Hybrid)"]
gene_scores  = [2.32, 3.18, 3.54, 3.54]
mech_scores  = [2.18, 1.57, 2.18, 2.11]
cite_scores  = [0.00, 2.00, 2.00, 2.00]
level_scores = [0.00, 0.93, 0.93, 0.86]
total_scores = [4.50, 7.68, 8.64, 8.50]

# ── 配色（暖绿农业风） ───────────────────────────────────
C_GENE  = "#1b4332"
C_MECH  = "#2d6a4f"
C_CITE  = "#52b788"
C_LEVEL = "#b7e4c7"
C_TEXT  = "#1b1b1b"
C_GRID  = "#e8e8e8"

# ── 画布（单图，居中） ──────────────────────────────────
fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=300)
fig.patch.set_facecolor("white")

x = np.arange(len(configs))
bar_width = 0.55

# 堆叠柱
b1 = ax.bar(x, gene_scores,  bar_width, label="基因命中（/4）",  color=C_GENE,  zorder=3)
b2 = ax.bar(x, mech_scores,  bar_width, bottom=gene_scores,
            label="机制准确（/3）",  color=C_MECH,  zorder=3)
b3 = ax.bar(x, cite_scores,  bar_width,
            bottom=[g + m for g, m in zip(gene_scores, mech_scores)],
            label="引用质量（/2）",  color=C_CITE,  zorder=3)
b4 = ax.bar(x, level_scores, bar_width,
            bottom=[g + m + c for g, m, c in zip(gene_scores, mech_scores, cite_scores)],
            label="证据分层（/1）",  color=C_LEVEL, zorder=3)


# 各段数值标注
def label_segments(ax, x_pos, bottoms, heights, fmt="{:.2f}",
                   fontsize=9, color="white"):
    for xi, bot, h in zip(x_pos, bottoms, heights):
        if h < 0.01:
            continue
        ax.text(xi, bot + h / 2, fmt.format(h),
                ha="center", va="center",
                fontsize=fontsize, color=color,
                fontweight="bold", zorder=5)


label_segments(ax, x, [0] * 4, gene_scores)
label_segments(ax, x, gene_scores, mech_scores)
label_segments(ax, x,
               [g + m for g, m in zip(gene_scores, mech_scores)],
               cite_scores)
label_segments(ax, x,
               [g + m + c for g, m, c in zip(gene_scores, mech_scores, cite_scores)],
               level_scores, color="#555555")

# 总分（柱顶）
for xi, tot in zip(x, total_scores):
    ax.text(xi, tot + 0.20, f"{tot:.2f}",
            ha="center", va="bottom",
            fontsize=11, fontweight="bold",
            color=C_TEXT, zorder=5)

# 满分参考线
ax.axhline(y=10, color="#aaaaaa", linestyle=":", linewidth=1, zorder=2)
ax.text(x[-1] + 0.45, 10.05, "满分", fontsize=8,
        color="#888888", va="bottom")

# 完整系统标注
ax.annotate(
    "完整系统\n(A3)",
    xy=(x[-1], total_scores[-1] + 0.20),
    xytext=(x[-1] - 0.85, total_scores[-1] + 1.6),
    fontsize=9, color="#1b4332",
    arrowprops=dict(arrowstyle="->", color="#1b4332", lw=1.3),
    ha="center",
    fontweight="bold",
)

# 样式
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=10.5)
ax.set_ylim(0, 11)
ax.set_yticks(range(0, 11, 2))
ax.set_ylabel("综合得分（满分10分）", fontsize=11)
ax.yaxis.grid(True, color=C_GRID, linestyle="--", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="x", length=0)

# 图例
ax.legend(
    loc="upper left", fontsize=9.5,
    framealpha=0.95, edgecolor="#dddddd",
    handlelength=1.5, handleheight=1.0,
)

# 标题
ax.set_title("消融实验各配置得分对比",
             fontsize=14, fontweight="bold", pad=14)

# 底部图注
fig.text(
    0.5, 0.01,
    "注：满分10分 = 基因命中(/4) + 机制准确(/3) + 引用质量(/2) + 证据分层(/1)",
    ha="center", fontsize=9, color="#666666", style="italic"
)

plt.tight_layout(pad=2.0)

# 保存
out = Path(__file__).parent / "ablation_figure.png"
plt.savefig(str(out), dpi=300, facecolor="white", edgecolor="none",
            bbox_inches="tight")
print(f"✅ 图表已保存：{out}")
plt.close()
