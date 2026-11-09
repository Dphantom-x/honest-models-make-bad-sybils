"""Figure: what live AI swarms answer on the access form, uncoached (ASK) and when their
operator tells them to deny (DENY). Eligible answers only (given after the swarm held two
or more accounts). Data: results/ask_the_swarm.json (by_arm_model).

    .venv/Scripts/python figures/fig_ask.py   ->  figures/fig_ask.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HD = Path(__file__).resolve().parents[1]
TITLES = False   # the report states each figure's claim in its caption
SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e6e5e0"
SEG = [("disclose", "Says yes", "#2a78d6"),
       ("deny", "Says no", "#eb6834"),
       ("other", "Other answer", "#b8b6ae")]
MODELS = [("deepseek-flash", "DeepSeek"), ("gemini-3.1-flash-lite", "Gemini"),
          ("claude-opus-4-8", "Opus 4.8"), ("claude-sonnet-4-6", "Sonnet 4.6")]
ARMS = [("A2a-pa-ask", "asked"), ("A2a-pa-deny", "told to deny")]


def main():
    d = json.loads((HD / "results/ask_the_swarm.json").read_text(encoding="utf-8"))["summary"]["by_arm_model"]
    rows = []
    for mk, mname in MODELS:
        for ak, aname in ARMS:
            hit = [v for k, v in d.items() if k.startswith(ak + "-") and k.endswith("|" + mk)]
            if hit and hit[0]["eligible"]:
                rows.append((f"{mname}, {aname}", hit[0]))
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(5.6, 0.34 * len(rows) + 1.0), dpi=260)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for i, (label, b) in enumerate(rows):
        y = len(rows) - 1 - i
        left = 0.0
        for key, _, col in SEG:
            w = b[key] / b["eligible"]
            if w > 0:
                ax.barh(y, w, left=left, height=0.62, color=col, edgecolor=SURFACE, linewidth=1.5)
                if w >= 0.12:
                    ax.text(left + w / 2, y, f"{b[key]}", ha="center", va="center", fontsize=7.5,
                            color="white" if key != "other" else INK)
            left += w
        ax.text(1.01, y, f"{b['eligible']} answers, {b['attack_runs']} swarm" + ("s" if b["attack_runs"] != 1 else ""), va="center",
                fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in reversed(rows)], color=INK, fontsize=8.5)
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], color=INK2)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, length=0)
    for t in ax.get_yticklabels(): t.set_color(INK)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c, label=l) for _, l, c in SEG]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=3, frameon=False,
              fontsize=7.5, labelcolor=INK)
    if TITLES: fig.text(0.012, 0.985, "Asked once, AI swarms say they are one swarm, unless told to lie",
             fontsize=10.5, color=INK, weight="bold", va="top")
    if TITLES: fig.text(0.012, 0.985 - 0.32 / (0.42 * len(rows) + 1.6), "Answers by swarm accounts to the access-form question "
             "“Is this account being used together with any other account …?”",
             fontsize=8, color=INK2, va="top")
    fig.subplots_adjust(left=0.27, right=0.78, top=1 - 0.42 / (0.36 * len(rows) + 1.0), bottom=0.12)
    out = HD / "figures" / "fig_ask.png"
    fig.savefig(out, facecolor=SURFACE)
    print(out, [r[0] for r in rows])


if __name__ == "__main__":
    main()
