import pandas as pd
import numpy as np
from pathlib import Path

def generate(start='2019-01-01', periods=72, seed=42, out='sample_sales.csv'):
    np.random.seed(seed)
    idx = pd.date_range(start=start, periods=periods, freq='MS')
    # Seasonal pattern + trend + noise
    trend = np.linspace(1000, 5000, periods)
    seasonal = 300 * np.sin(2 * np.pi * (np.arange(periods) % 12) / 12)
    noise = np.random.normal(0, 200, periods)
    sales = trend + seasonal + noise
    sales = np.maximum(0, sales)
    df = pd.DataFrame({'date': idx, 'amount': sales.round(2)})
    df.to_csv(out, index=False)
    print(f"Generated {out} with {periods} rows")

if __name__ == '__main__':
    generate()