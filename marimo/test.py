import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full", app_title="Analysis")


@app.cell
def imports():
    import marimo as mo
    import polars as pl
    import altair as alt
    import numpy as np4

    return alt, mo, pl


@app.cell
def title(mo):
    mo.md("""
    # 🎧 Reactive dataframes with polars + AltairSomething went wrong
    Failed to fetch dynamically imported module: http://127.0.0.1:36157/assets/vega-embed-container-CH1lX0V6.js
    If this is an issue with marimo, please report it on GitHub.

    Move a control or drag a box on the chart. **Nothing is re-run by hand** —
    marimo re-executes every cell that depends on what changed.
    """)
    return


@app.cell
def data():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _rng = np.random.default_rng(7)
    _n = 400

    _genres = ["Pop", "Hip-Hop", "Rock", "Electronic", "Jazz"]
    _genre = _rng.choice(_genres, _n, p=[0.30, 0.25, 0.20, 0.15, 0.10])

    _base = {"Pop": 0.65, "Hip-Hop": 0.72, "Rock": 0.80, "Electronic": 0.88, "Jazz": 0.35}
    _energy = np.clip([_base[g] + _rng.normal(0, 0.10) for g in _genre], 0.05, 1.0)

    _year = _rng.integers(2015, 2026, _n)

    # louder + newer tracks stream a bit more, with heavy lognormal spread
    _streams = 10 ** (_rng.normal(6.0, 0.45, _n) + 0.9 * (_energy - 0.6) + 0.06 * (_year - 2015))

    _adj = ["Neon", "Velvet", "Midnight", "Golden", "Electric",
            "Paper", "Crimson", "Silent", "Wild", "Lunar"]
    _noun = ["Cathedral", "River", "Machine", "Ghost", "Harbor",
             "Signal", "Mirage", "Engine", "Garden", "Static"]
    _name = [f"{a} {b}" for a, b in zip(_rng.choice(_adj, _n), _rng.choice(_noun, _n))]

    tracks = pl.DataFrame(
        {
            "track": _name,
            "genre": _genre,
            "year": _year,
            "energy": np.round(_energy, 3),
            "streams_m": np.round(_streams / 1_000_000, 3),
        }
    )

    tracks
    """)
    return


@app.cell
def controls(mo, tracks):
    genre_pick = mo.ui.multiselect(
        options=sorted(tracks["genre"].unique().to_list()),
        value=sorted(tracks["genre"].unique().to_list()),
        label="Genres",
    )
    year_range = mo.ui.range_slider(
        start=2015, stop=2025, step=1, value=[2018, 2025],
        label="Years", show_value=True,
    )
    min_energy = mo.ui.slider(
        start=0.0, stop=1.0, step=0.05, value=0.0,
        label="Min energy", show_value=True,
    )

    mo.hstack([genre_pick, year_range, min_energy], justify="start", gap=2)
    return genre_pick, min_energy, year_range


@app.cell
def filter_tracks(genre_pick, min_energy, mo, pl, tracks, year_range):
    filtered = tracks.filter(
        pl.col("genre").is_in(genre_pick.value)
        & pl.col("year").is_between(year_range.value[0], year_range.value[1])
        & (pl.col("energy") >= min_energy.value)
    )

    mo.md(f"Matching **{filtered.height:,}** of **{tracks.height:,}** tracks.")
    return (filtered,)


@app.cell
def chart(alt, filtered, mo):
    chart = mo.ui.altair_chart(
        alt.Chart(filtered, height=380)
        .mark_circle(size=90, opacity=0.7)
        .encode(
            x=alt.X("energy:Q", title="Energy", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("streams_m:Q", title="Streams (millions)", scale=alt.Scale(type="log")),
            color=alt.Color("genre:N", title="Genre"),
            tooltip=["track", "genre", "year", "energy", "streams_m"],
        )
    )

    chart
    return (chart,)


@app.cell
def selection(chart, mo, pl):
    sel = chart.value

    if sel.height == 0:
        _out = mo.callout(
            mo.md("👆 **Drag a box across the chart** (or click a genre in the legend). "
                  "Your selection lands in `chart.value` as a *polars* DataFrame, and this cell reruns."),
            kind="info",
        )
    else:
        _by_genre = (
            sel.group_by("genre")
            .agg(
                pl.len().alias("tracks"),
                pl.col("streams_m").mean().round(2).alias("avg_streams_m"),
                pl.col("energy").mean().round(3).alias("avg_energy"),
            )
            .sort("tracks", descending=True)
        )
        _top = sel.sort("streams_m", descending=True).head(8).select(
            "track", "genre", "year", "energy", "streams_m"
        )
        _out = mo.vstack([
            mo.md(f"### Selected **{sel.height}** tracks"),
            mo.md("**By genre**"),
            mo.ui.table(_by_genre, selection=None),
            mo.md("**Biggest in selection**"),
            mo.ui.table(_top, selection=None),
        ])

    _out
    return


@app.cell
def explain(mo):
    mo.md("""
    ### What just happened

    | Cell | Defines | Reruns when |
    |---|---|---|
    | data | `tracks` | never (it is the source) |
    | controls | `genre_pick`, `year_range`, `min_energy` | `tracks` changes |
    | filter | `filtered` | any control moves |
    | chart | `chart` | `filtered` changes |
    | selection | `sel` | you select on the chart |

    marimo reads the variables each cell **defines** and **references**, builds a
    DAG, and reruns descendants in order. There is no "Run All", and no stale
    state — deleting a cell also deletes its variables.

    One rule to internalise: a UI element's `.value` must be read in a *different*
    cell than the one that creates it. Same cell = no reactivity.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
