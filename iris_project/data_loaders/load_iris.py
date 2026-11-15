"""
iris_project/data_loaders/load_iris.py
----------------------------------------
Mage data_loader block: load_iris
Loads the sklearn Iris dataset as a pandas DataFrame.
"""

try:
    from mage_ai.data_preparation.decorators import data_loader, test
except ImportError:
    def data_loader(fn):
        return fn
    def test(fn):
        return fn


@data_loader
def load_data(*args, **kwargs):
    """
    Load the Iris dataset from sklearn.

    Returns
    -------
    pandas.DataFrame
        150 rows × 5 columns (4 features + target).
    """
    from sklearn.datasets import load_iris

    iris = load_iris(as_frame=True)
    df = iris.frame
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "Output must not be None"
    assert len(output) == 150, "Iris dataset must have 150 rows"
    assert output.shape[1] == 5, "Iris frame must have 5 columns (4 features + target)"
