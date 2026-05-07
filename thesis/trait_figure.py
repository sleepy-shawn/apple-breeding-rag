"""
图 5-2：完整系统在不同性状问题中的评测表现

绘图原则：
1. 保留综合得分、基因召回率和题数三类信息。
2. 降低工程化表述，突出苹果品质性状。
3. 使用论文插图中更常见的双栏横向柱图。
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.rcParams["font.family"] = ["sans-serif"]
matplotlib.rcParams["font.sans-serif"] = [
    "PingFang SC",
    "Hiragino Sans GB",
    "Songti SC",
    "STHeiti",
    "Arial Unicode MS",
    "Microsoft YaHei",
    "Noto Sans CJK SC",
    "DejaVu Sans",
]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42


DATA = [
    {"trait": "颜色", "score": 9.20, "recall": 0.96, "count": 5},
    {"trait": "硬度", "score": 9.00, "recall": 0.93, "count": 5},
    {"trait": "酸度", "score": 8.60, "recall": 0.83, "count": 5},
    {"trait": "采收期", "score": 8.25, "recall": 0.94, "count": 4},
    {"trait": "糖度", "score": 7.75, "recall": 0.78, "count": 4},
    {"trait": "通用方法", "score": 8.00, "recall": None, "count": 5},
]

SYSTEM_AVG = 8.50

TRAIT_COLORS = {
    "颜色": "#b9413e",
    "硬度": "#3b7f5b",
    "酸度": "#d49b36",
    "采收期": "#6b8fbf",
    "通用方法": "#8c96a6",
    "糖度": "#7a5c9e",
}

TEXT = "#222222"
SUBTLE = "#6f6f6f"
GRID = "#e6e1d8"
AVG = "#c85f4a"
BG = "#fbfaf7"


def pct(value: float) -> str:
    return f"{round(value * 100):.0f}％"


def main() -> None:
    traits = [item["trait"] for item in DATA]
    y = np.arange(len(DATA))

    fig, (ax_score, ax_recall) = plt.subplots(
        ncols=2,
        figsize=(9.4, 5.2),
        dpi=300,
        gridspec_kw={"width_ratios": [1.34, 1.0], "wspace": 0.16},
    )
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.11, right=0.975, top=0.86, bottom=0.19)
    for ax in (ax_score, ax_recall):
        ax.set_facecolor(BG)

    score_colors = [TRAIT_COLORS[item["trait"]] for item in DATA]

    ax_score.barh(
        y,
        [item["score"] for item in DATA],
        color=score_colors,
        height=0.55,
        alpha=0.92,
        edgecolor="none",
    )
    ax_score.axvline(
        SYSTEM_AVG,
        color=AVG,
        linestyle=(0, (4, 3)),
        linewidth=1.4,
        zorder=3,
    )
    ax_score.text(
        SYSTEM_AVG + 0.04,
        -0.72,
        "系统均分 8.50",
        ha="left",
        va="center",
        fontsize=9,
        color=AVG,
    )

    for idx, item in enumerate(DATA):
        ax_score.text(
            item["score"] + 0.10,
            idx,
            f"{item['score']:.2f}",
            ha="left",
            va="center",
            fontsize=10.5,
            fontweight="bold",
            color=TRAIT_COLORS[item["trait"]],
        )

    ax_score.set_yticks(y)
    ax_score.set_yticklabels(traits, fontsize=11.5, color=TEXT)
    ax_score.invert_yaxis()
    ax_score.set_ylim(len(DATA) - 0.45, -0.55)
    ax_score.set_xlim(0, 10.7)
    ax_score.set_xticks([0, 2, 4, 6, 8, 10])
    ax_score.set_xlabel("综合得分（满分 10 分）", fontsize=10, color=TEXT, labelpad=8)
    ax_score.set_title("A 综合得分", loc="left", fontsize=11.5, fontweight="bold", color=TEXT, pad=8)
    ax_score.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax_score.set_axisbelow(True)
    ax_score.tick_params(axis="x", colors=SUBTLE, labelsize=9, length=0)
    ax_score.tick_params(axis="y", length=0)

    recall_y = []
    recall_values = []
    recall_colors = []
    for idx, item in enumerate(DATA):
        if item["recall"] is None:
            continue
        recall_y.append(idx)
        recall_values.append(item["recall"] * 100)
        recall_colors.append(TRAIT_COLORS[item["trait"]])

    ax_recall.barh(
        recall_y,
        recall_values,
        color=recall_colors,
        height=0.55,
        alpha=0.86,
        edgecolor="none",
    )

    for idx, item in enumerate(DATA):
        if item["recall"] is None:
            ax_recall.text(
                2,
                idx,
                "不纳入基因召回评分",
                ha="left",
                va="center",
                fontsize=9.5,
                color=SUBTLE,
            )
        else:
            ax_recall.text(
                item["recall"] * 100 - 3.0,
                idx,
                pct(item["recall"]),
                ha="right",
                va="center",
                fontsize=10.5,
                fontweight="bold",
                color="white",
            )
        ax_recall.text(
            119,
            idx,
            f"{item['count']} 题",
            ha="right",
            va="center",
            fontsize=9.5,
            color=SUBTLE,
        )

    ax_recall.set_yticks(y)
    ax_recall.set_yticklabels([])
    ax_recall.invert_yaxis()
    ax_recall.set_ylim(len(DATA) - 0.45, -0.55)
    ax_recall.set_xlim(0, 122)
    ax_recall.set_xticks([0, 25, 50, 75, 100])
    ax_recall.set_xticklabels(["0", "25", "50", "75", "100"])
    ax_recall.set_xlabel("基因召回率（％）", fontsize=10, color=TEXT, labelpad=8)
    ax_recall.set_title("B 基因召回率", loc="left", fontsize=11.5, fontweight="bold", color=TEXT, pad=8)
    ax_recall.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax_recall.set_axisbelow(True)
    ax_recall.tick_params(axis="x", colors=SUBTLE, labelsize=9, length=0)
    ax_recall.tick_params(axis="y", length=0)

    for ax in (ax_score, ax_recall):
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#bfb8ae")
        ax.spines["bottom"].set_linewidth(0.8)

    fig.suptitle(
        "完整系统在不同性状问题中的表现",
        x=0.515,
        y=0.955,
        fontsize=13,
        fontweight="bold",
        color=TEXT,
    )
    fig.text(
        0.515,
        0.055,
        "注：左图为各类问题的平均综合得分；右图为含目标基因问题的基因召回率，通用方法类不参与该项评分。",
        ha="center",
        va="center",
        fontsize=8.7,
        color=SUBTLE,
    )

    out_dir = Path(__file__).parent
    png_path = out_dir / "figure_5_2_trait_lollipop.png"
    pdf_path = out_dir / "figure_5_2_trait_lollipop.pdf"
    fig.savefig(png_path, dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.12)
    fig.savefig(pdf_path, facecolor="white", bbox_inches="tight", pad_inches=0.12)
    print(f"图表已保存：{png_path}")
    print(f"矢量版本已保存：{pdf_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
