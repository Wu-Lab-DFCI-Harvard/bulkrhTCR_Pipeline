import os 
import pandas as pd
import argparse
import numpy as np
import math

def get_fraction(num,totalUMIs):
    return num/totalUMIs;
def calculate_simpson(UMI_Counts):
    return UMI_Counts ** 2

#sum over trimmed lists of UMIs
def sum_over(df):
    df['totalUMICount'] = df.filter(like='uniqueUMICountAggregated').sum(axis=1)
    totalUMIs=df['totalUMICount'].sum()
    df['Freq']=df['totalUMICount'].apply(get_fraction, totalUMIs=totalUMIs)
    umicount_columns = [col for col in df.columns if 'uniqueUMICountAggregated' in col]
    is_bigger_than_zero = df[umicount_columns] > 0
    df['replicate_frequency'] = is_bigger_than_zero.sum(axis=1)
    df = df.sort_values(by='totalUMICount',ascending=False)
    df.reset_index(drop=True, inplace=True)
    df.loc[0,'Total_UMI_Over_Replicates'] = totalUMIs
    df.loc[0,'Unique_Clonotypes'] = len(df)
    df = df.fillna('')
    return df

#Generate a condensed report for a biological sample
def simplify_report(df):
    data = df.copy()
    for column_name in df.columns:
        if 'uniqueUMICountAggregated' in column_name:
            sample_name = column_name.split('_')[0]
    #default_values
    fraction = data['totalUMICount']/sum(data['totalUMICount'])
    data['sample'] = sample_name
    data['ng_RNA_used'] = 80
    data['Simpson_Clonality'] = math.sqrt(sum((fraction) ** 2))
    data['Total_UMI_Over_Replicates'] = data['Total_UMI_Over_Replicates'][0]
    data['Unique_Clonotypes'] = data['Unique_Clonotypes'][0]
    columns_to_drop = ['uniqueUMICountAggregated','UMI_Lists', 'replicate_frequency']
    columns = [col for col in data.columns if any(substring in col for substring in columns_to_drop)]
    data = data.drop(columns, axis=1)
    return data
