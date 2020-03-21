# Scrape the cinema program

The goal of this task is to get scrapy to run and scrape the current cinema program from [berlin.de](https://www.berlin.de/kino/_bin/azfilm.php).

Before starting any scraping job we have to follow best practices to **scrape politely**:
* Check the Terms of Use ("Nutzungsbedingungen" or "Allgemeine Geschäftsbedingungen (AGB)" in German). In the case of berlin.de, we may scrape if we keep the data **only for private use** and if we store the **data in one system** only.
* Check robots.txt . In our case, [Berlin.de's robots.txt](https://www.berlin.de/robots.txt). Noone is allowed to scrape from paths in the form `/*/(S(*))`. For us this is fine, since the websites we want to scrape are:

`https://www.berlin.de/kino/_bin/azfilm.php`

and

`https://www.berlin.de/kino/_bin/kinodetail.php/<cinema-code>`

---
**NOTE**

In this workshop, we will prepend `http://web.archive.org/web/20191102035415/` to the cinema detail urls. This is because of the berlin.de website currently not showing any movie titles due to corona virus. Hence, we will retrieve a cinema program from 2nd November 2019 instead of the current one.

---

# Steps:

1. [Clone or download main project](#step1)
2. [Install scrapy project requirements](#step2)
3. [Scrape data and write to json file](#step3)
4. [Enhance spyder](#step4)


## Clone or download main project <a name="step1"></a>

&#8594; First, **clone or download** [this repository](https://github.com/laufergall/movies-knowledgegraph/tree/workshop).

We will be making changes to different files in this project.

**Important**: your `<project-dir>` is the root project folder. If you `cd` to `<project-dir>`, you should see the folders `backend`, `mongo`, `scrapy`, and the files `.gitignore` and `README.md`.


## Install scrapy project requirements <a name="step2"></a>

You need Python 3.7.4.

&#8594; **Install requirements.txt** (under `<project-dir>/scrapy`). If you have conda installed, then:

```bash
conda create -n webscraping python=3.7.4
conda activate webscraping

cd <project-dir>/scrapy
pip install -r requirements.txt
```


## Scrape data and write to json file <a name="step3"></a>

&#8594; You can **start the spider** by just:

```bash
cd <project-dir>/scrapy/kinoprogramm
scrapy crawl kinoprogramm -o ../data/kinoprogramm.json
```

Data will be written to the file specified with the `-o` parameter.

However, this file does not contain any data (yet). We need to fix our spider.


## Enhance spyder <a name="step4"></a>

&#8594; **Add this code** to `<project-dir>/scrapy/kinoprogramm/spiders/kinoprogramm.py`, replacing line 105:

```python
cinema = Cinema(
	name=self.get_name(response),
	description=self.get_description(response),
	address=Address(street=self.get_street(response),
					postal_code=self.get_postal_code(response),
					district=self.get_district(response),
					city='Berlin',
					country='Germany'),
	contact=Contact(telephone=self.get_telephone(response)),
	prices=self.get_prices(response),
	shows=self.create_shows(titles, movies_times)
)
```

&#8594; **Run the spyder** again and verify that the data in the json file looks right.

```bash
scrapy crawl kinoprogramm -o ../data/kinoprogramm_right_content.json
```

Now we are properly scraping different pieces of information (name, description,...) from every cinema under [berlin.de](https://www.berlin.de/kino/_bin/azfilm.php).

The `parse()` method receives as input a response from the start_url: https://www.berlin.de/kino/_bin/azfilm.php. The method extracts hrefs for websites corresponding to each cinema, like for instance [Acud Kino](https://www.berlin.de/kino/_bin/kinodetail.php/30151). Each cinema website is parsed separately, by the method `parse_cinema()`. 
