from pandas.core.groupby.generic import DataFrameGroupBy


def genres(df_genres_data):
    genres = df_genres_data.groupby(['genre'])

    median_count = (genres['site_index'].count()).median()

    def filter_median(groups: DataFrameGroupBy):
        return groups.filter(lambda group: group['site_index'].count() > median_count).groupby(['genre'])

    return filter_median(genres)