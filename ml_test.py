import seaborn as sns
from IPython.core.pylabtools import figsize

iris = sns.load_dataset("iris")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#%%
iris.head()

#%%
sns.pairplot(iris, hue="species", size=1.5)
plt.show()
#%%
from mpl_toolkits.mplot3d import Axes3D
# mpl.use('WebAgg')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

img = ax.scatter(iris['sepal_length'], iris['sepal_width'], iris['petal_length'], c=iris['petal_width'], cmap=plt.hot())
fig.colorbar(img)
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

#%%
from sklearn.decomposition import PCA
model = PCA(n_components=2)

model.fit(x_iris)

X_2D = model.transform(x_iris)

#%%
iris['PCA1'] = X_2D[:, 0]
iris['PCA2'] = X_2D[:, 1]
sns.lmplot(x="PCA1", y="PCA2", hue='species', data=iris, fit_reg=False)
plt.show()

#%%
from sklearn.mixture import GaussianMixture
model = GaussianMixture(n_components=3, covariance_type="full")
model.fit(x_iris)
y_gmm = model.predict(x_iris)

#%%
iris['cluster'] = y_gmm
sns.lmplot(x="PCA1", y="PCA2", hue='species', data=iris, col="cluster", fit_reg=False)
plt.show()

###########################################################
#%%
from sklearn.datasets import load_digits
digits = load_digits()

#%%
fig, axes = plt.subplots(10, 10, figsize=(8,8),
                         subplot_kw={'xticks':[], 'yticks':[]},
                         gridspec_kw=dict(hspace=0.1, wspace=0.1))

for i, ax in enumerate(axes.flat):
    ax.imshow(digits.images[i], cmap='binary', interpolation='nearest')
    ax.text(0.05, 0.05, str(digits.target[i]),
            transform=ax.transAxes, color='green')

plt.show()

#%%
X = digits.data
y = digits.target

#%%
from sklearn.manifold import Isomap
iso = Isomap(n_components=2)
iso.fit(digits.data)
data_projected = iso.transform(digits.data)
data_projected.shape

#%%
plt.scatter(x=data_projected[:, 0], y=data_projected[:, 1], s=5,c=digits.target, edgecolors='none',
            alpha=0.5, cmap=plt.cm.get_cmap('Spectral', 10))
plt.colorbar(label='digit label', ticks=range(10))
plt.clim(-0.5, 9.5)
plt.show()

#%%
from sklearn.model_selection import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=0)

#%%
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(Xtrain, ytrain)
y_model = model.predict(Xtest)

#%%
from sklearn.metrics import accuracy_score
accuracy_score(ytest, y_model)

#%%
from sklearn.metrics import confusion_matrix
plt.close()
mat = confusion_matrix(ytest, y_model)
sns.heatmap(mat, square=True, annot=True, cbar=False)
plt.xlabel('predicted value')
plt.ylabel('true value')
plt.show()

#%%
fig, axes = plt.subplots(10, 10, figsize=(8,8),
                         subplot_kw={'xticks': [], 'yticks': []},
                         gridspec_kw=dict(hspace=0.1, wspace=0.1))

test_images = Xtest.reshape(-1, 8, 8)

for i, ax in enumerate(axes.flat):
    ax.imshow(test_images[i], cmap='binary', interpolation='nearest')
    ax.text(0.05, 0.05, str(y_model[i]),
            transform=ax.transAxes,
            color='green' if (ytest[i] == y_model[i]) else 'red')

plt.show()

#???????
