% Practical Methodology in Deep Learning
% Hakase. Hana
% Aug 23, 2017

Practical Methodology in Deep Learning
===

*It is important to be able to determine the right course of action rather
than blindly guessing.*

The following practival design process is recommended:

1. Determine your goals, i.e. the metrics.

2. Establish a working end-to-end pipeline as soon as possible,
including the estimation of the appropriate performance metrics.

3. Instrument the system well to determine bottlenecks in performance.

4. Repeatedly make increamental changes based on specifig findings from your
instrumentation.


Performance Metrics
===

Your error metrix will guide all of you future actions.

Default Baseline Models
===

* Choose the general category of model based on the structure of your data.
If the input is fixed-size vectors, use a feedforward network. If the input
is a sequence, use a gated recurrent network (e.g. LSTM or GRU).

* A reasonable choice of optimization algorighm is SGD with momentum with
a decaying learning rate. A verya reasonable alternative is Adam.

* Unless your training set contains tens of millions of examples or more,
you should include some mild forms of regularization from the start.
For example, Early Stopping, Dropout, and Batch Normalization.

Determining Whether to Gather More Data
===

* If test set performance is much worse than training set performance, then
gathering more data is one of the most effictive solutions.

* A simple alternative to gathering more data is to reduce the size of the
model or improve regularization, by adjusting hyperparameters such as weight
decay coefficients, or by adding regularization strategies such as dropout.

Selecting Hyperparameters
===

There are two basic approaches to choosing these hyperparameters: choosing
them manually and choosing them automatically. Choosing the hyperparameters
manually requires understanding what the hyperparameters do and how machine
learning models achieve good generalization.

---

Manual selection
---

The primary goal of manual hyperparameter search is to adjest the effective
capacity of the model to match the complexity of the task. A model with more
layers and more hidden units per layer has higher representational capacity
-- it is capable of representing more complicated functions.

The generalization error typically follows a U-shaped curve when plotted
as a function of one of the hyperparameters. For some hyperparameters,
oerfitting occurs when the value of the hyperparameter is large. However,
not every hyperparameter will be able to explore the entire U-shaped curve. 

---

The learning rate is perhaps the most important hyperparameter.
---

The effective capacity of the model is highest when the learning rate is
correct for the optimization problem, not when the learning rate is especially
large or especially small. The learning rate has a U-shaped curve for training
error.

* When the learning rate is too large, gradient descent can inadvertently
increase rather than decrease the training error.

* When the learning rate is too small, training is not only slower, but may
become permanently stuck with a high trianing error.

This effect is poorly understood.

---

Other than the learning rate
---

Tuning the parameters other than the learning rate requires monitoring both
trianing and test error to diagnose whether your model is overfitting or
underfitting, then adjesting its capacity apprpopriately.

* If your error on the training set is higher than your target error rate,
you have no choice but to increase capacity.

* If your error on the test set is higher than your target error rate,
to reduce the gap between train and test error, change regularization
hyperparameters to reduce effective model capacity, such as by adding
Dropout or weight decay.

* Most hyperparameters can be set by reasoning about whether they increase
or decreasee model capacity.


Debugging Strategies
===

When a machine learning systen performs poorly, it is usually difficult to
tell whether the poor performance is intrinsic to the algorighm itself or
wether there is a bug in the implementation of the algorithm. Furthermore,
most machine learning models have multiple parts that are each adaptive. If
one part is broken, the other parts can adapt and still achieve roughly
acceptable performance.

Most debugging strategies for neural nets are desgined to get around one
or both of these two difficulties. Either we design a case that is so simple
that the correct behavior actually can be predicted, or we design a test that
exercises one part of the neural network implementation in isolation.

---

Important Debugging Tests
---

* **Visualize the modelin action**:

* **Visualize the worst mistakes**:

* **Reasoning about software using train and test error**:

* **Fit a tiny dataset**:

* **Compare back-propagated derivatives to numerical derivatives**:

* **Monitor histograms of activations and gradient**:

Reference
===

1. *Ian Goodfellow, Yoshua Bengio, Aaron Courville*, Deep Learning, *pp. 424-445*.
