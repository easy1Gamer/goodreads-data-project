import seaborn as sns
iris = sns.load_dataset("iris")
import matplotlib.pyplot as plt

#%%
iris.head()

#%%
sns.pairplot(iris, hue="species", size=1.5)
plt.show()