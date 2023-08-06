import pyspark.sql as ps


def assert_frame_equal(left: ps.DataFrame, right: ps.DataFrame):
    assert sorted(left.collect()) == sorted(right.collect())
