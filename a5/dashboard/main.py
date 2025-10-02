# dashboard/main.py
import pandas as pd
from pathlib import Path
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select, Div
from bokeh.layouts import column, row
from bokeh.plotting import figure

# ---------- Load precomputed CSV ----------
HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "data" / "nyc311_monthly.csv"   # adjust if needed
if not CSV.exists():
    raise FileNotFoundError(f"Expected file not found: {CSV}")

df = pd.read_csv(CSV, dtype={"zipcode": str})
# only 2024 per the assignment
df = df[df["year"] == 2024].copy()
df["date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(int).astype(str) + "-01")

# ---------- Build ALL-NYC (weighted by count) ----------
all_df = (
    df.groupby(["year", "month", "date"], as_index=False)
      .apply(lambda g: pd.Series({"all_avg": (g["avg_hours"] * g["count"]).sum() / g["count"].sum()}))
      .reset_index(drop=True)
)

# ---------- Zipcode options ----------
# Filter out obvious junk like "00000" but keep everything else
zip_options = sorted(z for z in df["zipcode"].unique() if z != "00000")
if not zip_options:
    # fallback if everything was filtered
    zip_options = sorted(df["zipcode"].unique())

default_z1 = zip_options[0]
default_z2 = zip_options[1] if len(zip_options) > 1 else zip_options[0]

# ---------- Helper to build a combined table for selected zipcodes ----------
def build_table(z1: str, z2: str) -> pd.DataFrame:
    m = all_df[["date", "all_avg"]].copy()
    s1 = df[df["zipcode"] == z1].set_index("date")["avg_hours"]
    s2 = df[df["zipcode"] == z2].set_index("date")["avg_hours"]
    m["zip1_avg"] = m["date"].map(s1).fillna(0.0)
    m["zip2_avg"] = m["date"].map(s2).fillna(0.0)
    return m

table = build_table(default_z1, default_z2)
source = ColumnDataSource(table)

# ---------- Figure ----------
p = figure(
    x_axis_type="datetime",
    height=420,
    sizing_mode="stretch_width",
    title="NYC 311 — Monthly Avg Response Time (hours), 2024",
)
# lines + markers so single-month data is still visible
l_all  = p.line("date", "all_avg",  source=source, line_width=3, color="black", legend_label="ALL 2024")
m_all  = p.circle("date", "all_avg", source=source, size=6, color="black")

l_z1   = p.line("date", "zip1_avg", source=source, line_width=3, color="royalblue", legend_label="Zip 1")
m_z1   = p.circle("date", "zip1_avg", source=source, size=6, color="royalblue")

l_z2   = p.line("date", "zip2_avg", source=source, line_width=3, color="crimson", legend_label="Zip 2")
m_z2   = p.circle("date", "zip2_avg", source=source, size=6, color="crimson")

p.legend.location = "top_left"   # valid in Bokeh 3.x
p.legend.click_policy = "hide"
p.xaxis.axis_label = "Month"
p.yaxis.axis_label = "Avg response time (hours)"

# ---------- Controls ----------
select1 = Select(title="Zipcode 1", value=default_z1, options=zip_options)
select2 = Select(title="Zipcode 2", value=default_z2, options=zip_options)
label = Div(text=f"<b>Comparing:</b> Zip 1 = {default_z1} &nbsp;&nbsp; Zip 2 = {default_z2}")

def update(attr, old, new):
    new_df = build_table(select1.value, select2.value)
    # IMPORTANT: assign a plain dict (Bokeh requirement)
    source.data = dict(ColumnDataSource(new_df).data)
    label.text = f"<b>Comparing:</b> Zip 1 = {select1.value} &nbsp;&nbsp; Zip 2 = {select2.value}"

select1.on_change("value", update)
select2.on_change("value", update)

curdoc().add_root(column(label, row(select1, select2), p))
curdoc().title = "NYC 311 Dashboard"
