# Postprocessing_Script

This is the post-processing script for bulkrhTCR protocol. 
This script was written and tested in

```
Python v3.9
Numpy v1.20.1
Panda v1.2.3
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
