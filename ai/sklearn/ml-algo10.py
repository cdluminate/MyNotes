
# coding: utf-8

# In[23]:


# 1. linear regression
import numpy as np
from sklearn.linear_model import LinearRegression

x_train = np.random.rand(100,1)
y_train = x_train * 2.0
print('train\t', x_train.shape, y_train.shape)
x_val = np.random.rand(100,1)
y_val = x_val * 2.0
print('val\t', x_val.shape, y_val.shape)

model = LinearRegression()
model.fit(x_train, y_train)
model.score(x_train, y_train)
print(model.coef_, model.intercept_)
pred = model.predict(x_val)
print('MSE on val', np.sum(np.square(pred - y_val)))


# In[53]:


# 2. logistic regression
import numpy as np
from sklearn.linear_model import LogisticRegression

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = LogisticRegression()
model.fit(x_train, y_train)
print(model.score(x_train, y_train))
print(model.coef_)
pred = model.predict(x_train)


# In[59]:


# 3. decision tree
import numpy as np
from sklearn.tree import DecisionTreeClassifier

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = DecisionTreeClassifier(criterion='gini')
model.fit(x_train, y_train)
model.score(x_train, y_train)
pred = model.predict(x_train)
print('MSE on train', np.sum(np.square((pred - y_train))))


# In[60]:


# 4. support vector machine
import numpy as np
from sklearn import svm

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = svm.SVC()
model.fit(x_train, y_train)
print(model.score(x_train, y_train))
pred = model.predict(x_train)


# In[62]:


# 5. naive bayes
import numpy as np
from sklearn.naive_bayes import GaussianNB

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = GaussianNB()
model.fit(x_train, y_train)
model.score(x_train, y_train)


# In[64]:


# 6. k-nearest-neighbor
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = KNeighborsClassifier(n_neighbors=5)
model.fit(x_train, y_train)
model.score(x_train, y_train)


# In[71]:


# 7. k-means
import numpy as np
from sklearn.cluster import KMeans

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = KMeans(n_clusters=2, random_state=0)
model.fit(x_train)
pred = model.predict(x_train)
print(np.sum(np.square(pred - y_train)))


# In[75]:


# 8. random forest
import numpy as np
from sklearn.ensemble import RandomForestClassifier

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = RandomForestClassifier()
model.fit(x_train, y_train)
print(model.score(x_train, y_train))
pred = model.predict(x_train)


# In[83]:


# 9. dimension reduction
import numpy as np
from sklearn.decomposition import PCA

x = np.random.rand(100, 1024)
model = PCA(n_components=20)
x_reduced = model.fit_transform(x)
print(x_reduced.shape)
xx = model.transform(x)


# In[86]:


# 10. Gradient Boosting
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

x_train = np.random.randn(200,2)
y_train = np.zeros((200,))
x_train[100:, :] += 1.0
y_train[100:] += 1.0

model = GradientBoostingClassifier(n_estimators=100, learning_rate=1., max_depth=1, random_state=0)
model.fit(x_train, y_train)
print(model.score(x_train, y_train))
pred = model.predict(x_train)

