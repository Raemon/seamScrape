SeamScrape
============

This project is for learning/demonstration purposes only. (I was practicing webscraping and wanted a meaningful project to cut my teeth against. I pulled data from Seamless Web to search for particular menu items. All rights belong to Seamless Web)

SeamScrape is for when you want to find, not just a good restaurant nearby, but the single *best* meal available. (Say you don't just want a good burger joint, you want the best veggie burger or BLT in your neighborhood). Search for "veggie burger", and it'll pull up all the highest rated items matching that name.)

If Seamless allowed access to their API, I'd have set this up to find out the current best items. Since they don't and I need to scrape manually, instead it just searches items from a particular neighborhood (in this case, Columbia campus in Manhattan)

Written in python, using Flask for the website, Selenium/urllib/BeautifulSoup for scraping, and SqlAlchemy/sqlite for the database.