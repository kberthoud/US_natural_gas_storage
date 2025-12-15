import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


processed_path = Path("../data/processed")
filename = "storage_with_HH_prices.csv"

df = pd.read_csv(
    processed_path / filename,
    parse_dates = ["period"]
    )

#print(df.columns)
df = df.rename(columns={
    "('hh_price', 'NG=F')":"hh_price"
    })

#print(df.columns)
df = df.dropna(subset={"hh_price","diff"})
print(df)

fig, ax_price = plt.subplots(figsize=(14, 6))

ax_price.plot(
    df["period"],
    df["hh_price"],
    linewidth=2,
    label="Henry Hub Front Month"
)

ax_price.set_ylabel("HH Front Month Price ($/MMBtu)")
ax_price.set_xlabel("Date")

ax_storage = ax_price.twinx()

ax_storage.fill_between(
    df["period"],
    df["diff"],
    alpha=0.3,
    label="Storage vs 5-Year Avg"
)

ax_storage.set_ylabel("Storage Surplus / Deficit (BCF)")

ax_storage.axhline(0, linewidth=1)

lines_1, labels_1 = ax_price.get_legend_handles_labels()
lines_2, labels_2 = ax_storage.get_legend_handles_labels()

ax_price.legend(
    lines_1 + lines_2,
    labels_1 + labels_2,
    loc="upper left"
)

fig.suptitle(
    "Henry Hub Front Month Prices vs Storage Surplus / Deficit",
    fontsize=14
)

fig.tight_layout()

plt.show()

#save the plot

fig_path = Path("../outputs/figures")
fig_path.mkdir(parents=True, exist_ok=True)

fig_filename = "storage_vs_HH.png"

fig.savefig(
    fig_path / fig_filename,
    dpi=150,
    bbox_inches="tight"
)
