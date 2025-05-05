import nltk
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import sqlalchemy as sqla
import seaborn as sns


#%%
## Шаг 1. подготовка данных (очистка, преобразование текста -> векторы чисел)
# Загрузить данные
# выделить признаки (описание) и целевой признак (жанры)


# TODO: добавлять название книги

# Чистка текста
# nltk + re
# 1. Оставить только описания на английском языке
# 2. удалить все не текстовые символы (знаки препинания)
# 3. Лишние пробелы
# 4. все в один регистр привести
# 5. токенизация
# 6. Удалить stopwords
# 7. Stemming vs Lemmatization

# Преобразование текста в числа


#%%
from pyspark.sql.connect.session import SparkSession


spark1 = SparkSession.builder.appName("TestApplication").remote("sc://10.0.220.155").getOrCreate() # The SQL config "spark.rpc.message.maxSize" cannot be found.
spark1.conf.set("spark.sql.session.localRelationCacheThreshold", 512 * 1024 * 1024)
# spark1.conf.set("spark.rpc.message.maxSize", "1000mb")
## pyspark --master yarn --conf spark.rpc.message.maxSize=1024
## spark.conf.set("spark.sql.legacy.setCommandRejectsSparkCoreConfs", False)
#start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.5.5 --master spark://Rooky.:7077 --conf spark.rpc.message.maxSize=1024
# --conf spark.executor.memory=10g --conf spark.executor.cores=6
#%%
# spark.sql('''select site_index, work_id, description, genres as genre from book_data where site_index >= 1 and site_index <= 3_000_000''')
#%%
db = sqla.create_engine('postgresql+psycopg2://postgres:root@localhost/goodreads_db')

df_desc_genres = pd.read_sql(sql='''select site_index, work_id, description, genres as genre
from book_data where site_index >= 1 and site_index <= 3_000_000''', con=db)
#%%
spark_df = spark1.createDataFrame(df_desc_genres.iloc[:100_000])
spark_df.describe().show()
#%%
CHUNK_SIZE = 100_000

final_df = None
for chunk in range(0, 3_000_000, CHUNK_SIZE):
    print(f"Обработка куска {chunk}")
    chunk_df_iloc = df_desc_genres.iloc[chunk:chunk + CHUNK_SIZE]
    if not chunk_df_iloc.empty:
        chunk_df = spark1.createDataFrame(chunk_df_iloc)
        if final_df is None:
            final_df = chunk_df
        else:
            final_df = final_df.union(chunk_df)

#%%
final_df.describe()

#%%
final

#%%
pandas_df = None
for chunk in range(0, 3_000_000, CHUNK_SIZE):
    print(f"Обработка куска {chunk}")
    chunk_df_iloc = spark_df.iloc[chunk:chunk + CHUNK_SIZE]
    chunk_df =
    pandas_df = pandas_df.union()
#%%

from pyspark.sql.functions import length, col

spark_df.filter(length(col("description"))>50).show()

#%%
# spark_df_desc_genres = spark.createDataFrame(df_desc_genres.iloc[:1000000])
# spark_df_desc_genres.show()













#%%
df_desc_genres = df_desc_genres[df_desc_genres["description"].apply(lambda x : len(x) > 50)]
df_desc_genres = df_desc_genres[df_desc_genres["genre"].apply(lambda x : len(x) > 0)]

df_desc_genres_exploded = df_desc_genres.explode('genre')

s_nb_books = df_desc_genres_exploded.groupby(['genre'])['site_index'].count()
top_100_genres = s_nb_books.sort_values(ascending=False).head(100)


#%%
df_prepared = df_desc_genres[df_desc_genres['genre'].isin(top_100_genres.index)].groupby(['site_index'])
df_prepared = df_prepared[['description', 'genre']].agg({'description': 'first', 'genre': list})



#%%


#%%
import re
from nltk.corpus import stopwords
from nltk.corpus import  wordnet as wn


text = """Vengeance ruled his day and nights.An infamous sea captain of the British
 Royal Navy, Devlin O’Neill is consumed with the need to destroy the man
  who brutally murdered his father. Having nearly ruined the Earl of Eastleigh
   financially, he is waiting to strike the final blow. And his opportunity comes
    in the form of a spirited young American woman, the earl’s niece, who is about
     to set his cold, calculating world on fire.Pride inflamed her spirit.Born and
      raised on a tobacco plantation, orphan Virginia Hughes is determined 
to rebuild her beloved Sweet Briar. Daringly, she sails to England alone,
 hoping to convince her uncle to lend her the funds. Instead she finds
  herself ruthlessly kidnapped by the notorious Devlin O’Neill. As his
   hostage, she will soon find her best-laid plans thwarted by a passion
    that could seal their fates forever…Love conquered them both…"""

def description_cleaning(text):
    eng_stopwords = stopwords.words('english')
    wnl = nltk.WordNetLemmatizer()
    text = text.lower()
    tokens = nltk.regexp_tokenize(text, pattern=r'\w+')
    tokens = [word for word in tokens if word not in eng_stopwords]
    tokens = [wnl.lemmatize(w) for w in tokens] #TODO: привести глаголы к инфинитиву
    return tokens

print(description_cleaning(text))

#%%
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# df_test = df_desc_genres.iloc[:10_000]

def language_detection(text):
    try:
        res = detect(text)
    except LangDetectException:
        res = np.nan
    return res


# df_test['language'] = df_test['description'].apply(language_detection)
# df_desc_genres['language'] = df_desc_genres['description'].apply(language_detection)

#%%






#%%

# df_test










#%%
## Шаг 2. Создание модели (выбор модели, обучение модели)
#%%
## Шаг 3. Оценка качества модели (метрики precise, accuracy)
#%%
## Шаг 4. Использование модели (predict)


