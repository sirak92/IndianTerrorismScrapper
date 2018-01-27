# IndianTerrorismScrapper
Project intends to scrape Indian terrorism events information for each state/district from the website(http://southasiaterrorism.trfetzer.com/states/IND-Maharashtra.html)  and store it in excel file.


## Prerequisites
To run this project you have to install Python3.6(https://www.python.org/downloads/)

## Installation
The following project have some requirments before running it. To install the required packages run:
```
pip3 install -r requirements.txt
```

## Usage
Iterate to home directory of the project and type:
```
scrapy crawl IndianTerrorismSpider
```
The scraper will generate the `IndianTerrorismData.xls` file in the same folder.
