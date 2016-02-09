Generate test data set with R
-----

`R CMD BATCH makeWeight.R`

Run python scripts
-----

### Look for out-of-bounds values to produce Data2.csv and Recoverable2.csv

`python checkWeight.py Data1.csv StrataIDs.csv StrataExternalBounds.csv Data2.csv`

### Create pairwise value differences

`python deltaWeight.py Data2.csv PairDiffs.csv`

#### Argument to restrict to closest 10 timepoints

`python deltaWeight.py Data2.csv PairDiffs_T10.csv -t 10`

#### Argument to restrict to timepoints within 180 days

`python deltaWeight.py Data2.csv PairDiffs_S180.csv -s 180`

TODO
-----

1. Clean raw data to produce Data1.csv and Recoverable1.csv
1. Analyze PairDiffs.csv to produce StrataInternalBounds.csv
1. Aggregate probable/questionable/improbable counts at the ValueID level
1. Filter to create Data3.csv and Recoverable3.csv
1. Attempt to recover values from Recoverable 1/2/3
