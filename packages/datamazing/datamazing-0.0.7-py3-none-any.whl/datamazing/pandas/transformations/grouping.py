import pandas as pd

from . import resampling


def _list(a):
    if not isinstance(a, list):
        return [a]
    return a


def _concat(a, b):
    return _list(a) + _list(b)


class GrouperResampler:
    def __init__(self, gb: "Grouper", on: str, resolution: pd.Timedelta):
        self.gb = gb
        self.on = on
        self.resolution = resolution
        self.resampler = self._get_resampler()

    def _get_resampler(self):
        pdf = (
            self.gb.df.set_index(_concat(self.on, self.gb.by))
            .unstack(self.gb.by)
            .reset_index(self.on)
        )
        return resampling.resample(pdf, self.on, self.resolution)

    def agg(self, method: str):
        resampled_pdf = self.resampler.agg(method)
        return (
            resampled_pdf.set_index(self.on)
            .stack(self.gb.by, dropna=True)
            .swaplevel(i=0, j=-1)
            .sort_index()
            .reset_index(_concat(self.gb.by, self.on))
        )


class Grouper:
    def __init__(self, df: pd.DataFrame, by: list[str]):
        self.df = df
        self.by = by

    def agg(self, method: str):
        return (
            self.df.set_index(self.by)
            .groupby(self.by, dropna=False)
            .aggregate(method)
            .reset_index()
        )

    def resample(self, on: str, resolution: pd.Timedelta):
        return GrouperResampler(self, on, resolution)

    def pivot(self, on: list[str], values: list[tuple[str]] = None):
        """
        Pivot table. Non-existing combinations will be filled
        with NaNs.

        Args:
            on (list[str]): Columns which to pivot
            values (list[tuple[str]], optional): Enforce
                the existence of columns with these names
                after pivoting. Defaults to None, in which
                case the values will be inferred from the
                pivoting column.
        """

        df = self.df.set_index(_concat(self.by, on))

        if values:
            by_vals = df.index.to_frame(index=False)[_list(self.by)]
            on_vals = pd.DataFrame(values, columns=_list(on))
            cross_vals = by_vals.merge(on_vals, how="cross")
            df = df.reindex(pd.MultiIndex.from_frame(cross_vals))

        df = df.unstack(on)

        df.columns = df.columns.map(
            lambda cols: "_".join([str(col) for col in cols[1:]]) + "_" + str(cols[0])
        ).str.strip("_")

        return df.reset_index()

    def latest(self, on: str):
        return (
            self.df.set_index(_concat(self.by, on))
            .sort_index(level=on)
            .groupby(self.by, dropna=False)
            .tail(1)
            .reset_index()
        )


def group(df: pd.DataFrame, by: list[str]):
    return Grouper(df, by)
