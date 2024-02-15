# MIXCR Workflow

<img width="1017" alt="Screenshot 2024-01-30 at 5 15 42 PM" src="https://github.com/Wu-Lab-DFCI-Harvard/bulkrhTCR_Script/assets/53489568/e2aa862c-29b5-4712-9515-8c07db6fa1de">

## Downloading MiXCR 

MiXCR Version Used: v4.4.2
Please install 4.4.0 or greater. Functionalities in this script will not be available in MiXCR version lower than v4.4.0. 

Pull MiXCR from the mixcr milaboratory repo
> wget https://github.com/milaboratory/mixcr/releases/download/v4.4.2/mixcr-4.4.2.zip

Unpack MiXCR Package
> unzip mixcr-4.4.2.zip

Check that MiXCR works 
> ~/mixcr/mixcr -v

LICENSING Key can be obtained here: https://licensing.milaboratories.com 

MiXCR License can be activated by,

> mixcr activate-license _**key**_

or 

mi.license file with the _**key**_ in the mixcr directory


## Step 1. Running MiXCR 

```
> mixcr analyze generic-amplicon-with-umi \
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
        R1.fastq \
        R2.fastq \
        path/out_dir \

```




Outputs (for each replicate):

Rep1_TRAD.tsv, Rep1_TRB.tsv, Rep1.clns, Rep1.vdjca, Rep1.align.txt, Rep1.assemble.txt, Rep1.refine.txt


## Step 2. Generating consensus clonotypes for a biological sample  

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


# Visualize number of unique clonotypes for TRA and TRB vGenes

```
Parameters

arg1: TRA final report
arg2: TRB final report
arg3: output directory
arg4: Sample Name 

Rscript visualize_clonotype_counts.R TRA_report.tsv TRB_report.tsv output_directory test
```
## Outputs 

![11-C1D1_TRAV](https://github.com/Wu-Lab-DFCI-Harvard/bulkrhTCR_Script/assets/53489568/b7da34fc-246d-4bd0-b2ee-0294dd72a1c7)
![11-C1D1_TRBV](https://github.com/Wu-Lab-DFCI-Harvard/bulkrhTCR_Script/assets/53489568/3b17f185-314b-4062-927e-faf6badcafa0)



