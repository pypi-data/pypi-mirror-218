import warnings

__version__ = "0.2.3"

warnings.warn(
    "iterable_etl is deprecated and will no longer be maintained. Consider using an appropriate ETL tool for this functionality.",
    FutureWarning,
)
