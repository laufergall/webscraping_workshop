# Call REST API endpoints to retrieve information

We add a REST API backend so that we can retrieve the data in MongoDB without having to use a db client. 

We want to prepare queries to retrieve data that our user will be interested in. The use case we consider is:
* Our user (who lives in Berlin) feels like going to the cinema. She wants to check out which movies are being played these days.
* When she chooses a movie, she wants to check at which times it is shown in the cinema in her district. She might not remember the full cinema name.
* Once she has seen the show times, she wants to look for the exact cinema address and the ticket prices.
* Finally, she wants to check which other movies are being played in the same cinema.

# Steps:

1. [Add backend service to docker-compose.yml](#step1)
2. [Access the Swagger UI in browser](#step2)
3. [Add cinemas endpoints](#step3)


## Add backend service to docker-compose.yml <a name="step1"></a>

&#8594; **Add these lines** to the docker-compose.yml file. Note that it has to be indented under `services:` (at the same level as `scrapy`, `mongodb`, and `mongoclient`):

```
backend:
build: ./backend
container_name: backend
ports:
  - 8001:8001
depends_on:
  - mongodb
environment:
  MONGODB_HOST: mongodb
  MONGODB_PORT: 27017
  MONGODB_USERNAME: root
  MONGODB_PASSWORD: 12345
  MONGODB_DB: kinoprogramm
  MONGODB_COLLECTION:  kinos
```

So, your docker-compose has to look like this one: `docker-compose.yml` (of this folder).

&#8594; **Build and start this container** by adding it to the others which are already up. On another terminal:

```
docker-compose up --build backend
```

See that this container is up by:

```
docker ps
```


## Access the Swagger UI in browser <a name="step2"></a>

The [Swagger UI](https://flask-restplus.readthedocs.io/en/stable/swagger.html) allows to visualize our API and use its different endpoints.

&#8594; To access the Swagger UI **open your browser and navigate** to `http://<local host>:8001`, where, as always, `<local host>` is `localhost` or your `docker-machine ip`.

&#8594; **Call the GET endpoint** `/movies/titles` to retrieve all movie titles currently shown in Berlin cinemas. You can also filter by indicating a sub-string which must be included in the title. 

Of course, you can also use curl, yet it is not so friendly. In your terminal: 

```bash
curl -X GET http://<local host>:8001/movies/titles

curl -X GET -d contains=elias http://<local host>:8001/movies/titles
```


## Add cinemas endpoints <a name="step3"></a>

&#8594; **Replace the file** `<project-dir>/backend/apis/api_cinemas.py` by `api_cinemas.py` of this folder.

&#8594; Now, **re-build and start the backend** image and launch the container:

```
docker-compose up --build backend
```

&#8594; **Refresh** `http://<local host>:8001` in your browser and see that four new endpoints appear under the namespace "cinemas":
* /cinemas/details
* /cinemas/movie_times
* /cinemas/names
* /cinemas/shows

&#8594; Step on the toes of our user and **use these endpoints** to replicate her "journey" from "I want to watch some new movie at the cinema" to "I know when to go where and for which movie".

Can you think of other use cases? Do you imagine how the frontend can look like?
