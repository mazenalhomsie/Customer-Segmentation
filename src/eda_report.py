import pandas as pd
import glob
import os

def analyze_csvs(data_dir='data'):
    files = glob.glob(os.path.join(data_dir, '*_sample.csv'))
    
    for file in files:
        print(f"\nAnalyzing: {os.path.basename(file)}")
        df = pd.read_csv(file)
        
        print(f"Shape: {df.shape}")
        print("\nColumn Info:")
        print(df.info())
        
        print("\nMissing Values:")
        print(df.isnull().sum())
        
        print("\nHead:")
        print(df.head(3))
        
        print("\nUnique Values (Categorical):")
        for col in df.select_dtypes(include='object').columns:
            print(f"{col}: {df[col].nunique()} unique")
            if df[col].nunique() < 10:
                print(f"   Values: {df[col].unique()}")

if __name__ == "__main__":
    analyze_csvs()
