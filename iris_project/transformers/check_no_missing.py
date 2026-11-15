"""
iris_project/transformers/check_no_missing.py
----------------------------------------------
Part C4 – custom block: validate the raw Iris dataset
Checks:
  - No missing values in any column.
  - Exactly 3 unique target classes.
"""

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn):
        return fn
    def test(fn):
        return fn


@transformer
def transform(df, *args, **kwargs):
    """
    Pass through the DataFrame after asserting data quality.
    Returns the same DataFrame so the next block can use it.
    """
    missing = df.isnull().sum().sum()
    n_classes = df["target"].nunique()

    print(f"Missing values: {missing}")
    print(f"Unique target classes: {n_classes}")

    if missing > 0:
        raise ValueError(f"Dataset has {missing} missing value(s).")
    if n_classes != 3:
        raise ValueError(f"Expected 3 target classes, found {n_classes}.")

    print("Data quality check PASSED: no missing values, exactly 3 classes.")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "Output must not be None"
    assert output.isnull().sum().sum() == 0, "Missing values detected"
    assert output["target"].nunique() == 3, "Expected exactly 3 target classes"
