import pandas as pd
import json

try:
    df = pd.read_excel('population.xlsx', header=0)
    print("Columns (Header 0):", list(df.columns)[:5])
    df2 = pd.read_excel('population.xlsx', header=1)
    print("Columns (Header 1):", list(df2.columns)[:5])
    df3 = pd.read_excel('population.xlsx', header=2)
    print("Columns (Header 2):", list(df3.columns)[:5])
    df4 = pd.read_excel('population.xlsx', header=3)
    print("Columns (Header 3):", list(df4.columns)[:5])
    print("Data sample:")
    for col in df4.columns[:6]:
        print(f"  {col}: {df4[col].iloc[0]}")
except Exception as e:
    print(f"Error: {e}")
