import pandas as pd
import requests
import config


# EXTRACT

# Send a single GET request to the API to recieve a JSON record with the movie_id specified
"""
API_KEY = config._api_key
url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY)

r = requests.get(url)
"""
# Request 6 movies with movie_id ranging from 550 to 555
# Create a loop that requests each movie one at a time and appends the response to a list

response_list = []
API_KEY = config._api_key

for movie_id in range(550, 556):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY)
    r = requests.get(url)
    response_list.append(r.json())

print(type(response_list))

# Create a pandas dataframe from the response list using from_dict()

df = pd.DataFrame.from_dict(response_list)  # generates a cleanly formatted dataframe with 6 rows and 38 columns.
#print(df.info())
#print(df['genres'])

# TRANSFORM

# Create a list of column names called df_columns that allows us to select the columns we want from the main df
df_columns = ['budget', 'genres', 'id', 'imdb_id', 'original_title', 'release_date', 'revenue', 'runtime']


# ...
genres_list = df['genres'].tolist()
flat_list = [item for sublist in genres_list for item in sublist]


# ...
result = []
for l in genres_list:
    r = []
    for d in l:
        r.append(d['name'])
    result.append(r)

df = df.assign(genres_all=result)


# Create the genres table
df_genres = pd.DataFrame.from_records(flat_list).drop_duplicates()


# ...
df_columns = ['budget', 'id', 'imdb_id', 'original_title', 'release_date', 'revenue', 'runtime']
df_genre_columns = df_genres['name'].to_list()
df_columns.extend(df_genre_columns)


# ...
s = df['genres_all'].explode()
df = df.join(pd.crosstab(s.index, s))


# Expand datetime column into a table
# We need to convert the release_date column into a datetime first
df['release_date'] = pd.to_datetime(df['release_date'])
df['day'] = df['release_date'].dt.day
df['month'] = df['release_date'].dt.month
df['year'] = df['release_date'].dt.year
df['day_of_week'] = df['release_date'].dt.day_name()
df_time_columns = ['id', 'release_date', 'day', 'month', 'year', 'day_of_week']


# LOAD

# We ended up creating 3 tables for the tmdb schema that we'll call movies, genres, and datetimes
# We export our tables by writing them to file.
# This will create 3 .csv files in the same directory that our script is in.

"""
df[df_columns].to_csv('tmdb_movies.csv', index=False)
df_genres.to_csv('tmdb_genres.csv', index=False)
df[df_time_columns].to_csv('tmdb_datetimes.csv', index=False)
"""
