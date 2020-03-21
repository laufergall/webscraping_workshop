# Write scraped data to database and connect to it with a db client

By the end of this task we will have our cinema program in a MongoDB database. The database, a database client, and the scraping job will run containerized on docker.

The containers for the database and for the client will be up permanently. Differently, the container with the scraping job will start only once when everything is launched, and will stop once the scraping has finished.


# Steps:

1. [Prepare docker](#Prepare docker)
2. [Add docker-compose.yml](#Add docker-compose.yml)
3. [Adapt scrapy pipeline](#Adapt scrapy pipeline)
4. [Start the three containers](#Start the three containers)
5. [Connect to db from Mongoclient](#Connect from Mongoclient)
6. [Connect to db from Robo3T](#Connect from Robo3T)

## Prepare docker

You should have already installed one of these:
* [Docker Toolbox for Windows](https://docs.docker.com/toolbox/toolbox_install_windows/#step-3-verify-your-installation)
* [Docker Toolbox for Mac](https://docs.docker.com/toolbox/toolbox_install_mac/#step-3-verify-your-installation)
* [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/)
* [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/)
* If you are on Linux (CentOS, Debian, Fedora, Oracle Linux, RHEL, SUSE, and Ubuntu), then you have the [Docker Engine](https://docs.docker.com/install/)

&#8594; If you have Docker Toolbox, **launch** the Docker QuickStart Terminal.

**Verify** your installation by:

&#8594; **Run**:

```bash
docker run hello-world
```

You should see in the output:

`Hello from Docker! This message shows that your installation appears to be working correctly.`

&#8594; **Run** the nginx server:

```
docker run --detach --publish=80:80 --name=webserver nginx
```

&#8594; In your browser, **navigate to** either:
* `http://192.168.99.100/` if you have Docker Toolbox
* `http://localhost/` if you have Docker Desktop

You should see the page: `Welcome to nginx! If you see this page,...`.

**Important** if you have Docker Toolbox: `192.168.99.100` if your docker-machine ip. Check if you have a different one with the command: `docker-machine ip`. For now on, instead of `localhost`, your local host is your docker-machine ip.

Now, you're all set with docker!


## Add docker-compose.yml

&#8594; **Copy** the `docker-compose.yml` file of this folder to your root project directory `<project-dir>/` (same level as `.gitignore`).

The docker-compose file is defining the three containers: `mongodb`, `mongoclient`, and `scrapy`. Note that we are indicating where to get or build docker images from, ports (in case of `mongodb` and `mongoclient`), and environment variables in case of `scrapy`, needed for the connection to the database.


## Adapt scrapy pipeline

In the scrapy pipelines file (`<project-dir>/scrapy/kinoprogramm/pipelines.py`), we define how our scraped data should be output. 

In the scrapy settings file (`<project-dir>/scrapy/kinoprogramm/settings.py`), we specify where our scraped data should be output to. In other words, we specify which class of scrapy pipelines to use.

Before (in Task 1), we were using the class `KinoprogrammPipeline` of pipelines to write to a json file. Now, we will use the class `MongoDBPipeline` to write to mongodb (which will be up in a docker container).

&#8594; **Replace** the `settings.py` file in `<project-dir>/scrapy/kinoprogramm/` by the one in this folder. The new lines (from line 71 to line 80) are: 

```python
ITEM_PIPELINES = {
    'kinoprogramm.pipelines.MongoDBPipeline': 300,
}

MONGODB_HOST = os.environ.get('MONGODB_HOST', '192.168.99.100')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', 'root')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '12345')
MONGODB_DB = os.environ.get('MONGODB_DB', 'kinoprogramm')
MONGODB_COLLECTION = os.environ.get('MONGODB_COLLECTION', 'kinos')
```

## Start the three containers

&#8594; To **start the containers**, we just build the images (with the current code) with:

(you need to be in the root project directory.

```bash
cd <project-dir>
```

```bash
docker-compose build
```

You would have to build again every time you make changes to the code.

And, when all is ready, up with:

```bash
docker-compose up
```

You'll see many logs with all that is going on, coloured depending on the container. When the scrapy job is finished, you will see: `scrapy exited with code 0`. Nice! The data has been scraped. Let us check it in next step.

&#8594; On another terminal, **verify that the two other containers are up** by:

```bash
docker ps
```

You should see a table-like output with `CONTAINER ID`, `IMAGE`, `COMMAND`, `CREATED`, `STATUS`, `PORTS` and `NAMES` for all containers you have up. 


## Connect to db from Mongoclient

We are going to verify that we have collected our current cinema program and has been stored in mongo db. Our [Nosqlclient](https://github.com/nosqlclient/nosqlclient) (formerly mongoclient) container should be up, as we checked in last step.

&#8594; In your browser, **go to** `http://<local host>:3300/`. As we mentioned [before](# Prepare docker), `<local host>` is either `localhost` or your docker-machine ip, depending on your docker installation.

&#8594; To **connect**:
1. Click on "Connect" (up-right corner).
2. Click on "Edit" the default connection.
3. Clear connection url. Under the "Connection" tab, replace Host `127.0.0.1` by your `<local host>`. Port: `27017`. Database Name: `kinoprogramm`.
4. Under tab "Authentication", `Scram-Sha-1` as Authentication Type, Username: `root`, Password: `12345`, Authentication DB: leave empty.
5. Click on "Save", and click on "Connect".

To see stored data: 
1. Go to "Collections" -> "kinos".
2. Example Query: find, Selector: `{"name": "Bali-Kino"}`, Explain: (unchecked), Options: (leave empty).
3. Execute.

To query data from the shell: 
1. Go to "Tools" -> "Shell"
2. Insert in the upper field:

```bash
use kinoprogramm
```

and any of these queries:

```bash
db.kinos.find( { name: "Bali-Kino" } )
db.kinos.find( { name: { $in: [ "Bali-Kino", "Acud Kino" ] } } )
db.kinos.find( { name: /Alex/ }, {name: 1, "shows.title": 1, _id: 0})
db.kinos.find( { "shows.title": /Eiskönigin/ }, {name: 1, _id: 0})
db.kinos.find( { name: /Cinemax/, "shows.title": /Bad Boys/ }, {name: 1, "address.street":1, "shows.$":1, _id: 0}).pretty()
```

Can you tell which SQL commands these correspond to?


## Connect to db from Robo3T

You can perform this step if you have installed [Robo 3T](https://robomongo.org/).

1. "File" -> "Connect" -> "Create".
2. "Connection" tab: Name: `connect to kinoprogramm`, Address: `<local host>`, Port: `27017`.
3. "Authentication" tab: Database: `kinoprogramm`, User Name: `root`, Pasword: `12345`, Auth Mechanism: `SCRAM-SHA-1`.
4. Example query: `db.getCollection('kinos').find({})`


## You could also...

Remove all scraped data, from the mongo client:

```bash
`db.getCollection('kinos').remove({})`
```

Scrape again (start scraping job, which will stop after finished):

```
docker-compose up scrapy
```

Stop all containers from docker-compose:

```
docker-compose down
```

Now, you can't connect anymore to the database, since it is down. You won't see the mongoclient either (port 3300). Data is lost.

If you made changes to the code, you have to build again: 

```
docker-compose build
```

And launch the containers again, as we already did [before](# Start the three containers).

```
docker-compose up
```