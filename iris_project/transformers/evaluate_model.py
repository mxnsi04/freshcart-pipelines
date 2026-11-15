"""
iris_project/transformers/evaluate_model.py
--------------------------------------------
Mage transformer block: evaluate_model  (Part C3 – evaluation branch)
Runs alongside save_results as a second downstream block from train_model.
Prints a confusion matrix and a metrics table (precision, recall, F1).
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
    Compute confusion matrix and per-class metrics from predictions.

    Parameters
    ----------
    df : DataFrame with columns [y_true, y_pred, accuracy]

    Returns
    -------
    dict  {'confusion_matrix': ..., 'report': ...}
    """
    from sklearn.metrics import confusion_matrix, classification_report
    import pandas as pd

    y_true = df["y_true"].values
    y_pred = df["y_pred"].values

    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred, output_dict=True)

    cm_df = pd.DataFrame(
        cm,
        index=["True 0", "True 1", "True 2"],
        columns=["Pred 0", "Pred 1", "Pred 2"],
    )

    report_df = pd.DataFrame(report).transpose()

    print("=== Confusion Matrix ===")
    print(cm_df.to_string())
    print("\n=== Classification Report ===")
    print(report_df[["precision", "recall", "f1-score", "support"]].to_string())

    return {"confusion_matrix": cm_df, "report": report_df}


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert "confusion_matrix" in output
    assert "report" in output
