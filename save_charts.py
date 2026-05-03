"""
Render all dashboard charts as high-quality images and save to picture/
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("picture", exist_ok=True)

# ── Load data ───────────────────────────────────────────────
fd  = pd.read_csv("dw/OLAP Failure Distribution by Failure Type.csv")
qr  = pd.read_csv("dw/OLAP Failure Rate by Product Quality Type.csv")
mc  = pd.read_csv("dw/OLAP Machine Condition vs Failure Rate.csv")
mt  = pd.read_csv("dw/OLAP Monthly Failure Trend.csv")
mt["Month Name"] = mt["Month Name"].str.strip()

PALETTE = {
    "Heat Dissipation Failure": "#EF5350",
    "Power Failure":            "#FF7043",
    "Overstrain Failure":       "#AB47BC",
    "Tool Wear Failure":        "#FFA726",
    "Random Failure":           "#78909C",
    "Low Quality":              "#EF5350",
    "Medium Quality":           "#FFA726",
    "High Quality":             "#66BB6A",
    "Low":                      "#66BB6A",
    "Medium":                   "#FFA726",
    "High":                     "#EF5350",
    "Critical":                 "#7B1FA2",
}
BG = "#FAFAFA"

def style(ax, title):
    ax.set_facecolor(BG)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

# ── 01: KPI Banner ──────────────────────────────────────────
fig, axes = plt.subplots(1, 4, figsize=(16, 3))
fig.patch.set_facecolor("#1565C0")
kpis = [
    ("📦 Total Records",    "6,390",   "#FFFFFF"),
    ("⚠️  Total Failures",  "245",     "#FFD54F"),
    ("📉 Avg Failure Rate", "3.83%",   "#80CBC4"),
    ("🔴 Top Failure Type", "Heat\nDissipation\nFailure", "#EF9A9A"),
]
for ax, (label, val, color) in zip(axes, kpis):
    ax.set_facecolor("#1565C0")
    ax.text(0.5, 0.65, val,  ha="center", va="center", fontsize=22, fontweight="bold", color=color, transform=ax.transAxes)
    ax.text(0.5, 0.2,  label, ha="center", va="center", fontsize=10, color="#B3E5FC", transform=ax.transAxes)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
plt.suptitle("🏭  Manufacturing Failure Analysis Dashboard  —  KPI Overview",
             fontsize=14, fontweight="bold", color="white", y=1.02)
plt.tight_layout()
plt.savefig("picture/01_kpi_cards.jpg", dpi=150, bbox_inches="tight", facecolor="#1565C0")
plt.close()
print("✓ 01_kpi_cards.jpg")

# ── 02: Failure Distribution Bar Chart ──────────────────────
failures = fd[fd["Failure Type"] != "No Failure"].sort_values("Occurrences", ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
colors = [PALETTE.get(t, "#90A4AE") for t in failures["Failure Type"]]
bars = ax.bar(failures["Failure Type"], failures["Occurrences"], color=colors, width=0.55, edgecolor="white", linewidth=1.5)
for bar, val in zip(bars, failures["Occurrences"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.2, str(val),
            ha="center", va="bottom", fontsize=12, fontweight="bold")
ax.set_xlabel("Failure Type", fontsize=12)
ax.set_ylabel("Number of Occurrences", fontsize=12)
ax.set_xticklabels(failures["Failure Type"], rotation=15, ha="right", fontsize=10)
style(ax, "📊  Failure Distribution by Type (excl. No Failure)")
plt.tight_layout()
plt.savefig("picture/02_failure_distribution_bar.jpg", dpi=150, bbox_inches="tight")
plt.close()
print("✓ 02_failure_distribution_bar.jpg")

# ── 03: Monthly Failure Trend Line Chart ────────────────────
fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
x = range(len(mt))
ax.fill_between(x, mt["Failures"], alpha=0.12, color="#1976D2")
ax.plot(x, mt["Failures"], color="#1976D2", linewidth=2.5, marker="o",
        markersize=8, markerfacecolor="white", markeredgewidth=2, markeredgecolor="#1976D2")
for i, (val, ops) in enumerate(zip(mt["Failures"], mt["Operations"])):
    ax.annotate(str(val), (i, val), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=11, fontweight="bold", color="#1565C0")
ax.set_xticks(x)
ax.set_xticklabels(mt["Month Name"], rotation=20, ha="right", fontsize=10)
ax.set_ylabel("Failure Count", fontsize=12)
ax.set_ylim(0, mt["Failures"].max() + 8)
style(ax, "📈  Monthly Failure Trend — 2023")
plt.tight_layout()
plt.savefig("picture/03_monthly_trend_line.jpg", dpi=150, bbox_inches="tight")
plt.close()
print("✓ 03_monthly_trend_line.jpg")

# ── 04: Machine Condition Scatter Plot ──────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
risk_colors = [PALETTE.get(r, "#90A4AE") for r in mc["Risk Level"]]
sizes = (mc["Failures"] / mc["Failures"].max()) * 2000 + 200
scatter = ax.scatter(mc["Condition"], mc["Failure Rate (%)"],
                     s=sizes, c=risk_colors, alpha=0.85, edgecolors="white", linewidth=2, zorder=3)
for _, row in mc.iterrows():
    ax.annotate(f"{row['Failure Rate (%)']:.1f}%",
                (row["Condition"], row["Failure Rate (%)"]),
                textcoords="offset points", xytext=(0, 16),
                ha="center", fontsize=11, fontweight="bold")
legend_patches = [mpatches.Patch(color=PALETTE[r], label=r) for r in ["Low","Medium","High","Critical"]]
ax.legend(handles=legend_patches, title="Risk Level", loc="upper left", fontsize=10)
ax.set_xlabel("Machine Condition", fontsize=12)
ax.set_ylabel("Failure Rate (%)", fontsize=12)
ax.set_xticklabels(mc["Condition"], rotation=12, ha="right", fontsize=9)
ax.set_xticks(range(len(mc)))
style(ax, "🔧  Machine Condition vs Failure Rate  (bubble size = failure count)")
ax.grid(axis="both", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("picture/04_machine_condition_scatter.jpg", dpi=150, bbox_inches="tight")
plt.close()
print("✓ 04_machine_condition_scatter.jpg")

# ── 05: Product Quality Bar Chart ───────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
colors_q = [PALETTE.get(q, "#90A4AE") for q in qr["Product Quality"]]
bars = ax.bar(qr["Product Quality"], qr["Failure Rate (%)"], color=colors_q,
              width=0.45, edgecolor="white", linewidth=1.5)
for bar, val in zip(bars, qr["Failure Rate (%)"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f"{val:.2f}%", ha="center", va="bottom", fontsize=13, fontweight="bold")
ax.set_xlabel("Product Quality Type", fontsize=12)
ax.set_ylabel("Failure Rate (%)", fontsize=12)
ax.set_ylim(0, qr["Failure Rate (%)"].max() + 1)
style(ax, "🏷️  Failure Rate by Product Quality Type")
plt.tight_layout()
plt.savefig("picture/05_product_quality_bar.jpg", dpi=150, bbox_inches="tight")
plt.close()
print("✓ 05_product_quality_bar.jpg")

# ── 06: Data Tables composite ───────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(18, 10))
fig.patch.set_facecolor("#F5F5F5")
fig.suptitle("📋  OLAP Data Tables — All Datasets", fontsize=15, fontweight="bold", y=1.01)

tables = [
    (fd[["Failure Type","Category","Occurrences","% of All Records"]],
     "Failure Distribution by Type"),
    (mt[["Month Name","Operations","Failures","Failure Rate (%)"]],
     "Monthly Failure Trend"),
    (mc[["Condition","Risk Level","Operations","Failures","Failure Rate (%)"]],
     "Machine Condition vs Failure Rate"),
    (qr[["Product Quality","Total Operations","Total Failures","Failure Rate (%)"]],
     "Failure Rate by Product Quality"),
]

for ax, (df, title) in zip(axes.flat, tables):
    ax.axis("off")
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    tbl = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center"
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.6)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_facecolor("#1565C0")
            cell.set_text_props(color="white", fontweight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#E3F2FD")
        cell.set_edgecolor("#BDBDBD")

plt.tight_layout()
plt.savefig("picture/06_data_tables.jpg", dpi=150, bbox_inches="tight")
plt.close()
print("✓ 06_data_tables.jpg")

# ── 07: Sidebar Filters illustration ────────────────────────
fig, ax = plt.subplots(figsize=(5, 10))
fig.patch.set_facecolor("#1E1E1E")
ax.set_facecolor("#1E1E1E")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)

sections = [
    ("🏭  Dashboard Filters", 0.96, 13, "#FFFFFF", "bold"),
    ("─" * 28, 0.92, 9, "#555555", "normal"),
    ("Failure Types", 0.88, 10, "#90CAF9", "bold"),
    ("☑ No Failure", 0.84, 9, "#EEEEEE", "normal"),
    ("☑ Heat Dissipation Failure", 0.80, 9, "#EEEEEE", "normal"),
    ("☑ Power Failure", 0.76, 9, "#EEEEEE", "normal"),
    ("☑ Overstrain Failure", 0.72, 9, "#EEEEEE", "normal"),
    ("☑ Tool Wear Failure", 0.68, 9, "#EEEEEE", "normal"),
    ("☑ Random Failure", 0.64, 9, "#EEEEEE", "normal"),
    ("─" * 28, 0.60, 9, "#555555", "normal"),
    ("Months", 0.56, 10, "#90CAF9", "bold"),
    ("☑ January  ☑ February  ☑ March", 0.52, 9, "#EEEEEE", "normal"),
    ("☑ April    ☑ May       ☑ June", 0.48, 9, "#EEEEEE", "normal"),
    ("☑ July     ☑ August    ☑ September", 0.44, 9, "#EEEEEE", "normal"),
    ("☑ October  ☑ November  ☑ December", 0.40, 9, "#EEEEEE", "normal"),
    ("─" * 28, 0.36, 9, "#555555", "normal"),
    ("Machine Conditions", 0.32, 10, "#90CAF9", "bold"),
    ("☑ New Tool (0-100 min)", 0.28, 9, "#EEEEEE", "normal"),
    ("☑ Mid-Life Tool (100-200 min)", 0.24, 9, "#EEEEEE", "normal"),
    ("☑ Aging Tool (200-240 min)", 0.20, 9, "#EEEEEE", "normal"),
    ("☑ Worn Tool (>240 min)", 0.16, 9, "#EEEEEE", "normal"),
    ("─" * 28, 0.12, 9, "#555555", "normal"),
    ("CO4031 BTL · Manufacturing DW", 0.06, 8, "#616161", "normal"),
]
for text, y, size, color, weight in sections:
    ax.text(0.5, y, text, ha="center", va="center", fontsize=size,
            color=color, fontweight=weight, transform=ax.transAxes,
            style="italic" if y == 0.06 else "normal",
            fontfamily="monospace" if "─" in text else "sans-serif")

plt.tight_layout()
plt.savefig("picture/07_sidebar_filters.jpg", dpi=150, bbox_inches="tight", facecolor="#1E1E1E")
plt.close()
print("✓ 07_sidebar_filters.jpg")

# ── 08: Full dashboard composite ────────────────────────────
fig = plt.figure(figsize=(20, 22))
fig.patch.set_facecolor("#F0F2F6")
fig.suptitle("🏭  Manufacturing Failure Analysis Dashboard  —  Full Overview",
             fontsize=18, fontweight="bold", y=0.99)

gs = fig.add_gridspec(3, 2, hspace=0.45, wspace=0.3,
                       top=0.95, bottom=0.04, left=0.06, right=0.97)

# Row 1: bar + line
ax1 = fig.add_subplot(gs[0, 0])
colors1 = [PALETTE.get(t, "#90A4AE") for t in failures["Failure Type"]]
bars1 = ax1.bar(failures["Failure Type"], failures["Occurrences"], color=colors1, width=0.55, edgecolor="white")
for bar, val in zip(bars1, failures["Occurrences"]):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, str(val),
             ha="center", va="bottom", fontsize=9, fontweight="bold")
ax1.set_xticklabels(failures["Failure Type"], rotation=15, ha="right", fontsize=8)
style(ax1, "Failure Distribution by Type")

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(BG)
x2 = range(len(mt))
ax2.fill_between(x2, mt["Failures"], alpha=0.12, color="#1976D2")
ax2.plot(x2, mt["Failures"], color="#1976D2", lw=2.5, marker="o",
         markersize=6, markerfacecolor="white", markeredgewidth=2, markeredgecolor="#1976D2")
for i, v in enumerate(mt["Failures"]):
    ax2.annotate(str(v), (i, v), xytext=(0,7), textcoords="offset points",
                 ha="center", fontsize=8, fontweight="bold", color="#1565C0")
ax2.set_xticks(x2); ax2.set_xticklabels(mt["Month Name"], rotation=25, ha="right", fontsize=7)
ax2.set_ylim(0, mt["Failures"].max() + 8)
style(ax2, "Monthly Failure Trend (2023)")

# Row 2: scatter + quality bar
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(BG)
s3 = (mc["Failures"]/mc["Failures"].max())*1500+150
c3 = [PALETTE.get(r,"#90A4AE") for r in mc["Risk Level"]]
ax3.scatter(range(len(mc)), mc["Failure Rate (%)"], s=s3, c=c3, alpha=0.85,
            edgecolors="white", linewidth=2, zorder=3)
ax3.set_xticks(range(len(mc)))
ax3.set_xticklabels(mc["Condition"], rotation=12, ha="right", fontsize=7.5)
for i, row in mc.iterrows():
    ax3.annotate(f"{row['Failure Rate (%)']:.1f}%", (i, row["Failure Rate (%)"]),
                 xytext=(0,12), textcoords="offset points", ha="center", fontsize=9, fontweight="bold")
lp = [mpatches.Patch(color=PALETTE[r], label=r) for r in ["Low","Medium","High","Critical"]]
ax3.legend(handles=lp, fontsize=8, title="Risk")
ax3.grid(axis="both", linestyle="--", alpha=0.4)
style(ax3, "Machine Condition vs Failure Rate")

ax4 = fig.add_subplot(gs[1, 1])
c4 = [PALETTE.get(q,"#90A4AE") for q in qr["Product Quality"]]
bars4 = ax4.bar(qr["Product Quality"], qr["Failure Rate (%)"], color=c4, width=0.4, edgecolor="white")
for bar, val in zip(bars4, qr["Failure Rate (%)"]):
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
             f"{val:.2f}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
ax4.set_ylim(0, qr["Failure Rate (%)"].max()+1)
style(ax4, "Failure Rate by Product Quality")

# Row 3: KPI row
ax5 = fig.add_subplot(gs[2, :])
ax5.set_facecolor("#1565C0")
ax5.set_xticks([]); ax5.set_yticks([])
for s in ax5.spines.values(): s.set_visible(False)
kpi_data = [
    (0.12, "📦 Total Records",    "6,390",   "#FFFFFF"),
    (0.37, "⚠️  Total Failures",  "245",     "#FFD54F"),
    (0.62, "📉 Avg Failure Rate", "3.83%",   "#80CBC4"),
    (0.87, "🔴 Top Failure Type", "Heat Dissipation Failure", "#EF9A9A"),
]
for x_, label, val, color in kpi_data:
    ax5.text(x_, 0.65, val,   ha="center", va="center", fontsize=18, fontweight="bold",
             color=color, transform=ax5.transAxes)
    ax5.text(x_, 0.25, label, ha="center", va="center", fontsize=10,
             color="#B3E5FC", transform=ax5.transAxes)

plt.savefig("picture/08_full_dashboard_composite.jpg", dpi=150, bbox_inches="tight")
plt.close()
print("✓ 08_full_dashboard_composite.jpg")

print("\n✅ All 8 screenshots saved to picture/")
