# Postprocessing_Script

This is the post-processing script for bulkrhTCR protocol. 
This script was written and tested in

```
Python v3.9
Numpy v1.20.1
Panda v1.2.3
```

## Main Script 

```
Parameters 

--TRA: TRA chain report from exportClonesOverlap 
--TRB: TRB chain report from exportClonesOverlap 
--out_dir: Output directory
--basename: 

merge.py --TRA TRA_Report --TRB TRB_Report --out_dir output_directory --basename test

Output:

output_directory/test_TRA_report.tsv
output_directory/test_TRB_report.tsv

output_directory/testCondensed_TRA_report.tsv
output_directory/testCondensed_TRB_report.tsv

```
