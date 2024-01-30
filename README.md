# MIXCR Workflow

Step 1 Running MiXCR 

```

mixcr analyze generic-amplicon-with-umi \
        --species hsa \
        --assemble-clonotypes-by CDR3 \
        --export-productive-clones-only \
        --rna \
        -f \
        --tag-pattern '^(R1:*)\(UMI:N{7})(R2:*)' \
        -Massemble.consensusAssemblerParameters=null \
        -Massemble.cloneAssemblerParameters.addReadsCountOnClustering=true \
        --floating-left-alignment-boundary \
        --floating-right-alignment-boundary C \
        R1_file \
        R2_file \
        out_dir \


```

Step 2 Filtering for non-functional CDR3 Sequence 

```
mixcr exportClones \
    --export-productive-clones-only \
    --filter-stops \
    --filter-out-of-frames \
    -tagCounts \
    Rep1.clns 
    Rep1.tsv

```

Step 3 Generating consensus clonotypes for a biological sample  

```

mixcr exportClonesOverlap \
    -tagCounts \ 
    -vGene \
    -jGene \ 
    --criteria "CDR3|AA|V|J" \
    Rep1.clns Rep2.clns Rep3.clns Rep4.clns \
    final_TCR_report.tsv
    
```

# Post-Processing Script

This is the post-processing script for bulkrhTCR protocol. 
This script was written and tested in

```
python v3.9
numpy v1.20.1
panda v1.2.3
```
All scripts must be in same directory for the main script to function properly. 

## Scripts

### Main Script 

_modify.py:_ Main Script. Takes in TRA and TRB reports generated from MiXCR's exportClonesOverlap function. Outputs final report to a specified output directory. 

### Util Scripts 

_merge.py:_ Script to merge TRBV genes and cluster clonotypes based on J gene segments and CDR3 sequences

_update_umi.py:_ Script to remove UMIs with only one read count and remove clonotypes with no supporting UMIs

_generate_report.py:_ Script to generate a final report with UMI counts for each clonotypes 

```
Parameters 

--TRA: TRA chain report from exportClonesOverlap 
--TRB: TRB chain report from exportClonesOverlap 
--out_dir: Output directory
--basename: 

modify.py --TRA TRA_Report --TRB TRB_Report --out_dir output_directory --basename test

Output:

output_directory/test_TRA_report.tsv
output_directory/test_TRB_report.tsv

output_directory/testCondensed_TRA_report.tsv
output_directory/testCondensed_TRB_report.tsv

```

# Final Output Examples 

## TRA/TRB_report.tsv File Example

Columns: aaSeqCDR3, vGene, jGene, Sample1, Sample2, Sample3, Sample4, UMI_Lists, totalUMICount, Freq, replicate_frequency, Total_UMI_Over_Replicates, Unique_Clonotypes

<img width="1061" alt="Screenshot 2023-12-29 at 1 20 24 PM" src="https://github.com/Wu-Lab-DFCI-Harvard/bulkrhTCR_Script/assets/53489568/34861e70-7681-484f-8d86-3c253140e08b">

## CondensedTRA/TRB_report.tsv File Example 

Columns: aaSeqCDR3, vGene, jGene, totalUMICount, Freq, Total_UMI_Over_Replicates, Unique_Clonotypes, sampleng_RNA_used, Simpson_Clonality

<img width="1057" alt="Screenshot 2023-12-29 at 1 52 12 PM" src="https://github.com/Wu-Lab-DFCI-Harvard/bulkrhTCR_Script/assets/53489568/d4608d99-06ae-4365-817b-cefbce721f7b">



