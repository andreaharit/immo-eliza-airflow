import click
import pandas as pd

@click.command()
@click.option("--raw_dated_csv", help="Path to the raw CSV")
@click.option("--raw_merged_csv", help="Path to save the scrapped links CSV")
def merge_csv(raw_dated_csv, raw_merged_csv):
    print("got inside merging")
    df_original = pd.read_csv(raw_dated_csv) 
    df_additional =  pd.read_csv(raw_merged_csv) 
    df_merged = pd.concat([df_original,df_additional]).drop_duplicates().reset_index(drop=True)
    df_merged.to_csv(raw_merged_csv, encoding='utf-8', header='true',index=False)
    print("after merging")

if __name__ == "__main__":
    merge_csv()