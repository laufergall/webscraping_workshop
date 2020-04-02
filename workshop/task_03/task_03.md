# Call REST API endpoints to retrieve information

We add a REST API backend so that we can retrieve the data in MongoDB without having to use a db client, and with our "customized" endpoints. 

We want to prepare queries to retrieve data that our users will be interested in. The use case we consider is:
* Our users (who live in Berlin) feel like going to the cinema, and first want to check out which movies are being played these days.
* When the users have chosen a movie, they want to check at which times it is shown in a cinema closeby. They might not remember the full cinema name.
* Once they have seen all show times for the chosen movie, they want to look for the exact cinema address and the ticket prices.


# Steps:

1. [Add backend service to docker-compose.yml](#step1)
2. [Access the API endpoints](#step2)


## 1. Add backend service to docker-compose.yml <a name="step1"></a>

&#8594; **Add these lines** to the docker-compose.yml file. Note that it has to be indented under `services:` (at the same level as `mongodb`, `mongoclient`, and `scrapy`):

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
cd <project-dir>
docker-compose up --build backend
```

On another terminal, see that the backend container is done with building and already up by:

```
docker ps
```


## 2. Access the API endpoints <a name="step2"></a>

The [Swagger UI](https://flask-restplus.readthedocs.io/en/stable/swagger.html) allows to visualize our API and use its different endpoints.

&#8594; To access the Swagger UI **open your browser and navigate** to `http://<local host>:8001`, where, as always, `<local host>` is `localhost` or your `docker-machine ip`.

&#8594; **Call the GET endpoint** `/movies/titles` to retrieve all movie titles currently shown in Berlin cinemas. Clicking on movies, then on "Try it out" under "/movies/titles", and then on "Execute". Optionally, you can also filter by indicating (as the "contains" parameter) a sub-string which must be included in the title. You should see a Response, hopefully with Code 200!

Of course, you can also make GET requests with curl, yet this is not so friendly. 

In your terminal, if you have curl installed:

```bash
curl -X GET http://<local host>:8001/movies/titles

curl -X GET -d contains=das http://<local host>:8001/movies/titles
```

Or, in the browser:

```bash
http://<local host>:8001/movies/titles

http://<local host>:8001/movies/titles?contains=das
```

&#8594; Step on the toes of our user and **use these endpoints**, under **/movies/** and under **/cinemas/**, to replicate her "journey" from "I want to watch some new movie at the cinema" to "I know when to go where and for which movie".

Can you think of other use cases? 

Do you imagine how the frontend can look like?

[Continue to](../concluding_remarks.md) concluding remarks.
