# FootyStats
A basic web scraper to scrape the footy stats from the FootyWire site, https://www.footywire.com

The scraper scrapes the entire match list from 1965 to current and places it into a DB.

The purpose of the scraper is to get the footy stats to place into a DB for later use and analysis.

python -m pip install --upgrade pip

pip install scrapy sqlalchemy bs4 python-dateutil

usage:
in Windows Powershell
.\FootyStats\scripts\activate.ps1

at the command prompt
scrapy crawl FootyWire

Addtitional Tools:
FootyWireMissed.py (spider name -> 'FWMissed')
FootyWireSingle.py (spider name -> 'FWSingle')

FootyWireMissed scrapes the pages that are in the file 'missed.txt'
If the original scrape is unable to process the page, it will generate an error and log the error into error.log.

From this error.log, it will be in the format of 'Unable to dowload FootyWire ID: mid=xxxx'. copy and paste this into the file, missed.txt and save.

run at command prompt:
scrapy crawl FWMissed.

FootyWireSingle is used for an individual, ie 10525, and modify the FootyWireSingle.py at line 55, url = self.base_url + 'ft_match_statistics?mid=xxxxx'. This spider can be easily modified to scrape multiple pages in a range, if so desired.