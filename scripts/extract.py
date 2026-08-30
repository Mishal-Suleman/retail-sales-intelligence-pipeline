"""
extract.py

Stage: RAW INGESTION

What this script does:
1. Reads both sheets from the raw Online Retail II file, exactly as downloaded.
2. Combines them into a single dataframe. No cleaning happens here, that is
   transform.py's job.
3. Applies the sampling decision from requirements.md (~80k rows, stratified by
   month). This is a scope decision, not a data quality fix, so it belongs at
   ingestion time, and it is logged clearly so this sampled file is never
   mistaken for the full dataset later.
4. Saves the result to data/processed/ and logs everything that happened.

Why sampling happens here and not in transform.py:
Sampling decides WHICH rows exist in the working dataset. Transform.py's job is
to clean the rows that ARE there (nulls, types, duplicates). Mixing "which rows
do we keep" with "how do we clean rows" makes the pipeline harder to reason
about later. Keeping them separate means anyone reading this repo can look at
extract.py alone and know exactly how the working dataset was chosen, without
digging through cleaning logic to find it.
"""

import pandas as pd
from pathlib import Path
from logger_config import get_logger

logger = get_logger("extract")

RAW_FILE = Path(__file__).resolve().parent.parent / "data" / "raw" / "online_retail_II.xlsx"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "01_combined_sampled.csv"
SHEET_NAMES = ["Year 2009-2010", "Year 2010-2011"]
DATE_COLUMN = "InvoiceDate"
TARGET_SAMPLE_SIZE = 80_000
RANDOM_SEED = 42  # fixed seed so the sample is reproducible; anyone rerunning this gets the same rows


def load_raw_sheets(path: Path) -> pd.DataFrame:
    logger.info(f"Starting raw ingestion from {path}")

    if not path.exists():
        logger.error(f"Raw file not found at {path}")
        raise FileNotFoundError(
            f"Expected raw file at {path}, but it does not exist. "
            f"Download the dataset and place it in data/raw/ with this exact filename, "
            f"or update RAW_FILE above to match what you actually named it."
        )

    frames = []
    for sheet in SHEET_NAMES:
        df = pd.read_excel(path, sheet_name=sheet)
        logger.info(f"Read sheet '{sheet}': {len(df):,} rows, {len(df.columns)} columns")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    logger.info(f"Combined both sheets: {len(combined):,} total rows")
    return combined


def stratified_sample_by_month(df: pd.DataFrame, date_col: str, target_size: int, seed: int) -> pd.DataFrame:
    df = df.copy()
    df["_year_month"] = pd.to_datetime(df[date_col]).dt.to_period("M")

    total_rows = len(df)
    fraction = target_size / total_rows
    logger.info(f"Sampling fraction: {fraction:.4f} (target {target_size:,} of {total_rows:,} rows)")

    sampled = (
        df.groupby("_year_month", group_keys=False)
        .apply(lambda x: x.sample(frac=fraction, random_state=seed))
    )
    sampled = sampled.drop(columns=["_year_month"])

    logger.info(f"Sampled result: {len(sampled):,} rows across {df['_year_month'].nunique()} months")
    return sampled


def main():
    logger.info("=" * 60)
    logger.info("EXTRACT STAGE STARTED")

    combined = load_raw_sheets(RAW_FILE)
    sampled = stratified_sample_by_month(
        combined, date_col=DATE_COLUMN, target_size=TARGET_SAMPLE_SIZE, seed=RANDOM_SEED
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    sampled.to_csv(OUTPUT_FILE, index=False)
    logger.info(f"Saved sampled dataset to {OUTPUT_FILE} ({len(sampled):,} rows)")

    logger.info("EXTRACT STAGE COMPLETE")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
