import pandas as pd

def load_and_prepare_data(path):
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Ensure label exists
    if 'label' not in df.columns:
        raise Exception("❌ 'label' column not found in dataset")

    # Drop non-numeric / unnecessary columns
    drop_cols = ['url', 'filename', 'domain', 'title', 'tld']
    drop_cols = [col for col in drop_cols if col in df.columns]

    X = df.drop(columns=drop_cols + ['label'])
    y = df['label']

    return X, y