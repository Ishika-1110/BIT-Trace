\# BIT-TRACE — Bitcoin P2P Anomaly Detection



This module contains the machine-learning pipeline developed for the

BIT-TRACE project to analyze historical Bitcoin P2P network observations

and identify unusual peer behavior.



\## Overview



The model analyzes peer-level behavioral features extracted from the

Bitcoin P2P crawler dataset.



The pipeline includes:



1\. P2P observation normalization

2\. Peer-level feature engineering

3\. Temporal activity analysis

4\. Network endpoint and service behavior analysis

5\. Isolation Forest anomaly detection

6\. Explainable anomaly reason codes

7\. Temporal holdout evaluation

8\. Reproducibility validation



The historical P2P dataset is used as a behavioral reference dataset.

It does not contain verified malicious/anomalous ground-truth labels.

Therefore, conventional classification accuracy, precision, recall,

F1-score, ROC-AUC, and PR-AUC are not reported for this branch.



\## Model



Algorithm:



\- Isolation Forest

\- 300 estimators

\- `contamination="auto"`

\- `random\\\_state=42`



The final model uses 28 numerical features.



\### Feature groups



\- Observation activity

\- Temporal persistence

\- Port diversity

\- Service diversity

\- Non-default port behavior

\- Reported block-height deviation

\- Hourly activity

\- Daily activity

\- Burst behavior

\- Activity variability



\## Preprocessing



The inference pipeline applies the same major preprocessing used during

model development:



\- Numeric feature validation

\- Missing/infinite-value handling

\- `log1p` transformation for selected non-negative skewed features

\- StandardScaler transformation

\- Isolation Forest scoring



The anomaly score is defined as:



```text

anomaly\\\_score = -IsolationForest.decision\\\_function(X)


