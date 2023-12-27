import os 
import pandas as pd
import argparse
import numpy as np

#filters out UMI that are supported by reads = 1
def string_to_dict(input_string):
    my_dict = {}
    count = 0
    if isinstance(input_string, str): 
        cleaned_string = input_string.replace('{', '').replace('}', '')
        items = cleaned_string.split(',')
        for item in items:
            if ':' in item:
                key,value = item.split(':')
            else:
                key,value = item.split('=')
            if float(value) < 2.0: 
                count = count + 1; 
                my_dict['count'] = count
            else:
                my_dict[key] = float(value)  # Convert value to float if necessarys
    return my_dict

def count_column(input):
    if not input:
        return 0
    else:
        if 'count' in input:
            return input['count'] 
        else:
            return 0;

#removes UMI then updates the count of uniqueUMI for each sample 
def update_UMI(df):
    for column_name in df.columns:
        if 'tagCounts' in column_name:
            new_column_name = column_name.replace('tagCounts', 'updatedTagCounts')
            df[new_column_name] = df[column_name].apply(string_to_dict)
            df['remove_count'] = df[new_column_name].apply(count_column)
            basename = column_name.split('tagCounts')[0].rstrip('_')
            UMI = basename + '_uniqueUMICountAggregated'
            df[UMI] = df[UMI] - df['remove_count']

    umicount_columns = [col for col in df.columns if 'uniqueUMICountAggregated' in col]
    is_bigger_than_zero = df[umicount_columns] > 0
    df['nSamples'] = is_bigger_than_zero.sum(axis=1)
    df = df[df['nSamples'] != 0]
    df = df.reset_index(drop=True)
    return df 