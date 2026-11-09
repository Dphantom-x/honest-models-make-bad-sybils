"""Figure: suspicion accelerates. For every live AI swarm episode (58), the collision-test
evidence against "these accounts are unrelated" as the swarm's collision-free family takes
more of the dataset. Data: results/ev/live_W3600.json (swarm families; window-independent),
thresholds from results/ev/ev_summary.json.

    .venv/Scripts/python figures/fig_suspicion.py   ->  figures/fig_suspicion.png
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
COL = {"Gemini 3.1 Flash-Lite": "#2a78d6", "DeepSeek Flash": "#eb6834", "Claude Opus 4.8 / Sonnet 4.6": "#1baf7a"}


def provider(run: str) -> str:
    if "deepseek" in run:
        return "DeepSeek Flash"
    if "opus48" in run or "sonnet46" in run:
        return "Claude Opus 4.8 / Sonnet 4.6"
    return "Gemini 3.1 Flash-Lite"


def main():
    live = json.loads((HD / "results/ev/live_W3600.json").read_text(encoding="utf-8"))["runs"]
    summ = json.loads((HD / "results/ev/ev_summary.json").read_text(encoding="utf-8"))
    t1 = summ["windows"]["3600"]["threshold_max_honest_E_401_412"]
    t24 = summ["windows"]["86400"]["threshold_max_honest_E_401_412"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(5.4, 3.5), dpi=260)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    counts = {k: 0 for k in COL}
    order = sorted(live, key=lambda r: list(COL).index(provider(r["run"])))
    for r in order:
        s = r["swarm_family"]
        if not s or not s["curve"]:
            continue
        p = provider(r["run"])
        counts[p] += 1
        xs = [0.0] + [u / s["n"] for u, _ in s["curve"]]
        ys = [0.0] + [e for _, e in s["curve"]]
        ax.plot(xs, ys, color=COL[p], lw=1.3 if "Claude" in p else 1.0,
                alpha=0.95 if "Claude" in p else 0.55, solid_capstyle="round", zorder=3 if "Claude" in p else 2)
    ends = {}
    for r in live:
        s = r["swarm_family"]
        if s and s["curve"]:
            key = (s["n"], s["covered"])
            ends.setdefault(key, []).append((provider(r["run"]), s["curve"][-1][1]))
    labelled = set()
    for (n, cov), lst in sorted(ends.items()):
        e = max(v for _, v in lst)
        if (n, cov) in labelled or not (cov == n or (n, cov) == (40, 24)):
            continue
        labelled.add((n, cov))
        txt = (f"{n}-shard dataset, all taken: 1 in $10^{{{e:.1f}}}$" if cov == n else
               f"{n}-shard dataset, {cov} taken: 1 in {10 ** e:,.0f}")
        ax.annotate(txt, (cov / n, e), xytext=(-6, 4), textcoords="offset points", ha="right",
                    fontsize=7.5, color=INK2)
    ax.text(0.025, 0.56, "Episodes on the same dataset trace the same curve:\n"
            "a clean split's evidence depends only on how much\nit has taken without a collision.",
            transform=ax.transAxes, ha="left", va="top", fontsize=7.5, color=INK2)
    for y, txt in ((t1, f"most collision-free honest group in 1 hour ({t1:.2f})"),
                   (t24, f"... in 24 hours ({t24:.2f})")):
        ax.axhline(y, color=MUTED, lw=1.0, ls=(0, (4, 3)), zorder=1)
        ax.text(0.005, y + 0.15, txt, color=INK2, fontsize=7.5, va="bottom", ha="left")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 12)
    ax.set_yticks([0, 3, 6, 9, 12])
    ax.set_yticklabels(["1 in 1", "1 in 1,000", "1 in a million", "1 in a billion", "1 in 10¹²"], color=INK2)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], color=INK2)
    ax.set_xlabel("Share of the dataset taken, with no shard taken twice", color=INK2)
    ax.set_ylabel("Chance that unrelated accounts\nwould have avoided every overlap", color=INK2)
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, length=0)
    handles = [plt.Line2D([], [], color=c, lw=2, label=f"{k} ({counts[k]})") for k, c in COL.items()]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1.0), frameon=False,
              fontsize=8, labelcolor=INK)
    if TITLES: fig.text(0.012, 0.975, "Every clean split makes “we’re unrelated” less believable, faster near the end",
             fontsize=10.5, color=INK, weight="bold", va="top")
    if TITLES: fig.text(0.012, 0.925, "Collision-test evidence for each of 58 live AI-swarm episodes, as its collision-free accounts "
             "take more of the gated dataset", fontsize=8, color=INK2, va="top")
    fig.subplots_adjust(left=0.23, right=0.95, top=0.97, bottom=0.14)
    out = HD / "figures" / "fig_suspicion.png"
    fig.savefig(out, facecolor=SURFACE)
    print(out, counts)


if __name__ == "__main__":
    main()
