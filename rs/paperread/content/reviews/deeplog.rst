---
title: "DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning"
date: 2018-09-11T06:39:50Z
---

kw: intrusion/anomaly detection, LSTM.

Abstract
--------

1. deep log, a deep neural network model utilizing long short-term memory
   to model a system log as a netural language sequence.

2. incrementally update the deeplog model in an online fashion so that
   it can adapt to new log patterns over time.

3. deeplog has outperformed other existing log-based anomaly detection
   methods based on traditional data mining methodologies.

Introduction
------------

4. existing approaches: (1) PCA based approaches over log message counters.
   (2) invariant mining based methods to capture co-occurrence patterns
   between different log keys. (3) workflow based methods to identify
   execution anomalies in program logic flaws.

5. challenges: log data are unstructured, and their format and semantics
   can vary significantly from system to system.

6. some existing methods use rule-based appraoches to address this issue,
   which requires specific domain knowledge, e.g. using features like
   "ip address" to parse a log. However, this does not work for general
   purpose anomaly detection where it is almost impossible to know
   a priori what are interesting features in different types of logs.
   (and to gurad against different types of attacks).

7. Anomaly detection has to be timely in order to be useful so that users
   can intervene in an ongoing attack or a system performance issue.
   Decisions are to be made in streaming feashion. As a result, offline
   methods that need to make several passes over the entire log data are
   not applicable in our setting.

8. previous work that use both normal and abnormal log data entires to
   train a binary classifier for anomaly detection is not useful in this
   context.

9. deeplog can be updated online according to user feedback.

Preliminaries
-------------

1. the state-of-the-art log parsing method is represented by spell, an
   unsupervised streaming parser that parses incoming log entires in an
   online fashion based on the idea of LCS (longest common subsequence).

Anomaly Detection
-----------------

1. we can model anomaly detection in a log key sequence as a multi-class
   classification problem, where each distinct log key defines a class.
   We train deeplog as a multi-class classifier over recent context. The
   input is a histroy of recent log keys, and the output is a probability
   distribution over the n log keys from K, representing the probability
   that the next log key in the sequence is a key :math:`k_i \in K`.

2. in practice, multiple log key values may appear as the next log entry.
   Our strategy is to sort the possible log keys K based on their
   probabilities :math:`Pr[m_t|w]`, and treat a key value as normal if
   it's among the top :math:`g` candidates. A log key is flagged as being
   from an abnormal execution otherwise.

Oneline update of anomaly detection models
------------------------------------------

Note that deeplog does not need to be re-trained from scratch. After the
initial training process, models in deeplog exist as several
multi-dimensional weight vectors. The update process feeds in new training
data, and adjucsts the weights to minimize the error between model output
and actual observed values from the false positive cases.

Conclusion
----------

Deeplog learns and encodes entire log message including timestamp,
log key, and parameter values. It performs anomaly detection at per
log entry level, rather than at per session level as many previous
methods are limited to.
