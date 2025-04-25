import seaborn as sns
iris = sns.load_dataset("iris")
import matplotlib.pyplot as plt
import numpy as np

#%%
iris.head()

#%%
sns.pairplot(iris, hue="species", size=1.5)
plt.show()

#%%
x_iris = iris.drop('species', axis=1)
x_iris.shape

#%%
y_iris = iris['species']
y_iris.shape

#%%
rng = np.random.RandomState(42)
x = 10 * rng.rand(50)
y = 2 * x - 1 + rng.randn(50)
plt.scatter(x, y)
plt.show()

#%%
from sklearn.linear_model import LinearRegression

model = LinearRegression(fit_intercept=True)

#%%
X = x[:, np.newaxis]

#%%
model.fit(X, y)

#%%
xfit = np.linspace(-1, 11)
Xfit = xfit[:, np.newaxis]
yfit = model.predict(Xfit)

#%%
plt.scatter(x, y)
plt.plot(xfit, yfit)
plt.show()

#%%
from sklearn.model_selection import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(x_iris, y_iris, random_state=1)

#%%
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(Xtrain, ytrain)
y_model = model.predict(Xtest)

#%%
from sklearn.metrics import accuracy_score
accuracy_score(ytest, y_model)