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
# 1. удалить все не текстовые символы (знаки препинания)
# 2. Лишние пробелы
# 3. Удалить stopwords
# 4. Оставить только описания на английском языке
# 5. токенизация
# 6. все в один регистр привести
# 7. Stemming

# Преобразование текста в числа
from utils import genres

db = sqla.create_engine('postgresql+psycopg2://postgres:root@localhost/goodreads_db')

df_desc_genres = pd.read_sql(sql='''select site_index, work_id, description, genres as genre
from book_data''', con=db)
#%%
df_desc_genres = df_desc_genres[df_desc_genres["genre"].apply(lambda x : len(x) > 0)]
df_desc_genres = df_desc_genres[df_desc_genres["description"].apply(lambda x : len(x) > 50)]
df_desc_genres_exploded = df_desc_genres.explode("genre")
# df_desc_genres = df_desc_genres[df_desc_genres_exploded["site_index"].isin(genres(df_desc_genres_exploded)["site_index"])]

#%%
# df_desc_genres = df_desc_genres_exploded.groupby("genre")

#%%
df_desc_genres = df_desc_genres[df_desc_genres["site_index"].isin(df_desc_genres.groupby("work_id")["site_index"].min())]
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

df_test = df_desc_genres.iloc[:10_000]

def language_detection(text):
    try:
        res = detect(text)
    except LangDetectException:
        res = np.nan
    return res


df_test['language'] = df_test['description'].apply(language_detection)
# df_desc_genres['language'] = df_desc_genres['description'].apply(language_detection)
#%%






#%%

df_test










#%%
## Шаг 2. Создание модели (выбор модели, обучение модели)
#%%
## Шаг 3. Оценка качества модели (метрики precise, accuracy)
#%%
## Шаг 4. Использование модели (predict)


