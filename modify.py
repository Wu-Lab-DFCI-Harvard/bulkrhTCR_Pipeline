import os 
import pandas as pd
import argparse
import numpy as np
from update_umi import update_UMI
from merge import merge
from generate_report import sum_over 
from generate_report import simplify_report

def readCSV(df): 
    data = pd.read_csv(df, sep='\t')
    return data

#Remove Unnecessary Columns 
def remove_columns(df,column_names):
    columns_to_drop = column_names
    columns = [col for col in df.columns if any(substring in col for substring in columns_to_drop)]
    df = df.drop(columns, axis=1)
    return df

#Unifying Gene Name For Convention
def gene_name(df):
    #Helper Function
    def get_unique_items(entry):
        items = entry.split(',')  # Split the entry into individual items
        cleaned_items = [item for item in items if not item == 'nan']
        return ','.join(set(cleaned_items))
    vGene = df.filter(like='bestVGene').columns.tolist()
    jGene = df.filter(like='bestJGene').columns.tolist()
    v_jGene = vGene + jGene
    for column in v_jGene:
        df[column] = df[column].astype(str)
    df['vGene'] = df[vGene].apply(lambda row: ','.join(row), axis=1)
    df['jGene'] = df[jGene].apply(lambda row: ','.join(row), axis=1)
    # Replace with the name of the column you want to process
    df['vGene'] = df['vGene'].apply(get_unique_items)
    df['jGene'] = df['jGene'].apply(get_unique_items)
    return df;

def merge_umi_lists(df):
    #merge UMI Lists between samples 
    def merge_dicts(row):
        merged_dict = {}
        for col_name,col_value in row.iteritems():
            if 'updatedTagCounts' in col_name:
                merged_dict.update(col_value)
        return merged_dict
    selected_columns = df.filter(like='updatedTagCounts')
    df['UMI_Lists'] = selected_columns.apply(merge_dicts, axis=1)
    df = df.drop(selected_columns,axis=1)
    return df

def main():
    parser = argparse.ArgumentParser(description="Edit MiXCR Output Files")

    parser.add_argument("--TRA",
                        dest="TRA",
                        type=str,
                        help="path to the TRA report file")
    
    parser.add_argument("--TRB",
                        dest="TRB",
                        type=str,
                        help="path to the TRB report file")

    parser.add_argument("--out_dir",
                        dest="out_dir",
                        type=str,
                        help="path to the output directory")
    parser.add_argument("--basename",
                        dest="basename",
		        type=str,
			help="name of the sample")

    args = parser.parse_args()

    TRA = args.TRA
    TRB = args.TRB
    out_dir = args.out_dir
    basename = args.basename
	
    #read in files 
    TRA = readCSV(TRA)
    TRB = readCSV(TRB)

    #drop unnecessary columns (readCount columns -> we want UMI counts)
    TRA = remove_columns(TRA,['read'])
    TRB = remove_columns(TRB,['read'])    

    #get unified gene names. 
    TRA = gene_name(TRA)
    TRB = gene_name(TRB)   

    #delete single read supported UMIs 
    TRA = update_UMI(TRA)
    TRB = update_UMI(TRB) 

    #remove another set of columns used for UMI merges 
    TRA = remove_columns(TRA,['tagCounts','bestVGene','bestJGene','remove_count','uniqueUMIFractionAggregated','nSamples'])
    TRB = remove_columns(TRB,['tagCounts','bestVGene','bestJGene','remove_count','uniqueUMIFractionAggregated','nSamples'])   

    #Merge TRBV genes
    TRA = merge(TRA)
    TRB = merge(TRB)

    #Merge UMI Lists Over Replicates to Obtain a Representative UMI Lists 
    TRA = merge_umi_lists(TRA)
    TRB = merge_umi_lists(TRB)

    #get total counts of UMIs 
    TRA = sum_over(TRA)
    TRB = sum_over(TRB)

    #Generate a final report
    TRA.to_csv(os.path.join(out_dir,basename + '_TRA_report.tsv'), sep = '\t')
    TRB.to_csv(os.path.join(out_dir,basename + '_TRB_report.tsv'), sep = '\t')

    #Simplify a Report
    TRA = simplify_report(TRA)
    TRB = simplify_report(TRB)

    TRA.to_csv(os.path.join(out_dir,basename + 'Condensed_TRA_report.tsv'), sep = '\t')
    TRB.to_csv(os.path.join(out_dir,basename + 'Condensed_TRB_report.tsv'), sep = '\t')

if __name__ == "__main__": main()