import pandas as pd
import numpy as np
import sqlalchemy as sqla
import pyspark

#%%
from pyspark.sql.connect.session import SparkSession
from pyspark.conf import SparkConf
new_conf = SparkConf()


spark1 = SparkSession.builder.appName("TestApplication").remote("sc://10.0.220.155").getOrCreate()

#%%
from datetime import datetime, date
from pyspark.sql import Row

df = spark1.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])
df

#%%
pandas_df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
df = spark1.createDataFrame(pandas_df)
df.show()

#%%
spark.stop()

#%%

