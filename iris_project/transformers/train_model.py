"""
iris_project/transformers/train_model.py
-----------------------------------------
Mage transformer block: train_model
Trains a DecisionTreeClassifier on the train split and evaluates it
on the test split.
"""

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(fn):
        return fn
    def test(fn):
        return fn

ACCURACY_THRESHOLD = 0.85


@transformer
def transform(df, *args, **kwargs):
    """
    Train a DecisionTreeClassifier and return predictions DataFrame.

    Runtime var  : max_depth (int, default 3)
    Returns      : DataFrame with columns [y_true, y_pred, split, accuracy]
    """
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score
    import pandas as pd

    max_depth = int(kwargs.get("max_depth", 3))

    feature_cols = [c for c in df.columns if c not in ("target", "split")]
    train = df[df["split"] == "train"]
    test_set = df[df["split"] == "test"]

    X_train = train[feature_cols]
    y_train = train["target"]
    X_test = test_set[feature_cols]
    y_test = test_set["target"]

    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"max_depth={max_depth}  test_accuracy={acc:.4f}")

    result = pd.DataFrame({
        "y_true": y_test.values,
        "y_pred": y_pred,
        "accuracy": acc,
    })
    return result


@test
def test_accuracy(output, *args) -> None:
    """Fail the pipeline if test accuracy is below the threshold."""
    assert output is not None, "Output must not be None"
    acc = float(output["accuracy"].iloc[0])
    assert acc >= ACCURACY_THRESHOLD, (
        f"Test accuracy {acc:.4f} is below threshold {ACCURACY_THRESHOLD}. "
        "save_results will NOT run."
    )
