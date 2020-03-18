# Web Scraping with Scrapy and MongoDB running on Docker

Have you ever wanted to know when a movie is shown in the cinema, but then been bothered by having to search the internet? In this workshop, we will scrape to collect our own cinema program using [scrapy](https://docs.scrapy.org/en/latest/). Data will be stored in a [MongoDB](https://www.mongodb.com/) database and different queries will allow us to retrieve any information we need. We will dockerize this application so that we are able to run it in any platform.

# Requirements

Technical:

* Python 3.7.4 (not tested with lower Python versions)
* An IDE, e.g. Spyder or PyCharm. You can follow [this guide](https://github.com/laufergall/pythonsql_workshop/blob/master/docs/get_started.md) to get python, anaconda environments, and an IDE set up.
* Docker Desktop or Docker Toolbox, whichever works in your system, [this post](https://nickjanetakis.com/blog/should-you-use-the-docker-toolbox-or-docker-for-mac-windows) can helpyou decide. Follow the [docker documentation](https://docs.docker.com/get-started/) to install Docker and verify your installation.
* [Robo 3T](https://robomongo.org/download) (formerly Robomongo)

Background knowledge:
* Basic Python
* Ideally but not required: basic SQL knowledge and some familiarity with Docker


# Workshop

## Introduction

This workshop consists on looking at different components of [my application](https://github.com/laufergall/movies-knowledgegraph) for scraping the cinema program, writing the data to a NoSQL database, and backend api enpoints for querying the data. 

This application still needs lots of improvement, but it serves to illustrate different aspects.

Based on this code, we will go through a series of [hands-on tasks](#Hands-on) to understand:

&#x2713; In General, how such an application can be architectured
&#x2713; Employing scrapy to retrieve data from the internet
&#x2713; Establishing the connection from scrapy to a database
&#x2713; Using a database client to check out the stored data
&#x2713; Implementing backend REST API endpoints to query the stored data in the form users need it
&#x2713; Dockerizing all components: scrapy, database, client, and backend

Introduction slides [here](workshop/introduction.html).

## Hands-on

1. [Scrape the cinema program](workshop/task_01.md)
2. [Write scraped data to database and connect to it with a db client](workshop/task_02.md)
3. [Call REST API endpoints to retrieve information](workshop/task_03.md)
