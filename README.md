# Full Stack Data Engineering Code Repo

### Goal
The primary goal of this project is to similate a real world data pipeline, wherein external data is captured through an API and made available to be used by a downstream application (in this case a dashboard)

There are 3 main components for this to be as close to a real data pipeline as possible:
1. There needs to be a data source that is flakey, and as such the system should be able to handle that flakiness
2. There needs to be a data store/data lake where raw data comes in, and is then processed by an ETL proccess
3. There needs to be an application at the end which consumed processed data and exposes it to the end user.


### Key Assumptions:
1. I do not know the business context behind the term - "Movie Provider"; As such I have assumed that to mean the Director of the movie, as they are the primary ones responsible for providing the movie
2. I do not know the business context behind the 2 databases. I have seen that Episode 7 (Force Awakens) does not exist in one of the databases. This could mean multiple things, however I have assumed that particular database to be older (since Episode 7 came out much later than the other movies) and not having the most updated data.
3. I do not know the business context behind the `Price` variable. They do not reflect any real world amount that I did a bit of Googling into, and I can only assume them to be arbitrary, but idempotent (as it seems from the multiple API calls) values.
4. Since I have assumed no real relation between the 2 databases, I have given the user the freedom to choose which database they want to check movie prices in. I have also given them the option to compare the cheapest movie from `cinemaworld` against the cheapest movie from `filmworld` if they so choose. That would technically be the cheapest movie overall.
5. Similarly for the director as well.  

`Please make sure that ports 5000, 8502, 9000 and 9001 are free on your system for the application to run.`

In order to run the application please use the following docker commands:

`docker compose build`
`docker compose up -d`

As discussed above there are 3 components to this application:

* Frontend Streamlist Dashboard - which is the end-user application
* Backend Flask API Gateway - which is the data gathering source for our application
* Minio Data Storage - which acts as our data store/data lake where ETL processes occur

Once you start up the services through `docker-compose` they should spin up and be available to use.

### System Architecture

![System Architecture](static/system_architecture.png)


### Streamlit Dashboard

The central application itself is a streamlit dashboard. This is available at `localhost:8501`

![Dashboard](static/dashboard_1.png)


There are 2 databases - `Cinemaworld` and `Filmword` that we can connect to via the dashboard. 

I have included a toggle there, so that the user can switch between the 2 databases at any time.


![Toggle Cinemaworld](static/dashboard_cw.png)

![Toggle Filmworld](static/dashboard_fw.png)


Upon toggling a database, the following workflow takes place:

1. Fetches all movie data, and stores it in the datalake
2. Shows a preview of the stored data
3. Next, iterates over all the movies and fetches their data
4. Stores each movie's data as a separate file, in its respective directory within the datalake
5. Computes cheapest movie and director

![Toggle Both](static/cheapest.png)

You can also toggle both to compare the prices of movies and directors across both the databases.


### Flask API

The Flask API is available at `localhost:5000`

It acts as an api gateway between the dashboard application and the external API.


### Minio Data Storage

The data storage/data lake is hosted on Minio. 

The GUI/Console is available at `localhost:9001`, and the API to use it is available at `localhost:9000`

In order to login to the console, you will need to use the access keys provided in the .env file.

![Data Storage Console Login](static/minio_login.png)


![Data Storage Bucket](static/minio_bucket_storage.png)



![Data Storage Partitions](static/minio_bucket_storage_partitions.png)
