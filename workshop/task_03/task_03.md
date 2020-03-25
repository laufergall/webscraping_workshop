# Call REST API endpoints to retrieve information

We add a REST API backend so that we can retrieve the data in MongoDB without having to use a db client. 

We want to prepare queries to retrieve data that our user will be interested in. The use case we consider is:
* Our users (who live in Berlin) feel like going to the cinema, and first want to check out which movies are being played these days.
* When the users have chosen a movie, they want to check at which times it is shown in a cinema closeby. They might not remember the full cinema name.
* Once they have seen all show times for the chosen movie, they want to look for the exact cinema address and the ticket prices.


# Steps:

1. [Add backend service to docker-compose.yml](#step1)
2. [Access the API endpoints](#step2)


## 1. Add backend service to docker-compose.yml <a name="step1"></a>

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

So, your docker-compose has to look like this one: [docker-compose.yml](docker-compose.yml).

&#8594; **Build and start this container** by adding it to the others which are already up. On another terminal:

```
docker-compose up --build backend
```

See that this container is up by:

```
docker ps
```


## 2. Access the API endpoints <a name="step2"></a>

The [Swagger UI](https://flask-restplus.readthedocs.io/en/stable/swagger.html) allows to visualize our API and use its different endpoints.

&#8594; To access the Swagger UI **open your browser and navigate** to `http://<local host>:8001`, where, as always, `<local host>` is `localhost` or your `docker-machine ip`.

&#8594; **Call the GET endpoint** `/movies/titles` to retrieve all movie titles currently shown in Berlin cinemas. You can also filter by indicating a sub-string which must be included in the title. 

Of course, you can also make GET requests with curl, yet it is not so friendly. 

In your terminal: 

```bash
curl -X GET http://<local host>:8001/movies/titles

curl -X GET -d contains=elias http://<local host>:8001/movies/titles
```

Or, in the browser:

```bash
curl -X GET http://<local host>:8001/movies/titles
```

&#8594; Step on the toes of our user and **use these endpoints** to replicate her "journey" from "I want to watch some new movie at the cinema" to "I know when to go where and for which movie".

Can you think of other use cases? Do you imagine how the frontend can look like?
