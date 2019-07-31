# AnimeScraper
This python script allows you to scrape the entire animeshows.tv database for their anime and mirror links. Also can download all images for series with getImage.py script


The following below will go through every series on the website, grab the series data, and place it into a table inside a database.

<code>python animeGrabber.py -i </code>


The command below will update your database with the latest episodes on the website.

<code>python animeGrabber.py -u </code>

The command below will download the poster picture for every series on the website

<code>python getImage.py </code>

Also, make sure that the data in the connection function matches your sql database
