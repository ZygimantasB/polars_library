import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import polars.selectors as cs

    return (pl,)


@app.cell
def _():
    df_path = r'/mnt/samsung/Datasets/csv_data/ToP 250 movies on imdb in 2026.csv'
    return (df_path,)


@app.cell
def _(df_path, pl):
    df = pl.read_csv(df_path)
    return (df,)


@app.cell
def _(df):
    print(df.collect_schema())
    return


@app.cell
def _(df):
    df.glimpse()
    return


@app.cell
def _(df):
    df.describe()
    return


@app.cell
def _(df):
    df.estimated_size('mb')
    return


@app.cell
def _(df):
    df.shape()
    return


@app.cell
def _(df):
    df.height
    return


@app.cell
def _(df):
    df.width()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
