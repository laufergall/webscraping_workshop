# Scrape the cinema program

The goal of this task is to get scrapy to run and scrape the current cinema program from [berlin.de](https://www.berlin.de/kino/_bin/index.php). We want to scrape different pieces of information from every cinema: name, description, address, contact, prices, and shows (movie titles and times).

> **NOTE**: In this workshop, we will prepend `http://web.archive.org/web/20191102035415/` to the cinema detail URLs. This is because of the berlin.de website currently not showing any movie titles due to corona virus. Hence, we will retrieve an older cinema program instead of the current one.

Take a look at the main berlin.de cinemas [website](https://www.berlin.de/kino/_bin/index.php), from where we get all cinema codes.

This is a cinema [website](https://www.berlin.de/kino/_bin/kinodetail.php/32139) with the cinema details and current cinema program (might be empty due to corona virus). In this example: "CineStar Cubix am Alexanderplatz", (cinema code: "32139").

And [this website](http://web.archive.org/web/20191102035415/https://www.berlin.de/kino/_bin/kinodetail.php/32139) also corresponds to "CinemaxX Berlin", yet we get it from web.archive.org, from 2nd November 2019, so that we can scrape movie titles and show times. Depending on when the particular cinema website was stored in web.archive.org, we might get movies from older dates for other cinemas.


# Scraping politeness

Before starting any scraping job we have to follow best practices to **scrape politely**:
* Check the Terms of Use ("Nutzungsbedingungen" or "Allgemeine Geschäftsbedingungen (AGB)" in German). In the case of berlin.de, we may scrape if we keep the data **only for private use** and if we store the **data in one system** only.
* Check robots.txt . In our case, [Berlin.de's robots.txt](https://www.berlin.de/robots.txt). Nobody is allowed to scrape from paths in the form `/*/(S(*))`. For us this is fine, since the websites we want to scrape are:

`https://www.berlin.de/kino/_bin/azfilm.php`

and

`https://www.berlin.de/kino/_bin/kinodetail.php/<cinema-code>`


# Steps:

1. [Clone or download main project](#step1)
2. [Install scrapy project requirements](#step2)
3. [Scrape data and write to JSON file](#step3)

## 1. Clone or download main project <a name="step1"></a>

&#8594; First, **download** [this zip file](https://github.com/laufergall/movies-knowledgegraph/archive/workshop.zip)
that contains a base project for you to work on it.

We will be making changes to different files in this project.

> **Important**: your `<project-dir>` is the path to the root project folder, in my case: `C:\Users\Laura\Downloads\movies-knowledgegraph-workshop`. If you `cd` to where you have `<project-dir>`, you should see the folders `backend`, `mongo`, `scrapy`, and the files `.gitignore` and `README.md`.


## 2. Install scrapy project requirements <a name="step2"></a>

You need Python 3.7.4.

&#8594; **Install requirements.txt** (under `<project-dir>/scrapy`).

If you are not using conda, you can simply create and activate a virtual environment:

```bash
python -m venv webscraping
source webscraping/bin/activate  # for macOS and Linux
webscraping/Scripts/activate.bat  # for Windows

cd <project-dir>/scrapy
pip install -r requirements.txt
```

If you have conda installed, then:

```bash
conda create -n webscraping python=3.7.4
conda activate webscraping

cd <project-dir>/scrapy
pip install -r requirements.txt
```

Note that you might need backward slashes (`\`).


## 3. Scrape data and write to JSON file <a name="step3"></a>

&#8594; You can **start the spider** by just:

```bash
cd <project-dir>/scrapy/kinoprogramm
scrapy crawl kinoprogramm -o ../data/kinoprogramm.json
```

Data will be written to the file specified with the `-o` parameter. In our case: `<project-dir>/scrapy/data/kinoprogramm.json`.


The main code resposible for scraping lies in `scrapy/kinoprogramm/spiders/kinoprogramm.py` file. Open the file and take a look. 
The `parse()` method receives as input a response from the start_url: https://www.berlin.de/kino/_bin/azfilm.php. The method extracts hrefs for websites corresponding to each cinema, like for instance [Kant Kino](http://web.archive.org/web/20191102035415/https://www.berlin.de/kino/_bin/kinodetail.php/30208). Each cinema website is parsed separately, by the method `parse_cinema()`.

&#8594; Open the file with the scraped data `scrapy/data/kinoprogramm.json` to verify that the data in the file looks fine with the right information from every cinema, which we also see online. Look for the different cinemas in the main berlin.de cinemas [website](https://www.berlin.de/kino/_bin/index.php), using the dropdown next to "Kino".

Remember that the name, description, address, contact, and prices are there; only the movies are missing (due to corona virus). Remember, to see the movies we are actually scraping (older, from web.archive), add `http://web.archive.org/web/20191102035415/` before the cinema details url, like in the example below:

Example:
* Cinema details url ("Kant Kino", cinema code "30208"): `https://www.berlin.de/kino/_bin/kinodetail.php/30208`
* Same cinema, with older movies (from 29th Sept. 2019): `http://web.archive.org/web/20191102035415/https://www.berlin.de/kino/_bin/kinodetail.php/30208`
