import pyspark.sql as ps
import pyspark.sql.functions as f


class Grouper:
    def __init__(self, df: ps.DataFrame, by: list[str]):
        self.df = df
        self.by = by

    def latest(self, on: str):
        version_window = ps.Window.partitionBy(self.by).orderBy(f.desc(on))
        return (
            self.df.withColumn("__version", f.row_number().over(version_window))
            .filter(f.col("__version") == 1)
            .drop("__version")
        )


def group(df: ps.DataFrame, by: list[str]):
    return Grouper(df, by)
