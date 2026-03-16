"""ML training pipeline.

Supports classification and regression tasks using scikit-learn.
Experiments are tracked via MLflow.

Supported algorithms
--------------------
Classification:
  random_forest_classifier  — RandomForestClassifier
  logistic_regression       — LogisticRegression

Regression:
  random_forest_regressor   — RandomForestRegressor
  linear_regression         — LinearRegression
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression

# ── Algorithm registry ────────────────────────────────────────────────────────
# Each key is the string callers pass to ModelTrainer(algorithm=...)
# New algorithms can be added here without changing any other code.

CLASSIFIERS: dict[str, Any] = {
    "random_forest_classifier": RandomForestClassifier(
        n_estimators=100, random_state=42
    ),
    "logistic_regression": LogisticRegression(
        max_iter=1000, random_state=42
    ),
}

REGRESSORS: dict[str, Any] = {
    "random_forest_regressor": RandomForestRegressor(
        n_estimators=100, random_state=42
    ),
    "linear_regression": LinearRegression(),
}

ALL_ALGORITHMS: dict[str, Any] = {**CLASSIFIERS, **REGRESSORS}


@dataclass
class TrainingResult:
    """Captures the outcome of a completed training run."""

    algorithm: str
    task: str           # "classification" | "regression"
    mlflow_run_id: str
    artefact_path: str

    # Classification metrics — None for regression tasks
    accuracy: float | None = None
    f1: float | None = None

    # Regression metrics — None for classification tasks
    r2: float | None = None
    rmse: float | None = None

    params: dict[str, Any] = field(default_factory=dict)


class ModelTrainer:
    """Trains a scikit-learn estimator on a pandas DataFrame.

    Parameters
    ----------
    algorithm:
        One of the keys defined in ALL_ALGORITHMS.
    target_column:
        Name of the column to predict.
    test_size:
        Fraction of rows held out for evaluation (default 20%).

    Raises
    ------
    ValueError
        If ``algorithm`` is not in the registry.
    """

    def __init__(
        self,
        algorithm: str,
        target_column: str,
        test_size: float = 0.2,
    ) -> None:
        if algorithm not in ALL_ALGORITHMS:
            raise ValueError(
                f"Unknown algorithm {algorithm!r}. "
                f"Valid options: {sorted(ALL_ALGORITHMS)}"
            )

        self.algorithm = algorithm
        self.target_column = target_column
        self.test_size = test_size
        self._task = (
            "classification" if algorithm in CLASSIFIERS else "regression"
        )

    # train() and helper methods will be added in upcoming commits.
