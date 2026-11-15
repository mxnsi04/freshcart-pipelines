"""
iris_project/transformers/prepare_data.py
-----------------------------------------
Mage transformer block: prepare_data
Splits the Iris DataFrame into train (80 %) and test (20 %) sets and
adds a 'split' column.

The @transformer and @test decorators are imported conditionally so the
file can be imported and unit-tested outside of a running Mage server.
"""

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    # Allow import outside Mage (e.g. in pytest) by defining no-op decorators.
    def transformer(fn):
        return fn

    def test(fn):
        return fn


@transformer
def transform(df, *args, **kwargs):
    """
    Split the DataFrame into train / test sets (80 / 20).

    Parameters
    ----------
    df : pandas.DataFrame
        Full Iris dataset (150 rows, columns: sepal length (cm),
        sepal width (cm), petal length (cm), petal width (cm), target).

    Returns
    -------
    pandas.DataFrame
        Original DataFrame with an additional 'split' column whose values
        are 'train' (120 rows) or 'test' (30 rows).
    """
    test_size = kwargs.get("test_size", 0.2)

    from sklearn.model_selection import train_test_split

    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=42
    )

    train_df = train_df.copy()
    test_df = test_df.copy()

    train_df["split"] = "train"
    test_df["split"] = "test"

    result = train_df._append(test_df).sort_index()
    return result


@test
def test_output(output, *args) -> None:
    """Verify the split column exists and proportions are correct."""
    assert output is not None, "Output must not be None"
    assert "split" in output.columns, "Output must contain a 'split' column"
    assert len(output) == 150, "Output must have 150 rows"
    train_count = (output["split"] == "train").sum()
    test_count = (output["split"] == "test").sum()
    assert train_count == 120, f"Expected 120 train rows, got {train_count}"
    assert test_count == 30, f"Expected 30 test rows, got {test_count}"
