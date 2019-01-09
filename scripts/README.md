## QC of AD-Data

Three QC's are added. There are in total 148*148 connections in each connectome(subject). Each QC finds the number of outlier connections among these connections.
If this number exceeds a certain limit, the connectome is marked as an outlier subject. The definition of a outlier connection is different for each QC.

### QC1:
1. Computes mean and standard deviation for every connections across subjects.
2. For every subject compute how many standard deviation away it's connections are from the mean.
3. A connection is marked as an outlier if it is more than 2 standard deviation away from the mean.
4. If a subject has more than 10% outlier connection (outlier percentage) of the total connections then it is marked as an outlier.
5. Result: No outlier subject found.

### QC2:
First two steps are same as QC1

3. Computes average standard deviation for each connections across subjects.
4. If the standard deviation for a connection is 4 times more than the average, it is marked as an outlier connection.
5. If a subject has more than 10% outlier connection (outlier percentage) of the total connections then it is marked as an outlier.
6. Result: No outlier subject found.

### QC3:
1. Find the mean of the connectomes.
2. Binarize the mean and all the other connectomes.
3. Compare every connectome with the mean.
4. If a subject has more than 30% mismatch (outlier percentage), it is marked as outlier.
5. Result: 58 outlier found.

### Plot:
Plot for three QC's.  
xAxis -> acceptable percentage of outlier connections for a subject (outlier percentage).  
yAxis -> Number of outlier subjects.  

![QC Plot](https://github.com/mturja-vf-ic-bd/Tractography_ADNI/blob/master/scripts/qc.png)
