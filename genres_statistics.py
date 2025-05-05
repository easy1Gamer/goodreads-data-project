import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import sqlalchemy as sqla
import seaborn as sns
from IPython.core.pylabtools import figsize

#%%
db = sqla.create_engine('postgresql+psycopg2://postgres:root@localhost/goodreads_db')

#%%
#%%
# TODO : метрика противоречивости оценок

#Gathering genres statistics
#%%
df_genres_data = pd.read_sql(sql='''with genres_data as (select site_index, work_id, book_name, author, rating, nb_ratings, nb_reviews,
 nb_5_stars, nb_4_stars, nb_3_stars, nb_2_stars, nb_1_stars, nb_pages, extract(year from publication_date) as publication_year, genres as Genre,
 awards as award
from book_data
where site_index >= 1 and site_index <= 3_000_000)
select *
from genres_data''', con= db).drop_duplicates('work_id').explode('genre')



#%%
from utils import genres

#%%Среднее кол-во написанных отзывов на книгу по жанрам, беру только жанры, у которых кол-во книг выше медианного

s_nb_books = genres(df_genres_data)['site_index'].count()
s_sum_reviews =  genres(df_genres_data)['nb_reviews'].sum()
nbraitings_by_book = s_sum_reviews / s_nb_books
f, ax = plt.subplots(figsize=(16,8))
ax.set(title="Mean number of ratings given by genre")
sns.barplot(nbraitings_by_book.sort_values(ascending=False).iloc[0:14], orient="h")
plt.show()

#%%Среднее кол-во страниц по жанру
s_nbpages_genre = df_genres_data.groupby(['genre'])['nb_pages'].mean()
f1, ax1 = plt.subplots(figsize=(16,8))
ax1.set(title="Mean number of pages by genre", xlabel="Pages")
sns.barplot(s_nbpages_genre.sort_values(ascending=False).iloc[:14], orient="h")
plt.show()
#%%
df_genres_data.groupby(['genre'])['nb_pages'].std()

# |(значение - среднее) / std| > 1

#%%Cреднее кол-во наград по жанру, беру жанры, в которых кол-во книг больше медианного
#TODO: Перестало роботать после изменения unnest
s_count_awards = genres(df_genres_data)['award'].count()
nb_awards = s_count_awards / s_nb_books
f2, ax2 = plt.subplots(figsize=(16,8))
ax2.set(title="Mean number of awards by genre", xlabel="Awards")
sns.barplot(nb_awards.sort_values(ascending=False).iloc[:19], orient="h")
plt.show()

#%%


#%%Исследование распределения оценок
# val_index = filter_median(genres)['rating'].mean().index
df_genre_rating = pd.DataFrame(data=[genres(df_genres_data)['rating'].mean(), genres(df_genres_data)['rating'].max(),
                                    genres(df_genres_data)['rating'].min()]).transpose()
df_genre_rating.columns = ['Mean', 'Max', 'Min']

df_genres_plot = df_genres_data[df_genres_data['genre'].isin(df_genre_rating.index)]
df_genres_plot1 = df_genres_plot[['genre', 'rating']]

f3, ax3 = plt.subplots(figsize=(10,8))
ax3.set(title="Rating disribution")
sns.boxplot(data=df_genres_plot1[df_genres_plot1["genre"].isin(np.random.choice(df_genre_rating.index, 5))], x="genre", y="rating")
plt.show()
#%%

#%%
df_genres_stars = genres(df_genres_data)





#%% Кол-во жанров по годам
df_genres_date = df_genres_data.groupby(['publication_year', 'genre']).count()['site_index']
idx = pd.IndexSlice

import matplotlib.animation

f4, ax4 = plt.subplots(figsize=(12, 8))

def genre_date_animate(year):
    ax4.clear()
    ax4.set(xlabel="Books Published", ylabel="Genre")
    ax4.set_title(f"Year: {year}")
    df_genre_cur_date = df_genres_date.loc[idx[year, :]].sort_values(ascending=False)[:15]
    sns.barplot(data=df_genre_cur_date, orient="h")

ani = matplotlib.animation.FuncAnimation(fig=f4, func=genre_date_animate, frames=df_genres_date.unstack().index,
                                         interval=500, repeat=True)

ani.save(filename="plots/animation.gif", writer="Pillow")
#%%

genres['site_index'].count().sort_values()





#%% TODO: Соответствие описания реальным жанрам
df_genres_date.unstack().index[700:710]

#%%
s_nb_books.sort_values().head(n=10)