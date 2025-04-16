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

db = sqla.create_engine('postgresql+psycopg2://postgres:root@localhost/goodreads_db')

df_desc_genres = pd.read_sql(sql='''select site_index, work_id, description, genres
from book_data''', con=db)
#%%
df_desc_genres = df_desc_genres[df_desc_genres["site_index"].isin(df_desc_genres.groupby("work_id")["site_index"].min())]
#%%
df_desc_genres = df_desc_genres[df_desc_genres["genres"].apply(lambda x : len(x) > 0)]



#%%
## Шаг 2. Создание модели (выбор модели, обучение модели)
#%%
## Шаг 3. Оценка качества модели (метрики precise, accuracy)
#%%
## Шаг 4. Использование модели (predict)


