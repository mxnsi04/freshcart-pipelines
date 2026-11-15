"""
iris_project/data_exporters/save_results.py
--------------------------------------------
Mage data_exporter block: save_results
Saves predictions to iris_predictions.csv only if train_model passed its @test.
"""

try:
    from mage_ai.data_preparation.decorators import data_exporter, test
except ImportError:
    def data_exporter(fn):
        return fn
    def test(fn):
        return fn

OUTPUT_PATH = "iris_predictions.csv"


@data_exporter
def export_data(df, *args, **kwargs):
    """Write predictions DataFrame to CSV."""
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} predictions to {OUTPUT_PATH}")


@test
def test_output(output, *args) -> None:
    import os
    assert os.path.exists(OUTPUT_PATH), f"{OUTPUT_PATH} was not created"
