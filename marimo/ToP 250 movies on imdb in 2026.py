import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return (pl,)


@app.cell
def _():
    df_path = r'/mnt/samsung/Datasets/csv_data/ToP 250 movies on imdb in 2026.csv'
    return (df_path,)


@app.cell
def _(df_path, pl):
    df = pl.read_csv(df_path)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
