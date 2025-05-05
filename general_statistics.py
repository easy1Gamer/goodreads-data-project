import pandas as pd
import numpy as np
import re
import sqlalchemy as sqla
import matplotlib.pyplot as plt
import seaborn as sns
import pyspark
from pyspark.sql.connect.session import SparkSession


#%%
pd.set_option('display.max_columns', None)
#%%

db = sqla.create_engine('postgresql+psycopg2://postgres:root@localhost/goodreads_db')

#%%
df_base = pd.read_sql('select * from book_data where site_index >= 1', db)

#%%Распределение оценок по звездам, вводится квантиль
qn = float(input())
books_general_stats = df_base.drop_duplicates('work_id')
books_general_stats = books_general_stats.loc[:,['nb_ratings','nb_5_stars', 'nb_4_stars','nb_3_stars','nb_2_stars','nb_1_stars']]
books_general_stats = books_general_stats[books_general_stats['nb_ratings'] >= books_general_stats['nb_ratings'].quantile(qn)]
nb_ratings = books_general_stats['nb_ratings'].sum()
books_general_stats = books_general_stats.iloc[:, 1:].sum() / nb_ratings


f, ax = plt.subplots(figsize=(10, 10))
sns.barplot(x=books_general_stats.index, y=books_general_stats.values)
ax.set(ylim=[0,1], yticks=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], yticklabels=["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"])
ax.set(title="General rating distribution", xlabel="Stars", xticks=[0,1,2,3,4],xticklabels=["1 star", "2 stars", "3 stars", "4 stars", "5 stars"])
plt.savefig('plots/my_plot.png')
plt.show()

#%%
# ! pip install pyspark[sql]
# .venv\Scripts\activate
# Set-ExecutionPolicy Unrestricted -Force
# from pyspark.sql import SparkSession



spark = (
    SparkSession.builder
        .master("localhost")
)
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")