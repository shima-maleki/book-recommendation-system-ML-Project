"""
Standalone data ingestion pipeline.

Reads raw CSVs from the mounted Data directory and writes cleaned artifacts
into ./artifacts. Useful when you want to persist preprocessed data without
running model training.
"""
from src.components.data_ingestion import DataIngestion


def run():
    ingestion = DataIngestion()
    ingestion.initiate_data_ingestion()


if __name__ == "__main__":
    run()
