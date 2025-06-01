import os
import pandas as pd
from pathlib import Path
from src.fingpt_agents.utils.logger_utils import logger

class DataProcessingAgent:
    def __init__(self, input_dir="data/processed/", output_dir="data/processed_data/"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("[INIT] DataProcessingAgent initialized.")
    
    def load_data(self):
        # Load all CSV files from input_dir
        csv_files = list(Path(self.input_dir).glob("*.csv"))
        if not csv_files:
            logger.warning(f"[WARN] No CSV files found in {self.input_dir}")
            return {}

        dataframes = {}
        for file in csv_files:
            df = pd.read_csv(file, index_col=0, parse_dates=True)
            dataframes[file.stem] = df
            logger.info(f"[LOAD] Loaded {file.name} with {len(df)} rows.")
        return dataframes
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Fill missing values with forward fill, then backward fill as fallback
        missing_before = df.isnull().sum().sum()
        df_clean = df.ffill().bfill()
        missing_after = df_clean.isnull().sum().sum()

        logger.info(f"[CLEAN] Missing values before: {missing_before}, after: {missing_after}")

        # Example feature: daily returns per stock (if 'Close' column exists)
        close_cols = [col for col in df_clean.columns if col.lower().startswith("close")]
        for col in close_cols:
            ret_col = col.replace("Close", "Return")
            df_clean[ret_col] = df_clean[col].pct_change()
            logger.info(f"[FEATURE] Added returns column: {ret_col}")

        # Drop initial row with NaN returns
        df_clean.dropna(inplace=True)
        logger.info(f"[CLEAN] Dropped rows with NaNs after feature engineering. Rows now: {len(df_clean)}")

        return df_clean

    def save_processed(self, dataframes):
        for name, df in dataframes.items():
            file_path = Path(self.output_dir) / f"{name}_processed.csv"
            df.to_csv(file_path)
            logger.info(f"[SAVE] Saved processed data to {file_path}")

    def run(self):
        logger.info("[RUN] Starting data processing pipeline.")
        dataframes = self.load_data()
        if not dataframes:
            logger.error("[ERROR] No data to process. Exiting.")
            return
        
        processed_dfs = {}
        for name, df in dataframes.items():
            logger.info(f"[PROCESS] Processing {name}...")
            processed_dfs[name] = self.clean_data(df)

        self.save_processed(processed_dfs)
        logger.info("[DONE] Data processing complete.")
