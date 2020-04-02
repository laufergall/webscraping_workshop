# Concluding remarks

Hopefully you have successfully completed the three proposed tasks!

To stop your running containers

```bash
cd <project-dir>
docker-compose down
```

Remember that always when you start your containers with `docker-compose up`, the scraping process will start in a container and stop when it has finished. The other 3 containers (mongodb, mongoclient, backend) will stay up. You could run the scraping job again later or on a different day (if the other containers are still up) by `docker-compose up scrapy` - but you might get duplicates. So, this application is meant to be started "manually" whenever the user would like to search which movies are being played in Berlin cinemas.

This workshop intends to be an example to illustrate how you could get started if you want to develop your own webscraping API. Remember our [general architecture](img/Architecture.png). 
1. You'll need at least the scraping part of it (with scrapy, or with requests + BeautifulSoup) and probably schedule it as a job, e.g. to run once a day.
2. Also, figure out where to write the data to and how to persist the data.
3. Additionally, you can add an API to be able to query the data you have scraped in the form you / your users need it. Alternatively, you could just build and attach a Dashboard that displays the data.

Some ideas for extensions to the current application are: 
* deploy the scraping part as a scheduled job
* deploy the database so that data is persisted
* add a nice and usable front-end
* add/enhance the existing API endpoints
* scrape other movie-related data

Feel free to contribute to my main [repo](https://github.com/laufergall/movies-knowledgegraph) "movies-knowledgegraph", where the workshop materials come from (as a simplification of the master branch).
