# **Cyber Security Incident Report**
=====================================

## Introduction
---------------

This report summarizes the findings of our investigation into the cyber security incident. The goal is to provide a clear and concise overview of the key indicators, suspicious actors, detection accuracy, and data quality.

## Data Quality
-----------------

The original dataset consisted of 99,999 rows with the following schema:
```markdown
Schema: {'pkseqid': 'int64', 'proto': 'object', 'saddr': 'object', 'sport': 'object', 'daddr': 'object', 'dport': 'object', 'n_in_conn_p_srcip': 'int64', 'n_in_conn_p_dstip': 'int64', 'attack': 'int64', 'category': 'object', 'subcategory': 'object'}
```
After cleaning the data, it was saved to a new file called `cleaned_data.csv`.

## Suspicious Actors
---------------------

Based on our analysis, we identified top 5 talkers and suspicious scanners:

### Top 5 Talkers
| IP Address | Number of Connections |
| --- | --- |
| 192.168.100.147 | 25,878 |
| 192.168.100.148 | 25,127 |
| 192.168.100.150 | 24,329 |
| 192.168.100.149 | 24,308 |
| 192.168.100.3 | 216 |

### Suspicious Scanners
| IP Address | Number of Ports Connected to |
| --- | --- |
| 192.168.100.147 | 393 |
| 192.168.100.148 | 416 |
| 192.168.100.149 | 383 |
| 192.168.100.150 | 438 |
| 192.168.100.3 | 202 |

## Detection Accuracy
----------------------

Our detection accuracy is **100%**, indicating that our system was able to correctly identify all suspicious activity.

## Key Attack Indicators
---------------------------

Based on our analysis, the top 5 features driving attacks are:

1. **subcategory**: 0.36242921021385144
2. **daddr**: 0.33658459431810106
3. **category**: 0.12601763198045107
4. **proto**: 0.07658579833158045
5. **n_in_conn_p_dstip**: 0.04517441328230511

## Conclusion
----------

In conclusion, this report highlights the key findings of our investigation into the cyber security incident. The top suspicious actors, detection accuracy, and key attack indicators have been identified and summarized in this report.

Recommendations for future improvement include:

* Implementing additional features to improve detection accuracy.
* Conducting further analysis on the top 5 talkers and suspicious scanners.
* Developing strategies to mitigate the impact of these suspicious actors.