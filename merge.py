import os 
import pandas as pd
import argparse
import numpy as np

#Merge TRBV genes based on primer location 
def mergeTRB(vGene): 
    if vGene in ["TRBV6-2", "TRBV6-3", "TRBV6-5", "TRBV6-6"]:
        return "TRBV6-2/3/5/6"
    elif vGene in ["TRBV12-3", "TRBV12-4"]:
        return "TRBV12-3/4"
    else:
        return vGene

def sum_grouped_rows(group):
    return group.sum()

#Merge UMI lists when clustered
def merge_dicts_for_group(row1, row2):
    result = row1.copy()
    for i in range(len(row1)):
        if not result[i] and not row2[i]: 
            result[i] = {}
        else:
            for key, value in row2[i].items():
                if key in result[i]:
                    result[i][key] += value
                else:
                    result[i][key] = value
    return result

#Count UMI lists except for UMI with one read count
def count_keys_except_count(dict, count):
    count = count.copy()
    for i in range(len(dict)):
        count_UMI = 0; 
        for key, value in dict[i].items():
            if key != 'count':
                count_UMI = count_UMI + 1
        
        count[i] = count_UMI; 
    return count


def merge(TRB):
    #Main Merge Script
    CDR3_J_dict = dict() 
    TRB['vGene'] = TRB['vGene'].apply(mergeTRB)
    column_names = TRB.columns
    TRB_copy=TRB
    TRB = TRB.to_numpy()
    list = []
    counter = 0
    #Generating J and CDR3 Dictionary
    for row in TRB:
        if ((row[0], row[2])) not in CDR3_J_dict:
            CDR3_J_dict[(row[0], row[2])] = [counter] 
        else:
            CDR3_J_dict[(row[0], row[2])].append(counter)
        counter = counter + 1
    
    # Get the index of the TagCounts column, and UniqueUMICounts column for each replicate
    filtered_columns = TRB_copy.filter(like='updatedTagCounts', axis=1)
    UMI_Columns = TRB_copy.filter(like='uniqueUMICount', axis=1)
    tag_indices = [TRB_copy.columns.get_loc(col) for col in filtered_columns.columns]
    UMI_indices = [TRB_copy.columns.get_loc(col) for col in UMI_Columns.columns]

    for key in CDR3_J_dict:
        #if there are multiple clonotypes with same J gene and CDR3 sequence
        if len(CDR3_J_dict[key])>1:
            maxSum = 0
            maxIndex = 0
            index = CDR3_J_dict[key]
            copy = TRB[int(index[0])].copy()
            for i in range(len(index)):
                new = TRB[int(index[i])][UMI_indices].sum()
                if not ((i+1) == len(index)):
                    copy[tag_indices] = merge_dicts_for_group(TRB[int(index[i+1])][tag_indices], copy[tag_indices])
                if new > maxSum: 
                    maxIndex = index[i]
                    maxSum = new; 
            TRB[int(maxIndex)][tag_indices] = copy[tag_indices]
            TRB[int(maxIndex)][UMI_indices] = count_keys_except_count(TRB[int(maxIndex)][tag_indices], TRB[int(maxIndex)][UMI_indices])
            for i in index:
                if i != maxIndex:
                    list.append(i)
    TRB = np.delete(TRB,list, axis=0)
    TRB = pd.DataFrame(TRB, columns=column_names)
    return TRB