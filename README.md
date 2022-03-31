# themoviedb.org ETL Pipeline
In this project, I extracted movies data from themoviesdb.org database through their API using Python.

## The ETL Process - tmdb.py
* **Extract:** 
1. Request data from the API and convert to a JSON record
2. Create a pandas dataframe

* **Transform:**
1. Select a list of columns that are needed in the fact table
2. Expand the genre column into a dimension table
3. Treat the genre column in the fact table with one-hot encoding
4. Expand the datetime column into a dimension table
5. That leaves us with 3 tables called movies, genres, and datetimes

* **Load:**
1. Export tables by writing them into csv files
