import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%%
data = np.arange(10)

#%%
data
#%%
plt.plot(data)
plt.show()

#%%

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax3.plot(np.random.standard_normal(50).cumsum())
ax1.hist(np.random.standard_normal(50), bins = 10)
ax2.scatter(np.arange(30), np.arange(30) + 3 * np.random.standard_normal(30), alpha=0.4)
plt.show()

#%%
fig, axes = plt.subplots(1,1)

plt.show()

#%%
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
for i in range(2):
    for j in range(2):
        axes[i, j].hist(np.random.standard_normal(100), bins = 10, color="black")
fig.subplots_adjust(wspace=0, hspace=0)

#%%
fig = plt.figure()
ax = fig.add_subplot()
ax.plot(np.random.standard_normal(30).cumsum(), linestyle="dashed", marker="o")
plt.show()

#%%
fig = plt.figure()
ax = fig.add_subplot()
data = np.random.standard_normal(30).cumsum()
ax.plot(data, color='orange', linestyle="dashed", label="Default")
ax.plot(data, color='blue', linestyle="dashed", drawstyle="steps-post", label="steps-post")
ax.legend()
plt.show()

#%%
fig, ax = plt.subplots(figsize=(10,8))
ax.plot(np.random.standard_normal(1000).cumsum())
ticks = ax.set_xticks([0,250,500,750,1000])
labels = ax.set_xticklabels(["one", "two", "three", "four", "five"], rotation=30)
ax.set_xlabel("Stages")
ax.set_title("Test plot")
plt.show()

#%%

s = pd.Series(np.random.standard_normal(10).cumsum(), index=np.arange(0,100,10))
s.plot()
plt.show()

#%%
df = pd.DataFrame(np.random.standard_normal((10,4)).cumsum(0), columns=["A", "B", "C", "D"], index=np.arange(0,100,10))
df.plot()
plt.show()

#%%
fig, axes = plt.subplots(2,1)
data = pd.Series(np.random.uniform(size=16), index=list("abcdefghijklmnop"))
data.plot.bar(ax=axes[0], color="black", alpha=0.7, rot=0)
data.plot.barh(ax=axes[1], color="black", alpha=0.7, rot=0)
plt.show()

#%%
df = pd.DataFrame(np.random.uniform(size=(6,4)), index=["one","two","three","four","five","six"],
                  columns=pd.Index(["A","B","C","D"], name="Genus"))
df.plot.bar(rot=0)
plt.show()

#%%
df.plot.barh(stacked=True, alpha=0.5)
plt.show()

#%%
comp1 = np.random.standard_normal(200)
comp2 = 10 + 2 * np.random.standard_normal(200)
values = pd.Series(np.concatenate([comp1, comp2]))
sns.histplot(values, bins=100,color="black")
plt.show()