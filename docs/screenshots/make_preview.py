#!/usr/bin/env python3
"""Compose section-by-section preview PNGs (matplotlib) from the same real
gold data used in the live HTML dashboard, since no live browser is
available in this build environment to capture an actual screenshot of
dashboard/index.html. These are STYLED RENDERS matching the dashboard's
palette and chart choices, not literal screenshots — see the README note.
Run after build_workbook.py.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
import gold_data as gd
from build_workbook import (compute_momentum, compute_regional_breakdown,
                             compute_concentration, compute_gold_allocation_leaders)

GOLD = "#b8860b"
GOLD_DARK = "#8b6508"
INK = "#2b2117"
INK_SOFT = "#6b5b3a"
RED = "#c62828"
GREEN = "#2e7d32"
PALETTE = ["#b8860b", "#d9a441", "#8b6508", "#e8c874", "#a9987a", "#5a4004"]
OUT_DIR = os.path.dirname(__file__)

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#ece2c8", "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK_SOFT, "ytick.color": INK_SOFT, "font.size": 9,
    "axes.titleweight": "bold", "axes.titlecolor": GOLD_DARK,
})


def clean(ax):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)


def suptitle(fig, text):
    fig.suptitle(text, fontsize=15, fontweight="bold", color=GOLD_DARK, y=0.985)


def save(fig, name):
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)
    print("Saved", path)


# =====================================================================
# 1) OVERVIEW — KPI band + top 10 reserves + regional split
# =====================================================================
fig = plt.figure(figsize=(13, 8.5))
suptitle(fig, "1. Overview - headline KPIs")
gs = fig.add_gridspec(2, 2, height_ratios=[0.68, 1.32], hspace=0.5, wspace=0.28)

concentration = compute_concentration()
regions = compute_regional_breakdown()
kpis = [
    ("RESERVES", f"{gd.WORLD_TOTAL_RESERVES_TONNES:,.0f} t", "World official gold reserves"),
    ("TOP HOLDER", "8,133 t", "Largest single holder: United States"),
    ("PRICE", "$3,432", "2025 avg gold price (USD/oz)"),
    ("DEMAND", f"{gd.DEMAND_TOTAL_2025:,.0f} t", "Record full-year 2025 demand"),
    ("TOP BUYER", "+322 t", "Top 3-yr buyer: Poland (2023-2025)"),
    ("CONCENTRATION", f"{concentration['top5Pct']*100:.0f}%", "Held by just the top 5 countries"),
]
ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.axis("off")
n = len(kpis)
box_w, gap = 1 / n * 0.92, 1 / n * 0.08
import textwrap

for i, (icon, val, lbl) in enumerate(kpis):
    x = i / n + gap / 2
    box = mpatches.FancyBboxPatch((x, 0.05), box_w, 0.85, boxstyle="round,pad=0.01,rounding_size=0.02",
                                   linewidth=1, edgecolor="#ece2c8", facecolor="#fffdf8", transform=ax_kpi.transAxes)
    ax_kpi.add_patch(box)
    ax_kpi.text(x + 0.015, 0.78, icon, fontsize=7, color=GOLD, fontweight="bold", transform=ax_kpi.transAxes)
    ax_kpi.text(x + 0.015, 0.45, val, fontsize=14, fontweight="bold", color=INK, transform=ax_kpi.transAxes)
    wrapped = "\n".join(textwrap.wrap(lbl, width=18))
    ax_kpi.text(x + 0.015, 0.30, wrapped, fontsize=6.3, color=GOLD_DARK, fontweight="bold",
                transform=ax_kpi.transAxes, va="top", linespacing=1.3)

ax1 = fig.add_subplot(gs[1, 0])
top10 = sorted(gd.RESERVES_BY_COUNTRY, key=lambda r: -r[2])[:10]
names = [r[1] for r in top10][::-1]
vals = [r[2] for r in top10][::-1]
ax1.barh(names, vals, color=GOLD)
ax1.set_title("Top 10 countries by official reserves (t)")
ax1.set_xlabel("Tonnes")
clean(ax1)

ax2 = fig.add_subplot(gs[1, 1])
wedges, _ = ax2.pie([r["tonnes"] for r in regions], colors=PALETTE, startangle=90,
                     wedgeprops=dict(width=0.42, edgecolor="white"))
total_r = sum(r["tonnes"] for r in regions)
ax2.legend(wedges, [f"{r['region']} ({r['tonnes']/total_r*100:.0f}%)" for r in regions],
           loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8, frameon=False)
ax2.set_title("Reserves by region")
save(fig, "preview_overview.png")

# =====================================================================
# 2) RESERVE HISTORY & CBGA ERA
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
suptitle(fig, "2. Reserve history - 26 years of sellers to buyers")

ax = axes[0]
years = [("Q2'26" if y == 2026.5 else str(int(y))) for y, _ in gd.WORLD_RESERVES_TREND]
vals = [t for _, t in gd.WORLD_RESERVES_TREND]
ax.plot(years, vals, color=GOLD, linewidth=2)
ax.fill_between(range(len(years)), vals, min(vals) - 500, color=GOLD, alpha=0.12)
ax.set_ylim(min(vals) - 300, max(vals) + 300)
ax.set_title("World official reserves, 2000-2026")
ax.set_xticks(range(0, len(years), 4))
ax.set_xticklabels([years[i] for i in range(0, len(years), 4)])
clean(ax)

ax = axes[1]
cbga_years = [str(y) for y, _, _ in gd.CBGA_ANNUAL_SALES]
cbga_vals = [t for _, t, _ in gd.CBGA_ANNUAL_SALES]
ax.plot(cbga_years, cbga_vals, color=RED, linewidth=2)
ax.fill_between(range(len(cbga_years)), cbga_vals, 0, color=RED, alpha=0.1)
ax.set_title("CBGA reported gross sales, 1999-2019 (t)")
ax.set_xticks(range(0, len(cbga_years), 3))
ax.set_xticklabels([cbga_years[i] for i in range(0, len(cbga_years), 3)])
clean(ax)
save(fig, "preview_history.png")

# =====================================================================
# 3) MOMENTUM, BUYERS & SELLERS
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
suptitle(fig, "3. Momentum - who's rising, who's flat")

ax = axes[0]
momentum = compute_momentum()
labels = [m["country"] for m in momentum][::-1]
pcts = [m["pctChange"] * 100 for m in momentum][::-1]
colors = [GOLD if p >= 0 else RED for p in pcts]
ax.barh(labels, pcts, color=colors)
ax.set_title("10-year % change in reserves")
ax.set_xlabel("% change")
ax.tick_params(axis="y", labelsize=8)
clean(ax)

ax = axes[1]
buyers = sorted(gd.TOP_BUYERS_3YR_2023_2025, key=lambda x: x[1])
ax.barh([b[0] for b in buyers], [b[1] for b in buyers], color=GOLD)
ax.set_title("Top cumulative buyers, 2023-2025 (t)")
clean(ax)
save(fig, "preview_buyers.png")

# =====================================================================
# 4) GOLD PRICE & DEMAND
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
suptitle(fig, "4. Global gold price and 2025 demand")

ax = axes[0]
years_p = [str(y) for y, _ in gd.PRICE_HISTORY]
prices = [p for _, p in gd.PRICE_HISTORY]
ax.plot(years_p, prices, color=GOLD_DARK, linewidth=2, marker="o", markersize=3)
ax.fill_between(range(len(years_p)), prices, 0, color=GOLD, alpha=0.12)
ax.scatter([len(years_p) - 1], [gd.PRICE_2025_RANGE[1]], color=RED, zorder=5, s=40, label="2025 high")
ax.scatter([len(years_p) - 1], [gd.PRICE_2025_RANGE[0]], color=GREEN, zorder=5, s=40, label="2025 low")
ax.set_ylim(0, gd.PRICE_2025_RANGE[1] * 1.1)
ax.set_title("Gold price, annual avg + 2025 intraday range (USD/oz)")
ax.set_xticks(range(0, len(years_p), 3))
ax.set_xticklabels([years_p[i] for i in range(0, len(years_p), 3)])
ax.legend(fontsize=8, frameon=False)
clean(ax)

ax = axes[1]
labels = [s for s, _ in gd.DEMAND_BY_SECTOR_2025]
vals = [t for _, t in gd.DEMAND_BY_SECTOR_2025]
wedges, _ = ax.pie(vals, colors=PALETTE, startangle=90, wedgeprops=dict(width=0.42, edgecolor="white"))
ax.legend(wedges, [f"{l} ({v/gd.DEMAND_TOTAL_2025*100:.0f}%)" for l, v in zip(labels, vals)],
          loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8, frameon=False)
ax.set_title(f"2025 demand by sector ({gd.DEMAND_TOTAL_2025:,.0f} t)")
save(fig, "preview_demand.png")

print("All preview images generated.")
